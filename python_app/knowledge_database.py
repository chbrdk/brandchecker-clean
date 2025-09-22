"""
Knowledge Database Manager for GPT Embeddings and Vector Search
"""

import os
import json
import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import requests
from datetime import datetime
import openai
from database import db_manager

logger = logging.getLogger(__name__)

class KnowledgeDatabaseManager:
    """Knowledge database manager for GPT embeddings and vector search"""
    
    def __init__(self):
        self.openai_client = None
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dimensions = 1536
        self.init_openai_client()
    
    def init_openai_client(self):
        """Initialize OpenAI client"""
        try:
            api_key = os.getenv('OPENAI_API_KEY', '')
            self.openai_client = openai.OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.openai_client = None
    
    def create_embedding(self, text: str) -> Optional[List[float]]:
        """Create embedding for text using OpenAI"""
        if not self.openai_client:
            logger.error("OpenAI client not available")
            return None
        
        try:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            return None
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into chunks with overlap"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for i in range(end, max(start, end - 100), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def extract_knowledge_from_analysis(self, pdf_id: str, analysis_data: Dict) -> List[Dict]:
        """Extract knowledge chunks from analysis data"""
        chunks = []
        chunk_index = 0
        
        # Extract from color analysis
        if 'color_analysis' in analysis_data:
            color_data = analysis_data['color_analysis']
            if 'colors' in color_data:
                for color in color_data['colors']:
                    content = f"Color: {color.get('name', 'Unknown')} - Hex: {color.get('hex', 'N/A')} - RGB: {color.get('rgb', [])} - Usage: {color.get('usage_count', 0)} times"
                    chunks.append({
                        'pdf_document_id': pdf_id,
                        'chunk_type': 'color_analysis',
                        'chunk_index': chunk_index,
                        'content': content,
                        'metadata': {
                            'color_hex': color.get('hex'),
                            'color_rgb': color.get('rgb'),
                            'usage_count': color.get('usage_count', 0),
                            'color_space': color.get('color_space', 'unknown')
                        }
                    })
                    chunk_index += 1
        
        # Extract from design color analysis
        if 'design_color_analysis' in analysis_data:
            design_data = analysis_data['design_color_analysis']
            if 'design_colors' in design_data:
                for color in design_data['design_colors']:
                    content = f"Design Color: {color.get('name', 'Unknown')} - Hex: {color.get('hex', 'N/A')} - Corrected: {color.get('corrected_hex', 'N/A')} - Distance: {color.get('correction_distance', 0)}"
                    chunks.append({
                        'pdf_document_id': pdf_id,
                        'chunk_type': 'color_analysis',
                        'chunk_index': chunk_index,
                        'content': content,
                        'metadata': {
                            'color_hex': color.get('hex'),
                            'corrected_hex': color.get('corrected_hex'),
                            'correction_distance': color.get('correction_distance'),
                            'color_space': color.get('color_space', 'unknown')
                        }
                    })
                    chunk_index += 1
        
        # Extract from font analysis
        if 'font_analysis' in analysis_data:
            font_data = analysis_data['font_analysis']
            if 'fonts' in font_data:
                for font in font_data['fonts']:
                    content = f"Font: {font.get('name', 'Unknown')} - Size: {font.get('size', 'N/A')} - Style: {font.get('style', 'N/A')} - Usage: {font.get('usage_count', 0)} times"
                    chunks.append({
                        'pdf_document_id': pdf_id,
                        'chunk_type': 'font_analysis',
                        'chunk_index': chunk_index,
                        'content': content,
                        'metadata': {
                            'font_name': font.get('name'),
                            'font_size': font.get('size'),
                            'font_style': font.get('style'),
                            'usage_count': font.get('usage_count', 0)
                        }
                    })
                    chunk_index += 1
        
        # Extract from layout analysis
        if 'layout_analysis' in analysis_data:
            layout_data = analysis_data['layout_analysis']
            if 'overall_stats' in layout_data:
                stats = layout_data['overall_stats']
                content = f"Layout: {stats.get('total_pages', 0)} pages - Width: {stats.get('avg_width', 0)} - Height: {stats.get('avg_height', 0)} - Aspect Ratio: {stats.get('avg_aspect_ratio', 0)}"
                chunks.append({
                    'pdf_document_id': pdf_id,
                    'chunk_type': 'layout_analysis',
                    'chunk_index': chunk_index,
                    'content': content,
                    'metadata': {
                        'total_pages': stats.get('total_pages', 0),
                        'avg_width': stats.get('avg_width', 0),
                        'avg_height': stats.get('avg_height', 0),
                        'avg_aspect_ratio': stats.get('avg_aspect_ratio', 0)
                    }
                })
                chunk_index += 1
        
        # Extract from image analysis
        if 'image_analysis' in analysis_data:
            image_data = analysis_data['image_analysis']
            if 'overall_stats' in image_data:
                stats = image_data['overall_stats']
                content = f"Images: {stats.get('total_images', 0)} images - Total Area: {stats.get('total_image_area', 0)} - Avg Size: {stats.get('avg_image_size', 0)}"
                chunks.append({
                    'pdf_document_id': pdf_id,
                    'chunk_type': 'image_analysis',
                    'chunk_index': chunk_index,
                    'content': content,
                    'metadata': {
                        'total_images': stats.get('total_images', 0),
                        'total_image_area': stats.get('total_image_area', 0),
                        'avg_image_size': stats.get('avg_image_size', 0)
                    }
                })
                chunk_index += 1
        
        # Extract from vector analysis
        if 'vector_analysis' in analysis_data:
            vector_data = analysis_data['vector_analysis']
            if 'overall_stats' in vector_data:
                stats = vector_data['overall_stats']
                content = f"Vectors: {stats.get('total_vectors', 0)} vector elements - Types: {stats.get('vector_types', [])}"
                chunks.append({
                    'pdf_document_id': pdf_id,
                    'chunk_type': 'vector_analysis',
                    'chunk_index': chunk_index,
                    'content': content,
                    'metadata': {
                        'total_vectors': stats.get('total_vectors', 0),
                        'vector_types': stats.get('vector_types', [])
                    }
                })
                chunk_index += 1
        
        return chunks
    
    def save_knowledge_chunks(self, chunks: List[Dict]) -> List[str]:
        """Save knowledge chunks to database with embeddings"""
        saved_chunk_ids = []
        
        for chunk in chunks:
            try:
                # Create embedding for the chunk content
                embedding = self.create_embedding(chunk['content'])
                if not embedding:
                    logger.warning(f"Failed to create embedding for chunk {chunk['chunk_index']}")
                    continue
                
                # Save chunk to database
                chunk_id = self.insert_knowledge_chunk(
                    pdf_document_id=chunk['pdf_document_id'],
                    chunk_type=chunk['chunk_type'],
                    chunk_index=chunk['chunk_index'],
                    content=chunk['content'],
                    metadata=chunk.get('metadata', {}),
                    embedding=embedding
                )
                
                if chunk_id:
                    saved_chunk_ids.append(chunk_id)
                    logger.info(f"Saved knowledge chunk {chunk_id} for {chunk['chunk_type']}")
                
            except Exception as e:
                logger.error(f"Error saving knowledge chunk: {e}")
        
        return saved_chunk_ids
    
    def insert_knowledge_chunk(self, pdf_document_id: str, chunk_type: str, chunk_index: int, 
                             content: str, metadata: Dict, embedding: List[float]) -> Optional[str]:
        """Insert a knowledge chunk with embedding"""
        query = """
        INSERT INTO knowledge_chunks (
            pdf_document_id, chunk_type, chunk_index, content, metadata, 
            embedding, embedding_model, embedding_created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        try:
            result = db_manager.execute_query_with_returning(
                query,
                (pdf_document_id, chunk_type, chunk_index, content, 
                 json.dumps(metadata), embedding, self.embedding_model, datetime.now())
            )
            
            if result and len(result) > 0:
                return str(result[0]['id'])
            return None
            
        except Exception as e:
            logger.error(f"Error inserting knowledge chunk: {e}")
            return None
    
    def search_knowledge(self, query_text: str, limit: int = 5, similarity_threshold: float = 0.7) -> List[Dict]:
        """Search knowledge base using vector similarity and text matching"""
        try:
            # Create embedding for query
            query_embedding = self.create_embedding(query_text)
            if not query_embedding:
                logger.error("Failed to create query embedding")
                return []
            
            # Search for chunks using text matching first
            query = """
            SELECT 
                kc.id,
                kc.chunk_type,
                kc.content,
                kc.metadata,
                kc.embedding_created_at,
                kc.created_at,
                kc.chunk_index,
                CASE 
                    WHEN kc.content ILIKE %s THEN 1.0
                    WHEN kc.content ILIKE %s THEN 0.8
                    ELSE 0.5
                END as similarity_score
            FROM knowledge_chunks kc
            WHERE kc.embedding IS NOT NULL
            AND (
                kc.content ILIKE %s 
                OR kc.content ILIKE %s
                OR kc.metadata::text ILIKE %s
            )
            ORDER BY similarity_score DESC, kc.created_at DESC
            LIMIT %s
            """
            
            # Create search patterns
            exact_pattern = f"%{query_text}%"
            word_pattern = f"%{'%'.join(query_text.split())}%"
            
            result = db_manager.execute_query(query, (
                exact_pattern, word_pattern, exact_pattern, word_pattern, exact_pattern, limit
            ))
            
            if result:
                chunks = []
                for row in result:
                    chunk = {
                        'id': row['id'],
                        'chunk_type': row['chunk_type'],
                        'content': row['content'],
                        'metadata': row['metadata'],
                        'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                        'chunk_index': row['chunk_index'],
                        'similarity_score': row['similarity_score']
                    }
                    chunks.append(chunk)
                
                # Filter by similarity threshold
                filtered_chunks = [chunk for chunk in chunks if chunk['similarity_score'] >= similarity_threshold]
                return filtered_chunks[:limit]
            
            # If no text matches, return recent chunks
            fallback_query = """
            SELECT 
                kc.id,
                kc.chunk_type,
                kc.content,
                kc.metadata,
                kc.embedding_created_at,
                kc.created_at,
                kc.chunk_index,
                0.3 as similarity_score
            FROM knowledge_chunks kc
            WHERE kc.embedding IS NOT NULL
            ORDER BY kc.created_at DESC
            LIMIT %s
            """
            
            fallback_result = db_manager.execute_query(fallback_query, (limit,))
            if fallback_result:
                chunks = []
                for row in fallback_result:
                    chunk = {
                        'id': row['id'],
                        'chunk_type': row['chunk_type'],
                        'content': row['content'],
                        'metadata': row['metadata'],
                        'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                        'chunk_index': row['chunk_index'],
                        'similarity_score': row['similarity_score']
                    }
                    chunks.append(chunk)
                return chunks
            
            return []
            
        except Exception as e:
            logger.error(f"Error searching knowledge: {e}")
            return []
    
    def query_knowledge_with_gpt(self, query_text: str, limit: int = 5) -> Dict:
        """Query knowledge base and generate GPT response"""
        try:
            # Search for relevant chunks
            search_results = self.search_knowledge(query_text, limit)
            
            if not search_results:
                return {
                    "success": False,
                    "error": "No relevant knowledge found",
                    "query_text": query_text
                }
            
            # Prepare context for GPT
            context = "\n\n".join([result['content'] for result in search_results])
            
            # Generate GPT response
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that analyzes PDF documents. Use the provided context to answer questions about colors, fonts, layout, images, and other design elements found in PDFs."
                    },
                    {
                        "role": "user",
                        "content": f"Context from PDF analysis:\n\n{context}\n\nQuestion: {query_text}"
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            response_text = response.choices[0].message.content
            
            # Save query and response
            query_id = self.save_knowledge_query(query_text, response_text, search_results)
            
            return {
                "success": True,
                "query_text": query_text,
                "response_text": response_text,
                "sources": search_results,
                "query_id": query_id,
                "total_sources": len(search_results)
            }
            
        except Exception as e:
            logger.error(f"Error querying knowledge with GPT: {e}")
            return {
                "success": False,
                "error": str(e),
                "query_text": query_text
            }
    
    def save_knowledge_query(self, query_text: str, response_text: str, sources: List[Dict]) -> Optional[str]:
        """Save knowledge query and response"""
        try:
            # Create embedding for query
            query_embedding = self.create_embedding(query_text)
            
            # Save query
            query = """
            INSERT INTO knowledge_queries (
                query_text, query_embedding, response_text, response_sources, model_used
            ) VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """
            
            result = db_manager.execute_query_with_returning(
                query,
                (query_text, query_embedding, response_text, 
                 json.dumps([{'chunk_id': s['id'], 'similarity_score': s['similarity_score']} for s in sources]),
                 'gpt-4o')
            )
            
            if result and len(result) > 0:
                query_id = str(result[0]['id'])
                
                # Save search history
                for i, source in enumerate(sources):
                    self.save_search_history(query_id, source['id'], source['similarity_score'], i + 1)
                
                return query_id
            
            return None
            
        except Exception as e:
            logger.error(f"Error saving knowledge query: {e}")
            return None
    
    def save_search_history(self, query_id: str, chunk_id: str, similarity_score: float, rank_position: int):
        """Save search history"""
        query = """
        INSERT INTO knowledge_search_history (
            query_id, chunk_id, similarity_score, rank_position
        ) VALUES (%s, %s, %s, %s)
        """
        
        try:
            db_manager.execute_query(query, (query_id, chunk_id, similarity_score, rank_position), fetch=False)
        except Exception as e:
            logger.error(f"Error saving search history: {e}")
    
    def get_knowledge_stats(self) -> Dict:
        """Get knowledge database statistics"""
        stats = {}
        
        try:
            # Count chunks
            result = db_manager.execute_query("SELECT COUNT(*) as count FROM knowledge_chunks")
            if result:
                stats['total_chunks'] = result[0]['count']
            
            # Count queries
            result = db_manager.execute_query("SELECT COUNT(*) as count FROM knowledge_queries")
            if result:
                stats['total_queries'] = result[0]['count']
            
            # Count chunks by type
            result = db_manager.execute_query("""
                SELECT chunk_type, COUNT(*) as count 
                FROM knowledge_chunks 
                GROUP BY chunk_type
            """)
            if result:
                stats['chunks_by_type'] = {row['chunk_type']: row['count'] for row in result}
            
            # Recent activity
            result = db_manager.execute_query("""
                SELECT COUNT(*) as count 
                FROM knowledge_chunks 
                WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '24 hours'
            """)
            if result:
                stats['recent_chunks_24h'] = result[0]['count']
            
        except Exception as e:
            logger.error(f"Error getting knowledge stats: {e}")
        
        return stats

    def embed_bosch_colors(self, bosch_colors_data: Dict) -> List[str]:
        """Embed Bosch colors JSON data into knowledge base"""
        chunks = []
        chunk_index = 0
        
        try:
            for color_family, color_variants in bosch_colors_data.items():
                if not color_variants:  # Skip empty color families
                    continue
                
                # Create chunk for color family
                family_content = f"Bosch Color Family: {color_family} - Contains {len(color_variants)} color variants"
                chunks.append({
                    'pdf_document_id': None,  # No specific PDF for Bosch colors
                    'chunk_type': 'bosch_colors',
                    'chunk_index': chunk_index,
                    'content': family_content,
                    'metadata': {
                        'color_family': color_family,
                        'variant_count': len(color_variants),
                        'source': 'bosch_colors.json'
                    }
                })
                chunk_index += 1
                
                # Create chunks for each color variant
                for variant_name, color_data in color_variants.items():
                    if isinstance(color_data, dict) and 'hex' in color_data:
                        hex_code = color_data.get('hex', '')
                        rgb = color_data.get('rgb', [])
                        cmyk = color_data.get('cmyk', [])
                        
                        content = f"Bosch Color: {color_family} {variant_name} - Hex: {hex_code} - RGB: {rgb} - CMYK: {cmyk}"
                        
                        chunks.append({
                            'pdf_document_id': None,  # No specific PDF for Bosch colors
                            'chunk_type': 'bosch_colors',
                            'chunk_index': chunk_index,
                            'content': content,
                            'metadata': {
                                'color_family': color_family,
                                'variant_name': variant_name,
                                'hex_code': hex_code,
                                'rgb_values': rgb,
                                'cmyk_values': cmyk,
                                'source': 'bosch_colors.json'
                            }
                        })
                        chunk_index += 1
            
            # Save chunks with embeddings
            if chunks:
                saved_chunk_ids = self.save_knowledge_chunks(chunks)
                logger.info(f"Successfully embedded {len(saved_chunk_ids)} Bosch color chunks")
                return saved_chunk_ids
            else:
                logger.warning("No Bosch color chunks to embed")
                return []
                
        except Exception as e:
            logger.error(f"Error embedding Bosch colors: {e}")
            return []
    
    def search_bosch_colors(self, query_text: str, limit: int = 5, similarity_threshold: float = 0.7) -> List[Dict]:
        """Search for Bosch colors in knowledge base"""
        try:
            # Search for bosch_colors chunks specifically
            query = """
            SELECT kc.id, kc.content, kc.metadata, kc.embedding,
                   kc.created_at, kc.chunk_type, kc.chunk_index
            FROM knowledge_chunks kc
            WHERE kc.chunk_type = 'bosch_colors'
            ORDER BY kc.created_at DESC
            LIMIT %s
            """
            
            results = db_manager.execute_query(query, (limit,))
            if not results:
                return []
            
            # Convert to list of dicts
            chunks = []
            for row in results:
                chunk = {
                    'id': row['id'],
                    'content': row['content'],
                    'metadata': row['metadata'],
                    'chunk_type': row['chunk_type'],
                    'chunk_index': row['chunk_index'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                    'similarity_score': 1.0  # Default score for exact matches
                }
                chunks.append(chunk)
            
            # Filter by similarity threshold (for now, return all as exact matches)
            filtered_chunks = [chunk for chunk in chunks if chunk['similarity_score'] >= similarity_threshold]
            
            return filtered_chunks[:limit]
            
        except Exception as e:
            logger.error(f"Error searching Bosch colors: {e}")
            return []
    
    def get_bosch_color_by_hex(self, hex_code: str) -> Optional[Dict]:
        """Get specific Bosch color by hex code"""
        try:
            # Normalize hex code (remove # if present and convert to uppercase)
            normalized_hex = hex_code.upper().replace('#', '')
            if not normalized_hex.startswith('#'):
                normalized_hex = f"#{normalized_hex}"
            
            query = """
            SELECT kc.id, kc.content, kc.metadata, kc.created_at
            FROM knowledge_chunks kc
            WHERE kc.chunk_type = 'bosch_colors' 
            AND (
                kc.metadata->>'hex_code' = %s
                OR kc.metadata->>'hex_code' = %s
                OR kc.metadata->>'hex_code' ILIKE %s
            )
            LIMIT 1
            """
            
            # Try different formats
            hex_with_hash = normalized_hex
            hex_without_hash = normalized_hex.replace('#', '')
            hex_pattern = f"%{hex_without_hash}%"
            
            results = db_manager.execute_query(query, (hex_with_hash, hex_without_hash, hex_pattern))
            if results:
                row = results[0]
                return {
                    'id': row['id'],
                    'content': row['content'],
                    'metadata': row['metadata'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting Bosch color by hex {hex_code}: {e}")
            return None

# Global knowledge database manager instance
knowledge_db_manager = KnowledgeDatabaseManager()
