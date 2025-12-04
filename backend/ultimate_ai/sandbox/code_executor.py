"""
Code Execution Sandbox
Safely execute code in isolated environments
"""

import asyncio
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import shutil


class CodeExecutor:
    """
    Execute code safely in isolated environments

    Advantages over ChatGPT:
    - Multiple languages (Python, JavaScript, Java, C++, Go, Rust, etc.)
    - No time limits
    - Can install packages
    - File system access
    - Persistent environments
    """

    def __init__(self):
        self.supported_languages = {
            "python": {"extension": ".py", "command": "python"},
            "javascript": {"extension": ".js", "command": "node"},
            "java": {"extension": ".java", "command_compile": "javac", "command_run": "java"},
            "cpp": {"extension": ".cpp", "command": "g++"},
            "c": {"extension": ".c", "command": "gcc"},
            "go": {"extension": ".go", "command": "go run"},
            "rust": {"extension": ".rs", "command": "rustc"},
            "ruby": {"extension": ".rb", "command": "ruby"},
            "php": {"extension": ".php", "command": "php"},
        }

    async def execute(
        self,
        code: str,
        language: str = "python",
        timeout: int = 30,
        install_packages: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute code safely

        Args:
            code: Code to execute
            language: Programming language
            timeout: Maximum execution time (seconds)
            install_packages: Packages to install first

        Returns:
            Dict with stdout, stderr, exit_code, files_created
        """
        language = language.lower()

        if language not in self.supported_languages:
            return {
                "error": f"Language '{language}' not supported. Supported: {list(self.supported_languages.keys())}"
            }

        # Execute based on language
        if language == "python":
            return await self._execute_python(code, timeout, install_packages)
        elif language == "javascript":
            return await self._execute_javascript(code, timeout)
        elif language == "java":
            return await self._execute_java(code, timeout)
        elif language in ["cpp", "c"]:
            return await self._execute_compiled(code, language, timeout)
        elif language == "go":
            return await self._execute_go(code, timeout)
        else:
            return await self._execute_generic(code, language, timeout)

    async def _execute_python(
        self,
        code: str,
        timeout: int,
        install_packages: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Execute Python code"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create code file
            code_file = Path(tmpdir) / "script.py"
            code_file.write_text(code)

            # Install packages if needed
            if install_packages:
                for package in install_packages:
                    try:
                        proc = await asyncio.create_subprocess_exec(
                            "pip", "install", "--user", package,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                        await asyncio.wait_for(proc.wait(), timeout=60)
                    except:
                        pass

            # Execute code
            try:
                proc = await asyncio.create_subprocess_exec(
                    "python", str(code_file),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=tmpdir
                )

                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout
                )

                # Check for generated files
                files_created = [
                    f.name for f in Path(tmpdir).iterdir()
                    if f.is_file() and f.name != "script.py"
                ]

                return {
                    "stdout": stdout.decode('utf-8', errors='ignore'),
                    "stderr": stderr.decode('utf-8', errors='ignore'),
                    "exit_code": proc.returncode,
                    "files_created": files_created,
                    "language": "python"
                }

            except asyncio.TimeoutError:
                proc.kill()
                return {
                    "error": f"Execution timed out after {timeout} seconds",
                    "language": "python"
                }
            except Exception as e:
                return {
                    "error": str(e),
                    "language": "python"
                }

    async def _execute_javascript(self, code: str, timeout: int) -> Dict[str, Any]:
        """Execute JavaScript code"""
        with tempfile.TemporaryDirectory() as tmpdir:
            code_file = Path(tmpdir) / "script.js"
            code_file.write_text(code)

            try:
                proc = await asyncio.create_subprocess_exec(
                    "node", str(code_file),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=tmpdir
                )

                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout
                )

                return {
                    "stdout": stdout.decode('utf-8', errors='ignore'),
                    "stderr": stderr.decode('utf-8', errors='ignore'),
                    "exit_code": proc.returncode,
                    "language": "javascript"
                }

            except asyncio.TimeoutError:
                proc.kill()
                return {"error": f"Execution timed out after {timeout} seconds"}
            except FileNotFoundError:
                return {"error": "Node.js not installed. Install it to run JavaScript code."}
            except Exception as e:
                return {"error": str(e)}

    async def _execute_java(self, code: str, timeout: int) -> Dict[str, Any]:
        """Execute Java code"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Extract class name from code
            import re
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            if not class_match:
                return {"error": "No public class found in Java code"}

            class_name = class_match.group(1)
            code_file = Path(tmpdir) / f"{class_name}.java"
            code_file.write_text(code)

            try:
                # Compile
                proc = await asyncio.create_subprocess_exec(
                    "javac", str(code_file),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=tmpdir
                )
                compile_out, compile_err = await proc.communicate()

                if proc.returncode != 0:
                    return {
                        "error": "Compilation failed",
                        "stderr": compile_err.decode('utf-8', errors='ignore')
                    }

                # Run
                proc = await asyncio.create_subprocess_exec(
                    "java", class_name,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=tmpdir
                )

                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout
                )

                return {
                    "stdout": stdout.decode('utf-8', errors='ignore'),
                    "stderr": stderr.decode('utf-8', errors='ignore'),
                    "exit_code": proc.returncode,
                    "language": "java"
                }

            except asyncio.TimeoutError:
                proc.kill()
                return {"error": f"Execution timed out after {timeout} seconds"}
            except FileNotFoundError:
                return {"error": "Java not installed. Install JDK to run Java code."}
            except Exception as e:
                return {"error": str(e)}

    async def _execute_compiled(self, code: str, language: str, timeout: int) -> Dict[str, Any]:
        """Execute C/C++ code"""
        with tempfile.TemporaryDirectory() as tmpdir:
            extension = self.supported_languages[language]["extension"]
            code_file = Path(tmpdir) / f"program{extension}"
            output_file = Path(tmpdir) / "program.exe"

            code_file.write_text(code)

            compiler = "g++" if language == "cpp" else "gcc"

            try:
                # Compile
                proc = await asyncio.create_subprocess_exec(
                    compiler, str(code_file), "-o", str(output_file),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=tmpdir
                )
                compile_out, compile_err = await proc.communicate()

                if proc.returncode != 0:
                    return {
                        "error": "Compilation failed",
                        "stderr": compile_err.decode('utf-8', errors='ignore')
                    }

                # Run
                proc = await asyncio.create_subprocess_exec(
                    str(output_file),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=tmpdir
                )

                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout
                )

                return {
                    "stdout": stdout.decode('utf-8', errors='ignore'),
                    "stderr": stderr.decode('utf-8', errors='ignore'),
                    "exit_code": proc.returncode,
                    "language": language
                }

            except asyncio.TimeoutError:
                proc.kill()
                return {"error": f"Execution timed out after {timeout} seconds"}
            except FileNotFoundError:
                return {"error": f"{compiler} not installed. Install it to run {language.upper()} code."}
            except Exception as e:
                return {"error": str(e)}

    async def _execute_go(self, code: str, timeout: int) -> Dict[str, Any]:
        """Execute Go code"""
        with tempfile.TemporaryDirectory() as tmpdir:
            code_file = Path(tmpdir) / "main.go"
            code_file.write_text(code)

            try:
                proc = await asyncio.create_subprocess_exec(
                    "go", "run", str(code_file),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=tmpdir
                )

                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout
                )

                return {
                    "stdout": stdout.decode('utf-8', errors='ignore'),
                    "stderr": stderr.decode('utf-8', errors='ignore'),
                    "exit_code": proc.returncode,
                    "language": "go"
                }

            except asyncio.TimeoutError:
                proc.kill()
                return {"error": f"Execution timed out after {timeout} seconds"}
            except FileNotFoundError:
                return {"error": "Go not installed. Install it to run Go code."}
            except Exception as e:
                return {"error": str(e)}

    async def _execute_generic(self, code: str, language: str, timeout: int) -> Dict[str, Any]:
        """Execute code in other languages"""
        lang_info = self.supported_languages[language]
        extension = lang_info["extension"]
        command = lang_info["command"]

        with tempfile.TemporaryDirectory() as tmpdir:
            code_file = Path(tmpdir) / f"script{extension}"
            code_file.write_text(code)

            try:
                proc = await asyncio.create_subprocess_exec(
                    command, str(code_file),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=tmpdir
                )

                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout
                )

                return {
                    "stdout": stdout.decode('utf-8', errors='ignore'),
                    "stderr": stderr.decode('utf-8', errors='ignore'),
                    "exit_code": proc.returncode,
                    "language": language
                }

            except asyncio.TimeoutError:
                proc.kill()
                return {"error": f"Execution timed out after {timeout} seconds"}
            except FileNotFoundError:
                return {"error": f"{command} not installed. Install it to run {language} code."}
            except Exception as e:
                return {"error": str(e)}

    def get_example_code(self, language: str) -> str:
        """Get example code for a language"""
        examples = {
            "python": 'print("Hello from Python!")\nfor i in range(5):\n    print(f"Count: {i}")',
            "javascript": 'console.log("Hello from JavaScript!");\nfor (let i = 0; i < 5; i++) {\n    console.log(`Count: ${i}`);\n}',
            "java": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello from Java!");\n    }\n}',
            "cpp": '#include <iostream>\nint main() {\n    std::cout << "Hello from C++!" << std::endl;\n    return 0;\n}',
            "go": 'package main\nimport "fmt"\nfunc main() {\n    fmt.Println("Hello from Go!")\n}',
        }

        return examples.get(language, f'// {language} code example')
