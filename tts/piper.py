#!/usr/bin/env python3
"""
Piper Text-to-Speech integration
"""

import os
import requests
import logging
from typing import Optional
import tempfile

logger = logging.getLogger(__name__)

class PiperTTS:
    """Piper TTS wrapper for voiceover generation"""
    
    def __init__(self, host: str = None, port: int = None):
        self.host = host or os.getenv('PIPER_HOST', 'localhost')
        self.port = port or int(os.getenv('PIPER_PORT', 8000))
        self.base_url = f"http://{self.host}:{self.port}"
    
    def is_available(self) -> bool:
        """Check if Piper service is available"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Piper unavailable: {e}")
            return False
    
    def get_voices(self) -> dict:
        """Get available voices"""
        try:
            response = requests.get(f"{self.base_url}/voices", timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            logger.error(f"Error fetching voices: {e}")
            return {}
    
    def synthesize(
        self,
        text: str,
        voice: str = 'en_US-lessac-medium',
        output_file: str = None,
        speed: float = 1.0,
        language: str = 'en_US'
    ) -> Optional[str]:
        """
        Synthesize text to speech
        
        Args:
            text: Text to synthesize
            voice: Voice model to use
            output_file: Output audio file path
            speed: Speech speed (0.5-2.0)
            language: Language code
        
        Returns:
            Path to generated audio file or None if failed
        """
        if not text or not text.strip():
            logger.error("Empty text provided for synthesis")
            return None
        
        if output_file is None:
            output_file = os.path.join(tempfile.gettempdir(), f"tts_{os.urandom(8).hex()}.wav")
        
        try:
            payload = {
                'text': text,
                'voice': voice,
                'lengthScale': speed
            }
            
            response = requests.post(
                f"{self.base_url}/api/tts",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Audio synthesized: {output_file}")
                return output_file
            else:
                logger.error(f"TTS synthesis failed: {response.status_code}")
                return None
        
        except Exception as e:
            logger.error(f"Error synthesizing audio: {e}")
            return None
