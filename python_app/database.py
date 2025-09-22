"""
Database connection and operations for Brandchecker
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from psycopg2.pool import SimpleConnectionPool

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database manager for Brandchecker application"""
    
    def __init__(self):
        self.connection_pool = None
        self.init_connection_pool()
    
    def init_connection_pool(self):
        """Initialize the database connection pool"""
        try:
            # Get database configuration from environment variables
            db_config = {
                'host': os.getenv('POSTGRES_HOST', 'brandchecker-postgres'),
                'port': os.getenv('POSTGRES_PORT', '5432'),
                'database': os.getenv('POSTGRES_DB', 'brandchecker'),
                'user': os.getenv('POSTGRES_USER', 'brandchecker_user'),
                'password': os.getenv('POSTGRES_PASSWORD', 'brandchecker_password')
            }
            
            # Create connection pool
            self.connection_pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                **db_config
            )
            logger.info("Database connection pool initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            self.connection_pool = None
    
    def get_connection(self):
        """Get a connection from the pool"""
        if self.connection_pool:
            return self.connection_pool.getconn()
        return None
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        if self.connection_pool and conn:
            self.connection_pool.putconn(conn)
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """Execute a database query"""
        conn = None
        try:
            conn = self.get_connection()
            if not conn:
                logger.error("No database connection available")
                return None
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.rowcount
            
            cursor.close()
            return result
            
        except Exception as e:
            logger.error(f"Database query error: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                self.return_connection(conn)
    
    def execute_query_with_returning(self, query: str, params: tuple = None):
        """Execute a database query with RETURNING clause"""
        conn = None
        try:
            conn = self.get_connection()
            if not conn:
                logger.error("No database connection available")
                return None
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            
            result = cursor.fetchall()
            conn.commit()
            
            cursor.close()
            return result
            
        except Exception as e:
            logger.error(f"Database query error: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                self.return_connection(conn)
    
    def insert_pdf_document(self, filename: str, filepath: str, file_size: int = None, page_count: int = None) -> Optional[str]:
        """Insert a new PDF document record"""
        query = """
        INSERT INTO pdf_documents (filename, filepath, file_size, page_count, analysis_status)
        VALUES (%s, %s, %s, %s, 'pending')
        ON CONFLICT (filepath) DO UPDATE SET
            filename = EXCLUDED.filename,
            file_size = EXCLUDED.file_size,
            page_count = EXCLUDED.page_count,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id
        """
        
        result = self.execute_query_with_returning(query, (filename, filepath, file_size, page_count))
        if result and len(result) > 0:
            return str(result[0]['id'])
        return None
    
    def update_analysis_status(self, pdf_id: str, status: str, completed: bool = False):
        """Update the analysis status of a PDF document"""
        query = """
        UPDATE pdf_documents 
        SET analysis_status = %s, 
            analysis_completed_at = CASE WHEN %s THEN CURRENT_TIMESTAMP ELSE analysis_completed_at END,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        
        return self.execute_query(query, (status, completed, pdf_id), fetch=False)
    
    def insert_color_analysis(self, pdf_id: str, analysis_type: str, analysis_data: Dict) -> Optional[str]:
        """Insert color analysis results"""
        query = """
        INSERT INTO color_analysis (pdf_document_id, analysis_type, total_colors, primary_color_space, color_management_strategy, analysis_data)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (pdf_document_id, analysis_type) DO UPDATE SET
            total_colors = EXCLUDED.total_colors,
            primary_color_space = EXCLUDED.primary_color_space,
            color_management_strategy = EXCLUDED.color_management_strategy,
            analysis_data = EXCLUDED.analysis_data,
            created_at = CURRENT_TIMESTAMP
        RETURNING id
        """
        
        total_colors = analysis_data.get('total_colors', 0)
        primary_color_space = analysis_data.get('primary_color_space', 'Unknown')
        color_management_strategy = analysis_data.get('color_management_strategy', 'Unknown')
        
        result = self.execute_query_with_returning(
            query, 
            (pdf_id, analysis_type, total_colors, primary_color_space, color_management_strategy, Json(analysis_data))
        )
        
        if result and len(result) > 0:
            return str(result[0]['id'])
        return None
    
    def insert_colors(self, color_analysis_id: str, colors: List[Dict]):
        """Insert individual color records"""
        if not colors:
            return
        
        query = """
        INSERT INTO colors (
            color_analysis_id, name, hex_code, rgb_values, rgb_precise, 
            cmyk_values, color_space, usage_count, usage_percentage, 
            sources, corrected_hex, corrected_rgb, correction_distance, original_values
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for color in colors:
            try:
                params = (
                    color_analysis_id,
                    color.get('name', ''),
                    color.get('hex', ''),
                    color.get('rgb', []),
                    color.get('rgb_precise', []),
                    color.get('cmyk', []),
                    color.get('color_space', ''),
                    color.get('usage_count', 0),
                    color.get('usage_percentage', 0.0),
                    color.get('sources', []),
                    color.get('corrected_hex', ''),
                    color.get('corrected_rgb', []),
                    color.get('correction_distance', 0.0),
                    color.get('original_values', [])
                )
                self.execute_query(query, params, fetch=False)
            except Exception as e:
                logger.error(f"Error inserting color {color.get('hex', 'unknown')}: {e}")
    
    def insert_complete_analysis(self, pdf_id: str, analysis_summary: Dict, complete_data: Dict, processing_time: float = None):
        """Insert complete analysis results"""
        query = """
        INSERT INTO complete_analysis (pdf_document_id, analysis_summary, complete_data, processing_time)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (pdf_document_id) DO UPDATE SET
            analysis_summary = EXCLUDED.analysis_summary,
            complete_data = EXCLUDED.complete_data,
            processing_time = EXCLUDED.processing_time,
            created_at = CURRENT_TIMESTAMP
        """
        
        return self.execute_query(query, (pdf_id, Json(analysis_summary), Json(complete_data), processing_time), fetch=False)
    
    def get_recent_analyses(self, limit: int = 10) -> List[Dict]:
        """Get recent analyses from the database"""
        query = """
        SELECT * FROM recent_analyses 
        ORDER BY created_at DESC 
        LIMIT %s
        """
        
        result = self.execute_query(query, (limit,))
        if result:
            return [dict(row) for row in result]
        return []
    
    def get_pdf_document(self, pdf_id: str) -> Optional[Dict]:
        """Get a PDF document by ID"""
        query = "SELECT * FROM pdf_documents WHERE id = %s"
        result = self.execute_query(query, (pdf_id,))
        if result:
            return dict(result[0])
        return None
    
    def get_pdf_document_by_filepath(self, filepath: str) -> Optional[Dict]:
        """Get a PDF document by filepath"""
        query = "SELECT * FROM pdf_documents WHERE filepath = %s"
        result = self.execute_query(query, (filepath,))
        if result:
            return dict(result[0])
        return None
    
    def get_color_analysis(self, pdf_id: str, analysis_type: str = 'all_colors') -> Optional[Dict]:
        """Get color analysis for a PDF document"""
        query = """
        SELECT ca.*, array_agg(c.*) as colors
        FROM color_analysis ca
        LEFT JOIN colors c ON ca.id = c.color_analysis_id
        WHERE ca.pdf_document_id = %s AND ca.analysis_type = %s
        GROUP BY ca.id
        """
        
        result = self.execute_query(query, (pdf_id, analysis_type))
        if result:
            return dict(result[0])
        return None
    
    def search_colors(self, hex_code: str = None, color_space: str = None, limit: int = 50) -> List[Dict]:
        """Search for colors in the database"""
        query = "SELECT * FROM colors WHERE 1=1"
        params = []
        
        if hex_code:
            query += " AND hex_code ILIKE %s"
            params.append(f"%{hex_code}%")
        
        if color_space:
            query += " AND color_space = %s"
            params.append(color_space)
        
        query += " ORDER BY usage_count DESC LIMIT %s"
        params.append(limit)
        
        result = self.execute_query(query, tuple(params))
        if result:
            return [dict(row) for row in result]
        return []
    
    def cleanup_old_analyses(self, days: int = 30):
        """Clean up old analysis data"""
        query = """
        DELETE FROM pdf_documents 
        WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '%s days'
        AND analysis_status = 'completed'
        """
        
        return self.execute_query(query, (days,), fetch=False)
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        stats = {}
        
        # Count documents
        result = self.execute_query("SELECT COUNT(*) as count FROM pdf_documents")
        if result:
            stats['total_documents'] = result[0]['count']
        
        # Count analyses
        result = self.execute_query("SELECT COUNT(*) as count FROM complete_analysis")
        if result:
            stats['total_analyses'] = result[0]['count']
        
        # Count colors
        result = self.execute_query("SELECT COUNT(*) as count FROM colors")
        if result:
            stats['total_colors'] = result[0]['count']
        
        # Recent activity
        result = self.execute_query("""
            SELECT COUNT(*) as count 
            FROM pdf_documents 
            WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '24 hours'
        """)
        if result:
            stats['recent_documents_24h'] = result[0]['count']
        
        return stats

# Global database manager instance
db_manager = DatabaseManager()
