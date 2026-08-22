#!/usr/bin/env python3
"""
Enhanced video routes with pipeline integration
"""

from flask import Blueprint, jsonify, request
import logging
import os
from datetime import datetime
from threading import Thread

logger = logging.getLogger(__name__)

bp = Blueprint('videos', __name__, url_prefix='/videos')

# Global job tracker (in production, use a database)
jobs = {}

@bp.route('/generate', methods=['POST'])
def generate_video():
    """Start video generation pipeline"""
    data = request.get_json()
    
    required_fields = ['topic', 'niche', 'language']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate inputs
    if not data['topic'].strip():
        return jsonify({'error': 'Topic cannot be empty'}), 400
    
    if len(data['topic']) > 500:
        return jsonify({'error': 'Topic too long (max 500 characters)'}), 400
    
    try:
        from backend.pipeline import VideoPipeline
        
        # Start generation in background thread
        pipeline = VideoPipeline()
        video_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        def run_pipeline():
            try:
                result = pipeline.generate(
                    topic=data['topic'],
                    niche=data.get('niche', 'Technology'),
                    language=data.get('language', 'English'),
                    video_length=data.get('video_length', 420),
                    voice=data.get('voice', 'en_US-lessac-medium'),
                    progress_callback=lambda progress, step: update_job_progress(video_id, progress, step)
                )
                
                if result:
                    jobs[video_id] = {
                        'status': 'completed',
                        'progress': 100,
                        'result': result
                    }
                else:
                    jobs[video_id] = {
                        'status': 'failed',
                        'progress': 0,
                        'error': 'Pipeline execution failed'
                    }
            except Exception as e:
                logger.error(f"Pipeline error: {e}")
                jobs[video_id] = {
                    'status': 'failed',
                    'progress': 0,
                    'error': str(e)
                }
        
        # Initialize job tracker
        jobs[video_id] = {
            'status': 'processing',
            'progress': 0,
            'current_step': 'Initializing'
        }
        
        # Run in background
        thread = Thread(target=run_pipeline, daemon=True)
        thread.start()
        
        return jsonify({
            'video_id': video_id,
            'status': 'processing',
            'progress': 0,
            'topic': data['topic'],
            'niche': data.get('niche'),
            'language': data.get('language')
        }), 202
    
    except Exception as e:
        logger.error(f"Generation start failed: {e}")
        return jsonify({'error': 'Failed to start video generation'}), 500

@bp.route('/status/<video_id>', methods=['GET'])
def get_video_status(video_id):
    """Get video generation status"""
    if video_id not in jobs:
        return jsonify({'error': 'Video not found'}), 404
    
    job = jobs[video_id]
    response = {
        'video_id': video_id,
        'status': job['status'],
        'progress': job['progress'],
        'current_step': job.get('current_step', '')
    }
    
    if job['status'] == 'completed' and 'result' in job:
        response['result'] = job['result']
    elif job['status'] == 'failed':
        response['error'] = job.get('error', 'Unknown error')
    
    return jsonify(response), 200

@bp.route('/list', methods=['GET'])
def list_videos():
    """List all generated videos"""
    storage_path = os.getenv('STORAGE_PATH', './storage')
    videos_path = os.path.join(storage_path, 'videos')
    
    try:
        if not os.path.exists(videos_path):
            return jsonify({'videos': [], 'total': 0}), 200
        
        videos = []
        for filename in os.listdir(videos_path):
            if filename.endswith('.mp4'):
                video_id = filename.replace('.mp4', '')
                filepath = os.path.join(videos_path, filename)
                
                # Get file info
                file_size = os.path.getsize(filepath)
                file_time = os.path.getmtime(filepath)
                
                video_info = {
                    'video_id': video_id,
                    'filename': filename,
                    'file_size': file_size,
                    'file_size_mb': round(file_size / (1024*1024), 2),
                    'created_at': datetime.fromtimestamp(file_time).isoformat(),
                    'status': 'completed'
                }
                
                # Check if we have metadata from job tracker
                if video_id in jobs and 'result' in jobs[video_id]:
                    result = jobs[video_id]['result']
                    video_info.update({
                        'title': result.get('title'),
                        'topic': result.get('topic'),
                        'duration': result.get('duration')
                    })
                
                videos.append(video_info)
        
        # Sort by creation date (newest first)
        videos.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'videos': videos,
            'total': len(videos)
        }), 200
    
    except Exception as e:
        logger.error(f"Error listing videos: {e}")
        return jsonify({'error': 'Failed to list videos'}), 500

@bp.route('/<video_id>', methods=['GET'])
def get_video(video_id):
    """Get video details"""
    storage_path = os.getenv('STORAGE_PATH', './storage')
    video_path = os.path.join(storage_path, 'videos', f"{video_id}.mp4")
    
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video not found'}), 404
    
    try:
        file_size = os.path.getsize(video_path)
        file_time = os.path.getmtime(video_path)
        
        response = {
            'video_id': video_id,
            'filename': f"{video_id}.mp4",
            'file_size': file_size,
            'file_size_mb': round(file_size / (1024*1024), 2),
            'created_at': datetime.fromtimestamp(file_time).isoformat(),
            'status': 'completed',
            'download_url': f"/videos/{video_id}/download"
        }
        
        # Add metadata if available
        if video_id in jobs and 'result' in jobs[video_id]:
            result = jobs[video_id]['result']
            response.update({
                'title': result.get('title'),
                'description': result.get('description'),
                'topic': result.get('topic'),
                'niche': result.get('niche'),
                'language': result.get('language'),
                'duration': result.get('duration'),
                'thumbnail': result.get('thumbnail_file'),
                'script': result.get('script_file')
            })
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error getting video: {e}")
        return jsonify({'error': 'Failed to get video details'}), 500

@bp.route('/<video_id>/download', methods=['GET'])
def download_video(video_id):
    """Download generated video"""
    from flask import send_file
    
    storage_path = os.getenv('STORAGE_PATH', './storage')
    video_path = os.path.join(storage_path, 'videos', f"{video_id}.mp4")
    
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video not found'}), 404
    
    try:
        return send_file(
            video_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name=f"{video_id}.mp4"
        )
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': 'Failed to download video'}), 500

@bp.route('/<video_id>', methods=['DELETE'])
def delete_video(video_id):
    """Delete video"""
    storage_path = os.getenv('STORAGE_PATH', './storage')
    video_path = os.path.join(storage_path, 'videos', f"{video_id}.mp4")
    thumbnail_path = os.path.join(storage_path, 'thumbnails', f"{video_id}.png")
    
    try:
        deleted = False
        
        if os.path.exists(video_path):
            os.remove(video_path)
            deleted = True
        
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        
        # Also remove from job tracker
        if video_id in jobs:
            del jobs[video_id]
        
        if deleted:
            return jsonify({'message': 'Video deleted successfully'}), 200
        else:
            return jsonify({'error': 'Video not found'}), 404
    
    except Exception as e:
        logger.error(f"Delete error: {e}")
        return jsonify({'error': 'Failed to delete video'}), 500

def update_job_progress(video_id: str, progress: int, step: str):
    """Update job progress"""
    if video_id in jobs:
        jobs[video_id]['progress'] = min(progress, 100)
        jobs[video_id]['current_step'] = step
