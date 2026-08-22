#!/usr/bin/env python3
"""
Video metadata management
"""

import os
import json
import logging
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class VideoMetadata:
    """Manage video metadata"""
    
    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or os.getenv('STORAGE_PATH', './storage')
        self.metadata_dir = os.path.join(self.storage_path, 'metadata')
        os.makedirs(self.metadata_dir, exist_ok=True)
    
    def save(
        self,
        video_id: str,
        title: str,
        description: str,
        tags: List[str],
        topic: str,
        niche: str,
        language: str,
        duration: int,
        thumbnail_path: str = None,
        video_path: str = None
    ) -> bool:
        """
        Save video metadata
        
        Args:
            video_id: Unique video identifier
            title: Video title
            description: Video description
            tags: List of tags
            topic: Video topic
            niche: Video niche
            language: Video language
            duration: Duration in seconds
            thumbnail_path: Path to thumbnail
            video_path: Path to video file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            metadata = {
                'video_id': video_id,
                'title': title,
                'description': description,
                'tags': tags,
                'topic': topic,
                'niche': niche,
                'language': language,
                'duration': duration,
                'thumbnail': thumbnail_path,
                'video_file': video_path,
                'created_at': datetime.now().isoformat(),
                'status': 'generated'
            }
            
            metadata_file = os.path.join(self.metadata_dir, f"{video_id}.json")
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Metadata saved for {video_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
            return False
    
    def load(self, video_id: str) -> Optional[Dict]:
        """
        Load video metadata
        
        Args:
            video_id: Video identifier
        
        Returns:
            Metadata dictionary or None
        """
        try:
            metadata_file = os.path.join(self.metadata_dir, f"{video_id}.json")
            
            if not os.path.exists(metadata_file):
                return None
            
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")
            return None
    
    def update(self, video_id: str, updates: Dict) -> bool:
        """
        Update video metadata
        
        Args:
            video_id: Video identifier
            updates: Dictionary with fields to update
        
        Returns:
            True if successful, False otherwise
        """
        try:
            metadata = self.load(video_id)
            if not metadata:
                return False
            
            metadata.update(updates)
            metadata['updated_at'] = datetime.now().isoformat()
            
            metadata_file = os.path.join(self.metadata_dir, f"{video_id}.json")
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Metadata updated for {video_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to update metadata: {e}")
            return False
    
    def list_all(self) -> List[Dict]:
        """
        List all video metadata
        
        Returns:
            List of metadata dictionaries
        """
        try:
            metadata_list = []
            
            if not os.path.exists(self.metadata_dir):
                return metadata_list
            
            for filename in os.listdir(self.metadata_dir):
                if filename.endswith('.json'):
                    video_id = filename.replace('.json', '')
                    metadata = self.load(video_id)
                    if metadata:
                        metadata_list.append(metadata)
            
            # Sort by creation date (newest first)
            metadata_list.sort(
                key=lambda x: x.get('created_at', ''),
                reverse=True
            )
            
            return metadata_list
        
        except Exception as e:
            logger.error(f"Failed to list metadata: {e}")
            return []
