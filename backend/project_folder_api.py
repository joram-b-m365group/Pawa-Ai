"""
Project Folder Management API
Handles creation and management of project folders for any type of project
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import subprocess
import platform

router = APIRouter(prefix="/project-folders", tags=["Project Folders"])


class CreateProjectFolderRequest(BaseModel):
    name: str
    path: str
    type: str
    subfolders: Optional[List[str]] = []


class OpenFolderRequest(BaseModel):
    path: str


@router.post("/create-project-folder")
async def create_project_folder(request: CreateProjectFolderRequest):
    """
    Create a new project folder with subfolders
    """
    try:
        # Normalize path
        project_path = os.path.normpath(request.path)

        # Create main project directory
        os.makedirs(project_path, exist_ok=True)

        # Create subfolders
        created_folders = []
        for subfolder in request.subfolders:
            subfolder_path = os.path.join(project_path, subfolder)
            os.makedirs(subfolder_path, exist_ok=True)
            created_folders.append(subfolder)

        # Create a README file
        readme_path = os.path.join(project_path, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# {request.name}\n\n")
            f.write(f"Project Type: {request.type}\n\n")
            f.write(f"Created by Pawa AI\n\n")
            f.write(f"## Structure\n\n")
            for folder in created_folders:
                f.write(f"- `{folder}/`\n")

        return {
            "success": True,
            "message": f"Project folder '{request.name}' created successfully",
            "path": project_path,
            "subfolders": created_folders
        }

    except PermissionError:
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: Cannot create folder at {request.path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create project folder: {str(e)}"
        )


@router.post("/open-folder")
async def open_folder(request: OpenFolderRequest):
    """
    Open a folder in the system's file explorer
    """
    try:
        folder_path = os.path.normpath(request.path)

        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")

        # Open folder based on OS
        system = platform.system()

        if system == "Windows":
            os.startfile(folder_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        else:  # Linux
            subprocess.run(["xdg-open", folder_path])

        return {
            "success": True,
            "message": f"Opened folder: {folder_path}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to open folder: {str(e)}"
        )


@router.get("/list-projects")
async def list_projects(base_path: Optional[str] = None):
    """
    List all projects in a given directory
    """
    try:
        if not base_path:
            # Default to user's home directory Projects folder
            home = os.path.expanduser("~")
            base_path = os.path.join(home, "Projects")

        if not os.path.exists(base_path):
            return {"projects": []}

        projects = []
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                # Check if it has a README to identify it as a Pawa project
                readme_path = os.path.join(item_path, "README.md")
                is_pawa_project = os.path.exists(readme_path)

                # Get folder info
                stat_info = os.stat(item_path)

                projects.append({
                    "name": item,
                    "path": item_path,
                    "is_pawa_project": is_pawa_project,
                    "created": stat_info.st_ctime,
                    "modified": stat_info.st_mtime,
                    "size": stat_info.st_size
                })

        return {"projects": projects}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list projects: {str(e)}"
        )


@router.get("/folder-info")
async def get_folder_info(path: str):
    """
    Get detailed information about a project folder
    """
    try:
        folder_path = os.path.normpath(path)

        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")

        # Count files and folders
        file_count = 0
        folder_count = 0
        total_size = 0

        for root, dirs, files in os.walk(folder_path):
            folder_count += len(dirs)
            file_count += len(files)
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                except:
                    pass

        # Get folder structure
        structure = []
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            structure.append({
                "name": item,
                "is_dir": os.path.isdir(item_path),
                "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0
            })

        stat_info = os.stat(folder_path)

        return {
            "path": folder_path,
            "file_count": file_count,
            "folder_count": folder_count,
            "total_size": total_size,
            "created": stat_info.st_ctime,
            "modified": stat_info.st_mtime,
            "structure": structure
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get folder info: {str(e)}"
        )


@router.delete("/delete-project")
async def delete_project(path: str, confirm: bool = False):
    """
    Delete a project folder (with confirmation)
    """
    try:
        if not confirm:
            raise HTTPException(
                status_code=400,
                detail="Deletion requires confirmation. Set confirm=true"
            )

        folder_path = os.path.normpath(path)

        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")

        # Safety check - don't delete system folders
        protected_paths = [
            os.path.expanduser("~"),
            "C:\\",
            "C:\\Windows",
            "C:\\Program Files",
            "/",
            "/bin",
            "/usr",
            "/etc"
        ]

        for protected in protected_paths:
            if folder_path.startswith(os.path.normpath(protected)):
                raise HTTPException(
                    status_code=403,
                    detail="Cannot delete system or protected folders"
                )

        import shutil
        shutil.rmtree(folder_path)

        return {
            "success": True,
            "message": f"Project folder deleted: {folder_path}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete project: {str(e)}"
        )
