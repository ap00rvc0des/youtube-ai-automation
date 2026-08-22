#!/usr/bin/env python3
"""
Test suite for YouTube AI Automation System
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from ai.llm import OllamaLLM
from tts.piper import PiperTTS
from video.generator import VideoGenerator
from thumbnails.generator import ThumbnailGenerator


class TestFlaskApp:
    """Test Flask application"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'name' in response.json
    
    def test_niches_endpoint(self, client):
        """Test niches endpoint"""
        response = client.get('/api/niches')
        assert response.status_code == 200
        assert 'niches' in response.json
        assert len(response.json['niches']) > 0


class TestOllamaLLM:
    """Test Ollama LLM integration"""
    
    def test_llm_initialization(self):
        """Test LLM initialization"""
        llm = OllamaLLM()
        assert llm.model is not None
        assert llm.host is not None
    
    def test_llm_availability(self):
        """Test if Ollama is available"""
        llm = OllamaLLM()
        # This test will pass/fail based on Ollama availability
        available = llm.is_available()
        # Don't assert - just log availability
        print(f"Ollama availability: {available}")


class TestPiperTTS:
    """Test Piper TTS integration"""
    
    def test_tts_initialization(self):
        """Test TTS initialization"""
        tts = PiperTTS()
        assert tts.base_url is not None
    
    def test_tts_availability(self):
        """Test if Piper is available"""
        tts = PiperTTS()
        available = tts.is_available()
        # Don't assert - just log availability
        print(f"Piper TTS availability: {available}")


class TestVideoGenerator:
    """Test Video generation"""
    
    def test_ffmpeg_check(self):
        """Test FFmpeg availability"""
        generator = VideoGenerator()
        # FFmpeg check is done in __init__
        assert generator is not None


class TestThumbnailGenerator:
    """Test Thumbnail generation"""
    
    def test_thumbnail_size(self):
        """Test thumbnail size"""
        generator = ThumbnailGenerator()
        assert generator.width == 1280
        assert generator.height == 720


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
