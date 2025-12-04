"""
Smart Defaults System
Auto-setup and intelligent configuration on first run
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import os
import platform

router = APIRouter(prefix="/setup", tags=["Smart Defaults"])


class UserSetup(BaseModel):
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    preferences: Dict[str, Any] = {}


class ProjectStructureDetection(BaseModel):
    project_path: str


class SmartDefaultsManager:
    """
    Manages smart defaults and auto-configuration
    """

    def __init__(self):
        self.config_dir = Path.home() / ".pawa_ai"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.setup_complete_file = self.config_dir / ".setup_complete"

    def is_first_run(self) -> bool:
        """Check if this is the first time running Pawa AI"""
        return not self.setup_complete_file.exists()

    def mark_setup_complete(self):
        """Mark setup as complete"""
        self.setup_complete_file.touch()
        with open(self.setup_complete_file, 'w') as f:
            f.write(f"Setup completed at {datetime.now().isoformat()}")

    def create_default_user(self) -> Dict[str, Any]:
        """Create a default user profile"""
        # Try to get system username
        system_user = os.getenv('USERNAME') or os.getenv('USER') or 'user'

        user_id = f"user_{int(datetime.now().timestamp())}"

        user_config = {
            "user_id": user_id,
            "name": system_user,
            "created_at": datetime.now().isoformat(),
            "preferences": {
                "theme": "dark",
                "preferred_model": "llama-3.3-70b-versatile",
                "auto_save": True,
                "show_line_numbers": True,
                "word_wrap": True,
                "font_size": 14,
                "enable_voice_coding": False,
                "enable_ai_suggestions": True,
                "auto_format_on_save": True,
                "show_minimap": True,
                "enable_keyboard_shortcuts": True
            },
            "recommended_features": [
                "voice_coding",
                "code_review",
                "project_templates",
                "codebase_indexing"
            ]
        }

        # Save to config
        self.save_config(user_config)

        return user_config

    def detect_project_structure(self, project_path: str) -> Dict[str, Any]:
        """
        Auto-detect project type and structure
        """
        path = Path(project_path)

        if not path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")

        project_info = {
            "path": str(path),
            "name": path.name,
            "type": "unknown",
            "language": "unknown",
            "framework": None,
            "has_git": False,
            "has_venv": False,
            "has_node_modules": False,
            "recommended_index_patterns": []
        }

        # Check for git
        if (path / ".git").exists():
            project_info["has_git"] = True

        # Detect Python projects
        if (path / "requirements.txt").exists() or (path / "setup.py").exists() or (path / "pyproject.toml").exists():
            project_info["type"] = "python"
            project_info["language"] = "python"
            project_info["recommended_index_patterns"] = ["*.py"]

            if (path / "venv").exists() or (path / ".venv").exists():
                project_info["has_venv"] = True

            # Detect frameworks
            if (path / "manage.py").exists():
                project_info["framework"] = "django"
            elif (path / "app.py").exists() or (path / "main.py").exists():
                try:
                    with open(path / "requirements.txt") as f:
                        content = f.read()
                        if "flask" in content.lower():
                            project_info["framework"] = "flask"
                        elif "fastapi" in content.lower():
                            project_info["framework"] = "fastapi"
                except:
                    pass

        # Detect JavaScript/TypeScript projects
        elif (path / "package.json").exists():
            project_info["type"] = "javascript"
            project_info["recommended_index_patterns"] = ["*.js", "*.jsx", "*.ts", "*.tsx"]

            if (path / "node_modules").exists():
                project_info["has_node_modules"] = True

            # Detect frameworks
            try:
                with open(path / "package.json") as f:
                    package_json = json.load(f)
                    dependencies = {**package_json.get("dependencies", {}), **package_json.get("devDependencies", {})}

                    if "react" in dependencies:
                        project_info["framework"] = "react"
                        project_info["language"] = "typescript" if (path / "tsconfig.json").exists() else "javascript"
                    elif "vue" in dependencies:
                        project_info["framework"] = "vue"
                    elif "angular" in dependencies or "@angular/core" in dependencies:
                        project_info["framework"] = "angular"
                    elif "next" in dependencies:
                        project_info["framework"] = "nextjs"
                    elif "express" in dependencies:
                        project_info["framework"] = "express"
            except:
                pass

        # Detect Go projects
        elif (path / "go.mod").exists():
            project_info["type"] = "go"
            project_info["language"] = "go"
            project_info["recommended_index_patterns"] = ["*.go"]

        # Detect Rust projects
        elif (path / "Cargo.toml").exists():
            project_info["type"] = "rust"
            project_info["language"] = "rust"
            project_info["recommended_index_patterns"] = ["*.rs"]

        # Detect Java projects
        elif (path / "pom.xml").exists() or (path / "build.gradle").exists():
            project_info["type"] = "java"
            project_info["language"] = "java"
            project_info["recommended_index_patterns"] = ["*.java"]

            if (path / "pom.xml").exists():
                project_info["framework"] = "maven"
            elif (path / "build.gradle").exists():
                project_info["framework"] = "gradle"

        return project_info

    def get_recommended_settings(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get recommended settings based on project type
        """
        settings = {
            "editor": {
                "tab_size": 4 if project_info.get("language") == "python" else 2,
                "insert_spaces": True,
                "detect_indentation": True,
                "trim_trailing_whitespace": True,
                "format_on_save": True
            },
            "indexing": {
                "enabled": True,
                "file_patterns": project_info.get("recommended_index_patterns", ["*.py", "*.js", "*.ts"]),
                "exclude_patterns": [
                    "node_modules/**",
                    "venv/**",
                    ".venv/**",
                    "*.min.js",
                    "dist/**",
                    "build/**",
                    "__pycache__/**",
                    ".git/**"
                ]
            },
            "ai": {
                "enable_suggestions": True,
                "enable_auto_complete": True,
                "enable_code_review": True,
                "preferred_model": "llama-3.3-70b-versatile"
            }
        }

        # Framework-specific settings
        if project_info.get("framework") == "react":
            settings["editor"]["tab_size"] = 2
            settings["indexing"]["file_patterns"].extend(["*.jsx", "*.tsx"])

        elif project_info.get("framework") == "django":
            settings["indexing"]["file_patterns"].append("*.html")
            settings["indexing"]["exclude_patterns"].extend(["staticfiles/**", "media/**"])

        return settings

    def save_config(self, config: Dict[str, Any]):
        """Save configuration to disk"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def load_config(self) -> Optional[Dict[str, Any]]:
        """Load configuration from disk"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return None

    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }


