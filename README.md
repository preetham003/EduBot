# EduBot - Educational AI Assistant

A comprehensive educational chatbot platform built with Streamlit and powered by Google Gemini AI, designed for students and faculty to engage in meaningful educational conversations.

## 🌟 Features

- **👥 User Management**: Registration and authentication system with role-based access (Student/Faculty)
- **💬 Text Queries**: Ask educational questions and get detailed, contextual responses
- **🖼️ Image Analysis**: Upload images for educational analysis and insights
- **📊 Analytics Dashboard**: Track learning progress and platform usage
- **🎨 Modern UI**: Beautiful, responsive interface with custom styling
- **📈 Faculty Tools**: Advanced analytics and user management for educators
- **📱 Mobile Friendly**: Responsive design that works on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free from Google AI Studio)

### Installation

1. **Clone or download the project files to your desired directory**

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     SECRET_KEY=your_secret_key_here
     DATABASE_PATH=edubot.db
     ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser and navigate to the provided URL (typically `http://localhost:8501`)**

## 🔑 Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key and add it to your `.env` file

## 📖 How to Use

### For Students:
1. **Register** with your details and select "Student" role
2. **Login** with your credentials
3. **Ask Questions**: Use the text query feature for any educational topic
4. **Upload Images**: Analyze diagrams, equations, or educational content
5. **Track Progress**: View your learning analytics and chat history

### For Faculty:
1. **Register** with "Faculty" role
2. **Access Advanced Features**: View platform analytics and user management
3. **Monitor Usage**: Track student engagement and popular topics
4. **Educational Support**: Use the same query features as students

## 🏗️ Project Structure

```
Chatbot/
├── app.py                 # Main Streamlit application
├── database.py           # Database models and operations
├── auth.py              # Authentication management
├── gemini_api.py        # Google Gemini API integration
├── ui_components.py     # UI components and layouts
├── style.css           # Custom CSS styling
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md         # This file
```

## 🔧 Configuration

### Database
- **Type**: SQLite (file-based, no additional setup required)
- **Location**: `edubot.db` (created automatically)
- **Tables**: Users, Chat Sessions, Messages, User Analytics

### Environment Variables
```env
GEMINI_API_KEY=your_gemini_api_key_here    # Required: Your Gemini API key
SECRET_KEY=your_secret_key_here            # Optional: For session security
DATABASE_PATH=edubot.db                    # Optional: Database file path
```

## 🛠️ Technical Details

### Backend Technologies:
- **Python**: Core programming language
- **SQLite**: Lightweight database for data persistence
- **Google Gemini AI**: Advanced AI model for text and image analysis
- **BCrypt**: Secure password hashing

### Frontend Technologies:
- **Streamlit**: Web application framework
- **Plotly**: Interactive charts and visualizations
- **Custom CSS**: Modern, responsive design
- **HTML/CSS**: Enhanced UI components

### Key Features Implementation:
- **Role-based Authentication**: Separate interfaces for students and faculty
- **Session Management**: Persistent chat sessions and user state
- **Image Processing**: PIL-based image handling for AI analysis
- **Real-time Analytics**: Live usage statistics and progress tracking
- **Error Handling**: Comprehensive error management and user feedback

## 📊 Database Schema

### Users Table
- User ID, Username, Email, Password Hash
- Role (Student/Faculty), Full Name, Department
- Creation timestamp, Last login, Active status

### Chat Sessions Table
- Session ID, User ID, Creation timestamp
- Last activity tracking

### Messages Table
- Message ID, Session ID, User ID
- Message type (text/image), Content, AI Response
- Timestamp for chronological ordering

### User Analytics Table
- User ID, Query counts (total, text, image)
- Last query date for activity tracking

## 🎨 UI Features

### Modern Design Elements:
- **Gradient Backgrounds**: Eye-catching visual appeal
- **Card-based Layout**: Clean, organized content presentation
- **Responsive Design**: Mobile and desktop compatibility
- **Interactive Elements**: Hover effects and smooth transitions
- **Color-coded Messages**: Easy distinction between user and bot messages

### User Experience:
- **Intuitive Navigation**: Clear tabs and sections
- **Loading Indicators**: Visual feedback during AI processing
- **Error Messages**: Helpful error guidance
- **Success Feedback**: Confirmation of actions
- **Quick Actions**: Shortcut buttons for common tasks

## � Post-Login Experience

Once authenticated, users are taken to a unified interaction dashboard:

- **Independent Sidebar Scroll**: The left sidebar houses your profile, logout button, quick actions, and a compact statistics block (total/text/image queries + last activity). It scrolls independently from the main chat area for uninterrupted conversation flow.
- **Real-time Chat Interface**: Modern, fixed bottom input bar with an embedded send butto. The chat history area only introduces its own scroll when messages exceed the viewport height—initially presenting a clean, scroll-free canvas.
- **Tabbed Interaction Modes**: Switch between the primary "Chat" tab and "Image Analysis" for vision-based educational queries without losing context.
- **Session Controls**: Clear the current chat instantly from the sidebar.
- **Responsive Layout**: Works smoothly across desktop and mobile, keeping the input anchored while you scroll through messages.

### Chat Behaviors
- Messages are visually differentiated (user vs EduBot) with accessible color contrasts.
- Automatic persistence: each send stores the interaction and updates analytics.
- Scroll activation only when needed—improves focus and reduces early visual noise.

## �🔐 Security Features

- **Password Hashing**: BCrypt for secure password storage
- **Session Management**: Secure user session handling
- **Input Validation**: Protection against malicious inputs
- **Role-based Access**: Restricted features based on user roles
- **Error Handling**: Secure error messages without sensitive information

## 🚀 Deployment Options

### Local Development:
```bash
streamlit run app.py
```

### Production Deployment:
- **Streamlit Cloud**: Direct deployment from GitHub
- **Heroku**: Container-based deployment
- **Docker**: Containerized deployment option
- **VPS/Cloud Server**: Manual server deployment

## 🆘 Troubleshooting

### Common Issues:

1. **"Import errors"** - Install requirements: `pip install -r requirements.txt`
2. **"Gemini API key not found"** - Check your `.env` file setup
3. **"Database errors"** - Ensure write permissions in the project directory
4. **"CSS not loading"** - Verify `style.css` file exists in the same directory

### Performance Tips:
- Keep image uploads under 10MB for best performance
- Clear chat history periodically for optimal experience
- Use specific, well-formed questions for better AI responses

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs and issues
- Suggesting new features
- Improving documentation
- Submitting pull requests

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Google Gemini AI** for providing the powerful AI capabilities
- **Streamlit** for the excellent web framework
- **SQLite** for the reliable database solution
- **Python Community** for the amazing ecosystem of libraries

---

**Happy Learning with EduBot! 🎓✨**