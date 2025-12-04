"""
Authentication Routes for Genius AI
Handles signup, login, logout, and session management
"""
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from auth_db import AuthDB

router = APIRouter(prefix="/auth", tags=["authentication"])

# Initialize auth database
auth_db = AuthDB()

# Request/Response Models
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    session_token: Optional[str] = None
    user: Optional[dict] = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str

# Dependency to get current user from session token
async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Get current user from session token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    session_token = authorization.replace("Bearer ", "")
    user = auth_db.validate_session(session_token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    return user

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """Create new user account"""
    # Validate input
    if len(request.username) < 3:
        return AuthResponse(
            success=False,
            message="Username must be at least 3 characters"
        )

    if len(request.password) < 6:
        return AuthResponse(
            success=False,
            message="Password must be at least 6 characters"
        )

    # Create user
    user_id = auth_db.create_user(
        request.username,
        request.email,
        request.password
    )

    if not user_id:
        return AuthResponse(
            success=False,
            message="Username or email already exists"
        )

    # Create session
    session_token = auth_db.create_session(user_id)

    return AuthResponse(
        success=True,
        message="Account created successfully",
        session_token=session_token,
        user={
            "id": user_id,
            "username": request.username,
            "email": request.email
        }
    )

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login user"""
    user = auth_db.authenticate_user(request.username, request.password)

    if not user:
        return AuthResponse(
            success=False,
            message="Invalid username or password"
        )

    # Create session
    session_token = auth_db.create_session(user['id'])

    return AuthResponse(
        success=True,
        message="Logged in successfully",
        session_token=session_token,
        user=user
    )

@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """Logout user"""
    if authorization and authorization.startswith("Bearer "):
        session_token = authorization.replace("Bearer ", "")
        auth_db.delete_session(session_token)

    return {"success": True, "message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        user_id=user['user_id'],
        username=user['username'],
        email=user['email']
    )

@router.get("/conversations")
async def get_conversations(user: dict = Depends(get_current_user)):
    """Get all conversations for current user"""
    conversations = auth_db.get_user_conversations(user['user_id'])
    return {"success": True, "conversations": conversations}

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    user: dict = Depends(get_current_user)
):
    """Delete a conversation"""
    auth_db.delete_conversation(conversation_id, user['user_id'])
    return {"success": True, "message": "Conversation deleted"}
