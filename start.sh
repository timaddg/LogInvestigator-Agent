#!/bin/bash

# Log Investigator Startup Script

echo "🚀 Starting Log Investigator..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📥 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env file not found!"
    echo "   Please create backend/.env with your GEMINI_API_KEY"
    echo "   Example:"
    echo "   GEMINI_API_KEY=your_api_key_here"
fi

# Install frontend dependencies
echo "📥 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create frontend environment file if it doesn't exist
if [ ! -f "frontend/.env.local" ]; then
    echo "🔧 Creating frontend environment file..."
    echo "FLASK_BACKEND_URL=http://localhost:8000" > frontend/.env.local
fi

echo "✅ Setup complete!"
echo ""
echo "🌐 To start the application:"
echo "   Terminal 1: python run.py web"
echo "   Terminal 2: cd frontend && npm run dev"
echo ""
echo "📖 For more options: python run.py --help" 