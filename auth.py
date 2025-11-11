import streamlit as st
import hashlib
from datetime import datetime
from database import Database
from typing import Optional, Dict, Any

class AuthManager:
    def __init__(self, db: Database):
        self.db = db
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_info' not in st.session_state:
            st.session_state.user_info = None
        if 'current_session_id' not in st.session_state:
            st.session_state.current_session_id = None
    
    def register_user(self, username: str, email: str, password: str, confirm_password: str,
                     role: str, full_name: str, department: str = None) -> tuple[bool, str]:
        """Register a new user"""
        # Validation
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if password != confirm_password:
            return False, "Passwords do not match"
        
        if "@" not in email or "." not in email:
            return False, "Please enter a valid email address"
        
        if not full_name.strip():
            return False, "Full name is required"
        
        # Attempt to create user
        success = self.db.create_user(username, email, password, role, full_name, department)
        
        if success:
            return True, "Registration successful! Please log in."
        else:
            return False, "Username or email already exists"
    
    def login_user(self, username: str, password: str) -> tuple[bool, str]:
        """Authenticate user login"""
        if not username or not password:
            return False, "Please enter both username and password"
        
        user_info = self.db.authenticate_user(username, password)
        
        if user_info:
            st.session_state.authenticated = True
            st.session_state.user_info = user_info
            st.session_state.current_session_id = self.db.create_chat_session(user_info['user_id'])
            return True, f"Welcome back, {user_info['full_name']}!"
        else:
            return False, "Invalid username or password"
    
    def logout_user(self):
        """Logout current user"""
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.session_state.current_session_id = None
        # Clear other session state variables
        for key in list(st.session_state.keys()):
            if key.startswith('chat_'):
                del st.session_state[key]
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current user information"""
        return st.session_state.get('user_info')
    
    def get_current_session_id(self) -> Optional[str]:
        """Get current chat session ID"""
        return st.session_state.get('current_session_id')
    
    def require_auth(self):
        """Decorator-like function to require authentication"""
        if not self.is_authenticated():
            st.error("🔒 Please log in to access this feature")
            st.stop()
    
    def require_role(self, required_role: str):
        """Require specific user role"""
        self.require_auth()
        user = self.get_current_user()
        if user and user['role'] != required_role:
            st.error(f"🚫 This feature is only available for {required_role}s")
            st.stop()
    
    def render_login_form(self):
        """Render login form"""
        st.subheader("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            # Replaced unsupported 'width' parameter with use_container_width for Streamlit compatibility
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                # Show loading animation
                with st.spinner("Logging in..."):
                    success, message = self.login_user(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    def render_register_form(self):
        """Render registration form"""
        st.subheader("📝 Register")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username*", placeholder="Choose a username")
                email = st.text_input("Email*", placeholder="your.email@domain.com")
                full_name = st.text_input("Full Name*", placeholder="Your full name")
            
            with col2:
                password = st.text_input("Password*", type="password", placeholder="At least 6 characters")
                confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
                role = st.selectbox("Role*", ["student", "faculty"])
            
            department = st.text_input("Department", placeholder="Your department (optional)")
            
            # Replaced unsupported 'width' parameter
            submit_button = st.form_submit_button("Register", use_container_width=True)
            
            if submit_button:
                success, message = self.register_user(
                    username, email, password, confirm_password, 
                    role, full_name, department if department else None
                )
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)
    
    def render_user_profile(self):
        """Render user profile section"""
        user = self.get_current_user()
        if not user:
            return
        # NOTE: Do NOT open a new st.sidebar context here (already inside one in caller)
        st.markdown("---")
        st.markdown("### 👤 Profile")
        st.write(f"**{user['full_name']}**")
        st.write(f"Role: {user['role'].title()}")
        if user['department']:
            st.write(f"Department: {user['department']}")
        st.write(f"Email: {user['email']}")
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            self.logout_user()
            st.rerun()