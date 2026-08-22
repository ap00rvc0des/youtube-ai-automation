#!/usr/bin/env python3
"""
Subtitle generation and management
"""

import os
import logging
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)

class SubtitleGenerator:
    """Generate subtitles from text or audio"""
    
    def __init__(self):
        self.storage_path = os.getenv('STORAGE_PATH', './storage')
    
    def text_to_srt(
        self,
        text: str,
        output_file: str,
        words_per_subtitle: int = 10,
        seconds_per_subtitle: float = 3.0
    ) -> Optional[str]:
        """
        Convert text to SRT format
        
        Args:
            text: Script text
            output_file: Output SRT file path
            words_per_subtitle: Words per subtitle chunk
            seconds_per_subtitle: Duration of each subtitle
        
        Returns:
            Path to generated SRT file or None
        """
        try:
            words = text.split()
            subtitles = []
            
            # Create subtitle chunks
            for i in range(0, len(words), words_per_subtitle):
                chunk = ' '.join(words[i:i + words_per_subtitle])
                
                start_time = i / words_per_subtitle * seconds_per_subtitle
                end_time = (i + words_per_subtitle) / words_per_subtitle * seconds_per_subtitle
                
                subtitle = {
                    'index': len(subtitles) + 1,
                    'start': start_time,
                    'end': end_time,
                    'text': chunk
                }
                subtitles.append(subtitle)
            
            # Write SRT file
            srt_content = self._generate_srt_content(subtitles)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            logger.info(f"SRT file created: {output_file}")
            return output_file
        
        except Exception as e:
            logger.error(f"Error creating SRT: {e}")
            return None
    
    @staticmethod
    def _generate_srt_content(subtitles: List[dict]) -> str:
        """Generate SRT file content"""
        content = ""
        for sub in subtitles:
            start_str = SubtitleGenerator._seconds_to_srt_time(sub['start'])
            end_str = SubtitleGenerator._seconds_to_srt_time(sub['end'])
            
            content += f"{sub['index']}\n"
            content += f"{start_str} --> {end_str}\n"
            content += f"{sub['text']}\n\n"
        
        return content
    
    @staticmethod
    def _seconds_to_srt_time(seconds: float) -> str:
        """Convert seconds to SRT time format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
