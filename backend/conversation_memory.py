"""
Conversation Memory System
Provides persistent conversation history, cross-session memory, and user preference learning
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from collections import defaultdict

router = APIRouter(prefix="/memory", tags=["Conversation Memory"])


class ConversationMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime
    tool_calls: Optional[List[Dict[str, Any]]] = None
    files_modified: Optional[List[str]] = None


class Conversation(BaseModel):
    conversation_id: str
    user_id: str
    project_path: Optional[str] = None
    title: str
    messages: List[ConversationMessage]
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []


class UserPreferences(BaseModel):
    user_id: str
    preferred_model: str = "llama-3.3-70b-versatile"
    code_style: Dict[str, Any] = {}
    favorite_languages: List[str] = []
    common_patterns: List[str] = []
    shortcuts: Dict[str, str] = {}


class CreateConversationRequest(BaseModel):
    user_id: str
    project_path: Optional[str] = None
    title: Optional[str] = "New Conversation"


class AddMessageRequest(BaseModel):
    conversation_id: str
    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    files_modified: Optional[List[str]] = None


class ConversationStore:
    """
    In-memory conversation store (in production, use PostgreSQL/MongoDB)
    """

    def __init__(self, storage_dir: str = "./data/conversations"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.conversations: Dict[str, Conversation] = {}
        self.user_preferences: Dict[str, UserPreferences] = {}
        self.conversation_index: Dict[str, List[str]] = defaultdict(list)  # user_id -> conversation_ids

        self._load_from_disk()

    def _load_from_disk(self):
        """Load conversations from disk on startup"""
        try:
            for file_path in self.storage_dir.glob("*.json"):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    conv = Conversation(**data)
                    self.conversations[conv.conversation_id] = conv
                    self.conversation_index[conv.user_id].append(conv.conversation_id)
        except Exception as e:
            print(f"Error loading conversations: {str(e)}")

    def _save_to_disk(self, conversation: Conversation):
        """Persist conversation to disk"""
        try:
            file_path = self.storage_dir / f"{conversation.conversation_id}.json"
            with open(file_path, 'w') as f:
                json.dump(conversation.dict(), f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving conversation: {str(e)}")

    def create_conversation(self, user_id: str, project_path: Optional[str] = None, title: str = "New Conversation") -> Conversation:
        """Create a new conversation"""
        conversation_id = f"conv_{user_id}_{int(datetime.now().timestamp())}"

        conversation = Conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            project_path=project_path,
            title=title,
            messages=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            tags=[]
        )

        self.conversations[conversation_id] = conversation
        self.conversation_index[user_id].append(conversation_id)
        self._save_to_disk(conversation)

        return conversation

    def add_message(self, conversation_id: str, role: str, content: str,
                    tool_calls: Optional[List[Dict[str, Any]]] = None,
                    files_modified: Optional[List[str]] = None) -> Conversation:
        """Add message to conversation"""
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")

        conversation = self.conversations[conversation_id]

        message = ConversationMessage(
            role=role,
            content=content,
            timestamp=datetime.now(),
            tool_calls=tool_calls,
            files_modified=files_modified
        )

        conversation.messages.append(message)
        conversation.updated_at = datetime.now()

        # Auto-generate title from first user message
        if len(conversation.messages) == 1 and conversation.title == "New Conversation":
            conversation.title = content[:50] + ("..." if len(content) > 50 else "")

        self._save_to_disk(conversation)

        return conversation

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        return self.conversations.get(conversation_id)

    def list_conversations(self, user_id: str, limit: int = 50) -> List[Conversation]:
        """List all conversations for a user"""
        conversation_ids = self.conversation_index.get(user_id, [])

        conversations = [
            self.conversations[cid]
            for cid in conversation_ids
            if cid in self.conversations
        ]

        # Sort by updated_at descending
        conversations.sort(key=lambda c: c.updated_at, reverse=True)

        return conversations[:limit]

    def search_conversations(self, user_id: str, query: str) -> List[Conversation]:
        """Search conversations by content"""
        user_conversations = self.list_conversations(user_id, limit=1000)

        results = []
        query_lower = query.lower()

        for conv in user_conversations:
            # Search in title
            if query_lower in conv.title.lower():
                results.append(conv)
                continue

            # Search in messages
            for msg in conv.messages:
                if query_lower in msg.content.lower():
                    results.append(conv)
                    break

        return results

    def delete_conversation(self, conversation_id: str):
        """Delete a conversation"""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            user_id = conv.user_id

            # Remove from index
            if user_id in self.conversation_index:
                self.conversation_index[user_id] = [
                    cid for cid in self.conversation_index[user_id]
                    if cid != conversation_id
                ]

            # Remove from memory
            del self.conversations[conversation_id]

            # Remove from disk
            file_path = self.storage_dir / f"{conversation_id}.json"
            if file_path.exists():
                file_path.unlink()

    def get_user_preferences(self, user_id: str) -> UserPreferences:
        """Get user preferences"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = UserPreferences(user_id=user_id)

        return self.user_preferences[user_id]

    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user preferences"""
        user_prefs = self.get_user_preferences(user_id)

        for key, value in preferences.items():
            if hasattr(user_prefs, key):
                setattr(user_prefs, key, value)

        return user_prefs


# Global store
conversation_store = ConversationStore()


@router.post("/conversations", response_model=Conversation)
async def create_conversation(request: CreateConversationRequest):
    """Create a new conversation"""
    try:
        conversation = conversation_store.create_conversation(
            user_id=request.user_id,
            project_path=request.project_path,
            title=request.title or "New Conversation"
        )
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")


@router.post("/conversations/message", response_model=Conversation)
async def add_message(request: AddMessageRequest):
    """Add a message to a conversation"""
    try:
        conversation = conversation_store.add_message(
            conversation_id=request.conversation_id,
            role=request.role,
            content=request.content,
            tool_calls=request.tool_calls,
            files_modified=request.files_modified
        )
        return conversation
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add message: {str(e)}")


@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation"""
    conversation = conversation_store.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.get("/conversations/user/{user_id}", response_model=List[Conversation])
