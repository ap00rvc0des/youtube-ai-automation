#!/usr/bin/env python3
"""
Thumbnail generation for YouTube videos
"""

import os
import logging
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class ThumbnailGenerator:
    """YouTube thumbnail generator"""
    
    STANDARD_SIZE = (1280, 720)  # YouTube standard
    
    def __init__(self):
        self.width, self.height = self.STANDARD_SIZE
    
    def create_thumbnail(
        self,
        title: str,
        output_path: str,
        background_color: Tuple[int, int, int] = (255, 0, 0),
        text_color: Tuple[int, int, int] = (255, 255, 255)
    ) -> Optional[str]:
        """
        Create a basic thumbnail with title text
        
        Args:
            title: Video title to display
            output_path: Output image file path
            background_color: RGB background color
            text_color: RGB text color
        
        Returns:
            Path to generated thumbnail or None if failed
        """
        try:
            # Create new image
            img = Image.new('RGB', self.STANDARD_SIZE, background_color)
            draw = ImageDraw.Draw(img)
            
            # Try to use a nice font, fallback to default
            try:
                font_size = 80
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            lines = self._wrap_text(title, 20)
            
            # Calculate text position (center)
            text = '\n'.join(lines)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
            
            # Add text with outline for better visibility
            outline_width = 3
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    draw.text((x + adj_x, y + adj_y), text, font=font, fill=(0, 0, 0))
            
            draw.text((x, y), text, font=font, fill=text_color)
            
            # Save thumbnail
            img.save(output_path, quality=95)
            logger.info(f"Thumbnail created: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            return None
    
    @staticmethod
    def _wrap_text(text: str, max_length: int = 20) -> list:
        """Wrap text to fit in specified width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= max_length:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
