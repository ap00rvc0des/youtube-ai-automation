#!/usr/bin/env python3
"""
Video generation pipeline
"""

import os
import logging
import subprocess
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class VideoGenerator:
    """Video generation using FFmpeg"""
    
    def __init__(self):
        self.ffmpeg_bin = 'ffmpeg'
        self.ffprobe_bin = 'ffprobe'
        self.check_ffmpeg()
    
    def check_ffmpeg(self) -> bool:
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(
                [self.ffmpeg_bin, '-version'],
                capture_output=True,
                check=True,
                timeout=5
            )
            logger.info("FFmpeg is available")
            return True
        except Exception as e:
            logger.error(f"FFmpeg not found: {e}")
            return False
    
    def create_video(
        self,
        output_path: str,
        resolution: str = '1080p',
        fps: int = 30,
        duration: int = 600,
        background: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a base video file
        
        Args:
            output_path: Output video file path
            resolution: Video resolution (1080p, 720p, etc.)
            fps: Frames per second
            duration: Video duration in seconds
            background: Background image or color
        
        Returns:
            Path to generated video or None if failed
        """
        # Parse resolution
        res_map = {
            '1080p': '1920x1080',
            '720p': '1280x720',
            '480p': '854x480'
        }
        dimensions = res_map.get(resolution, '1920x1080')
        width, height = dimensions.split('x')
        
        try:
            # Create a solid color video as base
            cmd = [
                self.ffmpeg_bin,
                '-f', 'lavfi',
                '-i', f'color=c=black:s={dimensions}:d={duration}',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-y',
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                logger.info(f"Video created: {output_path}")
                return output_path
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return None
        
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            return None
    
    def merge_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str
    ) -> Optional[str]:
        """
        Merge audio with video
        
        Args:
            video_path: Video file path
            audio_path: Audio file path
            output_path: Output video file path
        
        Returns:
            Path to merged video or None if failed
        """
        try:
            cmd = [
                self.ffmpeg_bin,
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                logger.info(f"Audio merged: {output_path}")
                return output_path
            else:
                logger.error(f"FFmpeg merge error: {result.stderr}")
                return None
        
        except Exception as e:
            logger.error(f"Error merging audio: {e}")
            return None
    
    def add_subtitles(
        self,
        video_path: str,
        subtitle_path: str,
        output_path: str
    ) -> Optional[str]:
        """
        Add subtitles to video
        
        Args:
            video_path: Video file path
            subtitle_path: SRT subtitle file path
            output_path: Output video file path
        
        Returns:
            Path to video with subtitles or None if failed
        """
        try:
            # Escape subtitle path for FFmpeg
            subtitle_filter = f"subtitles={subtitle_path.replace(os.sep, '/')}"
            
            cmd = [
                self.ffmpeg_bin,
                '-i', video_path,
                '-vf', subtitle_filter,
                '-c:a', 'copy',
                '-y',
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                logger.info(f"Subtitles added: {output_path}")
                return output_path
            else:
                logger.error(f"FFmpeg subtitle error: {result.stderr}")
                return None
        
        except Exception as e:
            logger.error(f"Error adding subtitles: {e}")
            return None
