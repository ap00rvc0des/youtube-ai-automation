# 🚀 YouTube AI Automation - Installation & Setup Guide

Complete step-by-step guide to get the system running on Windows, macOS, and Linux.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [macOS Installation](#macos-installation)
4. [Linux Installation](#linux-installation)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **RAM**: 8GB
- **Storage**: 20GB free
- **CPU**: 4 cores

### Recommended
- **RAM**: 16GB or more
- **Storage**: 50GB+ SSD
- **GPU**: NVIDIA CUDA or AMD ROCm (for faster processing)
- **Internet**: 10 Mbps+ (for downloading models)

---

## Windows Installation

### Step 1: Install Prerequisites

#### 1.1 Python 3.11+
```bash
# Download from https://www.python.org/downloads/
# OR use Chocolatey:
choco install python --version=3.11.0

# Verify:
python --version
# Should show: Python 3.11.x or higher
```

#### 1.2 Node.js 18+
```bash
# Download from https://nodejs.org/
# OR use Chocolatey:
choco install nodejs

# Verify:
node --version
npm --version
# Should show: v18.x or higher
```

#### 1.3 Git
```bash
choco install git
# Verify:
git --version
```

#### 1.4 FFmpeg
```bash
choco install ffmpeg

# Verify:
ffmpeg -version
```

#### 1.5 Docker Desktop (Optional but recommended)
```bash
# Download from https://www.docker.com/products/docker-desktop
# Install and start Docker Desktop

# Verify:
docker --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/ap00rvc0des/youtube-ai-automation.git
cd youtube-ai-automation
```

### Step 3: Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### Step 4: Install Python Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# This may take 5-10 minutes
```

### Step 5: Install Node.js Dependencies

```bash
cd frontend
npm install
cd ..

# This may take 3-5 minutes
```

### Step 6: Set Up Environment Configuration

```bash
# Copy the example file
copy .env.example .env

# Edit .env with your settings (optional for basic usage)
notep .env  # Open in Notepad, or use your favorite editor
```

### Step 7: Create Necessary Directories

```bash
mkdir storage\videos
mkdir storage\thumbnails
mkdir temp
mkdir logs
```

### Step 8: Install Ollama

1. Download from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Open PowerShell and run:

```bash
# Pull a model
ollama pull mistral

# Or other models:
ollama pull neural-chat  # Faster, smaller
ollama pull llama2       # Larger, better quality
```

### Step 9: Start Ollama Service

```bash
# In PowerShell:
ollama serve

# Keep this terminal open
# Ollama will run on http://localhost:11434
```

### Step 10: Start Backend (New PowerShell)

```bash
# Navigate to project directory
cd youtube-ai-automation

# Activate virtual environment
venv\Scripts\activate

# Start backend
python backend\app.py

# You should see: "Running on http://0.0.0.0:5000"
```

### Step 11: Start Frontend (New PowerShell)

```bash
# Navigate to project directory
cd youtube-ai-automation\frontend

# Start frontend dev server
npm run dev

# You should see: "Local: http://localhost:3000"
```

### Step 12: Access Application

Open browser and go to: **http://localhost:3000**

---

## macOS Installation

### Step 1: Install Prerequisites Using Homebrew

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.11
brew install node
brew install git
brew install ffmpeg

# Verify installations
python3 --version
node --version
ffmpeg -version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/ap00rvc0des/youtube-ai-automation.git
cd youtube-ai-automation
```

### Step 3: Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Python
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Node.js
cd frontend
npm install
cd ..
```

### Step 5: Configure Environment

```bash
cp .env.example .env
# Edit with your preferred editor:
nano .env
```

### Step 6: Create Directories

```bash
mkdir -p storage/videos
mkdir -p storage/thumbnails
mkdir -p temp
mkdir -p logs
```

### Step 7: Install Ollama

```bash
# Download from ollama.ai or use Homebrew
brew install --cask ollama

# Start it
ollama serve

# In another terminal, pull a model:
ollama pull mistral
```

### Step 8: Start Services

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - Backend:**
```bash
cd youtube-ai-automation
source venv/bin/activate
python backend/app.py
```

**Terminal 3 - Frontend:**
```bash
cd youtube-ai-automation/frontend
npm run dev
```

### Step 9: Access Application

Open browser: **http://localhost:3000**

---

## Linux Installation

### Step 1: Install Prerequisites (Ubuntu/Debian)

```bash
# Update package manager
sudo apt-get update
sudo apt-get upgrade

# Install dependencies
sudo apt-get install -y python3.11 python3.11-venv python3-pip
sudo apt-get install -y nodejs npm
sudo apt-get install -y git
sudo apt-get install -y ffmpeg
sudo apt-get install -y libsndfile1 libsndfile1-dev

# Verify
python3 --version
node --version
ffmpeg -version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/ap00rvc0des/youtube-ai-automation.git
cd youtube-ai-automation
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

cd frontend
npm install
cd ..
```

### Step 5: Configure Environment

```bash
cp .env.example .env
nano .env  # Edit as needed
```

### Step 6: Create Directories

```bash
mkdir -p storage/videos
mkdir -p storage/thumbnails
mkdir -p temp
mkdir -p logs
chmod -R 755 storage temp logs
```

### Step 7: Install Ollama

```bash
# Download and install
curl https://ollama.ai/install.sh | sh

# Start service
sudo systemctl start ollama

# Pull a model
ollama pull mistral
```

### Step 8: Run Setup Script (Optional)

```bash
chmod +x scripts/setup.sh
bash scripts/setup.sh
```

### Step 9: Start Services

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - Backend:**
```bash
cd youtube-ai-automation
source venv/bin/activate
python backend/app.py
```

**Terminal 3 - Frontend:**
```bash
cd youtube-ai-automation/frontend
npm run dev
```

### Step 10: Access Application

Open browser: **http://localhost:3000**

---

## Docker Installation (Recommended for Quick Setup)

```bash
# Clone repository
git clone https://github.com/ap00rvc0des/youtube-ai-automation.git
cd youtube-ai-automation

# Copy environment file
cp .env.example .env

# Start all services with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Accessing Application with Docker

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Ollama**: http://localhost:11434
- **Piper TTS**: http://localhost:8000

---

## Verification

### Check All Services

```bash
# Test Backend
curl http://localhost:5000/health
# Should return: {"status":"healthy",...}

# Test Frontend (open in browser)
http://localhost:3000
# Should show dashboard

# Test Ollama
curl http://localhost:11434/api/tags
# Should return list of models

# Test Piper TTS
curl http://localhost:8000/
# Should return 200 OK
```

### Generate Test Video

1. Open http://localhost:3000
2. Click "Generate Video"
3. Enter:
   - Topic: "The Future of AI"
   - Niche: "Artificial Intelligence"
   - Language: "English"
   - Video Length: "Medium (5-7 min)"
4. Click "Generate Video"
5. Wait for completion (5-15 minutes)
6. Video should appear in "History" tab

---

## Troubleshooting

### "Python not found"

```bash
# Windows - Add Python to PATH
# 1. Open Environment Variables (search in Start menu)
# 2. Edit System environment variables
# 3. Add Python installation path to PATH
# 4. Restart terminal/computer

# macOS/Linux
which python3
# Create alias if needed
alias python=python3
```

### "Ollama connection refused"

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# On macOS:
launchctl start com.ollama.Ollama
```

### "Port 5000 already in use"

```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process or change port in .env:
BACKEND_PORT=5001
```

### "Module not found" error

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### "npm: command not found"

```bash
# Install Node.js from https://nodejs.org/
# Or use package manager:
brew install node     # macOS
sudo apt install npm  # Linux
choco install nodejs  # Windows
```

### Out of Memory

```bash
# Use smaller LLM model
echo "OLLAMA_MODEL=neural-chat" >> .env

# Or reduce video quality
echo "VIDEO_OUTPUT_RESOLUTION=720p" >> .env
```

### Piper TTS "No module named piper"

```bash
# Install Piper TTS
pip install piper-tts

# Or download voice model
piper_download --voice en_US-lessac-medium

# Or use Docker (in docker-compose.yml)
```

---

## Next Steps

1. **Generate your first video** (see Verification section)
2. **Configure YouTube OAuth** (see README.md)
3. **Enable Auto-Scheduler** (see Settings in dashboard)
4. **Customize settings** in `.env` file
5. **Read full documentation** in README.md

---

## Need Help?

- **Issues**: https://github.com/ap00rvc0des/youtube-ai-automation/issues
- **Discussions**: https://github.com/ap00rvc0des/youtube-ai-automation/discussions
- **Documentation**: See README.md

---

**Made with ❤️ by YouTube AI Automation Team**
