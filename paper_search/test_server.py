#!/usr/bin/env python3
"""
测试脚本 - 验证MCP服务器改进功能
测试速率限制和三种搜索模式
"""

import asyncio
import time
from mcp_server import (
    search_pubmed,
    search_scholar,
    ScholarSearchMode,
    NCBI_RATE_LIMITER
)


async def test_rate_limiting():
    """测试NCBI API速率限制"""
    print("=" * 60)
    print("测试1: NCBI API 速率限制")
    print("=" * 60)

    # 尝试连续调用11次（超过限制）
    start_time = time.time()

    for i in range(11):
        await NCBI_RATE_LIMITER.acquire()
        elapsed = time.time() - start_time
        print(f"请求 {i+1}/11 - 已用时间: {elapsed:.2f}秒")

    total_time = time.time() - start_time
    print(f"\n总用时: {total_time:.2f}秒")
    print(f"预期: 至少1秒（因为速率限制为10次/秒）")

    if total_time >= 1.0:
        print("✅ 速率限制工作正常")
    else:
        print("❌ 速率限制可能未生效")

    print()


async def test_pubmed_search():
    """测试PubMed搜索"""
    print("=" * 60)
    print("测试2: PubMed 搜索功能")
    print("=" * 60)

    try:
        result = await search_pubmed("CRISPR", max_results=5)
        print(f"查询: {result['query']}")
        print(f"结果数量: {result['count']}")

        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
        else:
            print("✅ PubMed 搜索成功")
            for i, paper in enumerate(result['results'][:2], 1):
                print(f"\n{i}. {paper['title'][:80]}...")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

    print()


async def test_scholar_quick_mode():
    """测试Google Scholar快速模式"""
    print("=" * 60)
    print("测试3: Google Scholar 快速模式")
    print("=" * 60)

    try:
        result = await search_scholar("machine learning biology", mode=ScholarSearchMode.QUICK)
        print(f"查询: {result['query']}")
        print(f"模式: {result['mode']}")
        print(f"结果数量: {result['count']}")

        if 'error' in result and result['count'] == 0:
            print(f"❌ 错误: {result['error']}")
        else:
            print("✅ 快速模式搜索成功")
            for i, paper in enumerate(result['results'][:2], 1):
                print(f"\n{i}. {paper['title'][:80]}...")
                print(f"   引用数: {paper.get('cited_by', 'N/A')}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

    print()


async def test_scholar_relevance_mode():
    """测试Google Scholar相关度优化模式"""
    print("=" * 60)
    print("测试4: Google Scholar 相关度优化模式")
    print("=" * 60)

    try:
        result = await search_scholar(
            "hematopoietic stem cell",
            mode=ScholarSearchMode.RELEVANCE,
            num_results=5
        )
        print(f"查询: {result['query']}")
        print(f"模式: {result['mode']}")
        print(f"总搜索: {result.get('total_found', 'N/A')} 篇")
        print(f"返回: {result['count']} 篇")

        if 'error' in result and result['count'] == 0:
            print(f"❌ 错误: {result['error']}")
        else:
            print("✅ 相关度优化模式搜索成功")
            for i, paper in enumerate(result['results'][:2], 1):
                print(f"\n{i}. {paper['title'][:80]}...")
                print(f"   相关度分数: {paper.get('relevance_score', 'N/A')}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

    print()


async def test_scholar_deep_mode():
    """测试Google Scholar深度查找模式"""
    print("=" * 60)
    print("测试5: Google Scholar 深度查找模式")
    print("=" * 60)

    try:
        print("注意: 深度模式可能需要较长时间...")
        result = await search_scholar(
            "CRISPR gene editing",
            mode=ScholarSearchMode.DEEP,
            num_results=5
        )

        print(f"\n查询: {result['query']}")
        print(f"模式: {result['mode']}")
        print(f"文献池大小: {result.get('pool_size', 'N/A')} 篇")
        print(f"扩展查询数: {result.get('expansion_queries', 'N/A')}")
        print(f"返回: {result['count']} 篇")

        if 'error' in result and result['count'] == 0:
            print(f"❌ 错误: {result['error']}")
        else:
            print("\n✅ 深度查找模式搜索成功")
            print("\n顶级文献及其评分:")
            for i, paper in enumerate(result['results'], 1):
                print(f"\n{i}. {paper['title'][:80]}...")
                if 'scores' in paper:
                    scores = paper['scores']
                    print(f"   引用度: {scores['citation']}")
                    print(f"   相关度: {scores['relevance']}")
                    print(f"   时效性: {scores['recency']}")
                    print(f"   总分: {scores['total']}")
                print(f"   实际引用数: {paper.get('cited_by', 'N/A')}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

    print()


async def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("MCP 服务器功能测试")
    print("=" * 60 + "\n")

    # 运行测试
    await test_rate_limiting()
    await test_pubmed_search()
    await test_scholar_quick_mode()
    await test_scholar_relevance_mode()
    await test_scholar_deep_mode()

    print("=" * 60)
    print("所有测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
