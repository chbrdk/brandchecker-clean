#!/usr/bin/env python3
"""
Image Analysis API Service
REST API für Bildanalyse mit GPT-4o und SVG-Unterstützung
"""

import os
import json
import logging
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
from image_analysis_service import ImageAnalysisService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global service instance
image_service = None

def init_service():
    """Initialize the image analysis service"""
    global image_service
    try:
        image_service = ImageAnalysisService()
        logger.info("Image Analysis API service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize service: {e}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'image-analysis-api',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/analyze-image', methods=['POST'])
async def analyze_single_image():
    """Analysiert ein einzelnes Bild"""
    try:
        data = request.get_json()
        image_url = data.get('image_url', '').strip()
        
        if not image_url:
            return jsonify({'error': 'image_url parameter is required'}), 400
        
        logger.info(f"Analyzing single image: {image_url}")
        
        # Analysiere das Bild
        results = await image_service.analyze_images([image_url])
        
        if results and len(results) > 0:
            result = results[0]
            return jsonify({
                'status': 'success',
                'image_url': image_url,
                'analysis': result.get('analysis'),
                'logo_detected': result.get('logo_detected', False),
                'content_type': result.get('content_type'),
                'model_used': result.get('model_used'),
                'tokens_used': result.get('tokens_used'),
                'timestamp': result.get('timestamp')
            })
        else:
            return jsonify({'error': 'Failed to analyze image'}), 500
            
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/analyze-images', methods=['POST'])
async def analyze_multiple_images():
    """Analysiert mehrere Bilder"""
    try:
        data = request.get_json()
        image_urls = data.get('image_urls', [])
        max_images = data.get('max_images', 20)
        
        if not image_urls:
            return jsonify({'error': 'image_urls parameter is required'}), 400
        
        if not isinstance(image_urls, list):
            return jsonify({'error': 'image_urls must be a list'}), 400
        
        logger.info(f"Analyzing {len(image_urls)} images (max: {max_images})")
        
        # Analysiere die Bilder
        results = await image_service.analyze_images(image_urls, max_images=max_images)
        
        # Speichere Ergebnisse
        stats = image_service.save_results(results)
        
        return jsonify({
            'status': 'success',
            'total_processed': stats['total_processed'],
            'successful': stats['successful'],
            'errors': stats['errors'],
            'svg_converted': stats['svg_converted'],
            'logos_detected': stats['logos_detected'],
            'success_rate': stats['success_rate'],
            'logo_detection_rate': stats['logo_detection_rate'],
            'duration_seconds': stats['duration_seconds'],
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error analyzing images: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/analyze-all-extracted', methods=['POST'])
async def analyze_all_extracted_images():
    """Analysiert alle extrahierten Bilder aus den Brand Guidelines"""
    try:
        data = request.get_json()
        max_images = data.get('max_images', 50)
        
        # Lade extrahierte Bild-URLs
        urls_file = "/shared/JSON/extracted/image_urls.json"
        if not os.path.exists(urls_file):
            return jsonify({'error': 'Extracted image URLs file not found. Run extract_image_links.py first.'}), 404
        
        with open(urls_file, 'r', encoding='utf-8') as f:
            image_urls = json.load(f)
        
        logger.info(f"Analyzing {min(len(image_urls), max_images)} extracted images")
        
        # Analysiere die Bilder
        results = await image_service.analyze_images(image_urls, max_images=max_images)
        
        # Speichere Ergebnisse
        stats = image_service.save_results(results)
        
        return jsonify({
            'status': 'success',
            'total_extracted': len(image_urls),
            'total_processed': stats['total_processed'],
            'successful': stats['successful'],
            'errors': stats['errors'],
            'svg_converted': stats['svg_converted'],
            'logos_detected': stats['logos_detected'],
            'success_rate': stats['success_rate'],
            'logo_detection_rate': stats['logo_detection_rate'],
            'duration_seconds': stats['duration_seconds'],
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error analyzing extracted images: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/image-analysis/status', methods=['GET'])
def get_analysis_status():
    """Gibt den Status der Bildanalyse zurück"""
    try:
        # Prüfe ob extrahierte URLs vorhanden sind
        urls_file = "/shared/JSON/extracted/image_urls.json"
        extracted_count = 0
        if os.path.exists(urls_file):
            with open(urls_file, 'r', encoding='utf-8') as f:
                image_urls = json.load(f)
                extracted_count = len(image_urls)
        
        # Zähle bereits analysierte Bilder
        analyzed_count = 0
        analyzed_dir = "/shared/JSON/analyzed"
        if os.path.exists(analyzed_dir):
            analyzed_files = [f for f in os.listdir(analyzed_dir) if f.startswith('image_analysis_')]
            analyzed_count = len(analyzed_files)
        
        return jsonify({
            'status': 'ready',
            'extracted_images': extracted_count,
            'analyzed_files': analyzed_count,
            'service_initialized': image_service is not None,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/image-analysis/results', methods=['GET'])
def get_analysis_results():
    """Gibt die neuesten Analyseergebnisse zurück"""
    try:
        analyzed_dir = "/shared/JSON/analyzed"
        if not os.path.exists(analyzed_dir):
            return jsonify({'error': 'No analysis results found'}), 404
        
        # Finde die neueste Analyse-Datei
        analysis_files = [f for f in os.listdir(analyzed_dir) if f.startswith('image_analysis_')]
        if not analysis_files:
            return jsonify({'error': 'No analysis results found'}), 404
        
        latest_file = max(analysis_files)
        file_path = os.path.join(analyzed_dir, latest_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        return jsonify({
            'status': 'success',
            'latest_analysis': latest_file,
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting results: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Flask async support
@app.before_request
def before_request():
    """Handle async requests"""
    pass

@app.after_request
def after_request(response):
    """Handle async responses"""
    return response

if __name__ == '__main__':
    # Initialize service
    init_service()
    
    # Run Flask app
    port = int(os.getenv('PORT', 8002))
    app.run(host='0.0.0.0', port=port, debug=True)
