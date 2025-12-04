"""
AI Code Review System
Provides automated code quality checks, security analysis, and improvement suggestions
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path
import os
from groq import Groq
import json

router = APIRouter(prefix="/code-review", tags=["Code Review"])

# Initialize Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class CodeReviewRequest(BaseModel):
    code: str
    file_path: Optional[str] = None
    language: Optional[str] = None
    review_type: str = "comprehensive"  # comprehensive, security, performance, style


class Issue(BaseModel):
    severity: str  # critical, high, medium, low, info
    category: str  # security, performance, style, bug, best-practice
    line_number: Optional[int] = None
    title: str
    description: str
    suggestion: str
    code_snippet: Optional[str] = None


class CodeReviewResponse(BaseModel):
    overall_score: int  # 0-100
    summary: str
    issues: List[Issue]
    strengths: List[str]
    metrics: Dict[str, Any]


class FileReviewRequest(BaseModel):
    file_path: str
    project_root: Optional[str] = None
    review_type: str = "comprehensive"


class ProjectReviewRequest(BaseModel):
    project_path: str
    include_patterns: List[str] = ["*.py", "*.js", "*.ts", "*.tsx", "*.jsx"]
    exclude_patterns: List[str] = ["node_modules/**", "venv/**", "dist/**", "build/**"]


def detect_language(file_path: str, code: str = None) -> str:
    """Auto-detect programming language from file extension or code"""
    if file_path:
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.jsx': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.cs': 'csharp',
            '.swift': 'swift',
        }
        ext = Path(file_path).suffix
        return ext_to_lang.get(ext, 'unknown')

    return 'unknown'


def analyze_code_with_ai(code: str, language: str, review_type: str) -> CodeReviewResponse:
    """
    Use AI to perform comprehensive code review
    """

    # Build review prompt based on type
    review_focuses = {
        "comprehensive": "all aspects including security, performance, style, bugs, and best practices",
        "security": "security vulnerabilities, injection attacks, authentication issues, data exposure",
        "performance": "performance bottlenecks, inefficient algorithms, memory leaks, optimization opportunities",
        "style": "code style, formatting, naming conventions, documentation, readability"
    }

    focus = review_focuses.get(review_type, review_focuses["comprehensive"])

    prompt = f"""You are an expert code reviewer. Analyze the following {language} code focusing on {focus}.

Code to review:
```{language}
{code}
```

Provide a detailed code review in JSON format with the following structure:
{{
    "overall_score": <integer 0-100>,
    "summary": "<brief summary of code quality>",
    "issues": [
        {{
            "severity": "<critical|high|medium|low|info>",
            "category": "<security|performance|style|bug|best-practice>",
            "line_number": <line number if applicable, or null>,
            "title": "<brief issue title>",
            "description": "<detailed description>",
            "suggestion": "<how to fix it>",
            "code_snippet": "<problematic code snippet if applicable>"
        }}
    ],
    "strengths": [
        "<positive aspects of the code>"
    ],
    "metrics": {{
        "complexity": "<low|medium|high>",
        "maintainability": <integer 0-100>,
        "security_score": <integer 0-100>,
        "test_coverage_needed": <boolean>
    }}
}}

Be thorough and specific. Focus on actionable feedback.
Return ONLY valid JSON, no markdown formatting."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert code reviewer specializing in {language}. Provide detailed, actionable feedback."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent analysis
            max_tokens=4000
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
        review_data = json.loads(ai_response)

        # Convert to Pydantic models
        issues = [Issue(**issue) for issue in review_data.get("issues", [])]

        return CodeReviewResponse(
            overall_score=review_data.get("overall_score", 0),
            summary=review_data.get("summary", ""),
            issues=issues,
            strengths=review_data.get("strengths", []),
            metrics=review_data.get("metrics", {})
        )

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse AI response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Code review failed: {str(e)}"
        )


@router.post("/analyze", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """
    Analyze code snippet and provide detailed review
    """
    try:
        # Auto-detect language if not provided
        language = request.language or detect_language(
            request.file_path or "",
            request.code
        )

        # Perform AI code review
        review = analyze_code_with_ai(
            request.code,
            language,
            request.review_type
        )

        return review

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze code: {str(e)}"
        )


