#!/usr/bin/env python3
"""
YouTube AI Automation - Main Application Entry Point
Production-ready AI YouTube video generation system
"""

import os
import sys
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production'),
    BACKEND_HOST=os.getenv('BACKEND_HOST', '0.0.0.0'),
    BACKEND_PORT=int(os.getenv('BACKEND_PORT', 5000)),
    ENVIRONMENT=os.getenv('ENVIRONMENT', 'development'),
    STORAGE_PATH=os.getenv('STORAGE_PATH', './storage'),
    TEMP_PATH=os.getenv('TEMP_PATH', './temp'),
)

# Create necessary directories
for directory in [app.config['STORAGE_PATH'], app.config['TEMP_PATH']]:
    os.makedirs(directory, exist_ok=True)

# Import and register blueprints
try:
    from backend.routes import api, auth, videos, youtube
    app.register_blueprint(api.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(videos.bp)
    app.register_blueprint(youtube.bp)
    logger.info("All route blueprints registered successfully")
except ImportError as e:
    logger.error(f"Failed to import route blueprints: {e}")
    sys.exit(1)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'youtube-ai-automation',
        'environment': app.config['ENVIRONMENT']
    }), 200

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    """API root endpoint"""
    return jsonify({
        'name': 'YouTube AI Automation API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'api': '/api',
            'auth': '/auth',
            'videos': '/videos',
            'youtube': '/youtube'
        }
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

if __name__ == '__main__':
    host = app.config['BACKEND_HOST']
    port = app.config['BACKEND_PORT']
    debug = app.config['ENVIRONMENT'] == 'development'
    
    logger.info(f"Starting YouTube AI Automation Backend")
    logger.info(f"Environment: {app.config['ENVIRONMENT']}")
    logger.info(f"Listening on {host}:{port}")
    
    app.run(host=host, port=port, debug=debug)
