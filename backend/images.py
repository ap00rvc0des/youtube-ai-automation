#!/usr/bin/env python3
"""
Image retrieval from stock image APIs
"""

import os
import logging
import requests
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class ImageProvider:
    """Fetch images from free stock image APIs"""
    
    def __init__(self):
        self.storage_path = os.getenv('STORAGE_PATH', './storage')
        self.images_dir = os.path.join(self.storage_path, 'images')
        os.makedirs(self.images_dir, exist_ok=True)
    
    def search_pexels(self, query: str, count: int = 3) -> List[str]:
        """
        Search and download images from Pexels API
        
        Args:
            query: Search query
            count: Number of images to retrieve
        
        Returns:
            List of downloaded image paths
        """
        api_key = os.getenv('PEXELS_API_KEY')
        if not api_key:
            logger.warning("Pexels API key not configured")
            return []
        
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {"Authorization": api_key}
            params = {"query": query, "per_page": count}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for photo in data.get('photos', [])[:count]:
                img_url = photo['src']['large']
                img_response = requests.get(img_url, timeout=10)
                img_response.raise_for_status()
                
                # Save image
                filename = f"pexels_{photo['id']}.jpg"
                filepath = os.path.join(self.images_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                images.append(filepath)
                logger.info(f"Downloaded from Pexels: {filename}")
            
            return images
        
        except Exception as e:
            logger.error(f"Pexels search failed: {e}")
            return []
    
    def search_pixabay(self, query: str, count: int = 3) -> List[str]:
        """
        Search and download images from Pixabay API
        
        Args:
            query: Search query
            count: Number of images to retrieve
        
        Returns:
            List of downloaded image paths
        """
        api_key = os.getenv('PIXABAY_API_KEY')
        if not api_key:
            logger.warning("Pixabay API key not configured")
            return []
        
        try:
            url = "https://pixabay.com/api/"
            params = {
                "key": api_key,
                "q": query,
                "per_page": count,
                "image_type": "photo",
                "min_width": 1920,
                "min_height": 1080
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for hit in data.get('hits', [])[:count]:
                img_url = hit['largeImageURL']
                img_response = requests.get(img_url, timeout=10)
                img_response.raise_for_status()
                
                # Save image
                filename = f"pixabay_{hit['id']}.jpg"
                filepath = os.path.join(self.images_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                images.append(filepath)
                logger.info(f"Downloaded from Pixabay: {filename}")
            
            return images
        
        except Exception as e:
            logger.error(f"Pixabay search failed: {e}")
            return []
    
    def search(self, query: str, source: str = 'all', count: int = 3) -> List[str]:
        """
        Search images from multiple sources
        
        Args:
            query: Search query
            source: 'pexels', 'pixabay', or 'all'
            count: Number of images per source
        
        Returns:
            List of downloaded image paths
        """
        images = []
        
        if source in ['pexels', 'all']:
            images.extend(self.search_pexels(query, count))
        
        if source in ['pixabay', 'all']:
            images.extend(self.search_pixabay(query, count))
        
        return images