# Global manager
smart_defaults = SmartDefaultsManager()


@router.get("/is-first-run")
async def is_first_run():
    """Check if this is the first run"""
    return {
        "is_first_run": smart_defaults.is_first_run(),
        "config_exists": smart_defaults.config_file.exists()
    }


@router.post("/initialize")
async def initialize_setup(setup: Optional[UserSetup] = None):
    """
    Initialize Pawa AI with smart defaults
    """
    try:
        # Create default user if none provided
        if not setup:
            user_config = smart_defaults.create_default_user()
        else:
            user_config = {
                "user_id": setup.user_id,
                "name": setup.name,
                "email": setup.email,
                "created_at": datetime.now().isoformat(),
                "preferences": setup.preferences or smart_defaults.create_default_user()["preferences"]
            }
            smart_defaults.save_config(user_config)

        # Mark setup as complete
        smart_defaults.mark_setup_complete()

        # Get system info
        system_info = smart_defaults.get_system_info()

        return {
            "success": True,
            "user": user_config,
            "system": system_info,
            "message": "Pawa AI initialized successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)}")


@router.post("/detect-project")
async def detect_project(request: ProjectStructureDetection):
    """
    Detect project structure and recommend settings
    """
    try:
        project_info = smart_defaults.detect_project_structure(request.project_path)
        recommended_settings = smart_defaults.get_recommended_settings(project_info)

        return {
            "success": True,
            "project": project_info,
            "recommended_settings": recommended_settings,
            "auto_index": project_info.get("type") != "unknown"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Project detection failed: {str(e)}")


@router.get("/config")
async def get_config():
    """Get current configuration"""
    config = smart_defaults.load_config()

    if not config:
        return {"config": None, "message": "No configuration found"}

    return {"config": config}


@router.put("/config")
async def update_config(config: Dict[str, Any]):
    """Update configuration"""
    try:
        existing_config = smart_defaults.load_config() or {}
        updated_config = {**existing_config, **config}
        smart_defaults.save_config(updated_config)

        return {
            "success": True,
            "config": updated_config,
            "message": "Configuration updated successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update config: {str(e)}")


@router.get("/system-info")
async def get_system_info():
    """Get system information"""
    return smart_defaults.get_system_info()
