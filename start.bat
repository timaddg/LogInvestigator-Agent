@echo off

REM Log Investigator Startup Script for Windows

echo 🚀 Starting Log Investigator...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install backend dependencies
echo 📥 Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..

REM Check if .env file exists
if not exist "backend\.env" (
    echo ⚠️  Warning: backend\.env file not found!
    echo    Please create backend\.env with your GEMINI_API_KEY
    echo    Example:
    echo    GEMINI_API_KEY=your_api_key_here
)

REM Install frontend dependencies
echo 📥 Installing frontend dependencies...
cd frontend
npm install
cd ..

REM Create frontend environment file if it doesn't exist
if not exist "frontend\.env.local" (
    echo 🔧 Creating frontend environment file...
    echo FLASK_BACKEND_URL=http://localhost:8000 > frontend\.env.local
)

echo ✅ Setup complete!
echo.
echo 🌐 To start the application:
echo    Terminal 1: python run.py web
echo    Terminal 2: cd frontend ^&^& npm run dev
echo.
echo 📖 For more options: python run.py --help
pause 