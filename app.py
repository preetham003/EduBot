import streamlit as st
import os
from datetime import datetime, timedelta
from database import Database
from auth import AuthManager
from gemini_api import GeminiAPI
from ui_components import UIComponents
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="EduBot - Your Educational AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/edubot',
        'Report a bug': "https://github.com/yourusername/edubot/issues",
        'About': "# EduBot\nYour intelligent educational companion powered by Google Gemini AI"
    }
)

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), 'style.css')
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Fallback inline CSS if style.css doesn't exist
        st.markdown("""
            <style>
            .main { padding: 0rem 1rem; }
            .stButton>button {
                width: 100%;
                border-radius: 8px;
                height: 3em;
                font-weight: 600;
            }
            </style>
        """, unsafe_allow_html=True)

load_css()

# Initialize components
@st.cache_resource
def init_components():
    db = Database()
    auth = AuthManager(db)
    try:
        gemini = GeminiAPI()
    except ValueError as e:
        st.error(f"⚠️ {str(e)}")
        st.info("Please set your GEMINI_API_KEY in the .env file to use EduBot.")
        st.stop()
    ui = UIComponents()
    return db, auth, gemini, ui

db, auth, gemini, ui = init_components()

# Initialize session state
auth.init_session_state()

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True

def main():
    """Main application logic"""
    
    # Check authentication
    if not auth.is_authenticated():
        render_landing_page()
    else:
        render_dashboard()

def render_landing_page():
    """Render the landing page with login/register forms"""
    
    # Hero Section
    ui.render_hero_section()
    
    # Features Section
    st.markdown("---")
    ui.render_features_section()
    
    # Authentication Section
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; margin-top: 3rem;'>🚀 Get Started</h2>", unsafe_allow_html=True)
    
    # Tabs for Login and Register
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            auth.render_login_form()
    
    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            auth.render_register_form()

def render_dashboard():
    """Render the main dashboard for authenticated users"""
    
    user = auth.get_current_user()
    
    # Sidebar
    with st.sidebar:
        # Profile section at the top
        ui.render_profile_card(user)
        auth.render_user_profile()
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 New Chat Session", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.current_session_id = db.create_chat_session(user['user_id'])
            st.session_state.show_welcome = True
            st.rerun()
        
        if st.button("📜 View History", use_container_width=True):
            st.session_state.active_tab = "history"
            st.rerun()
        
        # Analytics in sidebar
        st.markdown("---")
        st.markdown("### 📊 Your Stats")
        analytics = db.get_user_analytics(user['user_id'])
        
        # Stats grid with better styling
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Queries", analytics['total_queries'])
            st.metric("Text Queries", analytics['text_queries'])
        with col2:
            st.metric("Image Queries", analytics['image_queries'])
            if analytics['last_query_date']:
                last_query_dt = datetime.fromisoformat(analytics['last_query_date'])
                today = datetime.now().date()
                last_query_date = last_query_dt.date()
                
                if last_query_date == today:
                    last_date_str = "Today"
                elif last_query_date == today - timedelta(days=1):
                    last_date_str = "Yesterday"
                else:
                    last_date_str = last_query_dt.strftime("%m/%d/%Y")
                
                st.metric("Last Active", last_date_str)
            else:
                st.metric("Last Active", "Never")
    
    # Main content area
    # Welcome message (only show once per session)
    if st.session_state.show_welcome:
        ui.render_welcome_message(user)
        st.session_state.show_welcome = False
    
    # Tabs for different sections
    if user['role'] == 'faculty':
        tab1, tab2, tab3 = st.tabs(["💬 Chat", "🖼️ Image Analysis", "📊 Analytics Dashboard"])
    else:
        tab1, tab2 = st.tabs(["💬 Chat", "🖼️ Image Analysis"])
    
    with tab1:
        render_chat_interface()
    
    with tab2:
        render_image_analysis()
    
    if user['role'] == 'faculty':
        with tab3:
            render_analytics_dashboard()

def render_chat_interface():
    """Render the text-based chat interface"""
    
    user = auth.get_current_user()
    
    # Chat container with custom styling
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.chat_history:
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                ui.render_user_message(message['content'])
            else:
                ui.render_bot_message(message['content'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input at the bottom
    st.markdown("---")
    
    # Suggestions for new users
    if not st.session_state.chat_history:
        st.markdown("#### 💡 Try asking:")
        suggestions = gemini.get_chat_suggestions(user['role'])
        
        cols = st.columns(len(suggestions[:3]))
        for idx, (col, suggestion) in enumerate(zip(cols, suggestions[:3])):
            with col:
                if st.button(f"💬 {suggestion}", key=f"sug_{idx}", use_container_width=True):
                    process_text_query(suggestion)
                    st.rerun()
    
    # Input form
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask me anything...",
                placeholder="Type your question here... (e.g., 'Explain photosynthesis' or 'How do I solve quadratic equations?')",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("Send 📤", use_container_width=True)
        
        if submit_button and user_input.strip():
            process_text_query(user_input)
            st.rerun()

def process_text_query(query: str):
    """Process a text-based query"""
    user = auth.get_current_user()
    
    # Add user message to chat history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': query
    })
    
    # Generate AI response
    with st.spinner("🤔 Thinking..."):
        response, success = gemini.generate_text_response(query)
    
    # Add bot response to chat history
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': response
    })
    
    # Save to database
    session_id = auth.get_current_session_id()
    if session_id:
        db.save_message(
            session_id=session_id,
            user_id=user['user_id'],
            message_type='text',
            user_message=query,
            bot_response=response
        )

