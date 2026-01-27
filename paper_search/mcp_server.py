#!/usr/bin/env python3
"""
MCP Server for Scientific Research Workflow
Provides tools for searching PubMed and Google Scholar
"""

import os
import json
import asyncio
import time
from pathlib import Path
from typing import Any, Optional, List
from urllib.parse import urlencode
from dataclasses import dataclass
from enum import Enum

# MCP imports
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# HTTP client
import httpx

# ============== Configuration ==============
# 优先级: 环境变量 > 配置文件 > 默认值

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "api_key.json"

def load_config():
    """从配置文件加载 API keys"""
    config = {
        "NCBI_API_KEY": "your_ncbi_api_key_here",
        "NCBI_EMAIL": "your_email@example.com",
        "SERPAPI_KEY": "your_serpapi_key_here"
    }

    # 如果配置文件存在，读取它
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"警告: 读取配置文件失败 ({e})，使用默认值", file=os.sys.stderr)

    return config

# 加载配置
config = load_config()

# 最终配置（环境变量优先）
NCBI_API_KEY = os.environ.get("NCBI_API_KEY", config["NCBI_API_KEY"])
NCBI_EMAIL = os.environ.get("NCBI_EMAIL", config["NCBI_EMAIL"])
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", config["SERPAPI_KEY"])

# ============== Rate Limiter ==============

class RateLimiter:
    """Rate limiter for API calls to ensure we don't exceed limits"""

    def __init__(self, max_calls: int, time_window: float):
        """
        Args:
            max_calls: Maximum number of calls allowed
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
        self._lock = asyncio.Lock()

    async def acquire(self):
        """Acquire permission to make a call, waiting if necessary"""
        async with self._lock:
            now = time.time()
            # Remove old calls outside the time window
            self.calls = [call_time for call_time in self.calls
                         if now - call_time < self.time_window]

            # If we've reached the limit, wait
            if len(self.calls) >= self.max_calls:
                sleep_time = self.time_window - (now - self.calls[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    # Clean up old calls after waiting
                    now = time.time()
                    self.calls = [call_time for call_time in self.calls
                                 if now - call_time < self.time_window]

            # Record this call
            self.calls.append(now)

# NCBI API rate limiter: 10 requests per second (actually 3 without API key, 10 with key)
# We'll use 10 as a safe limit
NCBI_RATE_LIMITER = RateLimiter(max_calls=10, time_window=1.0)

# ============== Search Modes ==============

class ScholarSearchMode(str, Enum):
    """Google Scholar search modes"""
    QUICK = "quick"  # First 10 papers
    RELEVANCE = "relevance"  # Top papers from first 200
    DEEP = "deep"  # Citation-based expansion with multi-criteria ranking

@dataclass
class PaperScore:
    """Score for ranking papers in deep search mode"""
    paper: dict
    citation_score: float  # 0-1, based on citation count
    relevance_score: float  # 0-1, based on query relevance
    recency_score: float  # 0-1, newer is better
    total_score: float  # Weighted combination

# ============== NCBI E-utilities Functions ==============

async def search_pubmed(query: str, max_results: int = 10) -> dict:
    """
    Search PubMed using NCBI E-utilities API
    With rate limiting to respect NCBI's 10 requests/second limit

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10)

    Returns:
        Dictionary with search results
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    # Step 1: Search for PMIDs (with rate limiting)
    await NCBI_RATE_LIMITER.acquire()

    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance",
    }

    if NCBI_API_KEY and NCBI_API_KEY != "your_ncbi_api_key_here":
        search_params["api_key"] = NCBI_API_KEY

    if NCBI_EMAIL and NCBI_EMAIL != "your_email@example.com":
        search_params["email"] = NCBI_EMAIL

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Get PMIDs
        search_response = await client.get(base_url, params=search_params)
        search_data = search_response.json()

        pmids = search_data.get("esearchresult", {}).get("idlist", [])

        if not pmids:
            return {
                "query": query,
                "count": 0,
                "results": []
            }

        # Step 2: Fetch summaries (with rate limiting)
        await NCBI_RATE_LIMITER.acquire()

        summary_params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "json",
        }

        if NCBI_API_KEY and NCBI_API_KEY != "your_ncbi_api_key_here":
            summary_params["api_key"] = NCBI_API_KEY

        if NCBI_EMAIL and NCBI_EMAIL != "your_email@example.com":
            summary_params["email"] = NCBI_EMAIL

        summary_response = await client.get(summary_url, params=summary_params)
        summary_data = summary_response.json()

        # Parse results
        results = []
        for pmid in pmids:
            if pmid in summary_data.get("result", {}):
                article = summary_data["result"][pmid]

                # Get authors
                authors = article.get("authors", [])
                author_list = ", ".join([
                    f"{a.get('name', '')}" for a in authors[:5]
                ])
                if len(authors) > 5:
                    author_list += " et al."

                result = {
                    "pmid": pmid,
                    "title": article.get("title", "N/A"),
                    "abstract": "",  # esummary doesn't provide abstract, would need efetch
                    "authors": author_list,
                    "pub_date": article.get("pubdate", "N/A"),
                    "journal": article.get("source", "N/A"),
                    "citation": article.get("citation", "N/A")
                }
                results.append(result)

        return {
            "query": query,
            "count": len(results),
            "results": results
        }


