# ============================================
# Multi-stage Build for YouTube AI Automation
# ============================================

# Stage 1: Python Backend
FROM python:3.11-slim as backend-builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    ffmpeg \
    libsndfile1 \
    libsndfile1-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Node.js Frontend
FROM node:18-alpine as frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --frozen-lockfile

# Copy source
COPY frontend/ .

# Build frontend
RUN npm run build

# Stage 3: Final runtime image
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend code
COPY backend/ ./backend/
COPY ai/ ./ai/
COPY tts/ ./tts/
COPY video/ ./video/
COPY thumbnails/ ./thumbnails/
COPY youtube/ ./youtube/
COPY scheduler/ ./scheduler/
COPY storage/ ./storage/

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy configuration files
COPY .env.example .
COPY README.md .

# Create directories
RUN mkdir -p logs temp

# Expose ports
EXPOSE 5000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Start application
CMD ["python", "backend/app.py"]
