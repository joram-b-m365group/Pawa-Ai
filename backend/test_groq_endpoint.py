"""Simple test server with just Groq - NOW WITH IMAGE & FILE SUPPORT!"""

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from typing import Optional
import base64
import uvicorn
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client
groq_client = Groq(api_key="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")

class ChatRequest(BaseModel):
    message: str
    image_data: Optional[str] = None  # Base64 encoded image

class ChatResponse(BaseModel):
    response: str
    model: str
    analyzed_file: Optional[str] = None

@app.get("/")
def root():
    return {"status": "running", "model": "Groq Llama 3.3 70B"}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # Check if image is included
        if request.image_data:
            # Use vision model for image analysis!
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyze this image and answer: {request.message}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": request.image_data  # Base64 data URL
                            }
                        }
                    ]
                }
            ]

            completion = groq_client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",  # Vision model!
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
            )

            return ChatResponse(
                response=completion.choices[0].message.content,
                model="Llama 3.2 90B Vision (FREE!)",
                analyzed_file="image"
            )

        else:
            # Regular text chat
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Genius AI, a helpful and intelligent assistant."
                    },
                    {
                        "role": "user",
                        "content": request.message
                    }
                ],
                temperature=0.7,
                max_tokens=2048,
            )

            return ChatResponse(
                response=completion.choices[0].message.content,
                model="Llama 3.3 70B (FREE via Groq!)"
            )

    except Exception as e:
        return ChatResponse(
            response=f"Error: {str(e)}",
            model="error"
        )


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), message: str = Form("Analyze this file")):
    """Upload and analyze image/document files"""
    try:
        # Read file
        contents = await file.read()

        # Check if it's an image
        if file.content_type and file.content_type.startswith('image/'):
            # Convert to base64
            base64_image = base64.b64encode(contents).decode('utf-8')
            data_url = f"data:{file.content_type};base64,{base64_image}"

            # Analyze with vision model
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": message
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_url
                            }
                        }
                    ]
                }
            ]

            completion = groq_client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
            )

            return ChatResponse(
                response=completion.choices[0].message.content,
                model="Llama 3.2 90B Vision",
                analyzed_file=file.filename
            )

        # Handle text files (PDF, TXT, etc.)
        elif file.content_type in ['text/plain', 'application/pdf']:
            # For now, just extract text and analyze
            text_content = contents.decode('utf-8', errors='ignore')[:10000]  # First 10k chars

            full_message = f"{message}\n\nFile content:\n{text_content}"

            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Genius AI analyzing a document."
                    },
                    {
                        "role": "user",
                        "content": full_message
                    }
                ],
                temperature=0.7,
                max_tokens=2048,
            )

            return ChatResponse(
                response=completion.choices[0].message.content,
                model="Llama 3.3 70B",
                analyzed_file=file.filename
            )

        else:
            return ChatResponse(
                response=f"Unsupported file type: {file.content_type}. Please upload images (PNG, JPG) or text files.",
                model="error",
                analyzed_file=file.filename
            )

    except Exception as e:
        return ChatResponse(
            response=f"Error analyzing file: {str(e)}",
            model="error"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
