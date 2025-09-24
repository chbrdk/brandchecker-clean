#!/usr/bin/env python3
"""
Importiert optimierte Brand-Daten in die PostgreSQL-Datenbank
"""

import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from typing import Dict, List, Any

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizedDataImporter:
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self.conn = None
    
    def connect_db(self):
        """Verbindung zur Datenbank herstellen"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.autocommit = True
            logger.info("Verbindung zur Datenbank hergestellt")
        except Exception as e:
            logger.error(f"Datenbankverbindung fehlgeschlagen: {e}")
            raise
    
    def disconnect_db(self):
        """Verbindung zur Datenbank schließen"""
        if self.conn:
            self.conn.close()
            logger.info("Datenbankverbindung geschlossen")
    
    def clear_existing_data(self):
        """Löscht vorhandene Brand-Daten"""
        logger.info("Lösche vorhandene Brand-Daten...")
        
        cursor = self.conn.cursor()
        try:
            # Lösche in umgekehrter Reihenfolge der Abhängigkeiten
            tables = [
                'brand_knowledge_chunks',
                'page_content',
                'page_sections', 
                'guideline_pages',
                'brand_assets',
                'asset_libraries',
                'brands'
            ]
            
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
                logger.info(f"Gelöscht: {table}")
            
            # Setze Sequenzen zurück
            cursor.execute("SELECT setval('brands_id_seq', 1, false)")
            cursor.execute("SELECT setval('asset_libraries_id_seq', 1, false)")
            cursor.execute("SELECT setval('brand_assets_id_seq', 1, false)")
            cursor.execute("SELECT setval('guideline_pages_id_seq', 1, false)")
            cursor.execute("SELECT setval('page_sections_id_seq', 1, false)")
            cursor.execute("SELECT setval('page_content_id_seq', 1, false)")
            cursor.execute("SELECT setval('brand_knowledge_chunks_id_seq', 1, false)")
            
            logger.info("Datenbank zurückgesetzt")
            
        except Exception as e:
            logger.error(f"Fehler beim Löschen der Daten: {e}")
            raise
        finally:
            cursor.close()
    
    def import_brands(self, graphql_data: Dict) -> int:
        """Importiert Brands"""
        logger.info("Importiere Brands...")
        
        cursor = self.conn.cursor()
        brand_id = None
        
        try:
            # Erstelle einen Standard-Brand
            cursor.execute("""
                INSERT INTO brands (name, description, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
                RETURNING id
            """, ("Bosch", "Bosch Brand Guidelines", ))
            
            brand_id = cursor.fetchone()[0]
            logger.info(f"Brand erstellt: ID {brand_id}")
            
        except Exception as e:
            logger.error(f"Fehler beim Import der Brands: {e}")
            raise
        finally:
            cursor.close()
        
        return brand_id
    
    def import_assets(self, graphql_data: Dict, brand_id: int):
        """Importiert Assets"""
        logger.info("Importiere Assets...")
        
        cursor = self.conn.cursor()
        
        try:
            # Erstelle Asset Library
            cursor.execute("""
                INSERT INTO asset_libraries (brand_id, name, description, created_at, updated_at)
                VALUES (%s, %s, %s, NOW(), NOW())
                RETURNING id
            """, (brand_id, "Bosch Assets", "Bosch Brand Assets"))
            
            library_id = cursor.fetchone()[0]
            
            # Importiere Assets
            assets = graphql_data.get('assets', [])
            for asset in assets:
                cursor.execute("""
                    INSERT INTO brand_assets (library_id, name, asset_type, url, description, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (library_id, name) DO UPDATE SET
                        asset_type = EXCLUDED.asset_type,
                        url = EXCLUDED.url,
                        description = EXCLUDED.description,
                        updated_at = NOW()
                """, (
                    library_id,
                    asset.get('name', 'Unknown Asset'),
                    asset.get('type', 'unknown'),
                    asset.get('url', ''),
                    asset.get('description', '')
                ))
            
            logger.info(f"Importiert: {len(assets)} Assets")
            
        except Exception as e:
            logger.error(f"Fehler beim Import der Assets: {e}")
            raise
        finally:
            cursor.close()
    
    def import_guidelines(self, html_data: Dict, brand_id: int):
        """Importiert Guideline-Seiten"""
        logger.info("Importiere Guideline-Seiten...")
        
        cursor = self.conn.cursor()
        
        try:
            # Erstelle Guideline-Seite
            cursor.execute("""
                INSERT INTO guideline_pages (brand_id, title, url, created_at, updated_at)
                VALUES (%s, %s, %s, NOW(), NOW())
                RETURNING id
            """, (brand_id, "Bosch Brand Guidelines", "https://brand.bosch.com"))
            
            page_id = cursor.fetchone()[0]
            
            # Erstelle Sektion
            cursor.execute("""
                INSERT INTO page_sections (page_id, heading, order_index, created_at, updated_at)
                VALUES (%s, %s, %s, NOW(), NOW())
                RETURNING id
            """, (page_id, "Brand Guidelines Content", 1))
            
            section_id = cursor.fetchone()[0]
            
            # Importiere Seiten-Inhalte
            pages = html_data.get('pages', [])
            for i, page in enumerate(pages):
                content = page.get('content', '')
                if len(content) > 10:  # Nur sinnvolle Inhalte
                    cursor.execute("""
                        INSERT INTO page_content (section_id, content_type, content, order_index, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, NOW(), NOW())
                        ON CONFLICT (section_id, order_index) DO UPDATE SET
                            content_type = EXCLUDED.content_type,
                            content = EXCLUDED.content,
                            updated_at = NOW()
                    """, (section_id, 'text', content, i + 1))
            
            logger.info(f"Importiert: {len(pages)} Seiten-Inhalte")
            
        except Exception as e:
            logger.error(f"Fehler beim Import der Guidelines: {e}")
            raise
        finally:
            cursor.close()
    
    def create_knowledge_chunks(self, html_data: Dict, brand_id: int):
        """Erstellt Knowledge Chunks für die Suche"""
        logger.info("Erstelle Knowledge Chunks...")
        
        cursor = self.conn.cursor()
        
        try:
            # Erstelle Chunks aus Seiten-Inhalten
            pages = html_data.get('pages', [])
            for i, page in enumerate(pages):
                content = page.get('content', '')
                if len(content) > 20:  # Nur sinnvolle Chunks
                    cursor.execute("""
                        INSERT INTO brand_knowledge_chunks (brand_id, content, content_type, metadata, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, NOW(), NOW())
                    """, (
                        brand_id,
                        content,
                        'text',
                        json.dumps({
                            'source': 'html',
                            'has_colors': page.get('has_colors', False),
                            'original_length': page.get('original_length', len(content))
                        })
                    ))
            
            # Erstelle spezielle Chunks für Farben
            colors = html_data.get('colors', [])
            for color in colors:
                color_content = f"Bosch Brand Color: {color['name']} - {color['value']} ({color['type']})"
                cursor.execute("""
                    INSERT INTO brand_knowledge_chunks (brand_id, content, content_type, metadata, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, NOW(), NOW())
                """, (
                    brand_id,
                    color_content,
                    'color',
                    json.dumps({
                        'color_type': color['type'],
                        'color_value': color['value'],
                        'color_name': color['name'],
                        'context': color.get('context', '')
                    })
                ))
            
            logger.info(f"Erstellt: {len(pages)} Text-Chunks, {len(colors)} Farb-Chunks")
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen der Knowledge Chunks: {e}")
            raise
        finally:
            cursor.close()
    
    def import_optimized_data(self, html_file: str, graphql_file: str):
        """Importiert optimierte Daten"""
        logger.info("Starte Import der optimierten Daten...")
        
        # Lade optimierte Daten
        with open(html_file, 'r', encoding='utf-8') as f:
            html_data = json.load(f)
        
        with open(graphql_file, 'r', encoding='utf-8') as f:
            graphql_data = json.load(f)
        
        # Lösche vorhandene Daten
        self.clear_existing_data()
        
        # Importiere Brands
        brand_id = self.import_brands(graphql_data)
        
        # Importiere Assets
        self.import_assets(graphql_data, brand_id)
        
        # Importiere Guidelines
        self.import_guidelines(html_data, brand_id)
        
        # Erstelle Knowledge Chunks
        self.create_knowledge_chunks(html_data, brand_id)
        
        logger.info("Import der optimierten Daten abgeschlossen!")

def main():
    """Hauptfunktion"""
    logger.info("Starte Import der optimierten Brand-Daten...")
    
    # Datenbank-Konfiguration
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'brandchecker'),
        'user': os.getenv('DB_USER', 'brandchecker'),
        'password': os.getenv('DB_PASSWORD', 'brandchecker')
    }
    
    # Pfade zu den optimierten Daten
    html_file = "shared/JSON/optimized/html_optimized.json"
    graphql_file = "shared/JSON/optimized/graphql_optimized.json"
    
    # Prüfe ob optimierte Daten existieren
    if not os.path.exists(html_file):
        logger.error(f"Optimierte HTML-Daten nicht gefunden: {html_file}")
        logger.info("Führe zuerst optimize_brand_data.py aus!")
        return
    
    if not os.path.exists(graphql_file):
        logger.error(f"Optimierte GraphQL-Daten nicht gefunden: {graphql_file}")
        logger.info("Führe zuerst optimize_brand_data.py aus!")
        return
    
    # Importiere Daten
    importer = OptimizedDataImporter(db_config)
    try:
        importer.connect_db()
        importer.import_optimized_data(html_file, graphql_file)
    except Exception as e:
        logger.error(f"Import fehlgeschlagen: {e}")
        raise
    finally:
        importer.disconnect_db()

if __name__ == "__main__":
    main()
