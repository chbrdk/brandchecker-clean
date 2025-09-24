#!/usr/bin/env python3
"""
Vector Index Optimization Script
Optimizes PostgreSQL vector indexes for best performance with brand guidelines data
"""

import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VectorIndexOptimizer:
    def __init__(self, db_config):
        """Initialize the index optimizer"""
        self.db_config = db_config
        self.connection = None
    
    def connect(self):
        """Connect to the database"""
        try:
            self.connection = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            logger.info("Connected to database successfully")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from database")
    
    def execute_sql(self, sql, params=None):
        """Execute SQL statement"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"SQL execution failed: {e}")
            self.connection.rollback()
            raise
    
    def get_table_stats(self, table_name):
        """Get table statistics"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        n_tup_ins as inserts,
                        n_tup_upd as updates,
                        n_tup_del as deletes,
                        n_live_tup as live_tuples,
                        n_dead_tup as dead_tuples,
                        last_vacuum,
                        last_autovacuum,
                        last_analyze,
                        last_autoanalyze
                    FROM pg_stat_user_tables 
                    WHERE tablename = %s
                """, (table_name,))
                
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Failed to get table stats: {e}")
            return None
    
    def optimize_vector_indexes(self):
        """Optimize vector indexes for best performance"""
        try:
            logger.info("Starting vector index optimization...")
            
            # 1. Update table statistics
            logger.info("Updating table statistics...")
            self.execute_sql("ANALYZE brand_knowledge_chunks")
            self.execute_sql("ANALYZE knowledge_chunks")
            
            # 2. Recreate vector indexes with optimal parameters
            logger.info("Recreating vector indexes...")
            
            # Drop existing vector indexes
            try:
                self.execute_sql("DROP INDEX IF EXISTS idx_brand_knowledge_chunks_embedding")
                self.execute_sql("DROP INDEX IF EXISTS idx_knowledge_chunks_embedding")
                self.execute_sql("DROP INDEX IF EXISTS idx_knowledge_queries_embedding")
            except Exception as e:
                logger.warning(f"Some indexes may not exist: {e}")
            
            # Get table size to determine optimal index parameters
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT COUNT(*) as count FROM brand_knowledge_chunks WHERE embedding IS NOT NULL
                """)
                embedding_count = cursor.fetchone()['count']
            
            # Calculate optimal lists parameter for ivfflat
            # Rule of thumb: lists = rows / 1000, minimum 10, maximum 1000
            lists = max(10, min(1000, embedding_count // 1000))
            
            logger.info(f"Creating optimized vector indexes with lists={lists}")
            
            # Create optimized vector indexes
            vector_index_sql = f"""
                CREATE INDEX idx_brand_knowledge_chunks_embedding_optimized 
                ON brand_knowledge_chunks 
                USING ivfflat (embedding vector_cosine_ops) 
                WITH (lists = {lists})
            """
            self.execute_sql(vector_index_sql)
            
            # 3. Create additional performance indexes
            logger.info("Creating additional performance indexes...")
            
            # Composite index for brand-specific searches
            self.execute_sql("""
                CREATE INDEX IF NOT EXISTS idx_brand_knowledge_chunks_brand_embedding 
                ON brand_knowledge_chunks (brand_id, chunk_type) 
                WHERE embedding IS NOT NULL
            """)
            
            # Partial index for embedded chunks only
            self.execute_sql("""
                CREATE INDEX IF NOT EXISTS idx_brand_knowledge_chunks_embedded_only 
                ON brand_knowledge_chunks (embedding_created_at, chunk_type) 
                WHERE embedding IS NOT NULL
            """)
            
            # 4. Update PostgreSQL configuration for vector operations
            logger.info("Updating PostgreSQL configuration...")
            
            # These settings optimize vector operations
            optimization_settings = [
                "SET work_mem = '256MB'",  # Increase work memory for vector operations
                "SET maintenance_work_mem = '512MB'",  # Increase maintenance memory
                "SET effective_cache_size = '1GB'",  # Assume 1GB cache
                "SET random_page_cost = 1.1",  # SSD optimization
            ]
            
            for setting in optimization_settings:
                try:
                    self.execute_sql(setting)
                    logger.info(f"Applied setting: {setting}")
                except Exception as e:
                    logger.warning(f"Could not apply setting {setting}: {e}")
            
            # 5. Vacuum and analyze for optimal performance
            logger.info("Running VACUUM and ANALYZE...")
            self.execute_sql("VACUUM ANALYZE brand_knowledge_chunks")
            self.execute_sql("VACUUM ANALYZE knowledge_chunks")
            
            logger.info("Vector index optimization completed successfully!")
            
        except Exception as e:
            logger.error(f"Vector index optimization failed: {e}")
            raise
    
    def create_materialized_views(self):
        """Create materialized views for common queries"""
        try:
            logger.info("Creating materialized views...")
            
            # Brand overview with embedding statistics
            self.execute_sql("""
                CREATE MATERIALIZED VIEW IF NOT EXISTS brand_embedding_overview AS
                SELECT 
                    b.id,
                    b.name,
                    b.slug,
                    COUNT(bkc.id) as total_chunks,
                    COUNT(CASE WHEN bkc.embedding IS NOT NULL THEN 1 END) as embedded_chunks,
                    ROUND(
                        COUNT(CASE WHEN bkc.embedding IS NOT NULL THEN 1 END)::numeric / 
                        NULLIF(COUNT(bkc.id), 0) * 100, 2
                    ) as embedding_coverage_percent,
                    MAX(bkc.embedding_created_at) as last_embedding_update,
                    b.created_at
                FROM brands b
                LEFT JOIN brand_knowledge_chunks bkc ON b.id = bkc.brand_id
                GROUP BY b.id, b.name, b.slug, b.created_at
                ORDER BY b.name
            """)
            
            # Embedding quality metrics
            self.execute_sql("""
                CREATE MATERIALIZED VIEW IF NOT EXISTS embedding_quality_metrics AS
                SELECT 
                    bkc.chunk_type,
                    COUNT(*) as total_chunks,
                    AVG(LENGTH(bkc.content)) as avg_content_length,
                    COUNT(CASE WHEN bkc.embedding IS NOT NULL THEN 1 END) as embedded_count,
                    ROUND(
                        COUNT(CASE WHEN bkc.embedding IS NOT NULL THEN 1 END)::numeric / 
                        COUNT(*) * 100, 2
                    ) as embedding_rate,
                    MAX(bkc.embedding_created_at) as last_update
                FROM brand_knowledge_chunks bkc
                GROUP BY bkc.chunk_type
                ORDER BY embedding_rate DESC
            """)
            
            # Create indexes on materialized views
            self.execute_sql("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_brand_embedding_overview_id 
                ON brand_embedding_overview (id)
            """)
            
            self.execute_sql("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_embedding_quality_metrics_type 
                ON embedding_quality_metrics (chunk_type)
            """)
            
            logger.info("Materialized views created successfully!")
            
        except Exception as e:
            logger.error(f"Failed to create materialized views: {e}")
            raise
    
    def refresh_materialized_views(self):
        """Refresh materialized views with latest data"""
        try:
            logger.info("Refreshing materialized views...")
            
            self.execute_sql("REFRESH MATERIALIZED VIEW brand_embedding_overview")
            self.execute_sql("REFRESH MATERIALIZED VIEW embedding_quality_metrics")
            
            logger.info("Materialized views refreshed successfully!")
            
        except Exception as e:
            logger.error(f"Failed to refresh materialized views: {e}")
            raise
    
    def generate_performance_report(self):
        """Generate a performance report"""
        try:
            logger.info("Generating performance report...")
            
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get embedding statistics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_chunks,
                        COUNT(CASE WHEN embedding IS NOT NULL THEN 1 END) as embedded_chunks,
                        ROUND(
                            COUNT(CASE WHEN embedding IS NOT NULL THEN 1 END)::numeric / 
                            COUNT(*) * 100, 2
                        ) as embedding_coverage
                    FROM brand_knowledge_chunks
                """)
                
                embedding_stats = cursor.fetchone()
                
                # Get index statistics
                cursor.execute("""
                    SELECT 
                        indexname,
                        indexdef
                    FROM pg_indexes 
                    WHERE tablename = 'brand_knowledge_chunks' 
                    AND indexname LIKE '%embedding%'
                    ORDER BY indexname
                """)
                
                embedding_indexes = cursor.fetchall()
                
                # Get table sizes
                cursor.execute("""
                    SELECT 
                        pg_size_pretty(pg_total_relation_size('brand_knowledge_chunks')) as table_size,
                        pg_size_pretty(pg_relation_size('brand_knowledge_chunks')) as data_size
                """)
                
                size_stats = cursor.fetchone()
                
                logger.info("=== PERFORMANCE REPORT ===")
                logger.info(f"Total chunks: {embedding_stats['total_chunks']}")
                logger.info(f"Embedded chunks: {embedding_stats['embedded_chunks']}")
                logger.info(f"Embedding coverage: {embedding_stats['embedding_coverage']}%")
                logger.info(f"Table size: {size_stats['table_size']}")
                logger.info(f"Data size: {size_stats['data_size']}")
                logger.info(f"Vector indexes: {len(embedding_indexes)}")
                
                for idx in embedding_indexes:
                    logger.info(f"  - {idx['indexname']}")
                
                return {
                    'embedding_stats': dict(embedding_stats),
                    'size_stats': dict(size_stats),
                    'indexes': [dict(idx) for idx in embedding_indexes]
                }
                
        except Exception as e:
            logger.error(f"Failed to generate performance report: {e}")
            return None


def main():
    """Main function to run the optimization"""
    # Database configuration
    db_config = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5433'),
        'database': os.getenv('POSTGRES_DB', 'brandchecker'),
        'user': os.getenv('POSTGRES_USER', 'brandchecker_user'),
        'password': os.getenv('POSTGRES_PASSWORD', 'brandchecker_password')
    }
    
    # Initialize optimizer
    optimizer = VectorIndexOptimizer(db_config)
    
    try:
        # Connect to database
        optimizer.connect()
        
        # Run optimization
        optimizer.optimize_vector_indexes()
        optimizer.create_materialized_views()
        optimizer.refresh_materialized_views()
        
        # Generate report
        report = optimizer.generate_performance_report()
        
        logger.info("Vector index optimization completed successfully!")
        
    except Exception as e:
        logger.error(f"Optimization process failed: {e}")
        raise
    
    finally:
        optimizer.disconnect()


if __name__ == "__main__":
    main()