@router.post("/file", response_model=CodeReviewResponse)
async def review_file(request: FileReviewRequest):
    """
    Review a specific file
    """
    try:
        # Determine file path
        if request.project_root:
            file_path = Path(request.project_root) / request.file_path
        else:
            file_path = Path(request.file_path)

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # Detect language
        language = detect_language(str(file_path), code)

        # Perform review
        review = analyze_code_with_ai(code, language, request.review_type)

        return review

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to review file: {str(e)}"
        )


@router.post("/project")
async def review_project(request: ProjectReviewRequest):
    """
    Review entire project (analyze multiple files)
    """
    try:
        project_path = Path(request.project_path)
        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project path not found")

        # Find all matching files
        files_to_review = []
        for pattern in request.include_patterns:
            files_to_review.extend(project_path.rglob(pattern))

        # Filter out excluded patterns
        excluded = set()
        for pattern in request.exclude_patterns:
            excluded.update(project_path.rglob(pattern))

        files_to_review = [f for f in files_to_review if f not in excluded]

        # Limit to reasonable number for performance
        if len(files_to_review) > 50:
            files_to_review = files_to_review[:50]

        # Review each file
        file_reviews = []
        total_issues = 0
        critical_issues = 0
        high_issues = 0

        for file_path in files_to_review:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                language = detect_language(str(file_path))
                review = analyze_code_with_ai(code, language, "comprehensive")

                # Count issues by severity
                for issue in review.issues:
                    total_issues += 1
                    if issue.severity == "critical":
                        critical_issues += 1
                    elif issue.severity == "high":
                        high_issues += 1

                file_reviews.append({
                    "file": str(file_path.relative_to(project_path)),
                    "score": review.overall_score,
                    "issues_count": len(review.issues),
                    "critical_issues": sum(1 for i in review.issues if i.severity == "critical"),
                    "high_issues": sum(1 for i in review.issues if i.severity == "high")
                })

            except Exception as e:
                print(f"Error reviewing {file_path}: {str(e)}")
                continue

        # Calculate project-level metrics
        avg_score = sum(r["score"] for r in file_reviews) / len(file_reviews) if file_reviews else 0

        return {
            "success": True,
            "project_path": str(project_path),
            "files_reviewed": len(file_reviews),
            "overall_score": int(avg_score),
            "total_issues": total_issues,
            "critical_issues": critical_issues,
            "high_issues": high_issues,
            "file_reviews": file_reviews,
            "summary": f"Reviewed {len(file_reviews)} files. Average score: {int(avg_score)}. Found {critical_issues} critical and {high_issues} high severity issues."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to review project: {str(e)}"
        )


@router.post("/suggest-improvements")
async def suggest_improvements(code: str, language: str = "python"):
    """
    Get AI-generated code improvements
    """
    try:
        prompt = f"""Analyze this {language} code and provide 3-5 specific improvements with refactored code examples.

Code:
```{language}
{code}
```

Return JSON with:
{{
    "improvements": [
        {{
            "title": "<improvement title>",
            "description": "<why this helps>",
            "before": "<original code snippet>",
            "after": "<improved code snippet>"
        }}
    ]
}}

Focus on practical, implementable improvements."""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are a {language} expert. Provide clear, practical code improvements."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=3000
        )

        ai_response = response.choices[0].message.content.strip()

        # Clean response
        if ai_response.startswith("```json"):
            ai_response = ai_response[7:]
        if ai_response.startswith("```"):
            ai_response = ai_response[3:]
        if ai_response.endswith("```"):
            ai_response = ai_response[:-3]

        return json.loads(ai_response.strip())

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to suggest improvements: {str(e)}"
        )


@router.get("/quality-metrics")
async def get_quality_metrics(file_path: str):
    """
    Get code quality metrics for a file
    """
    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise HTTPException(status_code=404, detail="File not found")

        with open(file_path_obj, 'r', encoding='utf-8') as f:
            code = f.read()

        # Basic metrics
        lines = code.split('\n')
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])

        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "blank_lines": total_lines - code_lines - comment_lines,
            "comment_ratio": round(comment_lines / code_lines * 100, 2) if code_lines > 0 else 0
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate metrics: {str(e)}"
        )
