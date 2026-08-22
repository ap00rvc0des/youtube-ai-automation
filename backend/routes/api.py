#!/usr/bin/env python3
"""
Core API endpoints for YouTube AI Automation
"""

from flask import Blueprint, jsonify, request
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/status', methods=['GET'])
def status():
    """Get system status and available services"""
    return jsonify({
        'status': 'operational',
        'services': {
            'llm': 'configured',
            'tts': 'configured',
            'video_encoder': 'available',
            'thumbnail_generator': 'available'
        }
    }), 200

@bp.route('/niches', methods=['GET'])
def get_niches():
    """Get available video niches"""
    niches = [
        'Interesting Facts',
        'History',
        'Technology',
        'Artificial Intelligence',
        'Science',
        'Mystery',
        'Gaming',
        'Automobiles',
        'Finance & Education'
    ]
    return jsonify({
        'niches': niches,
        'count': len(niches)
    }), 200

@bp.route('/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify({
        'ollama_available': True,
        'piper_available': True,
        'ffmpeg_available': True,
        'youtube_oauth_configured': False
    }), 200
