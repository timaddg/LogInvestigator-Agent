#!/usr/bin/env python3
"""
Log Investigator Web Interface

A Flask-based web application for uploading and analyzing log files with AI.
"""

import os
import json
import tempfile
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# Import our modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Get the project root directory (2 levels up from api/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FRONTEND_OUT_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'out')

from config.config import config
from logic.processors.log_loader import LogLoader
from logic.analyzers.ai_analyzer import AIAnalyzer
from logic.processors.log_downloader import LogDownloader
from utils.utils import display_log_statistics, display_analysis_results

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
ai_analyzer = AIAnalyzer()
log_downloader = LogDownloader()

ALLOWED_EXTENSIONS = {'json', 'log', 'txt', 'csv'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the Next.js frontend."""
    return send_from_directory(FRONTEND_OUT_DIR, 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    """Serve static files from the Next.js build."""
    # Handle API routes by passing them to the backend
    if path.startswith('api/'):
        return jsonify({'error': 'API routes not available in static export'}), 404
    
    # Serve static files
    return send_from_directory(FRONTEND_OUT_DIR, path)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Please upload .json, .log, .txt, or .csv files'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load and analyze logs
        log_loader = LogLoader(filepath)
        logs = log_loader.load_logs()
        
        if not logs:
            return jsonify({'error': 'Failed to load logs from file'}), 400
        
        # Get log statistics
        stats = log_loader.get_log_statistics(logs)
        
        # Perform AI analysis
        analysis_result = ai_analyzer.analyze_logs(logs)
        
        if not analysis_result:
            return jsonify({'error': 'Failed to complete AI analysis'}), 500
        
        # Prepare response
        response = {
            'success': True,
            'filename': filename,
            'log_count': len(logs),
            'statistics': {
                'total_entries': stats.get('total_entries', 0),
                'unique_ips': stats.get('unique_ips', 0),
                'unique_user_agents': stats.get('unique_user_agents', 0),
                'status_codes': stats.get('status_codes', {}),
                'top_endpoints': stats.get('top_endpoints', []),
                'time_range': stats.get('time_range', {})
            },
            'analysis': analysis_result
        }
        
        return jsonify(response)
        
    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large. Maximum size is 50MB'}), 413
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/sources')
def list_sources():
    """List available log sources."""
    try:
        sources = log_downloader.get_available_sources()
        return jsonify({'sources': sources})
    except Exception as e:
        return jsonify({'error': f'Failed to get sources: {str(e)}'}), 500


@app.route('/download/<source_name>', methods=['POST'])
def download_logs(source_name):
    """Download logs from a specific source."""
    try:
        # Download logs
        downloaded_file = log_downloader.download_logs(source_name)
        
        if not downloaded_file:
            return jsonify({'error': f'Failed to download logs from {source_name}'}), 400
        
        # Load and analyze logs
        log_loader = LogLoader(downloaded_file)
        logs = log_loader.load_logs()
        
        if not logs:
            return jsonify({'error': 'Failed to load downloaded logs'}), 400
        
        # Get log statistics
        stats = log_loader.get_log_statistics(logs)
        
        # Perform AI analysis
        analysis_result = ai_analyzer.analyze_logs(logs)
        
        if not analysis_result:
            return jsonify({'error': 'Failed to complete AI analysis'}), 500
        
        # Prepare response
        response = {
            'success': True,
            'source': source_name,
            'filename': downloaded_file,
            'log_count': len(logs),
            'statistics': {
                'total_entries': stats.get('total_entries', 0),
                'unique_ips': stats.get('unique_ips', 0),
                'unique_user_agents': stats.get('unique_user_agents', 0),
                'status_codes': stats.get('status_codes', {}),
                'top_endpoints': stats.get('top_endpoints', []),
                'time_range': stats.get('time_range', {})
            },
            'analysis': analysis_result
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Failed to download and analyze logs: {str(e)}'}), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    # Validate configuration
    if not config.gemini_api_key:
        print("ERROR: GEMINI_API_KEY is required. Please check your .env file.")
        exit(1)
    
    print("Starting Log Investigator Web Interface...")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Max file size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.1f}MB")
    
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port) 