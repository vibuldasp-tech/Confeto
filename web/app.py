"""Flask web application for Document Gap Analysis."""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import logging

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.document_parser import DocumentParser
from src.gap_analyzer import GapAnalyzer
from src.report_generator import ReportGenerator
from src.ai_provider import get_ai_provider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max file size
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'uploads'
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'md'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_old_files():
    """Remove files older than 1 hour from uploads directory."""
    try:
        upload_dir = app.config['UPLOAD_FOLDER']
        now = datetime.now().timestamp()
        for file_path in upload_dir.glob('*'):
            if file_path.is_file():
                file_age = now - file_path.stat().st_mtime
                if file_age > 3600:  # 1 hour
                    file_path.unlink()
                    logger.info(f"Cleaned up old file: {file_path.name}")
    except Exception as e:
        logger.error(f"Error cleaning up files: {e}")


@app.route('/')
def index():
    """Render the main upload page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and initiate analysis."""
    try:
        # Clean up old files first
        cleanup_old_files()
        
        # Check if files were uploaded
        if 'user_document' not in request.files:
            return jsonify({'error': 'No user document uploaded'}), 400
        
        user_file = request.files['user_document']
        reference_files = request.files.getlist('reference_documents')
        
        if user_file.filename == '':
            return jsonify({'error': 'No user document selected'}), 400
        
        if len(reference_files) == 0 or reference_files[0].filename == '':
            return jsonify({'error': 'No reference documents uploaded'}), 400
        
        # Validate and save user document
        if not allowed_file(user_file.filename):
            return jsonify({'error': f'Invalid file type for user document. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        user_filename = secure_filename(user_file.filename)
        user_path = app.config['UPLOAD_FOLDER'] / f"user_{datetime.now().timestamp()}_{user_filename}"
        user_file.save(user_path)
        logger.info(f"Saved user document: {user_path}")
        
        # Validate and save reference documents
        reference_paths = []
        for ref_file in reference_files:
            if ref_file.filename and allowed_file(ref_file.filename):
                ref_filename = secure_filename(ref_file.filename)
                ref_path = app.config['UPLOAD_FOLDER'] / f"ref_{datetime.now().timestamp()}_{ref_filename}"
                ref_file.save(ref_path)
                reference_paths.append(ref_path)
                logger.info(f"Saved reference document: {ref_path}")
        
        if len(reference_paths) == 0:
            return jsonify({'error': 'No valid reference documents provided'}), 400
        
        # Check for API key
        try:
            ai_provider = get_ai_provider()
        except ValueError as e:
            return jsonify({'error': 'AI provider not configured. Please set API keys in environment variables.'}), 500
        
        # Perform gap analysis
        logger.info("Starting gap analysis")
        analyzer = GapAnalyzer(ai_provider=ai_provider)
        report = analyzer.analyze(
            str(user_path),
            [str(p) for p in reference_paths]
        )
        logger.info("Gap analysis completed")
        
        # Generate reports in different formats
        generator = ReportGenerator()
        
        # Save Markdown report
        md_path = app.config['UPLOAD_FOLDER'] / f"report_{datetime.now().timestamp()}.md"
        generator.save_report(report, str(md_path), format='markdown')
        
        # Save HTML report
        html_path = app.config['UPLOAD_FOLDER'] / f"report_{datetime.now().timestamp()}.html"
        generator.save_report(report, str(html_path), format='html')
        
        # Save JSON report
        json_path = app.config['UPLOAD_FOLDER'] / f"report_{datetime.now().timestamp()}.json"
        generator.save_report(report, str(json_path), format='json')
        
        # Clean up uploaded files
        try:
            user_path.unlink()
            for ref_path in reference_paths:
                ref_path.unlink()
        except Exception as e:
            logger.warning(f"Error cleaning up uploaded files: {e}")
        
        # Prepare response
        result = {
            'success': True,
            'report': report.to_dict(),
            'download_links': {
                'markdown': url_for('download_report', filename=md_path.name, _external=True),
                'html': url_for('download_report', filename=html_path.name, _external=True),
                'json': url_for('download_report', filename=json_path.name, _external=True)
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/download/<filename>')
def download_report(filename):
    """Download a generated report."""
    try:
        file_path = app.config['UPLOAD_FOLDER'] / filename
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        # Determine mimetype based on extension
        ext = file_path.suffix.lower()
        mimetypes = {
            '.md': 'text/markdown',
            '.html': 'text/html',
            '.json': 'application/json'
        }
        mimetype = mimetypes.get(ext, 'application/octet-stream')
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"gap_analysis_report{ext}",
            mimetype=mimetype
        )
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({'error': 'Download failed'}), 500


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size too large error."""
    return jsonify({'error': 'File too large. Maximum size is 20MB.'}), 413


@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error. Please try again.'}), 500


if __name__ == '__main__':
    # Check for API keys on startup
    try:
        ai_provider = get_ai_provider()
        logger.info(f"AI provider configured: {ai_provider.__class__.__name__}")
    except Exception as e:
        logger.warning(f"AI provider not configured: {e}")
        logger.warning("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
