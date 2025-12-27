"""
BID-ZONE Web API Server

Provides REST API endpoints for the construction estimating platform
"""

import os
import sys
from pathlib import Path
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.interfaces.franklin_os import FranklinOS

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Franklin OS
franklin = None

def get_franklin():
    """Get or create FranklinOS instance"""
    global franklin
    if franklin is None:
        franklin = FranklinOS()
    return franklin


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'service': 'BID-ZONE'
    }), 200


@app.route('/api/status', methods=['GET'])
def system_status():
    """Get system status"""
    try:
        franklin_os = get_franklin()
        status = franklin_os.get_system_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        return jsonify({
            'error': 'Failed to get system status',
            'message': str(e)
        }), 500


@app.route('/api/agents', methods=['GET'])
def agent_statistics():
    """Get agent statistics"""
    try:
        franklin_os = get_franklin()
        stats = franklin_os.get_agent_statistics()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error getting agent statistics: {str(e)}")
        return jsonify({
            'error': 'Failed to get agent statistics',
            'message': str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process a construction plan"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        project_name = request.form.get('project_name', 'Untitled Project')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file
        upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        
        logger.info(f"Processing file: {file_path} for project: {project_name}")
        
        # Process with Franklin OS
        franklin_os = get_franklin()
        result = franklin_os.process_project(
            project_name=project_name,
            file_path=file_path
        )
        
        return jsonify({
            'success': True,
            'project_name': project_name,
            'result': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({
            'error': 'Failed to process file',
            'message': str(e)
        }), 500


@app.route('/api/projects', methods=['GET'])
def list_projects():
    """List all processed projects"""
    try:
        output_folder = os.getenv('OUTPUT_FOLDER', 'outputs')
        projects = []
        
        if os.path.exists(output_folder):
            for project_dir in os.listdir(output_folder):
                project_path = os.path.join(output_folder, project_dir)
                if os.path.isdir(project_path):
                    projects.append({
                        'name': project_dir,
                        'path': project_path,
                        'files': os.listdir(project_path)
                    })
        
        return jsonify({
            'projects': projects,
            'count': len(projects)
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        return jsonify({
            'error': 'Failed to list projects',
            'message': str(e)
        }), 500


@app.route('/api/estimate/current', methods=['GET'])
def get_current_estimate():
    """Get real-time estimate of current processing project"""
    try:
        franklin_os = get_franklin()
        status = franklin_os.get_project_status()
        
        if status is None:
            return jsonify({
                'message': 'No project currently being processed'
            }), 404
        
        return jsonify({
            'project_name': status.get('name'),
            'processing_stage': status.get('processing_stage'),
            'current_estimate': status.get('current_estimate', 0.0),
            'current_items': status.get('current_items', 0),
            'status': status.get('status'),
            'stages': status.get('stages', {})
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting current estimate: {str(e)}")
        return jsonify({
            'error': 'Failed to get current estimate',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


def main():
    """Run the Flask application"""
    import argparse
    
    parser = argparse.ArgumentParser(description='BID-ZONE Web API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    logger.info(f"Starting BID-ZONE Web API on {args.host}:{args.port}")
    logger.info(f"Debug mode: {args.debug}")
    
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )


if __name__ == '__main__':
    main()
