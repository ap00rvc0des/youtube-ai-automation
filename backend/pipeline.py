#!/usr/bin/env python3
"""
Main video generation pipeline orchestrator
"""

import os
import logging
from typing import Optional, Dict
from pathlib import Path
import uuid
from datetime import datetime

from ai.llm import OllamaLLM
from tts.piper import PiperTTS
from video.generator import VideoGenerator
from thumbnails.generator import ThumbnailGenerator

logger = logging.getLogger(__name__)

class VideoPipeline:
    """Complete video generation pipeline"""
    
    def __init__(self):
        self.llm = OllamaLLM()
        self.tts = PiperTTS()
        self.video_gen = VideoGenerator()
        self.thumbnail_gen = ThumbnailGenerator()
        self.storage_path = os.getenv('STORAGE_PATH', './storage')
        self.temp_path = os.getenv('TEMP_PATH', './temp')
    
    def generate(
        self,
        topic: str,
        niche: str,
        language: str = 'English',
        video_length: int = 420,
        voice: str = 'en_US-lessac-medium',
        progress_callback=None
    ) -> Optional[Dict]:
        """
        Complete video generation pipeline
        
        Args:
            topic: Video topic
            niche: Video niche/category
            language: Script language
            video_length: Target video length in seconds
            voice: TTS voice model
            progress_callback: Function to call for progress updates
        
        Returns:
            Dictionary with video info or None if failed
        """
        video_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        try:
            # Step 1: Generate Script
            self._update_progress(progress_callback, 5, "Generating Script")
            logger.info(f"[{video_id}] Generating script for topic: {topic}")
            
            script = self.llm.generate_script(topic, niche, language)
            if not script:
                logger.error(f"[{video_id}] Script generation failed")
                return None
            
            logger.info(f"[{video_id}] Script generated ({len(script)} chars)")
            script_file = self._save_script(video_id, script)
            
            # Step 2: Generate Metadata
            self._update_progress(progress_callback, 15, "Generating Metadata")
            logger.info(f"[{video_id}] Generating title and description")
            
            title = self.llm.generate_title(topic) or f"{topic} - {niche}"
            description = self.llm.generate_description(topic, [niche]) or f"Learn about {topic}"
            
            logger.info(f"[{video_id}] Metadata generated")
            
            # Step 3: Generate Voiceover
            self._update_progress(progress_callback, 30, "Creating Voiceover")
            logger.info(f"[{video_id}] Generating voiceover")
            
            audio_file = self.tts.synthesize(
                script,
                voice=voice,
                output_file=os.path.join(self.temp_path, f"{video_id}_audio.wav")
            )
            
            if not audio_file:
                logger.error(f"[{video_id}] Voiceover generation failed")
                return None
            
            logger.info(f"[{video_id}] Voiceover generated")
            
            # Step 4: Create Base Video
            self._update_progress(progress_callback, 50, "Creating Video")
            logger.info(f"[{video_id}] Creating base video")
            
            resolution = os.getenv('VIDEO_OUTPUT_RESOLUTION', '1080p')
            fps = int(os.getenv('VIDEO_FPS', 30))
            
            base_video = self.video_gen.create_video(
                output_path=os.path.join(self.temp_path, f"{video_id}_base.mp4"),
                resolution=resolution,
                fps=fps,
                duration=video_length
            )
            
            if not base_video:
                logger.error(f"[{video_id}] Base video creation failed")
                return None
            
            logger.info(f"[{video_id}] Base video created")
            
            # Step 5: Merge Audio
            self._update_progress(progress_callback, 65, "Merging Audio")
            logger.info(f"[{video_id}] Merging audio with video")
            
            video_with_audio = self.video_gen.merge_audio(
                video_path=base_video,
                audio_path=audio_file,
                output_path=os.path.join(self.temp_path, f"{video_id}_with_audio.mp4")
            )
            
            if not video_with_audio:
                logger.error(f"[{video_id}] Audio merge failed")
                return None
            
            logger.info(f"[{video_id}] Audio merged")
            
            # Step 6: Generate Subtitles
            self._update_progress(progress_callback, 75, "Generating Subtitles")
            logger.info(f"[{video_id}] Generating subtitles")
            
            subtitle_file = self._generate_subtitles(video_id, script)
            
            # Step 7: Add Subtitles to Video
            if subtitle_file:
                self._update_progress(progress_callback, 85, "Adding Subtitles")
                logger.info(f"[{video_id}] Adding subtitles to video")
                
                final_video = self.video_gen.add_subtitles(
                    video_path=video_with_audio,
                    subtitle_path=subtitle_file,
                    output_path=os.path.join(self.storage_path, 'videos', f"{video_id}.mp4")
                )
            else:
                # Skip subtitles if generation failed
                final_video = video_with_audio
                final_video_path = os.path.join(self.storage_path, 'videos', f"{video_id}.mp4")
                if video_with_audio != final_video_path:
                    import shutil
                    shutil.copy(video_with_audio, final_video_path)
                final_video = final_video_path
            
            # Step 8: Generate Thumbnail
            self._update_progress(progress_callback, 90, "Creating Thumbnail")
            logger.info(f"[{video_id}] Generating thumbnail")
            
            thumbnail_file = self.thumbnail_gen.create_thumbnail(
                title=title,
                output_path=os.path.join(self.storage_path, 'thumbnails', f"{video_id}.png")
            )
            
            logger.info(f"[{video_id}] Thumbnail generated")
            
            # Step 9: Finalize
            self._update_progress(progress_callback, 95, "Finalizing")
            logger.info(f"[{video_id}] Finalizing video")
            
            self._cleanup_temp_files(video_id)
            
            # Step 10: Complete
            self._update_progress(progress_callback, 100, "Complete")
            
            result = {
                'video_id': video_id,
                'title': title,
                'description': description,
                'topic': topic,
                'niche': niche,
                'language': language,
                'video_file': final_video,
                'thumbnail_file': thumbnail_file,
                'script_file': script_file,
                'subtitle_file': subtitle_file,
                'status': 'completed',
                'created_at': datetime.now().isoformat(),
                'duration': video_length
            }
            
            logger.info(f"[{video_id}] Pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"[{video_id}] Pipeline failed: {e}", exc_info=True)
            self._cleanup_temp_files(video_id)
            return None
    
    def _save_script(self, video_id: str, script: str) -> str:
        """Save script to file"""
        script_path = os.path.join(self.storage_path, f"{video_id}_script.txt")
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script)
            logger.info(f"Script saved: {script_path}")
            return script_path
        except Exception as e:
            logger.error(f"Failed to save script: {e}")
            return None
    
    def _generate_subtitles(self, video_id: str, text: str) -> Optional[str]:
        """
        Generate SRT subtitle file from text
        
        This is a simplified implementation that creates basic subtitles.
        For production, use speech-to-text or more advanced methods.
        """
        try:
            srt_path = os.path.join(self.storage_path, f"{video_id}.srt")
            
            # Split text into chunks
            sentences = text.split('. ')
            
            srt_content = ""
            start_time = 0
            chunk_duration = 3  # seconds per chunk
            
            for i, sentence in enumerate(sentences, 1):
                if not sentence.strip():
                    continue
                
                end_time = start_time + chunk_duration
                
                # Format: HH:MM:SS,mmm --> HH:MM:SS,mmm
                start_str = self._seconds_to_srt_time(start_time)
                end_str = self._seconds_to_srt_time(end_time)
                
                srt_content += f"{i}\n"
                srt_content += f"{start_str} --> {end_str}\n"
                srt_content += f"{sentence.strip()}.\n\n"
                
                start_time = end_time
            
            with open(srt_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            logger.info(f"Subtitles generated: {srt_path}")
            return srt_path
            
        except Exception as e:
            logger.error(f"Failed to generate subtitles: {e}")
            return None
    
    @staticmethod
    def _seconds_to_srt_time(seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _cleanup_temp_files(self, video_id: str):
        """Clean up temporary files"""
        try:
            import glob
            temp_files = glob.glob(os.path.join(self.temp_path, f"{video_id}*"))
            for file in temp_files:
                try:
                    os.remove(file)
                    logger.debug(f"Removed temp file: {file}")
                except Exception as e:
                    logger.warning(f"Failed to remove temp file {file}: {e}")
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")
    
    @staticmethod
    def _update_progress(callback, progress: int, step: str):
        """Update progress via callback"""
        if callback:
            try:
                callback(progress=progress, step=step)
            except Exception as e:
                logger.error(f"Progress callback error: {e}")
