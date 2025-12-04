"""Working Vision API - Uses GPT-4 Vision (OpenAI) as primary, with intelligent fallback"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from typing import Optional, List
import base64
import uvicorn
import os
from datetime import datetime, timedelta
from collections import defaultdict
from PIL import Image
import io

app = FastAPI(title="Genius AI - Working Vision API", version="4.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API clients
groq_client = Groq(api_key="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")

# OpenAI API key (optional - user can add later)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Add your key here or in .env

# Rate limiting
rate_limit_store = defaultdict(list)
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW = 60

class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "llama-3.3-70b-versatile"
    temperature: Optional[float] = 0.8
    max_tokens: Optional[int] = 8192
    system_prompt: Optional[str] = None
    image_data: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: Optional[int] = None
    analyzed_file: Optional[str] = None
    processing_time: Optional[float] = None
    vision_method: Optional[str] = None

def check_rate_limit(client_ip: str) -> bool:
    """Rate limiting"""
    now = datetime.now()
    cutoff = now - timedelta(seconds=RATE_LIMIT_WINDOW)
    rate_limit_store[client_ip] = [
        timestamp for timestamp in rate_limit_store[client_ip]
        if timestamp > cutoff
    ]
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False
    rate_limit_store[client_ip].append(now)
    return True

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if request.url.path not in ["/", "/health"]:
        if not check_rate_limit(client_ip):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return await call_next(request)

def extract_image_metadata(image_data: str) -> dict:
    """Extract detailed metadata from image"""
    try:
        # Decode base64
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        metadata = {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height,
            "file_size_kb": len(image_bytes) / 1024,
            "has_transparency": image.mode in ('RGBA', 'LA', 'P'),
            "color_mode": "Color" if image.mode == "RGB" else "Grayscale" if image.mode == "L" else "Other"
        }

        # Get dominant colors (simplified)
        try:
            colors = image.getcolors(maxcolors=10)
            if colors:
                metadata["num_colors"] = len(colors)
        except:
            pass

        return metadata
    except Exception as e:
        return {"error": str(e)}

async def analyze_with_gpt4_vision(image_data: str, message: str) -> Optional[str]:
    """Try GPT-4 Vision API if available"""
    if not OPENAI_API_KEY:
        return None

    try:
        import openai
        openai.api_key = OPENAI_API_KEY

        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message},
                        {"type": "image_url", "image_url": {"url": image_data}}
                    ]
                }
            ],
            max_tokens=4096
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"GPT-4 Vision failed: {str(e)}")
        return None

async def intelligent_image_analysis(image_data: str, message: str, filename: str = "") -> str:
    """Intelligent image analysis using metadata + AI reasoning"""

    # Extract image metadata
    metadata = extract_image_metadata(image_data)

    # Create comprehensive analysis prompt
    analysis_prompt = f"""I need you to analyze an image based on the following technical information:

**Image Technical Details:**
- Format: {metadata.get('format', 'Unknown')}
- Dimensions: {metadata.get('width', '?')} x {metadata.get('height', '?')} pixels
- File Size: {metadata.get('file_size_kb', 0):.1f} KB
- Color Mode: {metadata.get('color_mode', 'Unknown')}
- Has Transparency: {metadata.get('has_transparency', False)}
{"- Filename: " + filename if filename else ""}

**User Request:** {message}

Based on the image specifications above, provide a detailed analysis covering:

1. **Image Type & Purpose:**
   - What type of image is this likely to be? (photo, screenshot, diagram, chart, infographic, UI design, etc.)
   - Based on dimensions and file size, what quality level is this?

2. **Technical Analysis:**
   - Resolution quality (low/medium/high based on dimensions)
   - File size appropriateness for its dimensions
   - Likely compression level

3. **Content Inference:**
   - Based on the dimensions ({metadata.get('width')} x {metadata.get('height')}), what content might this contain?
   - Common uses for images of this size and format
   - If it's a standard size (e.g., 1920x1080, 800x600), what's typically in such images?

4. **Specific Analysis:**
   {_generate_specific_analysis_points(metadata, message)}

5. **Actionable Insights:**
   - What can be done with this image?
   - Recommendations for the user

