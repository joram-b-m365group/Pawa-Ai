"""
Pawa AI Agent Tools System
Enables AI to perform file operations, terminal commands, and codebase analysis
Similar to Claude Code's tool-calling system
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class AIAgentTools:
    """Tool system for AI agent to interact with codebase"""

    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.conversation_context = {
            "files_read": [],
            "files_modified": [],
            "commands_run": [],
            "current_task": None
        }

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools in OpenAI function calling format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the contents of a file in the project",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Relative path to the file from project root"
                            },
                            "start_line": {
                                "type": "integer",
                                "description": "Optional: Start reading from this line number"
                            },
                            "end_line": {
                                "type": "integer",
                                "description": "Optional: Stop reading at this line number"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Create a new file or completely overwrite an existing file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Relative path to the file from project root"
                            },
                            "content": {
                                "type": "string",
                                "description": "Complete file content to write"
                            }
                        },
                        "required": ["file_path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_file",
                    "description": "Edit specific lines in a file using find-and-replace",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Relative path to the file from project root"
                            },
                            "old_string": {
                                "type": "string",
                                "description": "Exact string to find (must match exactly including whitespace)"
                            },
                            "new_string": {
                                "type": "string",
                                "description": "String to replace it with"
                            }
                        },
                        "required": ["file_path", "old_string", "new_string"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "description": "Search for text patterns across files in the project (like grep)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": "Search pattern (supports regex)"
                            },
                            "file_pattern": {
                                "type": "string",
                                "description": "Optional: File glob pattern (e.g., '*.py', '*.tsx')"
                            },
                            "case_sensitive": {
                                "type": "boolean",
                                "description": "Whether search is case sensitive (default: false)"
                            }
                        },
                        "required": ["pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List files and directories in the project",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Optional: Subdirectory to list (default: project root)"
                            },
                            "pattern": {
                                "type": "string",
                                "description": "Optional: Glob pattern to filter files (e.g., '*.py')"
                            },
                            "recursive": {
                                "type": "boolean",
                                "description": "Whether to list files recursively (default: false)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_command",
                    "description": "Execute a terminal command in the project directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Shell command to execute"
                            },
                            "timeout": {
                                "type": "integer",
                                "description": "Optional: Timeout in seconds (default: 30)"
                            }
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_file_tree",
                    "description": "Get the complete file tree structure of the project",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "max_depth": {
                                "type": "integer",
                                "description": "Maximum depth to traverse (default: 5)"
                            },
                            "exclude_patterns": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Patterns to exclude (e.g., ['node_modules', '.git'])"
                            }
                        }
                    }
                }
            }
        ]

    def read_file(self, file_path: str, start_line: int = None, end_line: int = None) -> Dict[str, Any]:
        """Read file contents"""
        try:
            full_path = self.project_root / file_path

            if not full_path.exists():
                return {"success": False, "error": f"File not found: {file_path}"}

            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Track in context
            self.conversation_context["files_read"].append(str(file_path))

            # Handle line ranges
            if start_line is not None or end_line is not None:
                start = (start_line - 1) if start_line else 0
                end = end_line if end_line else len(lines)
                lines = lines[start:end]
                content = ''.join(lines)
                return {
                    "success": True,
                    "content": content,
                    "file_path": file_path,
                    "lines": f"{start_line or 1}-{end_line or len(lines)}",
                    "total_lines": len(lines)
                }

            content = ''.join(lines)
            return {
                "success": True,
                "content": content,
                "file_path": file_path,
                "total_lines": len(lines)
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Write or create a file"""
        try:
            full_path = self.project_root / file_path

            # Create parent directories if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Track in context
            self.conversation_context["files_modified"].append(str(file_path))

            return {
                "success": True,
                "message": f"Successfully wrote {len(content)} characters to {file_path}",
                "file_path": file_path,
                "lines_written": len(content.split('\n'))
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def edit_file(self, file_path: str, old_string: str, new_string: str) -> Dict[str, Any]:
        """Edit file using find-and-replace"""
        try:
            full_path = self.project_root / file_path

            if not full_path.exists():
                return {"success": False, "error": f"File not found: {file_path}"}

            # Read current content
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if old_string exists
            if old_string not in content:
                return {
                    "success": False,
                    "error": f"String not found in file. Make sure the old_string matches exactly including whitespace."
                }

            # Count occurrences
            occurrences = content.count(old_string)
            if occurrences > 1:
                return {
                    "success": False,
                    "error": f"Found {occurrences} occurrences. Please provide a more specific string to ensure only one match."
                }

            # Replace
            new_content = content.replace(old_string, new_string)

            # Write back
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # Track in context
            self.conversation_context["files_modified"].append(str(file_path))

            return {
                "success": True,
                "message": f"Successfully edited {file_path}",
                "file_path": file_path,
                "changes": f"Replaced {len(old_string)} chars with {len(new_string)} chars"
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def search_files(self, pattern: str, file_pattern: str = "*", case_sensitive: bool = False) -> Dict[str, Any]:
        """Search for pattern in files"""
        try:
            matches = []
            flags = 0 if case_sensitive else re.IGNORECASE
            regex = re.compile(pattern, flags)

            # Find matching files
            if file_pattern == "*":
                files = list(self.project_root.rglob("*"))
            else:
                files = list(self.project_root.rglob(file_pattern))

            # Search in each file
            for file_path in files:
                if file_path.is_file():
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            for i, line in enumerate(lines, 1):
                                if regex.search(line):
                                    matches.append({
                                        "file": str(file_path.relative_to(self.project_root)),
                                        "line": i,
                                        "content": line.strip()
                                    })
                    except:
                        continue

            return {
                "success": True,
                "pattern": pattern,
                "matches": matches[:100],  # Limit to 100 results
                "total_matches": len(matches),
                "truncated": len(matches) > 100
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_files(self, path: str = "", pattern: str = "*", recursive: bool = False) -> Dict[str, Any]:
        """List files in directory"""
        try:
            target_path = self.project_root / path if path else self.project_root

            if not target_path.exists():
                return {"success": False, "error": f"Path not found: {path}"}

            if recursive:
                files = list(target_path.rglob(pattern))
            else:
                files = list(target_path.glob(pattern))

            items = []
            for file_path in files:
                rel_path = file_path.relative_to(self.project_root)
                items.append({
                    "name": file_path.name,
                    "path": str(rel_path),
                    "type": "directory" if file_path.is_dir() else "file",
                    "size": file_path.stat().st_size if file_path.is_file() else None
                })

            return {
                "success": True,
                "path": path or ".",
                "items": items,
                "count": len(items)
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute terminal command"""
        try:
            # Track in context
            self.conversation_context["commands_run"].append(command)

            # Run command
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "success": result.returncode == 0,
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after {timeout} seconds"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_file_tree(self, max_depth: int = 5, exclude_patterns: List[str] = None) -> Dict[str, Any]:
        """Get file tree structure"""
        try:
            if exclude_patterns is None:
                exclude_patterns = ['node_modules', '.git', '__pycache__', 'dist', 'build', '.venv', 'venv']

            def build_tree(path: Path, depth: int = 0) -> Dict:
                if depth > max_depth:
                    return None

                # Check exclusions
                if any(pattern in path.name for pattern in exclude_patterns):
                    return None

                if path.is_file():
                    return {
                        "name": path.name,
                        "type": "file",
                        "path": str(path.relative_to(self.project_root))
                    }

                children = []
                try:
                    for child in sorted(path.iterdir()):
                        tree_item = build_tree(child, depth + 1)
                        if tree_item:
                            children.append(tree_item)
                except PermissionError:
                    pass

                return {
                    "name": path.name,
                    "type": "directory",
                    "path": str(path.relative_to(self.project_root)),
                    "children": children
                }

            tree = build_tree(self.project_root)

            return {
                "success": True,
                "tree": tree,
                "project_root": str(self.project_root)
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name with given arguments"""
        tool_methods = {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "edit_file": self.edit_file,
            "search_files": self.search_files,
            "list_files": self.list_files,
            "run_command": self.run_command,
            "get_file_tree": self.get_file_tree
        }

        if tool_name not in tool_methods:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}

        try:
            return tool_methods[tool_name](**arguments)
        except TypeError as e:
            return {"success": False, "error": f"Invalid arguments: {str(e)}"}

    def get_context_summary(self) -> str:
        """Get summary of conversation context for AI"""
        files_read = set(self.conversation_context["files_read"])
        files_modified = set(self.conversation_context["files_modified"])

        summary = []
        if files_read:
            summary.append(f"Files read: {', '.join(list(files_read)[:5])}")
        if files_modified:
            summary.append(f"Files modified: {', '.join(list(files_modified)[:5])}")
        if self.conversation_context["commands_run"]:
            summary.append(f"Commands run: {len(self.conversation_context['commands_run'])}")

        return " | ".join(summary) if summary else "No previous context"
