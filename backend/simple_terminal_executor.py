"""
Simple Terminal Executor API
Provides REST endpoints to execute commands and get output
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import subprocess
import os
import sys

router = APIRouter(prefix="/terminal", tags=["Terminal"])


class ExecuteCommandRequest(BaseModel):
    command: str
    cwd: Optional[str] = None
    timeout: int = 30  # seconds


class ExecuteCommandResponse(BaseModel):
    output: str
    error: Optional[str] = None
    exit_code: int
    success: bool


@router.post("/execute", response_model=ExecuteCommandResponse)
async def execute_command(request: ExecuteCommandRequest):
    """
    Execute a shell command and return the output

    Supports:
    - Node.js (node file.js)
    - Python (python file.py)
    - TypeScript (ts-node file.ts)
    - Any shell command
    """
    try:
        # Set working directory
        cwd = request.cwd if request.cwd else os.getcwd()

        # Determine shell based on OS
        if sys.platform == "win32":
            # On Windows, use cmd.exe
            shell = True
            command = request.command
        else:
            # On Unix, use bash
            shell = True
            command = request.command

        # Execute command
        result = subprocess.run(
            command,
            shell=shell,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=request.timeout
        )

        # Get output
        output = result.stdout if result.stdout else ""
        error = result.stderr if result.stderr else None

        return ExecuteCommandResponse(
            output=output,
            error=error,
            exit_code=result.returncode,
            success=result.returncode == 0
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail=f"Command execution timed out after {request.timeout} seconds"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute command: {str(e)}"
        )


@router.post("/run-file")
async def run_file(file_path: str, file_type: str, cwd: Optional[str] = None):
    """
    Run a file based on its type

    Supported types:
    - javascript, js: Run with node
    - typescript, ts: Run with ts-node
    - python, py: Run with python
    """
    try:
        # Determine command based on file type
        if file_type in ['javascript', 'js']:
            command = f'node "{file_path}"'
        elif file_type in ['typescript', 'ts']:
            command = f'ts-node "{file_path}"'
        elif file_type in ['python', 'py']:
            command = f'python "{file_path}"'
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_type}"
            )

        # Execute
        request = ExecuteCommandRequest(command=command, cwd=cwd)
        return await execute_command(request)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run file: {str(e)}"
        )


@router.get("/check-tools")
async def check_available_tools():
    """
    Check which tools are available in the system
    """
    tools = {}

    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        tools['node'] = {
            'available': result.returncode == 0,
            'version': result.stdout.strip() if result.returncode == 0 else None
        }
    except:
        tools['node'] = {'available': False, 'version': None}

    # Check Python
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True, timeout=5)
        tools['python'] = {
            'available': result.returncode == 0,
            'version': result.stdout.strip() if result.returncode == 0 else None
        }
    except:
        tools['python'] = {'available': False, 'version': None}

    # Check TypeScript
    try:
        result = subprocess.run(['ts-node', '--version'], capture_output=True, text=True, timeout=5)
        tools['ts-node'] = {
            'available': result.returncode == 0,
            'version': result.stdout.strip() if result.returncode == 0 else None
        }
    except:
        tools['ts-node'] = {'available': False, 'version': None}

    return tools


@router.get("/health")
async def terminal_health():
    """Check if terminal executor is working"""
    try:
        # Simple test command
        result = subprocess.run(
            ['echo', 'hello'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return {
            'status': 'healthy',
            'test_output': result.stdout.strip()
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
