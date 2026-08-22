#!/usr/bin/env bash
# YouTube AI Automation - Start Script
# Starts all services (manual mode)

echo "🎬 YouTube AI Automation - Starting Services"
echo "============================================"
echo ""

# Function to display usage
usage() {
    echo "Usage: ./scripts/start.sh [option]"
    echo ""
    echo "Options:"
    echo "  backend    - Start only backend"
    echo "  frontend   - Start only frontend"
    echo "  ollama     - Start Ollama server"
    echo "  all        - Start all services (requires multiple terminals)"
    echo "  docker     - Start using Docker Compose"
    echo ""
}

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

case "$1" in
    backend)
        echo "Starting backend server..."
        source venv/bin/activate
        python backend/app.py
        ;;
    frontend)
        echo "Starting frontend development server..."
        cd frontend
        npm run dev
        ;;
    ollama)
        echo "Starting Ollama server..."
        ollama serve
        ;;
    docker)
        echo "Starting with Docker Compose..."
        docker-compose up
        ;;
    all)
        echo "To start all services, open 3-4 terminals and run:"
        echo ""
        echo "Terminal 1: ./scripts/start.sh ollama"
        echo "Terminal 2: ./scripts/start.sh backend"
        echo "Terminal 3: ./scripts/start.sh frontend"
        echo ""
        echo "Or use Docker Compose: ./scripts/start.sh docker"
        ;;
    *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
esac
