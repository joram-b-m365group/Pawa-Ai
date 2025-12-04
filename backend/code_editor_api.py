"""
Pawa AI Code Editor API
Handles file system operations, terminal commands, and code analysis
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import subprocess
import json
from pathlib import Path
from groq import Groq
import uvicorn
import threading
import http.server
import socketserver
from urllib.parse import unquote

app = FastAPI(title="Pawa AI Code Editor", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client for AI assistance
groq_client = Groq(api_key="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")

# Base directory for user projects (sandboxed)
PROJECTS_DIR = Path("user_projects")
PROJECTS_DIR.mkdir(exist_ok=True)

# Track currently opened project for preview
current_preview_project = None
preview_server = None
preview_port = 8002

class FileNode(BaseModel):
    name: str
    path: str
    type: str  # 'file' or 'directory'
    children: Optional[List['FileNode']] = None

class ReadFileRequest(BaseModel):
    path: str

class WriteFileRequest(BaseModel):
    path: str
    content: str

class DeleteFileRequest(BaseModel):
    path: str

class CreateFolderRequest(BaseModel):
    path: str

class ExecuteCommandRequest(BaseModel):
    command: str
    cwd: Optional[str] = None

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    question: str

class CodeEditRequest(BaseModel):
    file_path: str
    instruction: str
    context: Optional[str] = None

class BrowseRequest(BaseModel):
    path: Optional[str] = None  # If None, start from user's home or common folders

class OpenLocalProjectRequest(BaseModel):
    path: str  # Absolute path to local project

def is_safe_path(path: str) -> bool:
    """Check if path is within the projects directory"""
    try:
        full_path = (PROJECTS_DIR / path).resolve()
        return str(full_path).startswith(str(PROJECTS_DIR.resolve()))
    except:
        return False

def get_file_tree(directory: Path, relative_to: Path) -> FileNode:
    """Recursively build file tree"""
    try:
        relative_path = str(directory.relative_to(relative_to))
        node = FileNode(
            name=directory.name,
            path=relative_path,
            type='directory' if directory.is_dir() else 'file'
        )

        if directory.is_dir():
            children = []
            try:
                for item in sorted(directory.iterdir()):
                    # Skip hidden files and common ignore patterns
                    if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', 'venv', 'dist', 'build']:
                        continue
                    children.append(get_file_tree(item, relative_to))
                node.children = children
            except PermissionError:
                pass

        return node
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Pawa AI Code Editor API",
        "version": "1.0"
    }

@app.get("/projects")
def list_projects():
    """List all user projects"""
    try:
        projects = []
        for item in PROJECTS_DIR.iterdir():
            if item.is_dir():
                projects.append({
                    "name": item.name,
                    "path": item.name,
                    "created": item.stat().st_ctime
                })
        return {"projects": sorted(projects, key=lambda x: x['created'], reverse=True)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/projects/create")
def create_project(name: str):
    """Create a new project"""
    try:
        project_path = PROJECTS_DIR / name
        if project_path.exists():
            raise HTTPException(status_code=400, detail="Project already exists")

        project_path.mkdir(parents=True)

        # Create initial files
        (project_path / "README.md").write_text(f"# {name}\n\nCreated with Pawa AI")
        (project_path / "index.html").write_text("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Project</title>
</head>
<body>
    <h1>Hello from Pawa AI!</h1>
</body>
</html>""")

        return {"success": True, "message": f"Project '{name}' created", "path": name}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/browse/drives")
