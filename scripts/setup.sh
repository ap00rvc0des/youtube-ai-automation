#!/usr/bin/env bash
# YouTube AI Automation - Setup Script
# Installs all dependencies and configures the system

set -e  # Exit on error

echo "🎬 YouTube AI Automation - Setup Script"
echo "======================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "  Python version: $PYTHON_VERSION"

# Check Node.js version
echo "✓ Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "  ERROR: Node.js is not installed!"
    exit 1
fi
NODE_VERSION=$(node --version)
echo "  Node.js version: $NODE_VERSION"

# Create virtual environment
echo "✓ Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "✓ Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "  Python dependencies installed"

# Install Node.js dependencies
echo "✓ Installing Node.js dependencies..."
cd frontend
npm install
cd ..
echo "  Node.js dependencies installed"

# Copy environment file
echo "✓ Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  Created .env from .env.example"
    echo "  ⚠️  Please edit .env with your configuration!"
else
    echo "  .env already exists"
fi

# Create directories
echo "✓ Creating necessary directories..."
mkdir -p storage/videos
mkdir -p storage/thumbnails
mkdir -p temp
mkdir -p logs
echo "  Directories created"

# Check for external tools
echo "✓ Checking for external tools..."

if ! command -v ffmpeg &> /dev/null; then
    echo "  ⚠️  FFmpeg is not installed!"
    echo "  Install it with: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
else
    echo "  ✓ FFmpeg is installed"
fi

if ! command -v ollama &> /dev/null; then
    echo "  ⚠️  Ollama is not installed!"
    echo "  Install it from: https://ollama.ai"
else
    echo "  ✓ Ollama is installed"
fi

if ! command -v docker &> /dev/null; then
    echo "  ⚠️  Docker is not installed!"
    echo "  Install it from: https://docker.com"
else
    echo "  ✓ Docker is installed"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start Ollama: ollama serve"
echo "3. In another terminal, run: python backend/app.py"
echo "4. In another terminal, run: cd frontend && npm run dev"
echo "5. Open http://localhost:3000 in your browser"
echo ""