async def list_user_conversations(user_id: str, limit: int = 50):
    """List all conversations for a user"""
    conversations = conversation_store.list_conversations(user_id, limit=limit)
    return conversations


@router.get("/conversations/search/{user_id}")
async def search_conversations(user_id: str, query: str):
    """Search conversations by content"""
    results = conversation_store.search_conversations(user_id, query)
    return {"query": query, "results": results, "count": len(results)}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    try:
        conversation_store.delete_conversation(conversation_id)
        return {"success": True, "message": "Conversation deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")


@router.get("/preferences/{user_id}", response_model=UserPreferences)
async def get_user_preferences(user_id: str):
    """Get user preferences"""
    return conversation_store.get_user_preferences(user_id)


@router.put("/preferences/{user_id}", response_model=UserPreferences)
async def update_user_preferences(user_id: str, preferences: Dict[str, Any]):
    """Update user preferences"""
    try:
        updated_prefs = conversation_store.update_user_preferences(user_id, preferences)
        return updated_prefs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update preferences: {str(e)}")


@router.get("/statistics/{user_id}")
async def get_user_statistics(user_id: str):
    """Get user statistics and insights"""
    conversations = conversation_store.list_conversations(user_id, limit=1000)

    total_conversations = len(conversations)
    total_messages = sum(len(conv.messages) for conv in conversations)

    # Count tool usage
    tool_usage = defaultdict(int)
    files_modified = set()

    for conv in conversations:
        for msg in conv.messages:
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_usage[tool_call.get('tool', 'unknown')] += 1
            if msg.files_modified:
                files_modified.update(msg.files_modified)

    # Recent activity
    recent_conversations = conversations[:10]

    return {
        "user_id": user_id,
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "tool_usage": dict(tool_usage),
        "unique_files_modified": len(files_modified),
        "recent_conversations": [
            {
                "id": conv.conversation_id,
                "title": conv.title,
                "updated_at": conv.updated_at,
                "message_count": len(conv.messages)
            }
            for conv in recent_conversations
        ]
    }