# ============== SerpApi Functions ==============

async def fetch_scholar_results(query: str, num_results: int, start: int = 0) -> dict:
    """
    Fetch results from Google Scholar via SerpApi

    Args:
        query: Search query string
        num_results: Number of results to fetch
        start: Starting index for pagination

    Returns:
        Raw API response
    """
    base_url = "https://serpapi.com/search"

    params = {
        "engine": "google_scholar",
        "q": query,
        "num": min(num_results, 20),  # SerpApi max is 20 per request
        "start": start,
        "api_key": SERPAPI_KEY,
        "hl": "en"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP Error: {e.response.status_code} - Please check your SerpApi key")
        except Exception as e:
            raise Exception(f"Error fetching scholar results: {str(e)}")


def parse_scholar_result(result: dict) -> dict:
    """Parse a single Google Scholar result"""
    summary_data = result.get("publication_info", {})
    authors = summary_data.get("authors", [])
    author_str = ", ".join(authors) if authors else "N/A"

    # Extract citation count
    cited_by = result.get("inline_links", {}).get("cited_by", {}).get("total", 0)
    try:
        cited_by = int(cited_by) if cited_by else 0
    except (ValueError, TypeError):
        cited_by = 0

    # Extract year
    year = summary_data.get("year", "N/A")
    try:
        year = int(year) if year != "N/A" else 0
    except (ValueError, TypeError):
        year = 0

    return {
        "title": result.get("title", "N/A"),
        "summary": result.get("snippet", "N/A"),
        "link": result.get("link", "N/A"),
        "authors": author_str,
        "year": year,
        "year_str": summary_data.get("year", "N/A"),
        "journal": summary_data.get("summary", "N/A"),
        "cited_by": cited_by,
        "cited_by_str": result.get("inline_links", {}).get("cited_by", {}).get("total", "N/A")
    }


async def search_scholar_quick(query: str, num_results: int = 10) -> dict:
    """
    Quick search mode: Return first N papers

    Args:
        query: Search query string
        num_results: Number of results to return (default: 10)

    Returns:
        Dictionary with search results
    """
    try:
        data = await fetch_scholar_results(query, num_results)
        organic_results = data.get("organic_results", [])

        results = [parse_scholar_result(result) for result in organic_results[:num_results]]

        return {
            "query": query,
            "mode": "quick",
            "count": len(results),
            "results": results
        }
    except Exception as e:
        return {
            "query": query,
            "mode": "quick",
            "error": str(e),
            "count": 0,
            "results": []
        }


async def search_scholar_relevance(query: str, num_results: int = 10) -> dict:
    """
    Relevance-optimized mode: Search through 200 papers and return most relevant

    Args:
        query: Search query string
        num_results: Number of top results to return (default: 10)

    Returns:
        Dictionary with search results
    """
    try:
        all_results = []
        num_to_fetch = 200

        # Fetch in batches of 20 (SerpApi limit)
        for start in range(0, num_to_fetch, 20):
            data = await fetch_scholar_results(query, 20, start=start)
            organic_results = data.get("organic_results", [])

            if not organic_results:
                break

            for result in organic_results:
                parsed = parse_scholar_result(result)
                # Add position-based relevance score (earlier = more relevant)
                parsed["relevance_score"] = 1.0 - (len(all_results) / num_to_fetch)
                all_results.append(parsed)

            if len(organic_results) < 20:
                break

        # Sort by relevance and return top N
        all_results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        top_results = all_results[:num_results]

        return {
            "query": query,
            "mode": "relevance",
            "total_found": len(all_results),
            "count": len(top_results),
            "results": top_results
        }
    except Exception as e:
        return {
            "query": query,
            "mode": "relevance",
            "error": str(e),
            "count": 0,
            "results": []
        }


async def search_scholar_deep(query: str, num_results: int = 5) -> dict:
    """
    Deep search mode: Citation-based expansion with multi-criteria ranking

    Steps:
    1. Get top papers from relevance-optimized mode (first pass)
    2. Filter papers to find most relevant ones
    3. Extract citations and perform citation-based search
    4. Rank all papers by: citation count, relevance, and recency
    5. Return top 5 papers

    Args:
        query: Search query string
        num_results: Number of top results to return (default: 5)

    Returns:
        Dictionary with search results
    """
    try:
        # Step 1: Get initial papers using relevance mode
        initial_result = await search_scholar_relevance(query, num_results=50)

        if "error" in initial_result or not initial_result["results"]:
            return {
                "query": query,
                "mode": "deep",
                "error": "Failed to get initial results for deep search",
                "count": 0,
                "results": []
            }

        initial_papers = initial_result["results"]

        # Step 2: Select top 20 most relevant papers for citation extraction
        top_papers = sorted(
            initial_papers,
            key=lambda x: x.get("relevance_score", 0),
            reverse=True
        )[:20]

        # Step 3: Extract unique citation keywords for expansion
        citation_queries = set()

        for paper in top_papers:
            # Use paper title terms for citation search
            title_words = paper["title"].lower().split()
            # Extract meaningful words (length > 3)
            meaningful_words = [w for w in title_words if len(w) > 4]
            citation_queries.update(meaningful_words[:5])  # Top 5 words per paper

        # Step 4: Perform citation-based searches
        all_papers = {paper["title"]: paper for paper in initial_papers}

        # Search for top citation terms
        for term in list(citation_queries)[:10]:  # Limit to 10 expansion searches
            expansion_query = f"{query} {term}"
            expansion_data = await fetch_scholar_results(expansion_query, 20)

            for result in expansion_data.get("organic_results", []):
                parsed = parse_scholar_result(result)
                title = parsed["title"]

                # Add to pool if not already present
                if title not in all_papers:
                    parsed["is_expansion"] = True
                    all_papers[title] = parsed

        # Step 5: Score and rank papers
        current_year = 2025
        paper_scores = []

        for paper in all_papers.values():
            # Normalize citation count (0-1)
            max_citations = max((p.get("cited_by", 0) for p in all_papers.values()), default=1)
            citation_score = min(paper.get("cited_by", 0) / max(max_citations, 1), 1.0)

            # Relevance score (from initial search or estimate)
            relevance_score = paper.get("relevance_score", 0.5)

            # Recency score (newer is better, papers from last 10 years get higher scores)
            year = paper.get("year", 0)
            if year > 0:
                years_old = current_year - year
                recency_score = max(0, 1.0 - (years_old / 20.0))  # 20-year window
            else:
                recency_score = 0.3  # Default for papers without year

            # Weighted total score (adjust weights as needed)
            # Citation: 40%, Relevance: 40%, Recency: 20%
            total_score = (
                0.4 * citation_score +
                0.4 * relevance_score +
                0.2 * recency_score
            )

            paper_scores.append(PaperScore(
                paper=paper,
                citation_score=citation_score,
                relevance_score=relevance_score,
                recency_score=recency_score,
                total_score=total_score
            ))

        # Sort by total score
        paper_scores.sort(key=lambda x: x.total_score, reverse=True)

        # Extract top N papers with scoring details
        top_papers_final = []
        for ps in paper_scores[:num_results]:
            p = ps.paper.copy()
            p["scores"] = {
                "citation": round(ps.citation_score, 3),
                "relevance": round(ps.relevance_score, 3),
                "recency": round(ps.recency_score, 3),
                "total": round(ps.total_score, 3)
            }
            top_papers_final.append(p)

        return {
            "query": query,
            "mode": "deep",
            "pool_size": len(all_papers),
            "expansion_queries": len(citation_queries),
            "count": len(top_papers_final),
            "results": top_papers_final
        }

    except Exception as e:
        return {
            "query": query,
            "mode": "deep",
            "error": str(e),
            "count": 0,
            "results": []
        }


async def search_scholar(
    query: str,
    mode: ScholarSearchMode = ScholarSearchMode.QUICK,
    num_results: int = 10
) -> dict:
    """
    Search Google Scholar using SerpApi with different modes

    Args:
        query: Search query string
        mode: Search mode (quick, relevance, deep)
        num_results: Number of results to return (default: 10)

    Returns:
        Dictionary with search results
    """
    if mode == ScholarSearchMode.QUICK:
        return await search_scholar_quick(query, num_results)
    elif mode == ScholarSearchMode.RELEVANCE:
        return await search_scholar_relevance(query, num_results)
    elif mode == ScholarSearchMode.DEEP:
        return await search_scholar_deep(query, num_results)
    else:
        return {
            "query": query,
            "error": f"Unknown search mode: {mode}",
            "count": 0,
            "results": []
        }


# ============== MCP Server Setup ==============

async def main():
    """Main entry point for the MCP server"""

    # Create server instance
    server = Server("research-workflow")

    # Register tools
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools"""
        return [
            Tool(
                name="search_pubmed",
                description=(
                    "Search PubMed database for scientific articles. "
                    "Returns Title, Abstract, Authors, and PubDate for top 10 most relevant papers. "
                    "Uses NCBI E-utilities API."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (e.g., 'hematopoietic stem cell heterogeneity')"
                        },
                        "max_results": {
                            "type": "number",
                            "description": "Maximum number of results (default: 10, max: 100)",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 100
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="search_scholar",
                description=(
                    "Search Google Scholar for scientific articles with multiple modes:\n"
                    "- quick: Returns first 10 papers (fastest mode)\n"
                    "- relevance: Searches through 200 papers and returns most relevant ones\n"
                    "- deep: Performs citation-based expansion, ranks papers by citation count, "
                    "relevance, and recency, then returns top 5 papers\n\n"
                    "Returns Title, Summary, Link, Authors, Year, Journal, and citation information. "
                    "Uses SerpApi Google Scholar API."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (e.g., 'hematopoietic stem cell heterogeneity')"
                        },
                        "mode": {
                            "type": "string",
                            "description": "Search mode: 'quick' (default, first 10), 'relevance' (top from 200), or 'deep' (citation-based expansion with multi-criteria ranking)",
                            "enum": ["quick", "relevance", "deep"],
                            "default": "quick"
                        },
                        "num_results": {
                            "type": "number",
                            "description": "Number of results to return (default: 10, for deep mode default is 5)",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 50
                        }
                    },
                    "required": ["query"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls"""

        if name == "search_pubmed":
            query = arguments.get("query")
            max_results = arguments.get("max_results", 10)

            if not query:
                return [TextContent(
                    type="text",
                    text="Error: 'query' parameter is required"
                )]

            result = await search_pubmed(query, max_results)

            # Format output as readable text
            output = f"## PubMed Search Results\n"
            output += f"Query: {result['query']}\n"
            output += f"Found: {result['count']} papers\n\n"

            for i, paper in enumerate(result.get('results', []), 1):
                output += f"### {i}. {paper['title']}\n"
                output += f"**PMID:** {paper['pmid']}\n"
                output += f"**Authors:** {paper['authors']}\n"
                output += f"**Journal:** {paper['journal']}\n"
                output += f"**Published:** {paper['pub_date']}\n"
                output += f"**Citation:** {paper['citation']}\n\n"
                output += "---\n\n"

            return [TextContent(type="text", text=output)]

        elif name == "search_scholar":
            query = arguments.get("query")
            mode_str = arguments.get("mode", "quick")
            num_results = arguments.get("num_results", 10)

            if not query:
                return [TextContent(
                    type="text",
                    text="Error: 'query' parameter is required"
                )]

            # Convert string mode to enum
            try:
                mode = ScholarSearchMode(mode_str)
            except ValueError:
                return [TextContent(
                    type="text",
                    text=f"Error: Invalid mode '{mode_str}'. Must be one of: quick, relevance, deep"
                )]

            # Adjust default for deep mode
            if mode == ScholarSearchMode.DEEP and num_results == 10:
                num_results = 5

            result = await search_scholar(query, mode, num_results)

            if "error" in result and result.get("count", 0) == 0:
                return [TextContent(
                    type="text",
                    text=f"Error: {result['error']}\n{result.get('message', '')}"
                )]

            # Format output as readable text
            output = f"## Google Scholar Search Results ({result.get('mode', mode_str).title()} Mode)\n"
            output += f"Query: {result['query']}\n"

            if result.get('mode') == 'deep':
                output += f"Pool Size: {result.get('pool_size', 'N/A')} papers\n"
                output += f"Expansion Queries: {result.get('expansion_queries', 'N/A')}\n"

            output += f"Returned: {result['count']} papers\n\n"

            for i, paper in enumerate(result.get('results', []), 1):
                output += f"### {i}. {paper['title']}\n"
                output += f"**Link:** {paper['link']}\n"
                output += f"**Summary:** {paper['summary'][:300]}...\n"  # Truncate long summaries
                output += f"**Authors:** {paper['authors']}\n"
                output += f"**Year:** {paper.get('year_str', paper.get('year', 'N/A'))}\n"
                output += f"**Journal:** {paper['journal']}\n"
                output += f"**Cited by:** {paper.get('cited_by_str', paper.get('cited_by', 'N/A'))} papers\n"

                # Add scores for deep mode
                if 'scores' in paper:
                    scores = paper['scores']
                    output += f"**Scores:** Citation={scores['citation']}, "
                    output += f"Relevance={scores['relevance']}, "
                    output += f"Recency={scores['recency']}, "
                    output += f"Total={scores['total']}\n"

                output += "\n---\n\n"

            return [TextContent(type="text", text=output)]

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="research-workflow",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
