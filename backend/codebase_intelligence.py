"""
Codebase Intelligence System
Provides semantic code search, dependency tracking, and intelligent context understanding
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path
import os
import json
import ast
import re
from collections import defaultdict
from groq import Groq

router = APIRouter(prefix="/codebase", tags=["Codebase Intelligence"])

# Initialize Groq for embeddings-like functionality
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class CodebaseIndexRequest(BaseModel):
    project_path: str
    file_patterns: List[str] = ["*.py", "*.js", "*.ts", "*.tsx", "*.jsx"]
    exclude_patterns: List[str] = ["node_modules/**", "venv/**", "*.min.js", "dist/**", "build/**"]


class SemanticSearchRequest(BaseModel):
    query: str
    project_path: str
    limit: int = 10


class Symbol(BaseModel):
    name: str
    type: str  # function, class, variable, import
    file_path: str
    line_number: int
    definition: str
    docstring: Optional[str] = None


class Dependency(BaseModel):
    source_file: str
    target_file: str
    imports: List[str]


class CodebaseIndex:
    """In-memory codebase index with semantic understanding"""

    def __init__(self):
        self.symbols: Dict[str, List[Symbol]] = defaultdict(list)
        self.dependencies: Dict[str, List[Dependency]] = defaultdict(list)
        self.file_contents: Dict[str, str] = {}
        self.file_summaries: Dict[str, str] = {}

    def index_python_file(self, file_path: Path, content: str):
        """Extract symbols from Python files"""
        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                # Extract functions
                if isinstance(node, ast.FunctionDef):
                    docstring = ast.get_docstring(node) or ""
                    self.symbols[str(file_path)].append(Symbol(
                        name=node.name,
                        type="function",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        definition=f"def {node.name}({self._get_function_args(node)})",
                        docstring=docstring
                    ))

                # Extract classes
                elif isinstance(node, ast.ClassDef):
                    docstring = ast.get_docstring(node) or ""
                    self.symbols[str(file_path)].append(Symbol(
                        name=node.name,
                        type="class",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        definition=f"class {node.name}",
                        docstring=docstring
                    ))

                # Extract imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        self.symbols[str(file_path)].append(Symbol(
                            name=alias.name,
                            type="import",
                            file_path=str(file_path),
                            line_number=node.lineno,
                            definition=f"import {alias.name}"
                        ))

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        self.symbols[str(file_path)].append(Symbol(
                            name=f"{module}.{alias.name}",
                            type="import",
                            file_path=str(file_path),
                            line_number=node.lineno,
                            definition=f"from {module} import {alias.name}"
                        ))

        except SyntaxError:
            pass  # Skip files with syntax errors

    def index_javascript_file(self, file_path: Path, content: str):
        """Extract symbols from JavaScript/TypeScript files using regex patterns"""
        # Function declarations
        func_pattern = r'(export\s+)?(async\s+)?function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('
        for match in re.finditer(func_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            self.symbols[str(file_path)].append(Symbol(
                name=match.group(3),
                type="function",
                file_path=str(file_path),
                line_number=line_num,
                definition=match.group(0)
            ))

        # Arrow functions assigned to const/let/var
        arrow_pattern = r'(export\s+)?(const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(async\s+)?\([^)]*\)\s*=>'
        for match in re.finditer(arrow_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            self.symbols[str(file_path)].append(Symbol(
                name=match.group(3),
                type="function",
                file_path=str(file_path),
                line_number=line_num,
                definition=match.group(0)
            ))

        # Class declarations
        class_pattern = r'(export\s+)?(default\s+)?class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)'
        for match in re.finditer(class_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            self.symbols[str(file_path)].append(Symbol(
                name=match.group(3),
                type="class",
                file_path=str(file_path),
                line_number=line_num,
                definition=match.group(0)
            ))

        # Imports
        import_pattern = r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(import_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            self.symbols[str(file_path)].append(Symbol(
                name=match.group(1),
                type="import",
                file_path=str(file_path),
                line_number=line_num,
                definition=match.group(0)
            ))

    def _get_function_args(self, node: ast.FunctionDef) -> str:
        """Extract function arguments as string"""
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        return ", ".join(args)

    def generate_file_summary(self, file_path: str, content: str) -> str:
        """Generate AI summary of file purpose"""
        try:
            # Get first 50 lines for context
            lines = content.split('\n')[:50]
            preview = '\n'.join(lines)

            prompt = f"""Analyze this code file and provide a 1-sentence summary of its purpose:

```
{preview}
```

