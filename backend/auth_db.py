"""
Authentication Database for Genius AI
Handles user management and session storage
"""
import sqlite3
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import os

class AuthDB:
    def __init__(self, db_path: str = "./genius_ai.db"):
        """Initialize authentication database"""
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)

        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        """)

        conn.commit()
        conn.close()

    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${pwd_hash}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, pwd_hash = password_hash.split('$')
            test_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return test_hash == pwd_hash
        except:
            return False

    def create_user(self, username: str, email: str, password: str) -> Optional[int]:
        """Create new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            password_hash = self.hash_password(password)

            cursor.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))

            user_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return user_id
        except sqlite3.IntegrityError:
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user info"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, email, password_hash
            FROM users
            WHERE username = ? OR email = ?
        """, (username, username))

        user = cursor.fetchone()
        conn.close()

        if user and self.verify_password(password, user['password_hash']):
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        return None

    def create_session(self, user_id: int) -> str:
        """Create new session for user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)

        cursor.execute("""
            INSERT INTO sessions (user_id, session_token, expires_at)
            VALUES (?, ?, ?)
        """, (user_id, session_token, expires_at))

        # Update last login
        cursor.execute("""
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

        return session_token

    def validate_session(self, session_token: str) -> Optional[Dict]:
        """Validate session and return user info"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.id, s.user_id, s.expires_at, u.username, u.email
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ?
        """, (session_token,))

        session = cursor.fetchone()
        conn.close()

        if session:
            expires_at = datetime.fromisoformat(session['expires_at'])
            if expires_at > datetime.now():
                return {
                    'user_id': session['user_id'],
                    'username': session['username'],
                    'email': session['email']
                }

        return None

    def delete_session(self, session_token: str):
        """Delete session (logout)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM sessions WHERE session_token = ?", (session_token,))

        conn.commit()
        conn.close()

    def create_conversation(self, conversation_id: str, user_id: int, title: str = "New Chat"):
        """Create new conversation for user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations (id, user_id, title)
            VALUES (?, ?, ?)
        """, (conversation_id, user_id, title))

        conn.commit()
        conn.close()

    def get_user_conversations(self, user_id: int) -> List[Dict]:
        """Get all conversations for user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, created_at, updated_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY updated_at DESC
        """, (user_id,))

        conversations = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return conversations

    def save_message(self, conversation_id: str, role: str, content: str):
        """Save message to conversation"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
        """, (conversation_id, role, content))

        # Update conversation timestamp
        cursor.execute("""
            UPDATE conversations
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (conversation_id,))

        conn.commit()
        conn.close()

    def get_conversation_messages(self, conversation_id: str) -> List[Dict]:
        """Get all messages in a conversation"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY created_at ASC
        """, (conversation_id,))

        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return messages

    def delete_conversation(self, conversation_id: str, user_id: int):
        """Delete conversation and its messages"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Verify ownership
        cursor.execute("""
            SELECT user_id FROM conversations WHERE id = ?
        """, (conversation_id,))

        conv = cursor.fetchone()
        if conv and conv['user_id'] == user_id:
            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            conn.commit()

        conn.close()

    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM sessions
            WHERE expires_at < CURRENT_TIMESTAMP
        """)

        conn.commit()
        conn.close()
