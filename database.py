import sqlite3
import bcrypt
from datetime import datetime
import uuid
from typing import Optional, List, Dict, Any

class Database:
    def __init__(self, db_path: str = "edubot.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('student', 'faculty')),
                full_name TEXT NOT NULL,
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Chat sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE NOT NULL,
                session_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                message_type TEXT NOT NULL CHECK(message_type IN ('text', 'image')),
                user_message TEXT,
                image_path TEXT,
                bot_response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # User analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                total_queries INTEGER DEFAULT 0,
                text_queries INTEGER DEFAULT 0,
                image_queries INTEGER DEFAULT 0,
                last_query_date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username: str, email: str, password: str, role: str, 
                   full_name: str, department: str = None) -> bool:
        """Create a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            user_id = str(uuid.uuid4())
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute('''
                INSERT INTO users (user_id, username, email, password_hash, role, full_name, department)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, email, password_hash, role, full_name, department))
            
            # Initialize user analytics
            cursor.execute('''
                INSERT INTO user_analytics (user_id)
                VALUES (?)
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, email, password_hash, role, full_name, department, is_active
            FROM users WHERE username = ?
        ''', (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user and user[7] and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            # Update last login
            self.update_last_login(user[0])
            return {
                'user_id': user[0],
                'username': user[1],
                'email': user[2],
                'role': user[4],
                'full_name': user[5],
                'department': user[6]
            }
        return None
    
    def update_last_login(self, user_id: str):
        """Update user's last login timestamp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
        conn.close()
    
    def create_chat_session(self, user_id: str) -> str:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_sessions (session_id, user_id)
            VALUES (?, ?)
        ''', (session_id, user_id))
        
        conn.commit()
        conn.close()
        return session_id
    
    def save_message(self, session_id: str, user_id: str, message_type: str, 
                    user_message: str = None, image_path: str = None, 
                    bot_response: str = ""):
        """Save a message to the database"""
        message_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (message_id, session_id, user_id, message_type, 
                                user_message, image_path, bot_response)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (message_id, session_id, user_id, message_type, user_message, image_path, bot_response))
        
        # Update session last activity
        cursor.execute('''
            UPDATE chat_sessions SET last_activity = CURRENT_TIMESTAMP 
            WHERE session_id = ?
        ''', (session_id,))
        
        # Update user analytics
        cursor.execute('''
            UPDATE user_analytics 
            SET total_queries = total_queries + 1,
                text_queries = text_queries + CASE WHEN ? = 'text' THEN 1 ELSE 0 END,
                image_queries = image_queries + CASE WHEN ? = 'image' THEN 1 ELSE 0 END,
                last_query_date = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (message_type, message_type, user_id))
        
        conn.commit()
        conn.close()
    
    def get_chat_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat history for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.message_type, m.user_message, m.image_path, m.bot_response, m.timestamp
            FROM messages m
            JOIN chat_sessions cs ON m.session_id = cs.session_id
            WHERE m.user_id = ?
            ORDER BY m.timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        messages = cursor.fetchall()
        conn.close()
        
        return [{
            'message_type': msg[0],
            'user_message': msg[1],
            'image_path': msg[2],
            'bot_response': msg[3],
            'timestamp': msg[4]
        } for msg in messages]
    
    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get analytics for a specific user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT total_queries, text_queries, image_queries, last_query_date
            FROM user_analytics WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'total_queries': result[0],
                'text_queries': result[1],
                'image_queries': result[2],
                'last_query_date': result[3]
            }
        return {'total_queries': 0, 'text_queries': 0, 'image_queries': 0, 'last_query_date': None}
    
    def get_all_users_analytics(self) -> List[Dict[str, Any]]:
        """Get analytics for all users (for faculty dashboard)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.username, u.full_name, u.role, u.department, u.created_at,
                   ua.total_queries, ua.text_queries, ua.image_queries, ua.last_query_date
            FROM users u
            LEFT JOIN user_analytics ua ON u.user_id = ua.user_id
            WHERE u.is_active = 1
            ORDER BY ua.total_queries DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'username': row[0],
            'full_name': row[1],
            'role': row[2],
            'department': row[3],
            'created_at': row[4],
            'total_queries': row[5] or 0,
            'text_queries': row[6] or 0,
            'image_queries': row[7] or 0,
            'last_query_date': row[8]
        } for row in results]