#!/usr/bin/env python3
"""
codebase-memory: analyze_codebase.py
=====================================
Walks a target directory, extracts structural facts from source files, and writes:

  memory/maps/file_index.json   — file path → language, role, classes, functions, imports
  memory/maps/call_graph.json   — import edges + adjacency list between source files

The AI agent then reads these JSON files to synthesise the human-readable layers:
  memory/modules/<n>.md         — per-module deep dives
  memory/codebase.md            — master index

Usage:
    python3 analyze_codebase.py [target_dir] [--output-dir memory/] [--incremental]

Supported languages: Python, TypeScript/JavaScript, Go, Rust, Java, Kotlin,
                     Ruby, PHP, C, C++, C#, Swift, Scala.
"""

import os
import sys
import json
import re
import ast
import argparse
from pathlib import Path
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────

IGNORE_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".next", "target", "vendor", ".idea", ".vscode",
    "coverage", ".nyc_output", ".eggs",
}
IGNORE_EXTENSIONS = {
    ".lock", ".sum", ".log", ".map", ".min.js", ".min.css",
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf",
    ".zip", ".tar", ".gz",
}
SOURCE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx",
    ".go", ".rs", ".java", ".kt", ".rb",
    ".php", ".c", ".cpp", ".h", ".hpp",
    ".cs", ".swift", ".scala",
}
CONFIG_FILES = {
    "package.json", "pyproject.toml", "setup.py", "Cargo.toml",
    "go.mod", "pom.xml", "Gemfile", "composer.json",
    "Makefile", "Dockerfile", "docker-compose.yml",
    "requirements.txt", ".env.example",
}
ENTRY_PATTERNS = {
    "main.py", "main.go", "main.rs", "main.ts", "main.js",
    "index.ts", "index.js", "app.py", "app.ts", "app.js",
    "server.py", "server.ts", "server.js",
    "wsgi.py", "asgi.py", "manage.py",
}
MAX_FILE_SIZE = 200_000  # bytes

# ── Directory role heuristics ─────────────────────────────────────────────────

