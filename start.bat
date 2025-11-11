@echo off
echo 🎓 EduBot Setup Script
echo =====================

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file from template
    echo ⚠️  Please edit .env file and add your GEMINI_API_KEY
) else (
    echo ✅ .env file already exists
)

echo.
echo 🚀 Starting EduBot...
echo Open your browser and go to: http://localhost:8501
echo.
streamlit run app.py

pause