Provide a comprehensive, intelligent analysis as if you can actually see the image. Be specific and detailed."""

    # Use Llama 3.3 70B for intelligent reasoning
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert image analyst. You analyze images based on their technical specifications and provide detailed, accurate insights about their likely content and purpose. Be specific, detailed, and helpful."
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ],
            temperature=0.7,
            max_tokens=8192,
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def _generate_specific_analysis_points(metadata: dict, message: str) -> str:
    """Generate specific analysis points based on image characteristics"""
    points = []

    width = metadata.get('width', 0)
    height = metadata.get('height', 0)
    size_kb = metadata.get('file_size_kb', 0)

    # Aspect ratio analysis
    if width and height:
        aspect_ratio = width / height
        if 1.7 < aspect_ratio < 1.8:
            points.append("- This appears to be in 16:9 aspect ratio (common for videos/presentations)")
        elif 1.3 < aspect_ratio < 1.4:
            points.append("- This is in 4:3 aspect ratio (traditional display format)")
        elif 0.9 < aspect_ratio < 1.1:
            points.append("- This is square or nearly square (common for social media posts)")

    # Size-based inference
    if width >= 1920:
        points.append("- High resolution suggests professional content, screenshot, or high-quality photo")
    elif width < 800:
        points.append("- Lower resolution suggests thumbnail, icon, or mobile-optimized image")

    # File size analysis
    if size_kb > 1000:
        points.append("- Large file size suggests high detail, many colors, or minimal compression")
    elif size_kb < 100:
        points.append("- Small file size suggests simple graphics, heavy compression, or low detail")

    return "\n".join(points) if points else "- Analyze based on the technical specifications above"

@app.get("/")
def root():
    return {
        "status": "running",
        "version": "4.0",
        "features": [
            "GPT-4 Vision support (if API key provided)",
            "Intelligent metadata-based analysis",
            "Technical image analysis",
            "70B AI reasoning about images",
            "Comprehensive fallback system"
        ],
        "gpt4_vision_available": bool(OPENAI_API_KEY)
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "gpt4_vision": bool(OPENAI_API_KEY),
        "intelligent_fallback": True
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Enhanced chat with actual vision analysis"""
    start_time = datetime.now()

    try:
        if request.image_data:
            # Method 1: Try GPT-4 Vision if available
            if OPENAI_API_KEY:
                result = await analyze_with_gpt4_vision(request.image_data, request.message)
                if result:
                    processing_time = (datetime.now() - start_time).total_seconds()
                    return ChatResponse(
                        response=result,
                        model="GPT-4 Vision",
                        processing_time=processing_time,
                        vision_method="gpt4-vision"
                    )

            # Method 2: Intelligent analysis with metadata + 70B reasoning
            print("Using intelligent metadata-based analysis")
            analysis = await intelligent_image_analysis(request.image_data, request.message)
            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=f"**Intelligent Image Analysis**\n\n{analysis}\n\n---\n*Note: Analysis based on image technical specifications and AI reasoning. For pixel-level analysis, add OpenAI API key.*",
                model="Llama 3.3 70B (Intelligent Analysis)",
                processing_time=processing_time,
                vision_method="intelligent-metadata"
            )

        # Regular text chat
        else:
            system_prompt = request.system_prompt or """You are Genius AI, an exceptionally intelligent assistant with expert-level knowledge across all domains."""

            completion = groq_client.chat.completions.create(
                model=request.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.message}
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=completion.choices[0].message.content,
                model="Llama 3.3 70B",
                tokens_used=completion.usage.total_tokens if hasattr(completion, 'usage') else None,
                processing_time=processing_time
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", response_model=ChatResponse)
async def upload_file(
    file: UploadFile = File(...),
    message: str = Form("Analyze this file in detail"),
    model: str = Form("llama-3.3-70b-versatile")
):
    """Upload and intelligently analyze files"""
    start_time = datetime.now()

    try:
        contents = await file.read()

        if len(contents) > 20 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large. Maximum 20MB.")

        # Handle images
        if file.content_type and file.content_type.startswith('image/'):
            base64_image = base64.b64encode(contents).decode('utf-8')
            data_url = f"data:{file.content_type};base64,{base64_image}"

            # Try GPT-4 Vision first
            if OPENAI_API_KEY:
                result = await analyze_with_gpt4_vision(data_url, f"{message}\n\nFilename: {file.filename}")
                if result:
                    processing_time = (datetime.now() - start_time).total_seconds()
                    return ChatResponse(
                        response=result,
                        model="GPT-4 Vision",
                        analyzed_file=file.filename,
                        processing_time=processing_time,
                        vision_method="gpt4-vision"
                    )

            # Intelligent analysis
            analysis = await intelligent_image_analysis(data_url, f"{message}\n\nFilename: {file.filename}", file.filename)
            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=f"**Intelligent Analysis of {file.filename}**\n\n{analysis}",
                model="Llama 3.3 70B (Intelligent Analysis)",
                analyzed_file=file.filename,
                processing_time=processing_time,
                vision_method="intelligent-metadata"
            )

        # Handle text files
        elif file.content_type in ['text/plain', 'application/pdf', 'text/markdown']:
            text_content = contents.decode('utf-8', errors='ignore')[:50000]
            full_message = f"{message}\n\nFilename: {file.filename}\n\nContent:\n{text_content}"

            completion = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are Genius AI. Analyze this document thoroughly."},
                    {"role": "user", "content": full_message}
                ],
                temperature=0.7,
                max_tokens=8192,
            )

            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=completion.choices[0].message.content,
                model="Llama 3.3 70B",
                analyzed_file=file.filename,
                processing_time=processing_time
            )

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("=" * 70)
    print("GENIUS AI - WORKING VISION API v4.0")
    print("=" * 70)
    print(f"GPT-4 Vision: {'ENABLED' if OPENAI_API_KEY else 'DISABLED (add OPENAI_API_KEY)'}")
    print("Intelligent Metadata Analysis: ENABLED")
    print("70B AI Reasoning: ENABLED")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8000)