DIR_ROLE_HINTS = {
    "auth": "Authentication & authorisation",
    "api": "API layer / HTTP handlers",
    "route": "Routing / URL dispatch",
    "router": "Routing / URL dispatch",
    "model": "Data models / ORM definitions",
    "schema": "Schema / serialiser definitions",
    "service": "Business logic / service layer",
    "repo": "Repository / database access layer",
    "repository": "Repository / database access layer",
    "db": "Database setup / migrations",
    "database": "Database setup / migrations",
    "migration": "Database migrations",
    "util": "Shared utilities & helpers",
    "utils": "Shared utilities & helpers",
    "helper": "Helper functions",
    "helpers": "Helper functions",
    "middleware": "Request/response middleware",
    "test": "Tests",
    "tests": "Tests",
    "spec": "Tests / specifications",
    "specs": "Tests / specifications",
    "config": "Configuration",
    "task": "Async / background tasks",
    "tasks": "Async / background tasks",
    "hook": "Hooks / event listeners",
    "hooks": "Hooks / event listeners",
    "component": "UI components",
    "components": "UI components",
    "page": "Page-level UI components",
    "pages": "Page-level UI components",
    "store": "State management",
    "type": "Type definitions",
    "types": "Type definitions",
    "interface": "Interfaces / contracts",
    "interfaces": "Interfaces / contracts",
    "handler": "Request handlers",
    "handlers": "Request handlers",
    "controller": "Controllers (MVC)",
    "controllers": "Controllers (MVC)",
    "view": "View layer / templates",
    "views": "View layer / templates",
    "template": "HTML/template files",
    "templates": "HTML/template files",
    "static": "Static assets",
    "public": "Publicly served assets",
    "script": "Scripts / tooling",
    "scripts": "Scripts / tooling",
    "lib": "Internal library code",
    "core": "Core / domain logic",
    "domain": "Domain layer",
    "infra": "Infrastructure / adapters",
    "infrastructure": "Infrastructure / adapters",
    "proto": "Protobuf definitions",
    "protos": "Protobuf definitions",
    "cmd": "CLI / command entry points",
    "bin": "Executables / entry points",
    "pkg": "Shared packages",
    "internal": "Internal packages (Go-style)",
    "common": "Shared common code",
    "shared": "Shared code",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def should_skip(rel: Path) -> bool:
    for part in rel.parts:
        if part in IGNORE_DIRS or part.endswith(".egg-info"):
            return True
    if rel.suffix.lower() in IGNORE_EXTENSIONS:
        return True
    abs_path = rel  # size check done separately
    return False


def read_head(path: Path, n: int = 60) -> list[str]:
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = []
            for _ in range(n):
                try:
                    lines.append(next(f))
                except StopIteration:
                    break
            return lines
    except Exception:
        return []


def detect_language(path: Path) -> str:
    return {
        ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript",
        ".js": "JavaScript", ".jsx": "JavaScript", ".go": "Go",
        ".rs": "Rust", ".java": "Java", ".kt": "Kotlin",
        ".rb": "Ruby", ".php": "PHP", ".c": "C", ".cpp": "C++",
        ".h": "C/C++ Header", ".hpp": "C++", ".cs": "C#",
        ".swift": "Swift", ".scala": "Scala",
    }.get(path.suffix.lower(), "Unknown")


def dir_role(name: str, files: list[Path]) -> str:
    key = name.lower().rstrip("s")  # naive singularisation fallback
    if name.lower() in DIR_ROLE_HINTS:
        return DIR_ROLE_HINTS[name.lower()]
    if key in DIR_ROLE_HINTS:
        return DIR_ROLE_HINTS[key]
    exts = {f.suffix.lower() for f in files}
    if ".html" in exts or ".jinja2" in exts:
        return "Templates / views"
    if ".proto" in exts:
        return "Protocol buffer definitions"
    if ".sql" in exts:
        return "SQL / migrations"
    return "—"


def infer_module(rel: Path, top_level_dirs: list[str]) -> str:
    """Map a file path to its top-level module name."""
    parts = rel.parts
    if len(parts) == 1:
        return "__root__"
    # Strip common source roots
    src_roots = {"src", "lib", "app", "pkg", "internal"}
    start = 1 if parts[0] in src_roots else 0
    if len(parts) > start:
        return parts[start]
    return "__root__"


# ── Language extractors ───────────────────────────────────────────────────────

def extract_python(path: Path) -> dict:
    result = {"classes": [], "functions": [], "imports": []}
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except Exception:
        return result

    top_level_fn_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            result["imports"].append(module)

    for node in ast.iter_child_nodes(tree):  # top-level only
        if isinstance(node, ast.ClassDef):
            methods = []
            for item in ast.iter_child_nodes(node):
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = [a.arg for a in item.args.args if a.arg not in ("self", "cls")]
                    methods.append({
                        "name": item.name,
                        "args": args,
                        "docstring": (ast.get_docstring(item) or "")[:120],
                        "lineno": item.lineno,
                    })
            result["classes"].append({
                "name": node.name,
                "docstring": (ast.get_docstring(node) or "")[:200],
                "methods": methods,
                "lineno": node.lineno,
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [a.arg for a in node.args.args]
            result["functions"].append({
                "name": node.name,
                "args": args,
                "docstring": (ast.get_docstring(node) or "")[:120],
                "lineno": node.lineno,
            })

    result["imports"] = list(dict.fromkeys(result["imports"]))[:25]
    return result


def extract_generic(path: Path, head_lines: list[str]) -> dict:
    result = {"classes": [], "functions": [], "imports": []}
    text = "".join(head_lines)

    class_re = re.compile(
        r"(?:^|\n)\s*(?:export\s+)?(?:abstract\s+)?(?:class|struct|interface|trait|enum)\s+(\w+)",
        re.MULTILINE,
    )
    for m in class_re.finditer(text):
        result["classes"].append({"name": m.group(1), "methods": []})

    fn_re = re.compile(
        r"(?:^|\n)\s*(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)\s*\(|"
        r"(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\(|"
        r"func\s+(?:\([^)]*\)\s+)?(\w+)\s*[(<]|"
        r"(?:pub(?:\s*\([^)]*\))?\s+)?fn\s+(\w+)\s*[(<])",
        re.MULTILINE,
    )
    for m in fn_re.finditer(text):
        name = next((g for g in m.groups() if g), None)
        if name:
            result["functions"].append({"name": name})

    import_re = re.compile(
        r"""(?:^|\n)\s*(?:import|require|use|#include|from)\s+['"<]?([^\s;'">{]+)['">;]?""",
        re.MULTILINE,
    )
    result["imports"] = list({m.group(1) for m in import_re.finditer(text)})[:25]

    return result


# ── Config parsers ────────────────────────────────────────────────────────────

def parse_project_config(root: Path) -> dict:
    info = {"name": None, "description": None, "version": None, "scripts": {}}

    pj = root / "package.json"
    if pj.exists():
        try:
            d = json.loads(pj.read_text())
            info.update(name=d.get("name"), description=d.get("description"),
                        version=d.get("version"), scripts=d.get("scripts", {}))
        except Exception:
            pass

    for fname in ("pyproject.toml", "setup.cfg", "Cargo.toml", "go.mod"):
        cfg = root / fname
        if cfg.exists():
            text = cfg.read_text(errors="replace")
            for field in ("name", "description", "version"):
                if not info[field]:
                    m = re.search(rf'{field}\s*[=:]\s*["\']?([^"\'\n]+)["\']?', text)
                    if m:
                        info[field] = m.group(1).strip()
            break

    return info


# ── Call graph builder ────────────────────────────────────────────────────────

def resolve_import_to_file(import_str: str, file_path: Path,
                            all_files: dict[str, dict]) -> str | None:
    """Best-effort: map an import string to an actual file in the index."""
    # Convert dotted module to path fragments
    parts = import_str.replace(".", "/").replace("-", "_")
    for candidate in all_files:
        if parts in candidate.replace("\\", "/"):
            return candidate
    return None


def build_call_graph(file_index: dict[str, dict]) -> dict:
    edges = []
    adjacency: dict[str, dict] = {}

    for file_path, meta in file_index.items():
        adjacency.setdefault(file_path, {"imports": [], "imported_by": []})
        for imp in meta.get("imports", []):
            resolved = resolve_import_to_file(imp, Path(file_path), file_index)
            if resolved and resolved != file_path:
                edges.append({"from": file_path, "to": resolved, "type": "import"})
                adjacency[file_path]["imports"].append(resolved)
                adjacency.setdefault(resolved, {"imports": [], "imported_by": []})
                adjacency[resolved]["imported_by"].append(file_path)

    # Deduplicate
    for node in adjacency.values():
        node["imports"] = list(dict.fromkeys(node["imports"]))
        node["imported_by"] = list(dict.fromkeys(node["imported_by"]))

    seen = set()
    deduped_edges = []
    for e in edges:
        key = (e["from"], e["to"])
        if key not in seen:
            seen.add(key)
            deduped_edges.append(e)

    return {"edges": deduped_edges, "adjacency": adjacency}


# ── Main walker ───────────────────────────────────────────────────────────────

def walk_codebase(root: Path) -> tuple[dict, dict]:
    """
    Returns (file_index, call_graph) dicts.
    """
    root = root.resolve()
    ts = datetime.now(timezone.utc).isoformat()
    project_config = parse_project_config(root)

    # Collect all source files
    all_source: list[Path] = []
    dir_file_groups: dict[str, list[Path]] = {}

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        if should_skip(rel):
            continue
        if path.stat().st_size > MAX_FILE_SIZE:
            continue

        parent_str = str(rel.parent)
        dir_file_groups.setdefault(parent_str, []).append(path)

        if rel.suffix.lower() in SOURCE_EXTENSIONS:
            all_source.append(path)

    # Build directory summary (for agent context)
    directories = {}
    for dir_str, files in dir_file_groups.items():
        dir_name = Path(dir_str).name
        directories[dir_str] = {
            "role": dir_role(dir_name, files),
            "file_count": len(files),
        }

    # Determine top-level modules
    top_dirs = [p.name for p in root.iterdir()
                if p.is_dir() and p.name not in IGNORE_DIRS]

    # Analyse each source file
    file_index: dict[str, dict] = {}
    languages: dict[str, int] = {}
    entry_points: list[str] = []
    config_files_found: list[str] = []

    for path in all_source:
        rel = path.relative_to(root)
        rel_str = str(rel)
        lang = detect_language(path)
        languages[lang] = languages.get(lang, 0) + 1

        if path.name in ENTRY_PATTERNS:
            entry_points.append(rel_str)
        if path.name in CONFIG_FILES:
            config_files_found.append(rel_str)

        head = read_head(path, 60)
        if lang == "Python":
            extracted = extract_python(path)
        else:
            extracted = extract_generic(path, head)

        # File-level comment / docstring
        file_comment = ""
        for line in head[:6]:
            stripped = line.strip().lstrip("#/*! ").strip()
            if stripped and not stripped.lower().startswith(("import", "from", "use ", "package")):
                file_comment = stripped[:200]
                break

        module = infer_module(rel, top_dirs)

        file_index[rel_str] = {
            "language": lang,
            "module": module,
            "role": dir_role(rel.parent.name, [path]),
            "comment": file_comment,
            "classes": [
                {"name": c["name"], "methods": [m["name"] for m in c.get("methods", [])]}
                for c in extracted["classes"]
            ],
            "functions": [f["name"] for f in extracted["functions"][:30]],
            "imports": extracted["imports"][:25],
        }

    # Build call graph from import relationships
    call_graph_data = build_call_graph(file_index)

    file_index_out = {
        "generated_at": ts,
        "project": project_config,
        "entry_points": entry_points,
        "languages": languages,
        "directories": directories,
        "files": file_index,
    }

    call_graph_out = {
        "generated_at": ts,
        **call_graph_data,
    }

    return file_index_out, call_graph_out


# ── Writer ────────────────────────────────────────────────────────────────────

def write_outputs(root: Path, output_dir: Path,
                  file_index: dict, call_graph: dict,
                  incremental: bool = False) -> None:
    maps_dir = output_dir / "maps"
    maps_dir.mkdir(parents=True, exist_ok=True)

    fi_path = maps_dir / "file_index.json"
    cg_path = maps_dir / "call_graph.json"

    if incremental and fi_path.exists():
        # Merge: update changed files, keep untouched ones
        existing_fi = json.loads(fi_path.read_text())
        existing_fi["files"].update(file_index["files"])
        existing_fi["generated_at"] = file_index["generated_at"]
        file_index = existing_fi

        existing_cg = json.loads(cg_path.read_text()) if cg_path.exists() else {}
        # Full rebuild of call graph (cheap, always consistent)

    fi_path.write_text(json.dumps(file_index, indent=2, default=str))
    cg_path.write_text(json.dumps(call_graph, indent=2, default=str))

    # Print summary for the agent
    modules = {}
    for rel_str, meta in file_index.get("files", {}).items():
        m = meta.get("module", "__root__")
        modules.setdefault(m, []).append(rel_str)

    print(json.dumps({
        "status": "ok",
        "file_index": str(fi_path),
        "call_graph": str(cg_path),
        "files_indexed": len(file_index.get("files", {})),
        "languages": file_index.get("languages", {}),
        "entry_points": file_index.get("entry_points", []),
        "modules": {m: len(files) for m, files in modules.items()},
        "next_steps": [
            f"Write memory/modules/{m}.md for each module listed above"
            for m in modules if m != "__root__"
        ] + ["Write memory/codebase.md last (master index)"],
    }, indent=2))


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Analyse a codebase and emit file_index.json + call_graph.json."
    )
    parser.add_argument("target", nargs="?", default=".",
                        help="Target directory (default: current dir)")
    parser.add_argument("--output-dir", default="memory",
                        help="Output directory for maps/ (default: memory/)")
    parser.add_argument("--incremental", action="store_true",
                        help="Merge into existing file_index rather than replacing")
    args = parser.parse_args()

    root = Path(args.target)
    if not root.is_dir():
        print(f"Error: '{root}' is not a directory", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir)
    print(f"Analysing {root.resolve()} …", file=sys.stderr)

    file_index, call_graph = walk_codebase(root)
    write_outputs(root, output_dir, file_index, call_graph, args.incremental)


if __name__ == "__main__":
    main()
