#!/bin/bash

echo "Starting Log Investigator on Render..."

# Set environment variables for Render
export NODE_ENV=production
export PYTHONPATH=/opt/render/project/src/backend
export PORT=${PORT:-8000}

# Create necessary directories
mkdir -p uploads
mkdir -p data

# Build frontend if not already built
if [ ! -d "frontend/out" ]; then
    echo "Building frontend..."
    cd frontend
    npm install
    npm run build
    cd ..
fi

echo "Starting backend on port $PORT..."

# Start the Flask backend
python run.py web 