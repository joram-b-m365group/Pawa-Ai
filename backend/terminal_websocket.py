"""
Terminal WebSocket Handler
Provides real-time terminal access via WebSocket
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pathlib import Path
import asyncio
import subprocess
import os
import sys

router = APIRouter(prefix="/terminal", tags=["Terminal"])

# Store active terminal sessions
active_sessions = {}


class TerminalSession:
    def __init__(self, websocket: WebSocket, project_path: str):
        self.websocket = websocket
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.process = None
        self.session_id = id(self)

    async def start_shell(self):
        """Start a shell process"""
        try:
            # Determine shell based on OS
            if sys.platform == "win32":
                shell = ["cmd.exe"]
            else:
                shell = ["/bin/bash"]

            # Start process
            self.process = await asyncio.create_subprocess_exec(
                *shell,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(self.project_path),
                env=os.environ.copy()
            )

            # Send initial prompt
            await self.websocket.send_text(f"Terminal started in: {self.project_path}\n\n")

        except Exception as e:
            await self.websocket.send_text(f"Error starting shell: {str(e)}\n")

    async def send_command(self, command: str):
        """Send command to shell"""
        if not self.process or self.process.returncode is not None:
            await self.websocket.send_text("Shell not running. Reconnect to start a new session.\n")
            return

        try:
            # Write command to stdin
            self.process.stdin.write(f"{command}\n".encode())
            await self.process.stdin.drain()

        except Exception as e:
            await self.websocket.send_text(f"Error sending command: {str(e)}\n")

    async def read_output(self):
        """Read output from shell and send to websocket"""
        if not self.process:
            return

        try:
            while True:
                # Read line from stdout
                line = await self.process.stdout.readline()
                if not line:
                    break

                # Send to websocket
                await self.websocket.send_text(line.decode('utf-8', errors='ignore'))

        except Exception as e:
            await self.websocket.send_text(f"\nError reading output: {str(e)}\n")

    async def close(self):
        """Close the terminal session"""
        if self.process and self.process.returncode is None:
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=2.0)
            except asyncio.TimeoutError:
                self.process.kill()
            except:
                pass


@router.websocket("/ws")
async def terminal_websocket(websocket: WebSocket, project_path: str = None):
    """
    WebSocket endpoint for terminal access
    Usage: ws://localhost:8000/terminal/ws?project_path=/path/to/project
    """
    await websocket.accept()

    session = TerminalSession(websocket, project_path)
    active_sessions[session.session_id] = session

    try:
        # Start shell
        await session.start_shell()

        # Create tasks for reading output and handling input
        output_task = asyncio.create_task(session.read_output())

        # Handle incoming commands
        while True:
            try:
                # Receive command from client
                data = await websocket.receive_text()

                if data == "__CLOSE__":
                    break

                # Send command to shell
                await session.send_command(data)

            except WebSocketDisconnect:
                break
            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}\n")

        # Cancel output task
        output_task.cancel()

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Terminal error: {str(e)}")
    finally:
        # Cleanup
        await session.close()
        if session.session_id in active_sessions:
            del active_sessions[session.session_id]
        try:
            await websocket.close()
        except:
            pass


@router.post("/execute")
async def execute_command(command: str, project_path: str = None):
    """
    Execute a single command and return output (non-interactive)
    Useful for one-off commands
    """
    try:
        working_dir = Path(project_path) if project_path else Path.cwd()

        # Execute command
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(working_dir),
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/active-sessions")
async def get_active_sessions():
    """Get list of active terminal sessions"""
    return {
        "count": len(active_sessions),
        "sessions": [
            {
                "id": session_id,
                "project_path": str(session.project_path),
                "alive": session.process and session.process.returncode is None
            }
            for session_id, session in active_sessions.items()
        ]
    }
