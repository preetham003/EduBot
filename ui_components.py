import streamlit as st
from datetime import datetime

class UIComponents:
    """Reusable UI components for the EduBot application"""
    
    def __init__(self):
        self.primary_color = "#667eea"
        self.secondary_color = "#764ba2"
    
    def render_hero_section(self):
        """Render the hero section on the landing page"""
        st.markdown("""
            <div class="hero-section">
                <h1 class="hero-title">🎓 Welcome to EduBot</h1>
                <p class="hero-subtitle">Your Intelligent Educational Companion</p>
                <p style="font-size: 1.1rem; margin-top: 1rem; opacity: 0.9;">
                    Powered by Google Gemini AI • Supporting Students & Faculty
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_features_section(self):
        """Render the features section"""
        st.markdown("<h2 style='text-align: center; margin: 2rem 0;'>✨ Key Features</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">💬</div>
                    <h3 class="feature-title">Smart Text Queries</h3>
                    <p class="feature-description">
                        Ask any educational question and get detailed, contextual responses 
                        powered by advanced AI technology.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">🖼️</div>
                    <h3 class="feature-title">Image Analysis</h3>
                    <p class="feature-description">
                        Upload diagrams, equations, charts, or any educational content 
                        for instant AI-powered analysis.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3 class="feature-title">Learning Analytics</h3>
                    <p class="feature-description">
                        Track your progress, view history, and access powerful insights 
                        about your learning journey.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <h3 class="feature-title">Personalized Experience</h3>
                    <p class="feature-description">
                        Role-based interface tailored for both students and faculty 
                        with specialized features for each.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3 class="feature-title">Secure & Private</h3>
                    <p class="feature-description">
                        Your data is protected with industry-standard encryption 
                        and secure authentication protocols.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h3 class="feature-title">Responsive Design</h3>
                    <p class="feature-description">
                        Access EduBot from any device - desktop, tablet, or mobile 
                        with a seamless experience.
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    def render_profile_card(self, user):
        """Render user profile card in sidebar"""
        role_emoji = "👨‍🎓" if user['role'] == 'student' else "👨‍🏫"
        
        st.markdown(f"""
            <div class="profile-card">
                <div class="profile-avatar">{role_emoji}</div>
                <div class="profile-name">{user['full_name']}</div>
                <div class="profile-role">{user['role']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    def render_welcome_message(self, user):
        """Render welcome message for authenticated users"""
        current_hour = datetime.now().hour
        
        if current_hour < 12:
            greeting = "Good Morning"
            emoji = "🌅"
        elif current_hour < 18:
            greeting = "Good Afternoon"
            emoji = "☀️"
        else:
            greeting = "Good Evening"
            emoji = "🌙"
        
        st.markdown(f"""
            <div class="welcome-box">
                <h2>{emoji} {greeting}, {user['full_name'].split()[0]}!</h2>
                <p style="font-size: 1.1rem; margin-top: 0.5rem;">
                    Welcome back to EduBot. How can I help you learn today?
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_user_message(self, message):
        """Render a user message bubble"""
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
                <div class="user-message">
                    {message}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    def render_bot_message(self, message):
        """Render a bot message bubble"""
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                <div class="bot-message">
                    {message}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    def render_stat_card(self, title, value, icon):
        """Render a statistics card"""
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{title}</div>
            </div>
        """, unsafe_allow_html=True)
    
    def render_info_box(self, title, content, icon="ℹ️"):
        """Render an information box"""
        st.markdown(f"""
            <div class="custom-card">
                <h3 style="color: {self.primary_color}; margin-bottom: 1rem;">
                    {icon} {title}
                </h3>
                <p style="color: #666; line-height: 1.6;">
                    {content}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_badge(self, text, badge_type="primary"):
        """Render a badge"""
        st.markdown(f"""
            <span class="badge badge-{badge_type}">{text}</span>
        """, unsafe_allow_html=True)
    
    def render_divider(self, text=""):
        """Render a styled divider"""
        if text:
            st.markdown(f"""
                <div style="text-align: center; margin: 2rem 0;">
                    <span style="background: white; padding: 0 1rem; color: #666; font-weight: 600;">
                        {text}
                    </span>
                    <hr style="margin-top: -0.7rem; border: none; border-top: 2px solid #e0e0e0;">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<hr style='border: none; border-top: 2px solid #e0e0e0; margin: 2rem 0;'>", unsafe_allow_html=True)
    
    def render_loading_animation(self, text="Loading..."):
        """Render a loading animation"""
        st.markdown(f"""
            <div style="text-align: center; padding: 2rem;">
                <div class="stSpinner"></div>
                <p style="margin-top: 1rem; color: #666;">{text}</p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_empty_state(self, title, description, icon="📭"):
        """Render an empty state placeholder"""
        st.markdown(f"""
            <div style="text-align: center; padding: 3rem; color: #999;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
                <h3 style="color: #666; margin-bottom: 0.5rem;">{title}</h3>
                <p>{description}</p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_success_message(self, message):
        """Render a success message"""
        st.markdown(f"""
            <div style="background: #d4edda; border-left: 5px solid #28a745; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong style="color: #155724;">✅ {message}</strong>
            </div>
        """, unsafe_allow_html=True)
    
    def render_error_message(self, message):
        """Render an error message"""
        st.markdown(f"""
            <div style="background: #f8d7da; border-left: 5px solid #dc3545; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong style="color: #721c24;">❌ {message}</strong>
            </div>
        """, unsafe_allow_html=True)
    
    def render_info_message(self, message):
        """Render an info message"""
        st.markdown(f"""
            <div style="background: #d1ecf1; border-left: 5px solid #17a2b8; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong style="color: #0c5460;">ℹ️ {message}</strong>
            </div>
        """, unsafe_allow_html=True)
    
    def render_warning_message(self, message):
        """Render a warning message"""
        st.markdown(f"""
            <div style="background: #fff3cd; border-left: 5px solid #ffc107; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong style="color: #856404;">⚠️ {message}</strong>
            </div>
        """, unsafe_allow_html=True)
    
    def render_progress_bar(self, progress, label=""):
        """Render a progress bar"""
        st.markdown(f"""
            <div style="margin: 1rem 0;">
                {f'<p style="margin-bottom: 0.5rem; color: #666;">{label}</p>' if label else ''}
                <div style="background: #e0e0e0; border-radius: 10px; overflow: hidden; height: 20px;">
                    <div style="background: linear-gradient(90deg, {self.primary_color} 0%, {self.secondary_color} 100%); 
                                width: {progress}%; height: 100%; transition: width 0.3s ease;">
                    </div>
                </div>
                <p style="text-align: right; margin-top: 0.3rem; color: #666; font-size: 0.9rem;">{progress}%</p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_timeline_item(self, title, description, date, icon="📅"):
        """Render a timeline item"""
        st.markdown(f"""
            <div style="display: flex; margin: 1.5rem 0; padding-left: 1rem; border-left: 3px solid {self.primary_color};">
                <div style="margin-right: 1rem; font-size: 1.5rem;">{icon}</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 0.3rem 0; color: {self.primary_color};">{title}</h4>
                    <p style="margin: 0 0 0.3rem 0; color: #666;">{description}</p>
                    <p style="margin: 0; font-size: 0.85rem; color: #999;">{date}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    def render_quote(self, text, author=""):
        """Render a styled quote"""
        st.markdown(f"""
            <div style="border-left: 4px solid {self.primary_color}; padding: 1rem 1.5rem; 
                        background: #f8f9fa; margin: 1.5rem 0; border-radius: 0 8px 8px 0;">
                <p style="font-style: italic; font-size: 1.1rem; margin: 0; color: #333;">
                    "{text}"
                </p>
                {f'<p style="margin: 0.5rem 0 0 0; color: #666; font-weight: 600;">— {author}</p>' if author else ''}
            </div>
        """, unsafe_allow_html=True)
    
    def render_collapsible_section(self, title, content, icon="📄"):
        """Render a collapsible section"""
        with st.expander(f"{icon} {title}"):
            st.markdown(content)
    
    def render_footer(self):
        """Render footer"""
        st.markdown("""
            <div style="text-align: center; padding: 2rem 0; margin-top: 3rem; border-top: 2px solid #e0e0e0;">
                <p style="color: #666; margin: 0;">
                    Made with ❤️ by EduBot Team | Powered by Google Gemini AI
                </p>
                <p style="color: #999; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                    © 2025 EduBot. All rights reserved.
                </p>
            </div>
        """, unsafe_allow_html=True)
