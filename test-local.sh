#!/bin/bash

# Test Log Investigator Locally
# This script helps you test the project without Docker

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${GREEN}=== $1 ===${NC}"
}

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        print_status "Created .env file. Please edit it with your GEMINI_API_KEY"
        print_status "Then run this script again."
        exit 1
    else
        print_error "env.example not found. Please create a .env file manually."
        exit 1
    fi
fi

print_header "Testing Log Investigator Locally"

# Check if Python virtual environment exists
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r backend/requirements.txt

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
cd frontend
npm install
cd ..

print_status "Starting backend server..."
print_status "Backend will be available at: http://localhost:8000"
print_status "Press Ctrl+C to stop the backend"

# Start backend in background
python run.py web &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    print_status "Backend is running successfully!"
else
    print_error "Backend failed to start. Check the logs above."
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

print_status "Starting frontend..."
print_status "Frontend will be available at: http://localhost:4000"
print_status "Press Ctrl+C to stop both services"

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Function to cleanup on exit
cleanup() {
    print_status "Stopping services..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    print_status "Services stopped."
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait 