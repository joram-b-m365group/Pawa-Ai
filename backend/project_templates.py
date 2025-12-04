"""
Smart Project Templates with AI Generation
Allows users to generate entire project structures using AI
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import os
from groq import Groq

router = APIRouter(prefix="/templates", tags=["Templates"])

# Initialize Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class TemplateRequest(BaseModel):
    name: str
    description: str
    project_type: str  # react, vue, nodejs, python, etc.
    features: List[str]  # Additional features to include
    output_path: str
    custom_requirements: Optional[str] = None


class FileStructure(BaseModel):
    path: str
    content: str
    is_directory: bool = False


class TemplateResponse(BaseModel):
    success: bool
    message: str
    files_created: List[str]
    project_path: str


# Predefined templates
PREDEFINED_TEMPLATES = {
    "react-tailwind-app": {
        "name": "React + Tailwind CSS App",
        "description": "Modern React app with Tailwind CSS, React Router, and best practices",
        "tech_stack": ["React", "TypeScript", "Tailwind CSS", "Vite", "React Router"],
        "files": [
            {"path": "package.json", "template": "react_package_json"},
            {"path": "tsconfig.json", "template": "react_tsconfig"},
            {"path": "vite.config.ts", "template": "vite_config"},
            {"path": "tailwind.config.js", "template": "tailwind_config"},
            {"path": "postcss.config.js", "template": "postcss_config"},
            {"path": "index.html", "template": "react_index_html"},
            {"path": "src/main.tsx", "template": "react_main"},
            {"path": "src/App.tsx", "template": "react_app"},
            {"path": "src/index.css", "template": "tailwind_css"},
            {"path": ".gitignore", "template": "react_gitignore"},
            {"path": "README.md", "template": "react_readme"},
        ]
    },
    "nodejs-express-api": {
        "name": "Node.js Express API",
        "description": "RESTful API with Express, TypeScript, and MongoDB",
        "tech_stack": ["Node.js", "Express", "TypeScript", "MongoDB", "JWT"],
        "files": [
            {"path": "package.json", "template": "express_package_json"},
            {"path": "tsconfig.json", "template": "express_tsconfig"},
            {"path": "src/server.ts", "template": "express_server"},
            {"path": "src/routes/index.ts", "template": "express_routes"},
            {"path": "src/controllers/index.ts", "template": "express_controllers"},
            {"path": "src/models/User.ts", "template": "express_user_model"},
            {"path": "src/middleware/auth.ts", "template": "express_auth_middleware"},
            {"path": ".env.example", "template": "express_env_example"},
            {"path": ".gitignore", "template": "node_gitignore"},
            {"path": "README.md", "template": "express_readme"},
        ]
    },
    "python-fastapi": {
        "name": "Python FastAPI",
        "description": "Modern Python API with FastAPI, async support, and PostgreSQL",
        "tech_stack": ["Python", "FastAPI", "PostgreSQL", "SQLAlchemy", "Pydantic"],
        "files": [
            {"path": "requirements.txt", "template": "fastapi_requirements"},
            {"path": "main.py", "template": "fastapi_main"},
            {"path": "models.py", "template": "fastapi_models"},
            {"path": "database.py", "template": "fastapi_database"},
            {"path": "routers/users.py", "template": "fastapi_users_router"},
            {"path": ".env.example", "template": "fastapi_env_example"},
            {"path": ".gitignore", "template": "python_gitignore"},
            {"path": "README.md", "template": "fastapi_readme"},
        ]
    },
    "nextjs-app": {
        "name": "Next.js Full-Stack App",
        "description": "Next.js 14+ with App Router, TypeScript, and Tailwind",
        "tech_stack": ["Next.js", "TypeScript", "Tailwind CSS", "App Router"],
        "files": [
            {"path": "package.json", "template": "nextjs_package_json"},
            {"path": "tsconfig.json", "template": "nextjs_tsconfig"},
            {"path": "next.config.js", "template": "nextjs_config"},
            {"path": "tailwind.config.ts", "template": "nextjs_tailwind_config"},
            {"path": "app/layout.tsx", "template": "nextjs_layout"},
            {"path": "app/page.tsx", "template": "nextjs_page"},
            {"path": "app/globals.css", "template": "nextjs_globals_css"},
            {"path": ".gitignore", "template": "nextjs_gitignore"},
            {"path": "README.md", "template": "nextjs_readme"},
        ]
    }
}


def generate_ai_project_structure(request: TemplateRequest) -> List[FileStructure]:
    """
    Use AI to generate a complete project structure based on requirements
    """
    prompt = f"""You are an expert software architect. Generate a complete project structure for the following requirements:

