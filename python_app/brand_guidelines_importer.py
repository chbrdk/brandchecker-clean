#!/usr/bin/env python3
"""
Brand Guidelines Data Importer
Imports GraphQL and HTML data into the PostgreSQL database for LLM analysis
"""

import json
import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BrandGuidelinesImporter:
    def __init__(self, db_config: Dict[str, str]):
        """Initialize the importer with database configuration"""
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
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False) -> Optional[List[Dict]]:
        """Execute a database query"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            self.connection.rollback()
            raise
    
    def get_brand_id(self, external_id: str) -> Optional[str]:
        """Get brand ID by external ID"""
        query = "SELECT id FROM brands WHERE external_id = %s"
        result = self.execute_query(query, (external_id,), fetch=True)
        return result[0]['id'] if result else None
    
    def import_graphql_data(self, graphql_file: str) -> bool:
        """Import GraphQL brand data"""
        try:
            with open(graphql_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info("Starting GraphQL data import...")
            
            # Import brand data
            brand_data = data.get('brand', {})
            if brand_data:
                brand_id = self.import_brand(brand_data)
                if not brand_id:
                    logger.error("Failed to import brand data")
                    return False
                
                # Import asset libraries
                libraries_data = data.get('libraries', [])
                for library_data in libraries_data:
                    library_id = self.import_asset_library(brand_id, library_data)
                    if library_id:
                        # Import assets for this library
                        assets_data = data.get('assets', {}).get('by_library', [])
                        for library_assets in assets_data:
                            if library_assets.get('library') == library_data.get('name'):
                                self.import_assets(library_id, library_assets.get('assets', []))
            
            logger.info("GraphQL data import completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"GraphQL import failed: {e}")
            return False
    
    def import_brand(self, brand_data: Dict[str, Any]) -> Optional[str]:
        """Import brand information"""
        try:
            external_id = brand_data.get('id')
            name = brand_data.get('name')
            slug = brand_data.get('slug')
            
            # Extract color information
            color_data = brand_data.get('color', {})
            rgb_data = color_data.get('rgb', {})
            primary_color_hex = color_data.get('hex')
            primary_color_rgb = [rgb_data.get('r'), rgb_data.get('g'), rgb_data.get('b')] if rgb_data else None
            
            query = """
                INSERT INTO brands (external_id, name, slug, primary_color_hex, primary_color_rgb)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (external_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    slug = EXCLUDED.slug,
                    primary_color_hex = EXCLUDED.primary_color_hex,
                    primary_color_rgb = EXCLUDED.primary_color_rgb,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """
            
            result = self.execute_query(query, (external_id, name, slug, primary_color_hex, primary_color_rgb), fetch=True)
            brand_id = result[0]['id'] if result else None
            
            if brand_id:
                logger.info(f"Brand imported successfully: {name} (ID: {brand_id})")
            
            return brand_id
            
        except Exception as e:
            logger.error(f"Failed to import brand: {e}")
            return None
    
    def import_asset_library(self, brand_id: str, library_data: Dict[str, Any]) -> Optional[str]:
        """Import asset library"""
        try:
            external_id = library_data.get('id')
            name = library_data.get('name')
            asset_count = library_data.get('asset_count', 0)
            asset_types = library_data.get('asset_types', [])
            
            query = """
                INSERT INTO asset_libraries (brand_id, external_id, name, asset_count, asset_types)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (brand_id, external_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    asset_count = EXCLUDED.asset_count,
                    asset_types = EXCLUDED.asset_types,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """
            
            result = self.execute_query(query, (brand_id, external_id, name, asset_count, asset_types), fetch=True)
            library_id = result[0]['id'] if result else None
            
            if library_id:
                logger.info(f"Asset library imported: {name} (ID: {library_id})")
            
            return library_id
            
        except Exception as e:
            logger.error(f"Failed to import asset library: {e}")
            return None
    
    def import_assets(self, library_id: str, assets_data: List[Dict[str, Any]]):
        """Import assets for a library"""
        try:
            for asset_data in assets_data:
                external_id = asset_data.get('id')
                title = asset_data.get('title')
                asset_type = asset_data.get('type')
                download_url = asset_data.get('download_url')
                preview_url = asset_data.get('preview_url')
                
                # Extract dimensions
                dimensions = asset_data.get('dimensions', {})
                width = dimensions.get('width')
                height = dimensions.get('height')
                
                size_bytes = asset_data.get('size_bytes')
                modified_at = asset_data.get('modified_at')
                
                # Extract file extension from title or type
                file_extension = asset_type if asset_type else None
                
                query = """
                    INSERT INTO brand_assets (library_id, external_id, title, asset_type, 
                                            download_url, preview_url, width, height, 
                                            size_bytes, file_extension, modified_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (library_id, external_id) DO UPDATE SET
                        title = EXCLUDED.title,
                        asset_type = EXCLUDED.asset_type,
                        download_url = EXCLUDED.download_url,
                        preview_url = EXCLUDED.preview_url,
                        width = EXCLUDED.width,
                        height = EXCLUDED.height,
                        size_bytes = EXCLUDED.size_bytes,
                        file_extension = EXCLUDED.file_extension,
                        modified_at = EXCLUDED.modified_at,
                        updated_at = CURRENT_TIMESTAMP
                """
                
                self.execute_query(query, (
                    library_id, external_id, title, asset_type,
                    download_url, preview_url, width, height,
                    size_bytes, file_extension, modified_at
                ))
            
            logger.info(f"Imported {len(assets_data)} assets for library {library_id}")
            
        except Exception as e:
            logger.error(f"Failed to import assets: {e}")
    
    def import_html_data(self, html_file: str) -> bool:
        """Import HTML guideline data"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info("Starting HTML data import...")
            
            # Get brand ID (assuming Bosch for now)
            brand_id = self.get_brand_id('eyJpZGVudGlmaWVyIjoxMDcsInR5cGUiOiJicmFuZCJ9')
            if not brand_id:
                logger.error("Brand not found. Please import GraphQL data first.")
                return False
            
            # Import guideline pages
            guideline_pages = data.get('guideline_pages', {})
            for page_path, page_data in guideline_pages.items():
                page_id = self.import_guideline_page(brand_id, page_path, page_data)
                if page_id:
                    # Import page sections and content
                    self.import_page_sections(page_id, page_data.get('sections', []))
                    self.import_page_content(page_id, page_data)
            
            logger.info("HTML data import completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"HTML import failed: {e}")
            return False
    
    def import_guideline_page(self, brand_id: str, page_path: str, page_data: Dict[str, Any]) -> Optional[str]:
        """Import guideline page"""
        try:
            title = page_data.get('title', '')
            url = page_data.get('url', '')
            
            query = """
                INSERT INTO guideline_pages (brand_id, page_path, title, url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (brand_id, page_path) DO UPDATE SET
                    title = EXCLUDED.title,
                    url = EXCLUDED.url,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """
            
            result = self.execute_query(query, (brand_id, page_path, title, url), fetch=True)
            page_id = result[0]['id'] if result else None
            
            if page_id:
                logger.info(f"Guideline page imported: {title} (ID: {page_id})")
            
            return page_id
            
        except Exception as e:
            logger.error(f"Failed to import guideline page: {e}")
            return None
    
    def import_page_sections(self, page_id: str, sections: List[Dict[str, Any]]):
        """Import page sections (headings)"""
        try:
            for i, section in enumerate(sections):
                heading_level = section.get('level', '')
                text = section.get('text', '')
                
                query = """
                    INSERT INTO page_sections (page_id, heading_level, text, section_order)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (page_id, section_order) DO UPDATE SET
                        heading_level = EXCLUDED.heading_level,
                        text = EXCLUDED.text
                """
                
                self.execute_query(query, (page_id, heading_level, text, i))
            
            logger.info(f"Imported {len(sections)} sections for page {page_id}")
            
        except Exception as e:
            logger.error(f"Failed to import page sections: {e}")
    
    def import_page_content(self, page_id: str, page_data: Dict[str, Any]):
        """Import page content (paragraphs, lists)"""
        try:
            content_order = 0
            
            # Import paragraphs
            paragraphs = page_data.get('paragraphs', [])
            for paragraph in paragraphs:
                query = """
                    INSERT INTO page_content (page_id, content_type, content, content_order)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (page_id, content_order) DO UPDATE SET
                        content_type = EXCLUDED.content_type,
                        content = EXCLUDED.content
                """
                
                self.execute_query(query, (page_id, 'paragraph', paragraph, content_order))
                content_order += 1
            
            # Import list items
            list_items = page_data.get('listItems', [])
            for list_item in list_items:
                query = """
                    INSERT INTO page_content (page_id, content_type, content, content_order)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (page_id, content_order) DO UPDATE SET
                        content_type = EXCLUDED.content_type,
                        content = EXCLUDED.content
                """
                
                self.execute_query(query, (page_id, 'list_item', list_item, content_order))
                content_order += 1
            
            # Import navigation items
            navigation = page_data.get('navigation', [])
            for nav_item in navigation:
                query = """
                    INSERT INTO page_content (page_id, content_type, content, content_order)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (page_id, content_order) DO UPDATE SET
                        content_type = EXCLUDED.content_type,
                        content = EXCLUDED.content
                """
                
                nav_text = f"{nav_item.get('text', '')} -> {nav_item.get('href', '')}"
                self.execute_query(query, (page_id, 'navigation', nav_text, content_order))
                content_order += 1
            
            logger.info(f"Imported content for page {page_id}")
            
        except Exception as e:
            logger.error(f"Failed to import page content: {e}")
    
    def create_knowledge_chunks(self, brand_id: str) -> bool:
        """Create knowledge chunks for LLM analysis"""
        try:
            logger.info("Creating knowledge chunks for brand guidelines...")
            
            # Create chunks from asset descriptions
            query = """
                INSERT INTO brand_knowledge_chunks (brand_id, chunk_type, source_type, source_id, 
                                                  chunk_index, content, metadata)
                SELECT 
                    %s,
                    'asset_description',
                    'graphql_asset',
                    ba.id::text,
                    0,
                    CONCAT('Asset: ', ba.title, ' (Type: ', ba.asset_type, ', Size: ', 
                           COALESCE(ba.width, 0), 'x', COALESCE(ba.height, 0), ')'),
                    jsonb_build_object(
                        'asset_type', ba.asset_type,
                        'library', al.name,
                        'dimensions', jsonb_build_object('width', ba.width, 'height', ba.height),
                        'size_bytes', ba.size_bytes
                    )
                FROM brand_assets ba
                JOIN asset_libraries al ON ba.library_id = al.id
                WHERE al.brand_id = %s
            """
            
            self.execute_query(query, (brand_id, brand_id))
            
            # Create chunks from guideline content
            query = """
                INSERT INTO brand_knowledge_chunks (brand_id, chunk_type, source_type, source_id, 
                                                  chunk_index, content, metadata)
                SELECT 
                    %s,
                    'guideline_text',
                    'html_page',
                    gp.id::text,
                    pc.content_order,
                    pc.content,
                    jsonb_build_object(
                        'content_type', pc.content_type,
                        'page_title', gp.title,
                        'page_path', gp.page_path
                    )
                FROM page_content pc
                JOIN guideline_pages gp ON pc.page_id = gp.id
                WHERE gp.brand_id = %s
                AND pc.content IS NOT NULL 
                AND LENGTH(TRIM(pc.content)) > 10
            """
            
            self.execute_query(query, (brand_id, brand_id))
            
            logger.info("Knowledge chunks created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create knowledge chunks: {e}")
            return False


def main():
    """Main function to run the importer"""
    # Database configuration
    db_config = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5433'),
        'database': os.getenv('POSTGRES_DB', 'brandchecker'),
        'user': os.getenv('POSTGRES_USER', 'brandchecker_user'),
        'password': os.getenv('POSTGRES_PASSWORD', 'brandchecker_password')
    }
    
    # File paths
    graphql_file = '/shared/JSON/graphql.json'
    html_file = '/shared/JSON/html.json'
    
    # Initialize importer
    importer = BrandGuidelinesImporter(db_config)
    
    try:
        # Connect to database
        importer.connect()
        
        # Import GraphQL data
        if os.path.exists(graphql_file):
            logger.info("Importing GraphQL data...")
            if importer.import_graphql_data(graphql_file):
                logger.info("GraphQL import successful")
            else:
                logger.error("GraphQL import failed")
                return False
        else:
            logger.warning(f"GraphQL file not found: {graphql_file}")
        
        # Import HTML data
        if os.path.exists(html_file):
            logger.info("Importing HTML data...")
            if importer.import_html_data(html_file):
                logger.info("HTML import successful")
            else:
                logger.error("HTML import failed")
                return False
        else:
            logger.warning(f"HTML file not found: {html_file}")
        
        # Create knowledge chunks
        brand_id = importer.get_brand_id('eyJpZGVudGlmaWVyIjoxMDcsInR5cGUiOiJicmFuZCJ9')
        if brand_id:
            importer.create_knowledge_chunks(brand_id)
        
        logger.info("Brand guidelines import completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Import process failed: {e}")
        return False
    
    finally:
        importer.disconnect()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
