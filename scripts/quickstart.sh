#!/usr/bin/env bash
# YouTube AI Automation - Quick Start Script
# Automated setup and start for development

set -e

echo "🎬 YouTube AI Automation - Quick Start"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if already running
if pgrep -f "python.*app.py" > /dev/null; then
    echo -e "${RED}❌ Backend is already running${NC}"
    exit 1
fi

echo -e "${YELLOW}•${NC} Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python 3 found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Node.js found"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${YELLOW}⚠️${NC}  FFmpeg is not installed (required for video generation)"
else
    echo -e "${GREEN}✓${NC} FFmpeg found"
fi

echo ""
echo -e "${YELLOW}•${NC} Setting up virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment exists"
fi

echo ""
echo -e "${YELLOW}•${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

echo ""
echo -e "${YELLOW}•${NC} Installing Python dependencies..."
pip install -q --upgrade pip setuptools wheel
pip install -q -r requirements.txt
echo -e "${GREEN}✓${NC} Python dependencies installed"

echo ""
echo -e "${YELLOW}•${NC} Installing Node.js dependencies..."
cd frontend
npm install -q
cd ..
echo -e "${GREEN}✓${NC} Node.js dependencies installed"

echo ""
echo -e "${YELLOW}•${NC} Creating directories..."
mkdir -p storage/videos
mkdir -p storage/thumbnails
mkdir -p temp
mkdir -p logs
echo -e "${GREEN}✓${NC} Directories created"

echo ""
echo -e "${YELLOW}•${NC} Checking environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓${NC} .env created from template (edit as needed)"
else
    echo -e "${GREEN}✓${NC} .env exists"
fi

echo ""
echo -e "${YELLOW}•${NC} Checking external services..."

if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Ollama is running"
else
    echo -e "${YELLOW}⚠️${NC}  Ollama is not running (start with: ollama serve)"
fi

if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Piper TTS is running"
else
    echo -e "${YELLOW}⚠️${NC}  Piper TTS is not running (start with Docker or manually)"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Ollama):"
echo -e "${YELLOW}  ollama serve${NC}"
echo ""
echo "Terminal 2 (Backend):"
echo -e "${YELLOW}  source venv/bin/activate${NC}"
echo -e "${YELLOW}  python backend/app.py${NC}"
echo ""
echo "Terminal 3 (Frontend):"
echo -e "${YELLOW}  cd frontend && npm run dev${NC}"
echo ""
echo "Then open browser to: http://localhost:3000"
echo ""
