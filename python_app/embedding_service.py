#!/usr/bin/env python3
"""
OpenAI Embedding Service for Brand Guidelines
Creates vector embeddings for semantic search and LLM integration
"""

import os
import json
import logging
import asyncio
import aiohttp
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import psycopg2
from flask import Response
import colorsys
from psycopg2.extras import RealDictCursor
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenAIEmbeddingService:
    def __init__(self, db_config: Dict[str, str]):
        """Initialize the embedding service"""
        self.db_config = db_config
        self.connection = None
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.embedding_model = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-large')
        self.fallback_embedding_model = os.getenv('FALLBACK_EMBEDDING_MODEL', 'text-embedding-3-small')
        self.embedding_dimensions = int(os.getenv('EMBEDDING_DIMENSIONS', '3072'))
        self.llm_model = os.getenv('LLM_MODEL', 'gpt-5')
        self.fallback_llm_model = os.getenv('FALLBACK_LLM_MODEL', 'gpt-4o')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert HEX color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hsv(self, r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convert RGB to HSV"""
        r, g, b = r/255.0, g/255.0, b/255.0
        return colorsys.rgb_to_hsv(r, g, b)
    
    def color_similarity(self, color1: str, color2: str) -> float:
        """Calculate color similarity between two HEX colors (0-1, higher = more similar)"""
        try:
            rgb1 = self.hex_to_rgb(color1)
            rgb2 = self.hex_to_rgb(color2)
            
            # Convert to HSV for better perceptual similarity
            hsv1 = self.rgb_to_hsv(*rgb1)
            hsv2 = self.rgb_to_hsv(*rgb2)
            
            # Calculate weighted distance
            h_diff = min(abs(hsv1[0] - hsv2[0]), 1 - abs(hsv1[0] - hsv2[0]))  # Hue is circular
            s_diff = abs(hsv1[1] - hsv2[1])
            v_diff = abs(hsv1[2] - hsv2[2])
            
            # Weighted similarity (hue is most important, then saturation, then value)
            similarity = 1 - (0.6 * h_diff + 0.3 * s_diff + 0.1 * v_diff)
            return max(0, min(1, similarity))
            
        except Exception:
            return 0.0
    
    def find_best_color_match(self, target_color: str, brand_colors: List[Dict[str, str]], 
                            threshold: float = 0.7) -> Optional[Dict[str, Any]]:
        """Find the best matching brand color for a target color"""
        best_match = None
        best_similarity = 0
        
        for brand_color in brand_colors:
            hex_value = brand_color.get('hex', '')
            if hex_value:
                similarity = self.color_similarity(target_color, hex_value)
                if similarity >= threshold and similarity > best_similarity:
                    best_match = {
                        'hex': hex_value,
                        'name': brand_color.get('name', 'Unknown'),
                        'similarity': similarity,
                        'rgb': brand_color.get('rgb', ''),
                        'cmyk': brand_color.get('cmyk', '')
                    }
                    best_similarity = similarity
        
        return best_match
    
    def connect_db(self):
        """Connect to PostgreSQL database"""
        if not self.connection:
            self.connection = psycopg2.connect(**self.db_config)
            logger.info("Connected to database")
    
    def disconnect_db(self):
        """Disconnect from database"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Disconnected from database")
    
    async def create_embedding(self, text: str, use_fallback: bool = False) -> Optional[List[float]]:
        """Create embedding for a single text with fallback support"""
        try:
            model = self.fallback_embedding_model if use_fallback else self.embedding_model
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "input": text,
                    "encoding_format": "float"
                }
                
                async with session.post(
                    "https://api.openai.com/v1/embeddings",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['data'][0]['embedding']
                    else:
                        error_text = await response.text()
                        logger.error(f"Embedding API error ({response.status}): {error_text}")
                        if not use_fallback and self.embedding_model != self.fallback_embedding_model:
                            logger.info(f"Trying fallback model: {self.fallback_embedding_model}")
                            return await self.create_embedding(text, use_fallback=True)
                        return None
                        
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            if not use_fallback and self.embedding_model != self.fallback_embedding_model:
                logger.info(f"Trying fallback model: {self.fallback_embedding_model}")
                return await self.create_embedding(text, use_fallback=True)
            return None
    
    def disconnect_db(self):
        """Disconnect from the database"""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from database")
    
    async def create_embedding(self, text: str, session: aiohttp.ClientSession, use_fallback: bool = False) -> Optional[List[float]]:
        """Create embedding for a single text with fallback support"""
        try:
            # Clean and truncate text
            text = text.strip()[:8000]  # OpenAI limit
            
            if not text or len(text) < 10:
                return None
            
            # Choose model (with fallback)
            model = self.fallback_embedding_model if use_fallback else self.embedding_model
            
            payload = {
                "model": model,
                "input": text,
                "encoding_format": "float"
            }
            
            # For text-embedding-3-large, we can specify dimensions
            if model == "text-embedding-3-large":
                payload["dimensions"] = self.embedding_dimensions
            
            async with session.post(
                f"{self.base_url}/embeddings",
                headers=self.headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['data'][0]['embedding']
                elif response.status == 404 and not use_fallback:
                    # Model not available, try fallback
                    logger.warning(f"Model {model} not available, trying fallback...")
                    return await self.create_embedding(text, session, use_fallback=True)
                else:
                    error_text = await response.text()
                    logger.error(f"OpenAI API error: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Failed to create embedding: {e}")
            return None
    
    async def create_embeddings_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Create embeddings for multiple texts in parallel"""
        embeddings = []
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.create_embedding(text, session) for text in texts]
            embeddings = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle exceptions
            for i, emb in enumerate(embeddings):
                if isinstance(emb, Exception):
                    logger.error(f"Embedding failed for text {i}: {emb}")
                    embeddings[i] = None
        
        return embeddings
    
    def get_texts_for_embedding(self, brand_id: str) -> List[Dict[str, Any]]:
        """Get all texts that need embeddings"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get brand asset descriptions
                cursor.execute("""
                    SELECT 
                        ba.id,
                        ba.title,
                        ba.asset_type,
                        al.name as library_name,
                        'asset_description' as chunk_type,
                        CONCAT('Asset: ', ba.title, ' (Type: ', ba.asset_type, 
                               ', Library: ', al.name, ', Size: ', 
                               COALESCE(ba.width, 0), 'x', COALESCE(ba.height, 0), ')') as content,
                        jsonb_build_object(
                            'asset_type', ba.asset_type,
                            'library', al.name,
                            'dimensions', jsonb_build_object('width', ba.width, 'height', ba.height),
                            'size_bytes', ba.size_bytes
                        ) as metadata
                    FROM brand_assets ba
                    JOIN asset_libraries al ON ba.library_id = al.id
                    WHERE al.brand_id = %s
                    AND ba.title IS NOT NULL
                    AND LENGTH(TRIM(ba.title)) > 3
                """, (brand_id,))
                
                asset_texts = cursor.fetchall()
                
                # Get image analysis results
                cursor.execute("""
                    SELECT 
                        iar.id,
                        iar.original_url,
                        iar.asset_category,
                        iar.compliance_score,
                        'image_analysis' as chunk_type,
                        CONCAT('Image Analysis: ', 
                               COALESCE(iar.asset_category, 'Unknown Asset'), 
                               ' (Compliance: ', COALESCE(iar.compliance_score, 0), '/100)',
                               CASE WHEN iar.logo_detected THEN ' - Logo detected' ELSE '' END,
                               CASE WHEN iar.brand_elements IS NOT NULL THEN 
                                   ' - Brand elements: ' || iar.brand_elements::text ELSE '' END
                        ) as content,
                        jsonb_build_object(
                            'image_url', iar.original_url,
                            'asset_category', iar.asset_category,
                            'compliance_score', iar.compliance_score,
                            'logo_detected', iar.logo_detected,
                            'brand_elements', iar.brand_elements,
                            'analysis_result', iar.analysis_result,
                            'source_context', iar.source_context
                        ) as metadata
                    FROM image_analysis_results iar
                    WHERE iar.brand_id = %s
                    AND iar.status = 'analyzed'
                    AND iar.analysis_result IS NOT NULL
                """, (brand_id,))
                
                image_texts = cursor.fetchall()
                
                # Get guideline content
                cursor.execute("""
                    SELECT 
                        pc.id,
                        pc.content,
                        'guideline_text' as chunk_type,
                        pc.content_type,
                        gp.title as page_title,
                        gp.page_path,
                        jsonb_build_object(
                            'content_type', pc.content_type,
                            'page_title', gp.title,
                            'page_path', gp.page_path
                        ) as metadata
                    FROM page_content pc
                    JOIN guideline_pages gp ON pc.page_id = gp.id
                    WHERE gp.brand_id = %s
                    AND pc.content IS NOT NULL 
                    AND LENGTH(TRIM(pc.content)) > 10
                    AND pc.content_type IN ('paragraph', 'list_item')
                """, (brand_id,))
                
                guideline_texts = cursor.fetchall()
                
                # Get page sections (headings)
                cursor.execute("""
                    SELECT 
                        ps.id,
                        ps.text as content,
                        'guideline_heading' as chunk_type,
                        ps.heading_level,
                        gp.title as page_title,
                        gp.page_path,
                        jsonb_build_object(
                            'heading_level', ps.heading_level,
                            'page_title', gp.title,
                            'page_path', gp.page_path
                        ) as metadata
                    FROM page_sections ps
                    JOIN guideline_pages gp ON ps.page_id = gp.id
                    WHERE gp.brand_id = %s
                    AND ps.text IS NOT NULL 
                    AND LENGTH(TRIM(ps.text)) > 5
                """, (brand_id,))
                
                section_texts = cursor.fetchall()
                
                # Combine all texts
                all_texts = []
                all_texts.extend(asset_texts)
                all_texts.extend(image_texts)
                all_texts.extend(guideline_texts)
                all_texts.extend(section_texts)
                
                logger.info(f"Found {len(all_texts)} texts for embedding")
                return all_texts
                
        except Exception as e:
            logger.error(f"Failed to get texts for embedding: {e}")
            return []
    
    async def process_brand_embeddings(self, brand_id: str) -> bool:
        """Process all embeddings for a brand"""
        try:
            logger.info(f"Starting embedding process for brand {brand_id}")
            
            # Get all texts
            texts_data = self.get_texts_for_embedding(brand_id)
            if not texts_data:
                logger.warning("No texts found for embedding")
                return False
            
            # Extract texts and metadata
            texts = [item['content'] for item in texts_data]
            
            # Create embeddings in batches
            batch_size = 10  # OpenAI rate limit consideration
            all_embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_data = texts_data[i:i + batch_size]
                
                logger.info(f"Processing batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
                
                # Create embeddings
                embeddings = await self.create_embeddings_batch(batch_texts)
                
                # Store embeddings in database
                for j, (embedding, data) in enumerate(zip(embeddings, batch_data)):
                    if embedding is not None:
                        self.store_embedding(
                            brand_id=brand_id,
                            source_id=data['id'],
                            chunk_type=data['chunk_type'],
                            content=data['content'],
                            metadata=data['metadata'],
                            embedding=embedding
                        )
                
                # Rate limiting
                if i + batch_size < len(texts):
                    await asyncio.sleep(1)
            
            logger.info("Embedding process completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process brand embeddings: {e}")
            return False
    
    def store_embedding(self, brand_id: str, source_id: str, chunk_type: str, 
                       content: str, metadata: Dict[str, Any], embedding: List[float]):
        """Store embedding in database"""
        try:
            with self.connection.cursor() as cursor:
                # Check if embedding already exists
                cursor.execute("""
                    SELECT id FROM brand_knowledge_chunks 
                    WHERE brand_id = %s AND source_id = %s AND chunk_type = %s
                """, (brand_id, source_id, chunk_type))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing embedding
                    cursor.execute("""
                        UPDATE brand_knowledge_chunks 
                        SET content = %s, metadata = %s, embedding = %s,
                            embedding_model = %s, embedding_created_at = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, (content, json.dumps(metadata), embedding, 
                         self.embedding_model, datetime.utcnow(), existing[0]))
                else:
                    # Insert new embedding
                    cursor.execute("""
                        INSERT INTO brand_knowledge_chunks 
                        (brand_id, chunk_type, source_type, source_id, chunk_index, 
                         content, metadata, embedding, embedding_model, embedding_created_at)
                        VALUES (%s, %s, 'guideline_content', %s, 0, %s, %s, %s, %s, %s)
                    """, (brand_id, chunk_type, source_id, content, 
                         json.dumps(metadata), embedding, self.embedding_model, datetime.utcnow()))
                
                self.connection.commit()
                
        except Exception as e:
            logger.error(f"Failed to store embedding: {e}")
            self.connection.rollback()
    
    async def semantic_search(self, query: str, brand_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Perform semantic search using embeddings"""
        try:
            # Create embedding for query
            query_embeddings = await self.create_embeddings_batch([query])
            if not query_embeddings or query_embeddings[0] is None:
                logger.error("Failed to create query embedding")
                return []
            
            query_embedding = query_embeddings[0]
            
            # Search in database
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        bkc.id,
                        bkc.chunk_type,
                        bkc.content,
                        bkc.metadata,
                        b.name as brand_name,
                        1 - (bkc.embedding <=> %s::vector) as similarity_score
                    FROM brand_knowledge_chunks bkc
                    JOIN brands b ON bkc.brand_id = b.id
                    WHERE bkc.brand_id = %s
                    AND bkc.embedding IS NOT NULL
                    ORDER BY bkc.embedding <=> %s::vector
                    LIMIT %s
                """, (query_embedding, brand_id, query_embedding, limit))
                
                results = cursor.fetchall()
                
                # Convert to list of dicts
                search_results = []
                for row in results:
                    search_results.append({
                        'id': row['id'],
                        'chunk_type': row['chunk_type'],
                        'content': row['content'],
                        'metadata': row['metadata'],
                        'brand_name': row['brand_name'],
                        'similarity_score': float(row['similarity_score'])
                    })
                
                logger.info(f"Found {len(search_results)} semantic search results")
                return search_results
                
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []
    
    async def generate_llm_response(self, query: str, search_results: List[Dict[str, Any]], 
                                  session: aiohttp.ClientSession, use_fallback: bool = False) -> str:
        """Generate LLM response based on search results with fallback support"""
        try:
            if not search_results:
                return "Keine relevanten Informationen zu Ihrer Anfrage gefunden."
            
            # Prepare context from search results
            context_parts = []
            for i, result in enumerate(search_results[:5]):  # Top 5 results
                context_parts.append(f"[{i+1}] {result['content']}")
            
            context = "\n\n".join(context_parts)
            
            # Create LLM prompt
            prompt = f"""Du bist ein Experte für Brand Guidelines und Markenmanagement. 
Antworte auf Deutsch basierend auf den folgenden Brand-Guideline-Informationen:

Anfrage: {query}

Relevante Informationen:
{context}

Antworte präzise und hilfreich. Falls die Informationen nicht ausreichen, sage das ehrlich."""

            # Choose model (with fallback)
            model = self.fallback_llm_model if use_fallback else self.llm_model
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "Du bist ein Experte für Brand Guidelines und Markenmanagement."},
                    {"role": "user", "content": prompt}
                ],
                "max_completion_tokens": 2000  # GPT-5 uses max_completion_tokens and default temperature (1)
            }
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']['content']
                elif response.status == 404 and not use_fallback:
                    # Model not available, try fallback
                    logger.warning(f"LLM Model {model} not available, trying fallback...")
                    return await self.generate_llm_response(query, search_results, session, use_fallback=True)
                else:
                    error_text = await response.text()
                    logger.error(f"LLM API error: {response.status} - {error_text}")
                    return "Entschuldigung, ich konnte Ihre Anfrage nicht verarbeiten."
                    
        except Exception as e:
            logger.error(f"LLM response generation failed: {e}")
            return "Entschuldigung, es ist ein Fehler aufgetreten."
    
    async def generate_llm_response_streaming(self, query: str, search_results: List[Dict[str, Any]], 
                                           session: aiohttp.ClientSession, use_fallback: bool = False):
        """Generate streaming LLM response based on search results"""
        try:
            if not search_results:
                return "Keine relevanten Informationen zu Ihrer Anfrage gefunden."
            
            # For now, return regular response instead of streaming
            # Streaming implementation can be added later if needed
            return await self.generate_llm_response(query, search_results, session, use_fallback)
                    
        except Exception as e:
            logger.error(f"Streaming LLM generation failed: {e}")
            if not use_fallback and self.llm_model != self.fallback_llm_model:
                logger.info(f"Trying fallback LLM model: {self.fallback_llm_model}")
                return await self.generate_llm_response_streaming(query, search_results, session, use_fallback=True)
            return "Entschuldigung, ich konnte keine Antwort generieren."


async def main():
    """Main function to run the embedding service"""
    # Database configuration
    db_config = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5433'),
        'database': os.getenv('POSTGRES_DB', 'brandchecker'),
        'user': os.getenv('POSTGRES_USER', 'brandchecker_user'),
        'password': os.getenv('POSTGRES_PASSWORD', 'brandchecker_password')
    }
    
    # Initialize service
    service = OpenAIEmbeddingService(db_config)
    
    try:
        # Connect to database
        service.connect_db()
        
        # Get brand ID (assuming Bosch)
        brand_id = '9a933c7f-bd87-400f-b13a-b3bce7c822d8'  # From previous import
        
        # Process embeddings
        logger.info("Starting embedding process...")
        success = await service.process_brand_embeddings(brand_id)
        
        if success:
            logger.info("Embedding process completed successfully!")
            
            # Test semantic search
            logger.info("Testing semantic search...")
            test_query = "Welche Farben sind für Bosch Corporate erlaubt?"
            results = await service.semantic_search(test_query, brand_id, limit=5)
            
            for i, result in enumerate(results):
                logger.info(f"Result {i+1}: {result['similarity_score']:.3f} - {result['content'][:100]}...")
            
            # Test LLM response
            logger.info("Testing LLM response...")
            async with aiohttp.ClientSession() as session:
                response = await service.generate_llm_response(test_query, results, session)
                logger.info(f"LLM Response: {response}")
        else:
            logger.error("Embedding process failed")
            
    except Exception as e:
        logger.error(f"Main process failed: {e}")
    
    finally:
        service.disconnect_db()


if __name__ == "__main__":
    asyncio.run(main())
