"""
Undo/Redo System
Tracks all file modifications and provides rollback functionality
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import hashlib
from collections import deque

router = APIRouter(prefix="/undo", tags=["Undo/Redo System"])


class FileSnapshot(BaseModel):
    file_path: str
    content: str
    timestamp: datetime
    operation: str  # write, edit, delete
    content_hash: str
    user_id: Optional[str] = None


class UndoRequest(BaseModel):
    session_id: str
    steps: int = 1


class RedoRequest(BaseModel):
    session_id: str
    steps: int = 1


class UndoStackManager:
    """
    Manages undo/redo stacks for file modifications
    """

    def __init__(self, max_history_size: int = 100):
        self.max_history_size = max_history_size
        # session_id -> deque of snapshots
        self.undo_stacks: Dict[str, deque] = {}
        self.redo_stacks: Dict[str, deque] = {}
        self.snapshots_dir = Path("./data/snapshots")
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def _compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of file content"""
        return hashlib.sha256(content.encode()).hexdigest()

    def _save_snapshot_to_disk(self, snapshot: FileSnapshot) -> str:
        """Save snapshot to disk and return file path"""
        snapshot_id = f"{snapshot.content_hash}_{int(snapshot.timestamp.timestamp())}"
        snapshot_path = self.snapshots_dir / f"{snapshot_id}.json"

        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(snapshot.dict(), f, default=str, indent=2)

        return str(snapshot_path)

    def _load_snapshot_from_disk(self, snapshot_path: str) -> FileSnapshot:
        """Load snapshot from disk"""
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return FileSnapshot(**data)

    def push_snapshot(
        self,
        session_id: str,
        file_path: str,
        content: str,
        operation: str,
        user_id: Optional[str] = None
    ):
        """Push a new snapshot onto the undo stack"""
        if session_id not in self.undo_stacks:
            self.undo_stacks[session_id] = deque(maxlen=self.max_history_size)
            self.redo_stacks[session_id] = deque(maxlen=self.max_history_size)

        snapshot = FileSnapshot(
            file_path=file_path,
            content=content,
            timestamp=datetime.now(),
            operation=operation,
            content_hash=self._compute_hash(content),
            user_id=user_id
        )

        # Save to disk
        self._save_snapshot_to_disk(snapshot)

        # Push to undo stack
        self.undo_stacks[session_id].append(snapshot)

        # Clear redo stack when new operation is performed
        self.redo_stacks[session_id].clear()

        return snapshot

    def undo(self, session_id: str, steps: int = 1) -> List[FileSnapshot]:
        """Undo last N operations"""
        if session_id not in self.undo_stacks:
            raise ValueError(f"No undo history for session {session_id}")

        undo_stack = self.undo_stacks[session_id]
        redo_stack = self.redo_stacks[session_id]

        if len(undo_stack) == 0:
            raise ValueError("Nothing to undo")

        undone_snapshots = []

        for _ in range(min(steps, len(undo_stack))):
            snapshot = undo_stack.pop()
            redo_stack.append(snapshot)
            undone_snapshots.append(snapshot)

        return undone_snapshots

    def redo(self, session_id: str, steps: int = 1) -> List[FileSnapshot]:
        """Redo last N undone operations"""
        if session_id not in self.redo_stacks:
            raise ValueError(f"No redo history for session {session_id}")

        redo_stack = self.redo_stacks[session_id]
        undo_stack = self.undo_stacks[session_id]

        if len(redo_stack) == 0:
            raise ValueError("Nothing to redo")

        redone_snapshots = []

        for _ in range(min(steps, len(redo_stack))):
            snapshot = redo_stack.pop()
            undo_stack.append(snapshot)
            redone_snapshots.append(snapshot)

        return redone_snapshots

    def get_history(self, session_id: str, limit: int = 50) -> List[FileSnapshot]:
        """Get undo history for session"""
        if session_id not in self.undo_stacks:
            return []

        stack = list(self.undo_stacks[session_id])
        return stack[-limit:] if len(stack) > limit else stack

    def get_snapshot(self, session_id: str, index: int) -> Optional[FileSnapshot]:
        """Get specific snapshot from history"""
        if session_id not in self.undo_stacks:
            return None

        stack = list(self.undo_stacks[session_id])
        if 0 <= index < len(stack):
            return stack[index]

        return None

    def rollback_to_snapshot(self, session_id: str, index: int) -> FileSnapshot:
        """Rollback to specific snapshot in history"""
        snapshot = self.get_snapshot(session_id, index)

        if not snapshot:
            raise ValueError(f"Snapshot at index {index} not found")

        # Remove all snapshots after the target
        undo_stack = self.undo_stacks[session_id]

        while len(undo_stack) > index + 1:
            removed = undo_stack.pop()
            self.redo_stacks[session_id].append(removed)

        return snapshot

    def clear_history(self, session_id: str):
        """Clear all history for session"""
        if session_id in self.undo_stacks:
            self.undo_stacks[session_id].clear()
        if session_id in self.redo_stacks:
            self.redo_stacks[session_id].clear()


# Global undo manager
undo_manager = UndoStackManager()


@router.post("/snapshot")
async def create_snapshot(
    session_id: str,
    file_path: str,
    content: str,
    operation: str,
    user_id: Optional[str] = None
):
    """
    Create a snapshot before modifying a file
    """
    try:
        snapshot = undo_manager.push_snapshot(
            session_id=session_id,
            file_path=file_path,
            content=content,
            operation=operation,
            user_id=user_id
        )

        return {
            "success": True,
            "snapshot": snapshot,
            "message": "Snapshot created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create snapshot: {str(e)}")


@router.post("/undo")
async def undo_operation(request: UndoRequest):
    """
    Undo last N operations
    """
    try:
        snapshots = undo_manager.undo(
            session_id=request.session_id,
            steps=request.steps
        )

        return {
            "success": True,
            "snapshots": snapshots,
            "message": f"Undone {len(snapshots)} operation(s)"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Undo failed: {str(e)}")


@router.post("/redo")
async def redo_operation(request: RedoRequest):
    """
    Redo last N undone operations
    """
    try:
        snapshots = undo_manager.redo(
            session_id=request.session_id,
            steps=request.steps
        )

        return {
            "success": True,
            "snapshots": snapshots,
            "message": f"Redone {len(snapshots)} operation(s)"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redo failed: {str(e)}")


@router.get("/history/{session_id}")
async def get_history(session_id: str, limit: int = 50):
    """
    Get undo history for session
    """
    try:
        history = undo_manager.get_history(session_id, limit=limit)

        return {
            "success": True,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@router.post("/rollback/{session_id}")
async def rollback_to_snapshot(session_id: str, index: int):
    """
    Rollback to specific snapshot in history
    """
    try:
        snapshot = undo_manager.rollback_to_snapshot(session_id, index)

        # Restore file content
        file_path = Path(snapshot.file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(snapshot.content)

        return {
            "success": True,
            "snapshot": snapshot,
            "message": f"Rolled back to snapshot at {snapshot.timestamp}"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rollback failed: {str(e)}")


@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    """
    Clear all history for session
    """
    try:
        undo_manager.clear_history(session_id)

        return {
            "success": True,
            "message": "History cleared successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")


@router.get("/stats/{session_id}")
async def get_stats(session_id: str):
    """
    Get statistics about undo/redo history
    """
    undo_count = len(undo_manager.undo_stacks.get(session_id, []))
    redo_count = len(undo_manager.redo_stacks.get(session_id, []))

    return {
        "session_id": session_id,
        "undo_available": undo_count,
        "redo_available": redo_count,
        "total_operations": undo_count + redo_count
    }
