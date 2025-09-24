#!/usr/bin/env python3
"""
LLM API for Brand Guidelines Integration
Provides REST API endpoints for semantic search and compliance checking
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
import psycopg2
from psycopg2.extras import RealDictCursor
from embedding_service import OpenAIEmbeddingService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global service instance
embedding_service = None

def get_db_config():
    """Get database configuration from environment"""
    return {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5433'),
        'database': os.getenv('POSTGRES_DB', 'brandchecker'),
        'user': os.getenv('POSTGRES_USER', 'brandchecker_user'),
        'password': os.getenv('POSTGRES_PASSWORD', 'brandchecker_password')
    }

def init_service():
    """Initialize the embedding service"""
    global embedding_service
    try:
        db_config = get_db_config()
        embedding_service = OpenAIEmbeddingService(db_config)
        embedding_service.connect_db()
        logger.info("LLM API service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize service: {e}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Brand Guidelines LLM API'
    })

@app.route('/api/search', methods=['POST'])
async def semantic_search():
    """Semantic search endpoint"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        brand_id = data.get('brand_id', '')
        limit = data.get('limit', 10)
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        if not brand_id:
            return jsonify({'error': 'Brand ID is required'}), 400
        
        # Perform semantic search
        results = await embedding_service.semantic_search(query, brand_id, limit)
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Semantic search error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/ask', methods=['POST'])
async def ask_question():
    """Ask a question and get LLM response"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        brand_id = data.get('brand_id', '')
        limit = data.get('limit', 5)
        stream = data.get('stream', False)
        
        if not question:
            return jsonify({'error': 'Question parameter is required'}), 400
        
        if not brand_id:
            return jsonify({'error': 'Brand ID is required'}), 400
        
        # Perform semantic search first
        search_results = await embedding_service.semantic_search(question, brand_id, limit)
        
        # Generate LLM response
        async with aiohttp.ClientSession() as session:
            if stream:
                return await embedding_service.generate_llm_response_streaming(
                    question, search_results, session
                )
            else:
                response = await embedding_service.generate_llm_response(
                    question, search_results, session
                )
                
                return jsonify({
                    'question': question,
                    'answer': response,
                    'sources': search_results,
                    'source_count': len(search_results),
                    'timestamp': datetime.utcnow().isoformat()
                })
        
    except Exception as e:
        logger.error(f"Ask question error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get all available brands"""
    try:
        connection = psycopg2.connect(**get_db_config())
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    id,
                    name,
                    slug,
                    primary_color_hex,
                    primary_color_rgb,
                    created_at
                FROM brands
                ORDER BY name
            """)
            
            brands = cursor.fetchall()
            
            return jsonify({
                'brands': [dict(brand) for brand in brands],
                'count': len(brands),
                'timestamp': datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Get brands error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/brand/<brand_id>/assets', methods=['GET'])
def get_brand_assets(brand_id):
    """Get assets for a specific brand"""
    try:
        connection = psycopg2.connect(**get_db_config())
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    ba.id,
                    ba.title,
                    ba.asset_type,
                    ba.download_url,
                    ba.preview_url,
                    ba.width,
                    ba.height,
                    al.name as library_name
                FROM brand_assets ba
                JOIN asset_libraries al ON ba.library_id = al.id
                WHERE al.brand_id = %s
                ORDER BY ba.title
                LIMIT 100
            """, (brand_id,))
            
            assets = cursor.fetchall()
            
            return jsonify({
                'brand_id': brand_id,
                'assets': [dict(asset) for asset in assets],
                'count': len(assets),
                'timestamp': datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Get brand assets error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/brand/<brand_id>/guidelines', methods=['GET'])
def get_brand_guidelines(brand_id):
    """Get guideline pages for a specific brand"""
    try:
        connection = psycopg2.connect(**get_db_config())
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    gp.id,
                    gp.page_path,
                    gp.title,
                    gp.url,
                    COUNT(pc.id) as content_count
                FROM guideline_pages gp
                LEFT JOIN page_content pc ON gp.id = pc.page_id
                WHERE gp.brand_id = %s
                GROUP BY gp.id, gp.page_path, gp.title, gp.url
                ORDER BY gp.title
            """, (brand_id,))
            
            guidelines = cursor.fetchall()
            
            return jsonify({
                'brand_id': brand_id,
                'guidelines': [dict(guideline) for guideline in guidelines],
                'count': len(guidelines),
                'timestamp': datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Get brand guidelines error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/compliance/check', methods=['POST'])
async def check_compliance():
    """Check brand compliance for a document or content"""
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        brand_id = data.get('brand_id', '')
        check_type = data.get('check_type', 'general')  # general, colors, fonts, logos
        
        if not content:
            return jsonify({'error': 'Content parameter is required'}), 400
        
        if not brand_id:
            return jsonify({'error': 'Brand ID is required'}), 400
        
        # Perform semantic search for relevant guidelines
        query = f"Brand compliance guidelines for {check_type}"
        search_results = await embedding_service.semantic_search(query, brand_id, limit=10)
        
        # Generate compliance assessment
        compliance_prompt = f"""Du bist ein Experte für Brand-Compliance-Prüfung. 
Bewerte den folgenden Inhalt gegen die Brand-Guidelines:

Inhalt: {content}

Brand-Guidelines:
{chr(10).join([f"[{i+1}] {result['content']}" for i, result in enumerate(search_results[:5])])}

Bewerte auf einer Skala von 0-1 (0 = nicht konform, 1 = vollständig konform) und gib spezifische Empfehlungen."""

        async with aiohttp.ClientSession() as session:
            assessment = await embedding_service.generate_llm_response(
                compliance_prompt, search_results, session
            )
        
        # Calculate compliance score (simplified)
        compliance_score = 0.8  # This should be calculated based on the assessment
        
        return jsonify({
            'content': content,
            'brand_id': brand_id,
            'check_type': check_type,
            'compliance_score': compliance_score,
            'assessment': assessment,
            'relevant_guidelines': search_results,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Compliance check error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/embeddings/status', methods=['GET'])
def get_embedding_status():
    """Get status of embeddings for brands"""
    try:
        connection = psycopg2.connect(**get_db_config())
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    b.id as brand_id,
                    b.name as brand_name,
                    COUNT(bkc.id) as chunk_count,
                    COUNT(CASE WHEN bkc.embedding IS NOT NULL THEN 1 END) as embedded_count,
                    MAX(bkc.embedding_created_at) as last_embedding_update
                FROM brands b
                LEFT JOIN brand_knowledge_chunks bkc ON b.id = bkc.brand_id
                GROUP BY b.id, b.name
                ORDER BY b.name
            """)
            
            status_data = cursor.fetchall()
            
            return jsonify({
                'embedding_status': [dict(status) for status in status_data],
                'timestamp': datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Get embedding status error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/embeddings/generate', methods=['POST'])
async def generate_embeddings():
    """Generate embeddings for a brand"""
    try:
        data = request.get_json()
        brand_id = data.get('brand_id', '')
        
        if not brand_id:
            return jsonify({'error': 'Brand ID is required'}), 400
        
        # Generate embeddings
        success = await embedding_service.process_brand_embeddings(brand_id)
        
        if success:
            return jsonify({
                'brand_id': brand_id,
                'status': 'success',
                'message': 'Embeddings generated successfully',
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                'brand_id': brand_id,
                'status': 'error',
                'message': 'Failed to generate embeddings'
            }), 500
            
    except Exception as e:
        logger.error(f"Generate embeddings error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def run_app():
    """Run the Flask application"""
    try:
        init_service()
        logger.info("Starting LLM API server...")
        app.run(host='0.0.0.0', port=8001, debug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    run_app()