def list_drives():
    """List available drives (Windows) or common folders (Unix)"""
    try:
        import platform
        if platform.system() == 'Windows':
            import string
            from ctypes import windll
            drives = []
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drives.append(f"{letter}:")
                bitmask >>= 1
            return {"drives": drives}
        else:
            # For Unix-like systems, return common folders
            home = str(Path.home())
            return {"drives": [home, "/", "/usr", "/opt"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/browse/folder")
def browse_folder(request: BrowseRequest):
    """Browse folders and files in a directory"""
    try:
        if request.path:
            browse_path = Path(request.path)
        else:
            browse_path = Path.home()

        if not browse_path.exists():
            raise HTTPException(status_code=404, detail="Path not found")

        if not browse_path.is_dir():
            raise HTTPException(status_code=400, detail="Path is not a directory")

        items = []
        try:
            for item in sorted(browse_path.iterdir()):
                # Skip hidden files
                if item.name.startswith('.'):
                    continue

                items.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0
                })
        except PermissionError:
            pass

        return {
            "path": str(browse_path),
            "parent": str(browse_path.parent) if browse_path.parent != browse_path else None,
            "items": items
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/projects/open-local")
def open_local_project(request: OpenLocalProjectRequest):
    """Open a local project from file system"""
    global current_preview_project
    try:
        project_path = Path(request.path)

        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project path not found")

        if not project_path.is_dir():
            raise HTTPException(status_code=400, detail="Path is not a directory")

        # Store the project path for later operations
        current_preview_project = str(project_path)

        return {
            "success": True,
            "message": f"Opened local project: {project_path.name}",
            "path": str(project_path),
            "name": project_path.name
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/preview/start")
def start_preview():
    """Start preview server for current project"""
    global preview_server, current_preview_project

    if not current_preview_project:
        raise HTTPException(status_code=400, detail="No project open")

    try:
        # Simple HTTP server for preview
        os.chdir(current_preview_project)

        return {
            "success": True,
            "url": f"http://localhost:{preview_port}",
            "message": "Preview server started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/tree")
def get_files_tree(project: str, local: bool = False):
    """Get file tree for a project (supports both sandboxed and local projects)"""
    global current_preview_project
    try:
        if local or (current_preview_project and project == current_preview_project):
            # Local project - use full path
            project_path = Path(project)
            if not project_path.exists():
                raise HTTPException(status_code=404, detail="Project not found")
            tree = get_file_tree(project_path, project_path.parent)
        else:
            # Sandboxed project
            if not is_safe_path(project):
                raise HTTPException(status_code=403, detail="Access denied")

            project_path = PROJECTS_DIR / project
            if not project_path.exists():
                raise HTTPException(status_code=404, detail="Project not found")

            tree = get_file_tree(project_path, PROJECTS_DIR)

        return tree
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/serve")
def serve_file(path: str):
    """Serve binary files (images, PDFs, etc.) for viewing"""
    global current_preview_project
    try:
        # Check if this is a local project file (absolute path)
        if Path(path).is_absolute() or (current_preview_project and path.startswith(current_preview_project)):
            file_path = Path(path)
        else:
            # Sandboxed project
            if not is_safe_path(path):
                raise HTTPException(status_code=403, detail="Access denied")
            file_path = PROJECTS_DIR / path

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        if not file_path.is_file():
            raise HTTPException(status_code=400, detail="Not a file")

        return FileResponse(file_path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/read")
def read_file(request: ReadFileRequest):
    """Read file contents (supports both sandboxed and local projects)"""
    global current_preview_project
    try:
        # Check if this is a local project file (absolute path)
        if Path(request.path).is_absolute() or (current_preview_project and request.path.startswith(current_preview_project)):
            file_path = Path(request.path)
        else:
            # Sandboxed project
            if not is_safe_path(request.path):
                raise HTTPException(status_code=403, detail="Access denied")
            file_path = PROJECTS_DIR / request.path

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        if not file_path.is_file():
            raise HTTPException(status_code=400, detail="Not a file")

        content = file_path.read_text(encoding='utf-8', errors='ignore')
        return {"content": content, "path": str(file_path)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/write")
def write_file(request: WriteFileRequest):
    """Write file contents (supports both sandboxed and local projects)"""
    global current_preview_project
    try:
        # Check if this is a local project file (absolute path)
        if Path(request.path).is_absolute() or (current_preview_project and request.path.startswith(current_preview_project)):
            file_path = Path(request.path)
        else:
            # Sandboxed project
            if not is_safe_path(request.path):
                raise HTTPException(status_code=403, detail="Access denied")
            file_path = PROJECTS_DIR / request.path

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(request.content, encoding='utf-8')

        return {"success": True, "message": "File saved", "path": str(file_path)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/delete")
def delete_file(request: DeleteFileRequest):
    """Delete a file or directory"""
    try:
        if not is_safe_path(request.path):
            raise HTTPException(status_code=403, detail="Access denied")

        file_path = PROJECTS_DIR / request.path
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        if file_path.is_file():
            file_path.unlink()
        else:
            import shutil
            shutil.rmtree(file_path)

        return {"success": True, "message": "Deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/create-folder")
def create_folder(request: CreateFolderRequest):
    """Create a new folder"""
    try:
        if not is_safe_path(request.path):
            raise HTTPException(status_code=403, detail="Access denied")

        folder_path = PROJECTS_DIR / request.path
        folder_path.mkdir(parents=True, exist_ok=True)

        return {"success": True, "message": "Folder created"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/terminal/execute")
def execute_command(request: ExecuteCommandRequest):
    """Execute a terminal command (sandboxed)"""
    try:
        # Whitelist of safe commands
        safe_commands = ['npm', 'python', 'node', 'git', 'ls', 'dir', 'cat', 'echo', 'mkdir', 'touch']
        command_parts = request.command.split()

        if not command_parts or command_parts[0] not in safe_commands:
            raise HTTPException(status_code=403, detail="Command not allowed")

        cwd = PROJECTS_DIR / request.cwd if request.cwd else PROJECTS_DIR

        if not is_safe_path(str(cwd.relative_to(PROJECTS_DIR)) if request.cwd else ""):
            raise HTTPException(status_code=403, detail="Access denied")

        result = subprocess.run(
            request.command,
            shell=True,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timeout")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/analyze-code")
async def analyze_code(request: CodeAnalysisRequest):
    """AI code analysis"""
    try:
        prompt = f"""You are an expert {request.language} developer. Analyze the following code and answer the question.

Code:
```{request.language}
{request.code}
```

Question: {request.question}

Provide a clear, concise answer with code examples if needed."""

        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert software developer and code analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096,
        )

        return {
            "analysis": completion.choices[0].message.content,
            "tokens_used": completion.usage.total_tokens if hasattr(completion, 'usage') else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/edit-code")
async def edit_code(request: CodeEditRequest):
    """AI-powered code editing"""
    try:
        # Read the file
        if not is_safe_path(request.file_path):
            raise HTTPException(status_code=403, detail="Access denied")

        file_path = PROJECTS_DIR / request.file_path
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        current_code = file_path.read_text(encoding='utf-8', errors='ignore')

        # Determine language from file extension
        ext = file_path.suffix
        lang_map = {'.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                    '.html': 'html', '.css': 'css', '.jsx': 'jsx', '.tsx': 'tsx'}
        language = lang_map.get(ext, 'text')

        prompt = f"""You are an expert developer. Edit the following code according to the instruction.

Current code:
```{language}
{current_code}
```

Instruction: {request.instruction}

{f"Additional context: {request.context}" if request.context else ""}

IMPORTANT: Return ONLY the complete modified code, with no explanations or markdown formatting. Just the raw code."""

        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert software developer. Return only code, no explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=8192,
        )

        new_code = completion.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if new_code.startswith('```'):
            lines = new_code.split('\n')
            new_code = '\n'.join(lines[1:-1]) if len(lines) > 2 else new_code

        # Save the edited file
        file_path.write_text(new_code, encoding='utf-8')

        return {
            "success": True,
            "message": "Code edited successfully",
            "new_code": new_code
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("=" * 70)
    print("PAWA AI CODE EDITOR API")
    print("=" * 70)
    print("File Operations: ENABLED")
    print("Terminal: ENABLED (Sandboxed)")
    print("AI Code Assistant: ENABLED")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8001)