Project Name: {request.name}
Description: {request.description}
Project Type: {request.project_type}
Features: {', '.join(request.features)}
{f'Custom Requirements: {request.custom_requirements}' if request.custom_requirements else ''}

Generate a JSON response with the following structure:
{{
    "files": [
        {{
            "path": "relative/path/to/file.ext",
            "content": "complete file content here",
            "is_directory": false
        }},
        ...
    ],
    "folders": ["folder1", "folder2", ...]
}}

Include:
1. All necessary configuration files (package.json, tsconfig.json, etc.)
2. Core application files with actual working code (not placeholders)
3. README.md with setup instructions
4. .gitignore file
5. Environment variable examples
6. Basic folder structure

Make the code production-ready, follow best practices, and include proper error handling.
Return ONLY valid JSON, no markdown formatting or explanations."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a software architecture expert. Generate complete, production-ready project structures with actual working code."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=8000
        )

        # Parse AI response
        ai_response = response.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if ai_response.startswith("```json"):
            ai_response = ai_response[7:]
        if ai_response.startswith("```"):
            ai_response = ai_response[3:]
        if ai_response.endswith("```"):
            ai_response = ai_response[:-3]

        ai_response = ai_response.strip()
        structure_data = json.loads(ai_response)

        files = []

        # Add folders
        for folder in structure_data.get("folders", []):
            files.append(FileStructure(
                path=folder,
                content="",
                is_directory=True
            ))

        # Add files
        for file_data in structure_data.get("files", []):
            files.append(FileStructure(
                path=file_data["path"],
                content=file_data["content"],
                is_directory=file_data.get("is_directory", False)
            ))

        return files

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse AI response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI generation failed: {str(e)}"
        )


def create_project_files(files: List[FileStructure], base_path: str) -> List[str]:
    """
    Create all files and folders in the project structure
    """
    created_files = []
    base_path = Path(base_path)

    # Create base directory if it doesn't exist
    base_path.mkdir(parents=True, exist_ok=True)

    for file_structure in files:
        file_path = base_path / file_structure.path

        try:
            if file_structure.is_directory:
                # Create directory
                file_path.mkdir(parents=True, exist_ok=True)
                created_files.append(str(file_path))
            else:
                # Create parent directories if they don't exist
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Write file content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_structure.content)

                created_files.append(str(file_path))

        except Exception as e:
            print(f"Error creating {file_path}: {str(e)}")
            continue

    return created_files


@router.post("/generate", response_model=TemplateResponse)
async def generate_project_template(request: TemplateRequest):
    """
    Generate a new project from AI-generated template
    """
    try:
        # Generate project structure using AI
        file_structures = generate_ai_project_structure(request)

        # Create all files and folders
        created_files = create_project_files(file_structures, request.output_path)

        return TemplateResponse(
            success=True,
            message=f"Project '{request.name}' created successfully with {len(created_files)} files",
            files_created=created_files,
            project_path=request.output_path
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate project: {str(e)}"
        )


@router.get("/predefined")
async def get_predefined_templates():
    """
    Get list of predefined project templates
    """
    return {
        "templates": [
            {
                "id": key,
                "name": template["name"],
                "description": template["description"],
                "tech_stack": template["tech_stack"]
            }
            for key, template in PREDEFINED_TEMPLATES.items()
        ]
    }


@router.post("/predefined/{template_id}")
async def create_from_predefined(template_id: str, project_name: str, output_path: str):
    """
    Create a project from a predefined template
    """
    if template_id not in PREDEFINED_TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")

    template = PREDEFINED_TEMPLATES[template_id]

    try:
        # Convert predefined template to TemplateRequest
        request = TemplateRequest(
            name=project_name,
            description=template["description"],
            project_type=template_id.split("-")[0],
            features=template["tech_stack"],
            output_path=output_path
        )

        # Generate using AI
        return await generate_project_template(request)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create project from template: {str(e)}"
        )


@router.post("/customize")
async def customize_template(template_id: str, request: TemplateRequest):
    """
    Customize a predefined template with additional requirements
    """
    if template_id not in PREDEFINED_TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")

    template = PREDEFINED_TEMPLATES[template_id]

    # Merge template features with custom requirements
    enhanced_request = TemplateRequest(
        name=request.name,
        description=f"{template['description']}. {request.description}",
        project_type=request.project_type or template_id.split("-")[0],
        features=list(set(template["tech_stack"] + request.features)),
        output_path=request.output_path,
        custom_requirements=request.custom_requirements
    )

    return await generate_project_template(enhanced_request)
