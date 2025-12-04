"""
Long-Term Memory System
Persistently stores and retrieves knowledge across sessions
"""

import json
import sqlite3
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path


class LongTermMemory:
    """
    Persistent memory system that remembers:
    - User preferences
    - Past conversations
    - Learned facts
    - Important context
    """

    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path

        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT,
                assistant_response TEXT,
                metadata TEXT
            )
        """)

        # Facts table - stores learned information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT NOT NULL,
                category TEXT,
                confidence REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source TEXT
            )
        """)

        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                preference_key TEXT NOT NULL,
                preference_value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, preference_key)
            )
        """)

        # Knowledge base table - semantic memory
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def store_conversation(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Store a conversation turn

        Args:
            conversation_id: Unique conversation identifier
            user_message: What the user said
            assistant_response: What the AI responded
            metadata: Additional context (agent used, confidence, etc.)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations (conversation_id, user_message, assistant_response, metadata)
            VALUES (?, ?, ?, ?)
        """, (
            conversation_id,
            user_message,
            assistant_response,
            json.dumps(metadata) if metadata else None
        ))

        conn.commit()
        conn.close()

    def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history

        Args:
            conversation_id: Conversation to retrieve
            limit: Maximum number of messages

        Returns:
            List of conversation turns
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_message, assistant_response, timestamp, metadata
            FROM conversations
            WHERE conversation_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (conversation_id, limit))

        rows = cursor.fetchall()
        conn.close()

        # Convert to list of dicts (reverse to chronological order)
        history = []
        for row in reversed(rows):
            history.append({
                "user": row[0],
                "assistant": row[1],
                "timestamp": row[2],
                "metadata": json.loads(row[3]) if row[3] else None
            })

        return history

    def store_fact(
        self,
        fact: str,
        category: str = "general",
        confidence: float = 1.0,
        source: str = "learned"
    ):
        """
        Store a learned fact

        Args:
            fact: The factual information
            category: Category (science, history, user_preference, etc.)
            confidence: How confident we are (0.0 - 1.0)
            source: Where this came from
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facts (fact, category, confidence, source)
            VALUES (?, ?, ?, ?)
        """, (fact, category, confidence, source))

        conn.commit()
        conn.close()

    def recall_facts(
        self,
        category: Optional[str] = None,
        min_confidence: float = 0.5,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recall learned facts

        Args:
            category: Filter by category
            min_confidence: Minimum confidence threshold
            limit: Maximum number of facts

        Returns:
            List of facts
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute("""
                SELECT fact, category, confidence, timestamp, source
                FROM facts
                WHERE category = ? AND confidence >= ?
                ORDER BY confidence DESC, timestamp DESC
                LIMIT ?
            """, (category, min_confidence, limit))
        else:
            cursor.execute("""
                SELECT fact, category, confidence, timestamp, source
                FROM facts
                WHERE confidence >= ?
                ORDER BY confidence DESC, timestamp DESC
                LIMIT ?
            """, (min_confidence, limit))

        rows = cursor.fetchall()
        conn.close()

        facts = []
        for row in rows:
            facts.append({
                "fact": row[0],
                "category": row[1],
                "confidence": row[2],
                "timestamp": row[3],
                "source": row[4]
            })

        return facts

    def set_preference(
        self,
        preference_key: str,
        preference_value: str,
        user_id: str = "default"
    ):
        """
        Store user preference

        Args:
            preference_key: Preference name
            preference_value: Preference value
            user_id: User identifier
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO preferences (user_id, preference_key, preference_value)
            VALUES (?, ?, ?)
        """, (user_id, preference_key, preference_value))

        conn.commit()
        conn.close()

    def get_preference(
        self,
        preference_key: str,
        user_id: str = "default"
    ) -> Optional[str]:
        """
        Get user preference

        Args:
            preference_key: Preference to retrieve
            user_id: User identifier

        Returns:
            Preference value or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT preference_value
            FROM preferences
            WHERE user_id = ? AND preference_key = ?
        """, (user_id, preference_key))

        row = cursor.fetchone()
        conn.close()

        return row[0] if row else None

    def store_knowledge(self, topic: str, content: str):
        """
        Store knowledge about a topic

        Args:
            topic: Topic/subject
            content: Knowledge content
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO knowledge (topic, content)
            VALUES (?, ?)
        """, (topic, content))

        conn.commit()
        conn.close()

    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search knowledge base (simple text search for now)

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            Relevant knowledge entries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Simple text search (can be upgraded to vector search later)
        cursor.execute("""
            SELECT topic, content, timestamp
            FROM knowledge
            WHERE topic LIKE ? OR content LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit))

        rows = cursor.fetchall()
        conn.close()

        knowledge = []
        for row in rows:
            knowledge.append({
                "topic": row[0],
                "content": row[1],
                "timestamp": row[2]
            })

        return knowledge

    def get_statistics(self) -> Dict[str, int]:
        """
        Get memory statistics

        Returns:
            Statistics about stored data
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Count conversations
        cursor.execute("SELECT COUNT(*) FROM conversations")
        stats["total_messages"] = cursor.fetchone()[0]

        # Count unique conversations
        cursor.execute("SELECT COUNT(DISTINCT conversation_id) FROM conversations")
        stats["unique_conversations"] = cursor.fetchone()[0]

        # Count facts
        cursor.execute("SELECT COUNT(*) FROM facts")
        stats["learned_facts"] = cursor.fetchone()[0]

        # Count knowledge entries
        cursor.execute("SELECT COUNT(*) FROM knowledge")
        stats["knowledge_entries"] = cursor.fetchone()[0]

        # Count preferences
        cursor.execute("SELECT COUNT(*) FROM preferences")
        stats["user_preferences"] = cursor.fetchone()[0]

        conn.close()

        return stats