def render_image_analysis():
    """Render the image analysis interface"""
    
    user = auth.get_current_user()
    
    st.markdown("### 🖼️ Upload an Image for Analysis")
    st.markdown("Upload educational content like diagrams, equations, charts, or any visual material for detailed analysis.")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Supported formats: PNG, JPG, JPEG, GIF, BMP"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
            # Optional query about the image
            image_query = st.text_area(
                "Ask something specific about this image (optional):",
                placeholder="E.g., 'Explain the diagram', 'What formula is shown?', 'Describe the process illustrated'",
                height=100
            )
            
            analyze_button = st.button("🔍 Analyze Image", use_container_width=True, type="primary")
    
    with col2:
        if uploaded_file and analyze_button:
            with st.spinner("🔍 Analyzing image..."):
                # Process image
                image_data = gemini.process_uploaded_image(uploaded_file)
                
                if image_data:
                    # Generate response
                    response, success = gemini.generate_image_response(image_data, image_query)
                    
                    # Display response
                    if success:
                        st.markdown("### 🤖 EduBot's Analysis:")
                        ui.render_bot_message(response)
                        
                        # Save to database
                        session_id = auth.get_current_session_id()
                        if session_id:
                            db.save_message(
                                session_id=session_id,
                                user_id=user['user_id'],
                                message_type='image',
                                user_message=image_query if image_query else "Image analysis request",
                                image_path=uploaded_file.name,
                                bot_response=response
                            )
                        
                        st.success("✅ Analysis complete and saved to your history!")
                    else:
                        st.error("❌ Failed to analyze the image. Please try again.")
                else:
                    st.error("❌ Failed to process the image. Please ensure it's a valid image file.")
        elif not uploaded_file:
            # Show example/instructions
            st.markdown("""
            ### 📚 What can I analyze?
            
            - **Mathematics**: Equations, graphs, geometric figures
            - **Science**: Diagrams, chemical structures, lab setups
            - **Charts & Graphs**: Data visualizations, infographics
            - **Textbook Content**: Pages, formulas, problem statements
            - **Handwritten Notes**: Clear handwriting (printed is better)
            - **Presentations**: Slides, educational posters
            
            #### 💡 Tips for best results:
            - Use clear, high-resolution images
            - Ensure good lighting and contrast
            - Avoid blurry or distorted images
            - Focus on one concept per image
            """)

def render_analytics_dashboard():
    """Render analytics dashboard for faculty"""
    
    st.markdown("### 📊 Platform Analytics")
    st.markdown("Overview of platform usage and user engagement")
    
    # Get all users analytics
    all_users = db.get_all_users_analytics()
    
    if not all_users:
        st.info("No user data available yet.")
        return
    
    # Summary metrics
    total_users = len(all_users)
    total_queries = sum(user['total_queries'] for user in all_users)
    total_text = sum(user['text_queries'] for user in all_users)
    total_images = sum(user['image_queries'] for user in all_users)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Users", total_users)
    with col2:
        st.metric("💬 Total Queries", total_queries)
    with col3:
        st.metric("📝 Text Queries", total_text)
    with col4:
        st.metric("🖼️ Image Queries", total_images)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Query type distribution
        st.markdown("#### Query Type Distribution")
        fig = go.Figure(data=[go.Pie(
            labels=['Text Queries', 'Image Queries'],
            values=[total_text, total_images],
            hole=.3,
            marker_colors=['#667eea', '#764ba2']
        )])
        fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top users by query count
        st.markdown("#### Most Active Users")
        top_users = sorted(all_users, key=lambda x: x['total_queries'], reverse=True)[:5]
        
        if top_users:
            users_df = {
                'User': [u['username'] for u in top_users],
                'Queries': [u['total_queries'] for u in top_users]
            }
            
            fig = px.bar(
                users_df,
                x='Queries',
                y='User',
                orientation='h',
                color='Queries',
                color_continuous_scale='Purples'
            )
            fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # User table
    st.markdown("#### 📋 All Users Overview")
    
    # Prepare data for table
    user_data = []
    for user in all_users:
        user_data.append({
            'Username': user['username'],
            'Full Name': user['full_name'],
            'Role': user['role'].title(),
            'Department': user['department'] or 'N/A',
            'Total Queries': user['total_queries'],
            'Text': user['text_queries'],
            'Images': user['image_queries'],
            'Last Active': user['last_query_date'][:10] if user['last_query_date'] else 'Never'
        })
    
    st.dataframe(user_data, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
