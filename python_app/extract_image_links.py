#!/usr/bin/env python3
"""
Image-Links-Extraktor für Brand Guidelines
Extrahiert alle Bild-URLs aus HTML- und GraphQL-JSON für GPT-5 Bildanalyse
"""

import json
import re
import os
import logging
from typing import Dict, List, Any, Set
from urllib.parse import urlparse
from datetime import datetime

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageLinkExtractor:
    def __init__(self):
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.tiff', '.ico'}
        self.image_urls = set()
        self.image_metadata = []
        self.processed_urls = 0
        
    def is_image_url(self, url: str) -> bool:
        """Prüft ob eine URL ein Bild ist"""
        if not url or not isinstance(url, str):
            return False
            
        # Prüfe Dateiendung
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Prüfe explizite Dateiendungen
        for ext in self.image_extensions:
            if path.endswith(ext):
                return True
        
        # Prüfe auf CDN-Patterns (Frontify, etc.)
        if 'cdn-assets' in url or 'frontify' in url:
            # Prüfe auf Bild-Parameter
            if any(param in url.lower() for param in ['format=webp', 'format=png', 'format=jpg', 'width=', 'height=']):
                return True
                
        return False
    
    def extract_image_metadata(self, url: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extrahiert Metadaten für ein Bild"""
        metadata = {
            'url': url,
            'domain': urlparse(url).netloc,
            'filename': urlparse(url).path.split('/')[-1],
            'context': context,
            'extracted_at': datetime.utcnow().isoformat()
        }
        
        # Extrahiere zusätzliche Parameter aus URL
        if 'width=' in url:
            width_match = re.search(r'width=(\d+)', url)
            if width_match:
                metadata['width'] = int(width_match.group(1))
                
        if 'height=' in url:
            height_match = re.search(r'height=(\d+)', url)
            if height_match:
                metadata['height'] = int(height_match.group(1))
                
        if 'format=' in url:
            format_match = re.search(r'format=(\w+)', url)
            if format_match:
                metadata['format'] = format_match.group(1)
        
        return metadata
    
    def extract_from_html_json(self, data: Dict[str, Any]) -> None:
        """Extrahiert Bild-URLs aus HTML-JSON"""
        logger.info("Extrahiere Bild-URLs aus HTML-JSON...")
        
        def search_recursively(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Prüfe auf 'src' Felder
                    if key == 'src' and isinstance(value, str):
                        if self.is_image_url(value):
                            context = {
                                'source': 'html_json',
                                'path': current_path,
                                'parent_data': {k: v for k, v in obj.items() if k != 'src'}
                            }
                            metadata = self.extract_image_metadata(value, context)
                            self.image_metadata.append(metadata)
                            self.image_urls.add(value)
                            logger.info(f"Bild gefunden: {value}")
                    
                    # Rekursiv weitersuchen
                    search_recursively(value, current_path)
                    
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_recursively(item, f"{path}[{i}]")
                    
            elif isinstance(obj, str):
                # Prüfe auf URLs in Text-Inhalten
                url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+\.(jpg|jpeg|png|gif|webp|svg|bmp|tiff|ico)'
                urls = re.findall(url_pattern, obj, re.IGNORECASE)
                for url in urls:
                    full_url = url[0] if isinstance(url, tuple) else url
                    if self.is_image_url(full_url):
                        context = {
                            'source': 'html_json_text',
                            'path': path,
                            'text_context': obj[:200] + '...' if len(obj) > 200 else obj
                        }
                        metadata = self.extract_image_metadata(full_url, context)
                        self.image_metadata.append(metadata)
                        self.image_urls.add(full_url)
                        logger.info(f"Bild in Text gefunden: {full_url}")
        
        search_recursively(data)
    
    def extract_from_graphql_json(self, data: Dict[str, Any]) -> None:
        """Extrahiert Bild-URLs aus GraphQL-JSON"""
        logger.info("Extrahiere Bild-URLs aus GraphQL-JSON...")
        
        def search_recursively(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Prüfe auf verschiedene URL-Felder
                    if key in ['url', 'src', 'image_url', 'thumbnail_url', 'preview_url'] and isinstance(value, str):
                        if self.is_image_url(value):
                            context = {
                                'source': 'graphql_json',
                                'path': current_path,
                                'field_type': key,
                                'parent_data': {k: v for k, v in obj.items() if k != key}
                            }
                            metadata = self.extract_image_metadata(value, context)
                            self.image_metadata.append(metadata)
                            self.image_urls.add(value)
                            logger.info(f"Bild gefunden: {value}")
                    
                    # Rekursiv weitersuchen
                    search_recursively(value, current_path)
                    
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_recursively(item, f"{path}[{i}]")
                    
            elif isinstance(obj, str):
                # Prüfe auf URLs in Text-Inhalten
                url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+\.(jpg|jpeg|png|gif|webp|svg|bmp|tiff|ico)'
                urls = re.findall(url_pattern, obj, re.IGNORECASE)
                for url in urls:
                    full_url = url[0] if isinstance(url, tuple) else url
                    if self.is_image_url(full_url):
                        context = {
                            'source': 'graphql_json_text',
                            'path': path,
                            'text_context': obj[:200] + '...' if len(obj) > 200 else obj
                        }
                        metadata = self.extract_image_metadata(full_url, context)
                        self.image_metadata.append(metadata)
                        self.image_urls.add(full_url)
                        logger.info(f"Bild in Text gefunden: {full_url}")
        
        search_recursively(data)
    
    def extract_from_graphql_json(self, data: Dict[str, Any]) -> None:
        """Extrahiert Bild-URLs aus GraphQL-JSON-Struktur"""
        logger.info("Extrahiere Bilder aus GraphQL-JSON...")
        
        def extract_from_assets(assets_list: List[Dict[str, Any]], library_name: str = "Unknown") -> None:
            """Extrahiert URLs aus Asset-Liste"""
            for asset in assets_list:
                if not isinstance(asset, dict):
                    continue
                
                # Extrahiere preview_url (PNG/JPEG Preview)
                preview_url = asset.get('preview_url')
                if preview_url and self.is_image_url(preview_url):
                    context = {
                        'source': 'graphql_asset_preview',
                        'library': library_name,
                        'asset_id': asset.get('id', 'unknown'),
                        'asset_title': asset.get('title', 'unknown'),
                        'asset_type': asset.get('type', 'unknown'),
                        'dimensions': asset.get('dimensions', {}),
                        'size_bytes': asset.get('size_bytes')
                    }
                    metadata = self.extract_image_metadata(preview_url, context)
                    self.image_metadata.append(metadata)
                    self.image_urls.add(preview_url)
                    logger.info(f"GraphQL Asset Preview: {preview_url}")
                
                # Extrahiere download_url (falls es ein Bild ist)
                download_url = asset.get('download_url')
                if download_url and self.is_image_url(download_url):
                    context = {
                        'source': 'graphql_asset_download',
                        'library': library_name,
                        'asset_id': asset.get('id', 'unknown'),
                        'asset_title': asset.get('title', 'unknown'),
                        'asset_type': asset.get('type', 'unknown')
                    }
                    metadata = self.extract_image_metadata(download_url, context)
                    self.image_metadata.append(metadata)
                    self.image_urls.add(download_url)
                    logger.info(f"GraphQL Asset Download: {download_url}")
        
        # Verarbeite Assets aus verschiedenen Libraries
        if 'assets' in data and 'by_library' in data['assets']:
            for library_data in data['assets']['by_library']:
                library_name = library_data.get('library', 'Unknown Library')
                assets_list = library_data.get('assets', [])
                logger.info(f"Verarbeite Library '{library_name}' mit {len(assets_list)} Assets")
                extract_from_assets(assets_list, library_name)
        
        # Fallback: Suche rekursiv nach allen URLs
        self.search_recursively_for_images(data, 'graphql_json')
        
        logger.info(f"GraphQL-Extraktion abgeschlossen: {len(self.image_urls)} URLs gefunden")
    
    def search_recursively_for_images(self, data: Any, source: str = "unknown") -> None:
        """Rekursive Suche nach Bild-URLs in beliebiger Datenstruktur"""
        def search_recursively(obj: Any, path: str = "root") -> None:
            if isinstance(obj, dict):
                for key, value in obj.items():
                    search_recursively(value, f"{path}.{key}")
                    
                    # Prüfe spezifische Schlüssel
                    if key in ['preview_url', 'download_url', 'url', 'src', 'image_url'] and isinstance(value, str):
                        if self.is_image_url(value):
                            context = {
                                'source': source,
                                'path': f"{path}.{key}",
                                'key': key
                            }
                            metadata = self.extract_image_metadata(value, context)
                            self.image_metadata.append(metadata)
                            self.image_urls.add(value)
                            logger.info(f"Bild in {path}.{key}: {value}")
                            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_recursively(item, f"{path}[{i}]")
                    
            elif isinstance(obj, str):
                # Prüfe auf URLs in Text-Inhalten
                url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+\.(jpg|jpeg|png|gif|webp|svg|bmp|tiff|ico)'
                urls = re.findall(url_pattern, obj, re.IGNORECASE)
                for url in urls:
                    full_url = url[0] if isinstance(url, tuple) else url
                    if self.is_image_url(full_url):
                        context = {
                            'source': f'{source}_text',
                            'path': path,
                            'text_context': obj[:200] + '...' if len(obj) > 200 else obj
                        }
                        metadata = self.extract_image_metadata(full_url, context)
                        self.image_metadata.append(metadata)
                        self.image_urls.add(full_url)
                        logger.info(f"Bild in Text gefunden: {full_url}")
        
        search_recursively(data)
    
    def categorize_images(self) -> Dict[str, List[Dict[str, Any]]]:
        """Kategorisiert Bilder nach Typ und Domain"""
        categories = {
            'logos': [],
            'avatars': [],
            'brand_assets': [],
            'frontify_cdn': [],
            'other': []
        }
        
        for metadata in self.image_metadata:
            url = metadata['url'].lower()
            filename = metadata['filename'].lower()
            
            # Kategorisierung basierend auf URL und Dateiname
            if 'logo' in url or 'logo' in filename or 'marke' in url:
                categories['logos'].append(metadata)
            elif 'avatar' in url or 'avatar' in filename:
                categories['avatars'].append(metadata)
            elif 'frontify' in metadata['domain'] or 'cdn-assets' in metadata['domain']:
                categories['frontify_cdn'].append(metadata)
            elif any(keyword in url for keyword in ['brand', 'bosch', 'corporate']):
                categories['brand_assets'].append(metadata)
            else:
                categories['other'].append(metadata)
        
        return categories
    
    def save_results(self, output_dir: str = "/shared/JSON/extracted") -> None:
        """Speichert die extrahierten Ergebnisse"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Alle URLs als Liste
        urls_file = os.path.join(output_dir, "image_urls.json")
        with open(urls_file, 'w', encoding='utf-8') as f:
            json.dump(list(self.image_urls), f, indent=2, ensure_ascii=False)
        
        # Vollständige Metadaten
        metadata_file = os.path.join(output_dir, "image_metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.image_metadata, f, indent=2, ensure_ascii=False)
        
        # Kategorisierte Bilder
        categories = self.categorize_images()
        categories_file = os.path.join(output_dir, "image_categories.json")
        with open(categories_file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=2, ensure_ascii=False)
        
        # Statistik
        stats = {
            'total_images': len(self.image_urls),
            'total_metadata_entries': len(self.image_metadata),
            'categories': {k: len(v) for k, v in categories.items()},
            'domains': {},
            'extraction_timestamp': datetime.utcnow().isoformat()
        }
        
        # Domain-Statistik
        for metadata in self.image_metadata:
            domain = metadata['domain']
            stats['domains'][domain] = stats['domains'].get(domain, 0) + 1
        
        stats_file = os.path.join(output_dir, "extraction_stats.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Ergebnisse gespeichert in: {output_dir}")
        logger.info(f"Statistiken: {stats}")

def main():
    extractor = ImageLinkExtractor()
    
    # HTML-JSON verarbeiten
    html_file = '/shared/JSON/html.json'
    if os.path.exists(html_file):
        logger.info(f"Lade HTML-JSON: {html_file}")
        with open(html_file, 'r', encoding='utf-8') as f:
            html_data = json.load(f)
        extractor.extract_from_html_json(html_data)
    else:
        logger.warning(f"HTML-JSON nicht gefunden: {html_file}")
    
    # GraphQL-JSON verarbeiten
    graphql_file = '/shared/JSON/graphql.json'
    if os.path.exists(graphql_file):
        logger.info(f"Lade GraphQL-JSON: {graphql_file}")
        with open(graphql_file, 'r', encoding='utf-8') as f:
            graphql_data = json.load(f)
        extractor.extract_from_graphql_json(graphql_data)
    else:
        logger.warning(f"GraphQL-JSON nicht gefunden: {graphql_file}")
    
    # Ergebnisse speichern
    extractor.save_results()
    
    logger.info(f"Extraktion abgeschlossen: {len(extractor.image_urls)} Bilder gefunden")

if __name__ == "__main__":
    main()
