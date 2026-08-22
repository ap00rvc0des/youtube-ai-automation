# 🎬 YouTube AI Automation System

**Production-ready AI YouTube video generation system** using free and open-source tools. Generate complete YouTube videos from topics with ZERO paid APIs or subscriptions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-green)](https://nodejs.org/)
![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-brightgreen)

## ✨ Features

### 🎯 Core Features (100% Free)

- ✅ **AI Script Generation** - Automatic engaging scripts using local Ollama (Mistral, Llama, Qwen)
- ✅ **Text-to-Speech** - High-quality voiceovers using Piper TTS
- ✅ **Video Editing** - Professional video creation with FFmpeg
- ✅ **Subtitle Generation** - Auto-generated SRT subtitles
- ✅ **Thumbnail Creation** - Beautiful YouTube thumbnails with Pillow
- ✅ **1080p Output** - YouTube-optimized video format
- ✅ **Metadata Generation** - Auto titles, descriptions, tags, hashtags
- ✅ **Local Scheduler** - Automated daily/weekly video generation

### 📦 Optional Features (Free APIs)

- 📸 **Stock Images** - Pexels & Pixabay API integration (free accounts)
- 📤 **YouTube Upload** - Official YouTube Data API integration
- 🎨 **AI Image Generation** - Stable Diffusion (local optional)

### 🚀 What You Can Generate

- **Interesting Facts** videos
- **History** documentaries  
- **Technology** explainers
- **AI & Machine Learning** tutorials
- **Science** educational content
- **Mystery** investigations
- **Gaming** reviews & tutorials
- **Automotive** content
- **Finance & Education** guides

---

## 📋 Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Troubleshooting](#troubleshooting)
8. [Free vs Optional Services](#free-vs-optional-services)
9. [Contributing](#contributing)
10. [License](#license)

---

## 📦 Requirements

### System Requirements

- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **RAM**: 8GB minimum (16GB recommended for Ollama)
- **Storage**: 20GB free (for models and generated videos)
- **GPU**: Optional (recommended for faster processing)

### Software Requirements

- **Python**: 3.11 or higher
- **Node.js**: 18 or higher  
- **FFmpeg**: Latest version
- **Ollama**: Latest version (for local LLM)
- **Piper TTS**: Docker or standalone
- **Git**: For cloning the repository

---

## 🚀 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/ap00rvc0des/youtube-ai-automation.git
cd youtube-ai-automation
```

### Step 2: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install Node.js Dependencies

```bash
cd frontend
npm install
cd ..
```

### Step 4: Install FFmpeg

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### Step 5: Install Ollama

1. Download from [ollama.ai](https://ollama.ai)
2. Install and start the service
3. Pull a model:

```bash
ollama pull mistral
# Or other models:
ollama pull llama2
ollama pull neural-chat
ollama pull qwen
```

4. Verify it's running:
```bash
curl http://localhost:11434/api/tags
```

### Step 6: Install Piper TTS (Docker)

```bash
# Using Docker (recommended)
docker run -d \
  --name piper-tts \
  -p 8000:8000 \
  rhasspy/piper:latest

# Verify it's running:
curl http://localhost:8000/
```

**Or install standalone:**
```bash
# On macOS/Linux:
pip install piper-tts

# Download voice model:
piper_download --voice en_US-lessac-medium
```

### Step 7: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings (optional API keys)
nano .env  # or use your favorite editor
```

---

## 🎯 Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app
```

### Manual Start (Development)

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
# Server running on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend running on http://localhost:3000
```

**Terminal 3 - Ensure Services are Running:**
```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Check Piper TTS
curl http://localhost:8000/
```

### Access the Application

Open your browser and navigate to: **http://localhost:3000**

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=5000
ENVIRONMENT=development

# Frontend
FRONTEND_PORT=3000

# LLM (Ollama)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral

# TTS (Piper)
PIPER_HOST=localhost
PIPER_PORT=8000

# Video Settings
VIDEO_OUTPUT_RESOLUTION=1080p
VIDEO_FPS=30
VIDEO_BITRATE=5000k

# Storage
STORAGE_PATH=./storage
TEMP_PATH=./temp

# Optional: YouTube OAuth (for uploads)
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_secret
YOUTUBE_REDIRECT_URI=http://localhost:3000/auth/youtube/callback

# Optional: Stock Image APIs
PEXELS_API_KEY=your_pexels_key
PIXABAY_API_KEY=your_pixabay_key
```

### LLM Model Selection

Edit `.env` to choose your LLM:

```bash
# Fast & lightweight (recommended)
OLLAMA_MODEL=neural-chat

# Balanced quality/speed
OLLAMA_MODEL=mistral

# Best quality (slower)
OLLAMA_MODEL=llama2

# Chinese language
OLLAMA_MODEL=qwen
```

---

## 📖 Usage

### Generate Your First Video

1. **Open Dashboard**: Go to http://localhost:3000
2. **Click "Generate Video"**
3. **Enter Details**:
   - Topic: "The Future of Artificial Intelligence"
   - Niche: "Artificial Intelligence"
   - Language: "English"
   - Video Length: "Medium (5-7 min)"
   - Voice: "Lessac (Male)"
4. **Click "Generate Video"**
5. **Wait** for the pipeline to complete:
   - Script generation (~30-60 seconds)
   - Voiceover synthesis (~60-120 seconds)
   - Video creation (~120-180 seconds)
   - Subtitle generation (~30 seconds)
   - Finalization (~30 seconds)

### View Generated Videos

1. **Go to "History"** tab
2. **Click on any video** to see details
3. **Download** the MP4 file
4. **Preview** before uploading to YouTube

### Upload to YouTube (Optional)

1. **Configure YouTube OAuth**:
   - Create OAuth credentials at [Google Cloud Console](https://console.cloud.google.com)
   - Add credentials to `.env`
   - Restart backend

2. **Authenticate**:
   - Click "Settings" → "YouTube Integration"
   - Click "Connect YouTube"
   - Authorize the app

3. **Upload Video**:
   - Go to History
   - Click video → "Upload to YouTube"
   - Fill in title, description, tags
   - Choose channel and privacy
   - Click "Upload"

### Schedule Automated Generation

1. **Go to Settings**
2. **Enable Scheduler**
3. **Set**:
   - Schedule time (e.g., 9:00 AM)
   - Frequency (Daily/Weekly/Monthly)
4. **Configure video topics** (upcoming feature)
5. **System will auto-generate** at scheduled times

---

## 📁 Project Structure

```
youtube-ai-automation/
├── backend/                    # Python Flask API
│   ├── app.py                 # Main application
│   ├── routes/                # API endpoints
│   │   ├── api.py            # Core API routes
│   │   ├── auth.py           # Authentication
│   │   ├── videos.py         # Video management
│   │   └── youtube.py        # YouTube integration
│   └── __init__.py
│
├── frontend/                   # React.js dashboard
│   ├── src/
│   │   ├── main.jsx          # React entry point
│   │   ├── App.jsx           # Main app component
│   │   ├── pages/            # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Generator.jsx
│   │   │   ├── History.jsx
│   │   │   └── Settings.jsx
│   │   ├── components/       # Reusable components
│   │   │   ├── Layout.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── ProgressBar.jsx
│   │   ├── services/         # API services
│   │   │   ├── api.js
│   │   │   ├── videoService.js
│   │   │   ├── authService.js
│   │   │   └── youtubeService.js
│   │   ├── store.js          # Zustand state management
│   │   ├── config.js         # Frontend configuration
│   │   └── index.css         # Global styles
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   └── index.html
│
├── ai/                         # AI/LLM module
│   ├── __init__.py
│   └── llm.py               # Ollama integration
│
├── tts/                        # Text-to-Speech module
│   ├── __init__.py
│   └── piper.py             # Piper TTS integration
│
├── video/                      # Video generation
│   ├── __init__.py
│   └── generator.py         # FFmpeg wrapper
│
├── thumbnails/                 # Thumbnail generation
│   ├── __init__.py
│   └── generator.py         # Pillow-based generator
│
├── youtube/                    # YouTube API
│   ├── __init__.py
│   └── client.py            # YouTube Data API
│
├── scheduler/                  # Task scheduling
│   ├── __init__.py
│   └── tasks.py             # APScheduler wrapper
│
├── storage/                    # Generated files
│   ├── videos/              # Output videos
│   └── thumbnails/          # Output thumbnails
│
├── temp/                       # Temporary files
├── logs/                       # Application logs
├── tests/                      # Unit & integration tests
├── scripts/                    # Utility scripts
│
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container definition
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── package.json               # Node.js dependencies
├── README.md                  # This file
└── LICENSE                    # MIT License
```

---

## 🔧 Troubleshooting

### Ollama Not Connecting

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it:
ollama serve

# Verify model is installed:
ollama list

# Pull a model if needed:
ollama pull mistral
```

### Piper TTS Not Working

```bash
# Check Piper health
curl http://localhost:8000/

# Check Docker container
docker ps | grep piper

# View container logs
docker logs piper-tts

# Restart container
docker restart piper-tts
```

### FFmpeg Errors

```bash
# Verify FFmpeg installation
ffmpeg -version

# Check for missing codecs (common issue):
ffmpeg -codecs | grep h264

# Reinstall if needed:
# Windows: choco install ffmpeg --force
# macOS: brew reinstall ffmpeg
# Linux: sudo apt-get install --reinstall ffmpeg
```

### Out of Disk Space

```bash
# Check disk usage
du -sh storage/
du -sh temp/

# Clear old temporary files
rm -rf temp/*

# Cleanup old videos (keep last 10):
ls -t storage/videos/ | tail -n +11 | xargs rm
```

### Backend Won't Start

```bash
# Check port availability
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill existing process and try again
# Or change port in .env: BACKEND_PORT=5001
```

### Memory Issues

```bash
# Monitor resource usage
top  # Linux
Activity Monitor  # macOS
Task Manager  # Windows

# Reduce Ollama model size:
OLLAMA_MODEL=neural-chat  # Smaller than mistral

# Limit concurrent operations in .env:
MAX_CONCURRENT_JOBS=1
```

### Video Quality Issues

```bash
# In .env, adjust video settings:
VIDEO_BITRATE=8000k      # Higher bitrate = better quality
VIDEO_FPS=60             # Higher FPS = smoother
VIDEO_OUTPUT_RESOLUTION=1440p  # Higher resolution
```

---

## 🆓 Free vs Optional Services

### ✅ Always Free (Included)

| Component | Tool | Cost | Notes |
|-----------|------|------|-------|
| **LLM** | Ollama (Mistral) | Free | Local, no API calls |
| **TTS** | Piper | Free | Local, high quality |
| **Video Editing** | FFmpeg | Free | Open source |
| **Image Creation** | Pillow | Free | Python library |
| **Scheduling** | APScheduler | Free | Local task scheduler |
| **Database** | SQLite | Free | Built-in |

### 🆓 Optional Free Services (No API calls without keys)

| Service | Purpose | API Key | Limit | Cost |
|---------|---------|---------|-------|------|
| **Pexels** | Stock images | Free | 200/hour | Free |
| **Pixabay** | Stock images | Free | 50/hour | Free |
| **YouTube Data API** | Video upload | Free | 10k quota | Free |

### ❌ NOT Included (Never Required)

- OpenAI API ❌
- Paid AI services ❌
- Premium TTS ❌
- Video editing software ❌
- Paid stock image services ❌

---

## 🔄 API Endpoints

### Core API

```
GET  /api/status              - System status
GET  /api/niches              - Available niches
GET  /api/config              - Configuration info
```

### Video Generation

```
POST /videos/generate         - Start video generation
GET  /videos/status/<id>      - Get generation progress
GET  /videos/list             - List all videos
GET  /videos/<id>             - Get video details
GET  /videos/<id>/download    - Download video file
DEL  /videos/<id>             - Delete video
```

### Authentication

```
GET  /auth/status             - Check auth status
GET  /auth/youtube/login      - Initiate YouTube OAuth
GET  /auth/youtube/callback   - OAuth callback
POST /auth/logout             - Logout
```

### YouTube

```
GET  /youtube/channels        - Get user channels
POST /youtube/upload          - Upload video
POST /youtube/schedule        - Schedule upload
```

---

## 📝 Sample API Usage

### Generate Video

```bash
curl -X POST http://localhost:5000/videos/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of AI",
    "niche": "Artificial Intelligence",
    "language": "English",
    "video_length": 420
  }'
```

### Check Status

```bash
curl http://localhost:5000/videos/status/video_20240822_101234
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_llm.py

# Frontend tests
cd frontend && npm run test
```

---

## 📦 Performance Tips

1. **Use smaller LLM models** for faster generation
   ```bash
   OLLAMA_MODEL=neural-chat  # ~4s per response
   ```

2. **Enable GPU acceleration** for Ollama
   ```bash
   export CUDA_VISIBLE_DEVICES=0
   ollama serve
   ```

3. **Reduce video resolution** for testing
   ```bash
   VIDEO_OUTPUT_RESOLUTION=720p
   ```

4. **Use SSD** for storage instead of HDD

5. **Allocate 16GB+ RAM** to system for optimal performance

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install black flake8 pylint

# Format code
black backend/

# Lint code
flake8 backend/
pylint backend/
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Local LLM framework
- [Piper TTS](https://github.com/rhasspy/piper) - Text-to-speech
- [FFmpeg](https://ffmpeg.org) - Video processing
- [Flask](https://flask.palletsprojects.com) - Python web framework
- [React](https://react.dev) - Frontend framework
- [Pillow](https://python-pillow.org) - Image processing

---

## ⭐ Star This Repository

If you find this project useful, please consider giving it a star! It helps others discover it.

---

## 📧 Support

For issues and questions:
- **GitHub Issues**: [Open an issue](https://github.com/ap00rvc0des/youtube-ai-automation/issues)
- **Discussions**: [Start a discussion](https://github.com/ap00rvc0des/youtube-ai-automation/discussions)

---

## 🗺️ Roadmap

- [ ] WebSocket support for real-time progress updates
- [ ] Batch video generation
- [ ] Advanced image generation integration
- [ ] Multi-language subtitle support
- [ ] Video optimization for different platforms (TikTok, Instagram)
- [ ] Advanced analytics and performance metrics
- [ ] Mobile app (React Native)
- [ ] Cloud deployment guides (AWS, Azure, GCP)
- [ ] Webhook support for external integrations
- [ ] REST API documentation (Swagger/OpenAPI)

---

**Made with ❤️ by the YouTube AI Automation team**
