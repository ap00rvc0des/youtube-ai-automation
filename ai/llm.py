#!/usr/bin/env python3
"""
Large Language Model integration via Ollama
"""

import os
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class OllamaLLM:
    """Ollama LLM wrapper for script generation"""
    
    def __init__(self, host: str = None, model: str = None):
        self.host = host or os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.model = model or os.getenv('OLLAMA_MODEL', 'mistral')
        self.endpoint = f"{self.host}/api/generate"
    
    def is_available(self) -> bool:
        """Check if Ollama service is available"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama unavailable: {e}")
            return False
    
    def generate_script(self, topic: str, niche: str, language: str = 'English') -> Optional[str]:
        """
        Generate a YouTube video script using the LLM
        
        Args:
            topic: Video topic
            niche: Video niche/category
            language: Script language
        
        Returns:
            Generated script or None if failed
        """
        prompt = self._build_script_prompt(topic, niche, language)
        
        try:
            response = requests.post(
                self.endpoint,
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'stream': False,
                    'temperature': 0.7
                },
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logger.error(f"LLM generation failed: {response.status_code}")
                return None
        
        except Exception as e:
            logger.error(f"Error generating script: {e}")
            return None
    
    def _build_script_prompt(self, topic: str, niche: str, language: str) -> str:
        """Build the prompt for script generation"""
        return f"""Generate a professional YouTube video script in {language} for a {niche} video about: {topic}

The script should include:
1. A compelling hook (first 3 seconds)
2. Introduction (who you are, what they'll learn)
3. Main content (3-5 key points with interesting facts)
4. Conclusion (summarize key takeaways)
5. Call to action (subscribe, like, comment)

Format:
[HOOK]
[Your hook here]

[INTRO]
[Your introduction]

[MAIN CONTENT]
[Your main points]

[CONCLUSION]
[Your conclusion]

[CTA]
[Your call to action]

Make it engaging, informative, and suitable for a 5-10 minute video."""
    
    def generate_title(self, topic: str) -> Optional[str]:
        """Generate a catchy YouTube title"""
        prompt = f"Generate a single compelling YouTube video title (under 60 characters) for: {topic}"
        
        try:
            response = requests.post(
                self.endpoint,
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'stream': False,
                    'temperature': 0.9
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
        except Exception as e:
            logger.error(f"Error generating title: {e}")
        
        return None
    
    def generate_description(self, topic: str, tags: list) -> Optional[str]:
        """Generate YouTube video description"""
        tags_str = ', '.join(tags)
        prompt = f"""Generate a YouTube video description for: {topic}
Tags: {tags_str}

Include:
- Hook/summary
- Key points
- Call to action
- Timestamps (estimated)

Keep it under 5000 characters."""
        
        try:
            response = requests.post(
                self.endpoint,
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'stream': False,
                    'temperature': 0.7
                },
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
        except Exception as e:
            logger.error(f"Error generating description: {e}")
        
        return None
