# Multi-stage Dockerfile for Log Investigator
# Builds both frontend and backend, then serves them together

# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci --only=production

# Copy frontend source code
COPY frontend/ ./

# Build frontend
RUN npm run build

# Stage 2: Build Backend
FROM python:3.11-slim AS backend-builder

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./
COPY run.py ./
COPY main.py ./
COPY env.example ./

# Stage 3: Final Runtime Image
FROM python:3.11-slim

# Install system dependencies for runtime
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy Python dependencies from backend stage
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend code
COPY --from=backend-builder /app/backend ./backend
COPY --from=backend-builder /app/run.py ./
COPY --from=backend-builder /app/main.py ./
COPY --from=backend-builder /app/env.example ./

# Copy built frontend from frontend stage
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/public ./frontend/public
COPY --from=frontend-builder /app/frontend/package.json ./frontend/package.json
COPY --from=frontend-builder /app/frontend/next.config.ts ./frontend/next.config.ts

# Install Node.js for serving frontend
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install frontend runtime dependencies
WORKDIR /app/frontend
RUN npm ci --only=production

# Create a startup script
WORKDIR /app
RUN echo '#!/bin/bash\n\
echo "Starting Log Investigator..."\n\
echo "Frontend: http://localhost:4000"\n\
echo "Backend:  http://localhost:8000"\n\
\n\
# Start backend in background\n\
python run.py web &\n\
BACKEND_PID=$!\n\
\n\
# Wait a moment for backend to start\n\
sleep 3\n\
\n\
# Start frontend\n\
cd frontend && npm start &\n\
FRONTEND_PID=$!\n\
\n\
# Wait for both processes\n\
wait $BACKEND_PID $FRONTEND_PID\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose ports
EXPOSE 4000 8000

# Set environment variables
ENV NODE_ENV=production
ENV PYTHONPATH=/app/backend

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["/app/start.sh"] 