Respond with only the summary, no additional text."""

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a code analysis expert. Provide concise file summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Code file: {Path(file_path).name}"


# Global index (in production, use Redis or similar)
codebase_indexes: Dict[str, CodebaseIndex] = {}


@router.post("/index")
async def index_codebase(request: CodebaseIndexRequest):
    """
    Index entire codebase for semantic search and intelligence
    """
    try:
        project_path = Path(request.project_path)
        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project path not found")

        index = CodebaseIndex()
        indexed_files = 0
        total_symbols = 0

        # Find all matching files
        files_to_index = []
        for pattern in request.file_patterns:
            files_to_index.extend(project_path.rglob(pattern))

        # Filter excluded patterns
        excluded = set()
        for pattern in request.exclude_patterns:
            excluded.update(project_path.rglob(pattern))

        files_to_index = [f for f in files_to_index if f not in excluded and f.is_file()]

        # Limit for performance
        if len(files_to_index) > 500:
            files_to_index = files_to_index[:500]

        # Index each file
        for file_path in files_to_index:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                index.file_contents[str(file_path)] = content

                # Index based on file type
                if file_path.suffix == '.py':
                    index.index_python_file(file_path, content)
                elif file_path.suffix in ['.js', '.ts', '.tsx', '.jsx']:
                    index.index_javascript_file(file_path, content)

                # Generate summary (for first 50 files to save time)
                if indexed_files < 50:
                    summary = index.generate_file_summary(str(file_path), content)
                    index.file_summaries[str(file_path)] = summary

                indexed_files += 1
                total_symbols += len(index.symbols.get(str(file_path), []))

            except Exception as e:
                print(f"Error indexing {file_path}: {str(e)}")
                continue

        # Store index
        codebase_indexes[request.project_path] = index

        return {
            "success": True,
            "files_indexed": indexed_files,
            "total_symbols": total_symbols,
            "message": f"Successfully indexed {indexed_files} files with {total_symbols} symbols"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index codebase: {str(e)}")


@router.post("/semantic-search")
async def semantic_search(request: SemanticSearchRequest):
    """
    Semantic search across codebase using AI
    """
    try:
        # Check if codebase is indexed
        if request.project_path not in codebase_indexes:
            raise HTTPException(status_code=404, detail="Codebase not indexed. Please index first.")

        index = codebase_indexes[request.project_path]

        # Create search context from all symbols
        all_symbols = []
        for file_symbols in index.symbols.values():
            all_symbols.extend(file_symbols)

        # Use AI to find relevant symbols
        symbols_text = "\n".join([
            f"{s.name} ({s.type}) in {s.file_path}:{s.line_number} - {s.definition}"
            for s in all_symbols[:500]  # Limit for token constraints
        ])

        prompt = f"""Given this codebase structure:

{symbols_text}

Find the most relevant code symbols for this query: "{request.query}"

Return a JSON array of the top {request.limit} most relevant symbol names, like:
["symbol1", "symbol2", "symbol3"]

Return ONLY the JSON array, no explanation."""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a code search expert. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )

        # Parse AI response
        relevant_names = json.loads(response.choices[0].message.content.strip())

        # Find full symbol details
        results = []
        for symbol in all_symbols:
            if symbol.name in relevant_names:
                results.append(symbol)

        return {
            "query": request.query,
            "results": results[:request.limit],
            "total_found": len(results)
        }

    except json.JSONDecodeError:
        # Fallback to simple text search
        return await simple_search(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


async def simple_search(request: SemanticSearchRequest):
    """Fallback simple text search"""
    index = codebase_indexes[request.project_path]

    all_symbols = []
    for file_symbols in index.symbols.values():
        all_symbols.extend(file_symbols)

    # Simple text matching
    query_lower = request.query.lower()
    results = [
        s for s in all_symbols
        if query_lower in s.name.lower() or (s.docstring and query_lower in s.docstring.lower())
    ]

    return {
        "query": request.query,
        "results": results[:request.limit],
        "total_found": len(results)
    }


@router.get("/file-summary")
async def get_file_summary(project_path: str, file_path: str):
    """Get AI-generated summary of a file"""
    if project_path not in codebase_indexes:
        raise HTTPException(status_code=404, detail="Codebase not indexed")

    index = codebase_indexes[project_path]

    if file_path in index.file_summaries:
        return {"file_path": file_path, "summary": index.file_summaries[file_path]}

    # Generate on-demand if not in cache
    if file_path in index.file_contents:
        summary = index.generate_file_summary(file_path, index.file_contents[file_path])
        index.file_summaries[file_path] = summary
        return {"file_path": file_path, "summary": summary}

    raise HTTPException(status_code=404, detail="File not found in index")


@router.get("/symbols")
async def get_symbols(project_path: str, file_path: Optional[str] = None):
    """Get all symbols in the codebase or specific file"""
    if project_path not in codebase_indexes:
        raise HTTPException(status_code=404, detail="Codebase not indexed")

    index = codebase_indexes[project_path]

    if file_path:
        return {"symbols": index.symbols.get(file_path, [])}

    # Return all symbols grouped by type
    by_type = defaultdict(list)
    for file_symbols in index.symbols.values():
        for symbol in file_symbols:
            by_type[symbol.type].append(symbol)

    return {
        "total": sum(len(symbols) for symbols in by_type.values()),
        "by_type": dict(by_type)
    }


@router.get("/project-context")
async def get_project_context(project_path: str):
    """Get high-level project context and architecture overview"""
    if project_path not in codebase_indexes:
        raise HTTPException(status_code=404, detail="Codebase not indexed")

    index = codebase_indexes[project_path]

    # Gather statistics
    total_files = len(index.file_contents)
    total_symbols = sum(len(symbols) for symbols in index.symbols.values())

    symbol_breakdown = defaultdict(int)
    for file_symbols in index.symbols.values():
        for symbol in file_symbols:
            symbol_breakdown[symbol.type] += 1

    # Get file summaries
    key_files = list(index.file_summaries.items())[:10]

    return {
        "project_path": project_path,
        "statistics": {
            "total_files": total_files,
            "total_symbols": total_symbols,
            "symbol_breakdown": dict(symbol_breakdown)
        },
        "key_files": [{"path": path, "summary": summary} for path, summary in key_files],
        "indexed": True
    }
