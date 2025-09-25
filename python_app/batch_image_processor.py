#!/usr/bin/env python3
"""
Batch Image Processor for Brand Guidelines
Extrahiert Bild-URLs, analysiert sie mit GPT-4o und speichert Ergebnisse in PostgreSQL
"""

import os
import json
import logging
import asyncio
import aiohttp
import base64
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse, parse_qs
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BatchImageProcessor:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Database configuration
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5433'),
            'database': os.getenv('POSTGRES_DB', 'brandchecker'),
            'user': os.getenv('POSTGRES_USER', 'brandchecker_user'),
            'password': os.getenv('POSTGRES_PASSWORD', 'brandchecker_password')
        }
        
        # Brand ID for Bosch (hardcoded for now)
        self.brand_id = "9a933c7f-bd87-400f-b13a-b3bce7c822d8"
        
        # Statistics
        self.stats = {
            'total_images': 0,
            'processed': 0,
            'successful': 0,
            'errors': 0,
            'svg_converted': 0,
            'logos_detected': 0,
            'tokens_used': 0,
            'start_time': None,
            'end_time': None
        }

    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.autocommit = False
            logger.info("Connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def disconnect_db(self):
        """Disconnect from database"""
        if hasattr(self, 'conn'):
            self.conn.close()
            logger.info("Disconnected from database")

    def extract_image_urls_from_json(self, json_file_path: str) -> List[Dict[str, Any]]:
        """Extract image URLs from JSON files with context information"""
        image_data = []
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Processing {json_file_path}")
            
            # Extract from HTML JSON structure (guideline_pages is a dict with paths as keys)
            if 'guideline_pages' in data:
                for page_path, page in data['guideline_pages'].items():
                    page_title = page.get('title', 'Unknown Page')
                    page_url = page.get('url', page_path)
                    
                    # Extract images from sections
                    for section in page.get('sections', []):
                        section_title = section.get('title', '')
                        
                        # Extract images from paragraphs
                        for paragraph in section.get('paragraphs', []):
                            if 'images' in paragraph:
                                for img in paragraph['images']:
                                    if 'src' in img:
                                        image_data.append({
                                            'url': img['src'],
                                            'alt': img.get('alt', ''),
                                            'title': img.get('title', ''),
                                            'width': img.get('width'),
                                            'height': img.get('height'),
                                            'source_context': f"{page_title} > {section_title}",
                                            'page_title': page_title,
                                            'page_url': page_url,
                                            'source_file': json_file_path
                                        })
            
            # Extract from GraphQL JSON structure (assets.by_library format)
            elif 'assets' in data and 'by_library' in data['assets']:
                for library_data in data['assets']['by_library']:
                    library_name = library_data.get('library', 'Unknown Library')
                    
                    for asset in library_data.get('assets', []):
                        asset_title = asset.get('title', 'Unknown Asset')
                        asset_id = asset.get('id', 'unknown')
                        
                        # Extract preview_url (PNG/JPEG Preview)
                        preview_url = asset.get('preview_url')
                        if preview_url:
                            image_data.append({
                                'url': preview_url,
                                'alt': asset_title,
                                'title': asset_title,
                                'width': asset.get('dimensions', {}).get('width'),
                                'height': asset.get('dimensions', {}).get('height'),
                                'source_context': f"GraphQL Asset Preview: {library_name}",
                                'page_title': library_name,
                                'page_url': '',
                                'source_file': json_file_path
                            })
                        
                        # Extract download_url (if it's an image)
                        download_url = asset.get('download_url')
                        if download_url and any(ext in download_url.lower() for ext in ['.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp']):
                            image_data.append({
                                'url': download_url,
                                'alt': asset_title,
                                'title': asset_title,
                                'width': asset.get('dimensions', {}).get('width'),
                                'height': asset.get('dimensions', {}).get('height'),
                                'source_context': f"GraphQL Asset Download: {library_name}",
                                'page_title': library_name,
                                'page_url': '',
                                'source_file': json_file_path
                            })
            
            # Extract from old GraphQL JSON structure (data.brand.assetLibraries format)
            elif 'data' in data and 'brand' in data['data']:
                brand = data['data']['brand']
                
                # Extract from asset libraries
                for library in brand.get('assetLibraries', []):
                    library_name = library.get('name', 'Unknown Library')
                    
                    for asset in library.get('assets', []):
                        asset_name = asset.get('name', 'Unknown Asset')
                        
                        # Extract main asset image
                        if 'image' in asset and 'url' in asset['image']:
                            image_data.append({
                                'url': asset['image']['url'],
                                'alt': asset_name,
                                'title': asset_name,
                                'width': asset['image'].get('width'),
                                'height': asset['image'].get('height'),
                                'source_context': f"Asset Library: {library_name}",
                                'page_title': library_name,
                                'page_url': '',
                                'source_file': json_file_path
                            })
                        
                        # Extract preview images
                        for preview in asset.get('previews', []):
                            if 'url' in preview:
                                image_data.append({
                                    'url': preview['url'],
                                    'alt': f"{asset_name} Preview",
                                    'title': f"{asset_name} Preview",
                                    'width': preview.get('width'),
                                    'height': preview.get('height'),
                                    'source_context': f"Asset Library: {library_name} > {asset_name} Preview",
                                    'page_title': library_name,
                                    'page_url': '',
                                    'source_file': json_file_path
                                })
            
            logger.info(f"Extracted {len(image_data)} images from {json_file_path}")
            return image_data
            
        except Exception as e:
            logger.error(f"Error processing {json_file_path}: {e}")
            return []

    def extract_all_image_urls(self) -> List[Dict[str, Any]]:
        """Extract image URLs from all JSON files or use pre-extracted URLs"""
        all_images = []
        
        # First try to use the new GraphQL JSON with AWS credentials
        new_graphql_file = "/shared/JSON/bosch_graphql_minimal_test_latest.json"
        if os.path.exists(new_graphql_file):
            try:
                logger.info(f"Processing new GraphQL file: {new_graphql_file}")
                all_images.extend(self.extract_image_urls_from_json(new_graphql_file))
                logger.info(f"Loaded {len(all_images)} images from new GraphQL file")
                
            except Exception as e:
                logger.warning(f"Failed to load new GraphQL file: {e}")
        
        # Fallback to working URLs (without AWS credentials)
        if not all_images:
            working_urls_file = "/shared/JSON/extracted/working_urls.json"
            if os.path.exists(working_urls_file):
                try:
                    with open(working_urls_file, 'r', encoding='utf-8') as f:
                        urls = json.load(f)
                    
                    # Convert URLs to image info format
                    for url in urls:
                        all_images.append({
                            'url': url,
                            'alt': '',
                            'title': '',
                            'width': None,
                            'height': None,
                            'source_context': 'GraphQL Assets (Frontify CDN)',
                            'page_title': 'Bosch Asset Libraries',
                            'page_url': '',
                            'source_file': working_urls_file
                        })
                    
                    logger.info(f"Loaded {len(all_images)} working URLs (Frontify CDN only)")
                    
                except Exception as e:
                    logger.warning(f"Failed to load working URLs: {e}")
        
        # Fallback to all extracted URLs if working URLs not available
        if not all_images:
            extracted_urls_file = "/shared/JSON/extracted/image_urls.json"
            if os.path.exists(extracted_urls_file):
                try:
                    with open(extracted_urls_file, 'r', encoding='utf-8') as f:
                        urls = json.load(f)
                    
                    # Convert URLs to image info format
                    for url in urls:
                        all_images.append({
                            'url': url,
                            'alt': '',
                            'title': '',
                            'width': None,
                            'height': None,
                            'source_context': 'Extracted from Brand Guidelines',
                            'page_title': 'Brand Guidelines',
                            'page_url': '',
                            'source_file': extracted_urls_file
                        })
                    
                    logger.info(f"Loaded {len(all_images)} pre-extracted image URLs (fallback)")
                    
                except Exception as e:
                    logger.warning(f"Failed to load pre-extracted URLs: {e}")
        
        # Fallback to extracting from JSON files
        if not all_images:
            # Process HTML JSON file
            html_file = "/shared/JSON/html.json"
            if os.path.exists(html_file):
                all_images.extend(self.extract_image_urls_from_json(html_file))
            
            # Process GraphQL JSON file
            graphql_file = "/shared/JSON/graphql.json"
            if os.path.exists(graphql_file):
                all_images.extend(self.extract_image_urls_from_json(graphql_file))
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_images = []
        for img in all_images:
            if img['url'] not in seen_urls:
                seen_urls.add(img['url'])
                unique_images.append(img)
        
        logger.info(f"Total unique images found: {len(unique_images)}")
        self.stats['total_images'] = len(unique_images)
        
        return unique_images

    def get_svg_preview_url(self, svg_url: str) -> str:
        """Generate PNG preview URL for SVG files from Frontify"""
        parsed = urlparse(svg_url)
        query_params = parse_qs(parsed.query)
        
        # Set PNG format parameters
        query_params['format'] = ['png']
        query_params['width'] = ['800']
        query_params['quality'] = ['100']
        
        # Remove 'svg' from path if present
        path_parts = parsed.path.split('/')
        if path_parts[-1].endswith('.svg'):
            path_parts[-1] = path_parts[-1].replace('.svg', '.png')
        new_path = '/'.join(path_parts)
        
        new_query = '&'.join([f"{k}={v[0]}" for k, v in query_params.items()])
        preview_url = f"{parsed.scheme}://{parsed.netloc}{new_path}?{new_query}"
        
        return preview_url

    async def download_image(self, session: aiohttp.ClientSession, url: str) -> Tuple[Optional[bytes], str, str]:
        """Download image with SVG conversion support"""
        try:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    data = await response.read()
                    content_type = response.headers.get('content-type', 'image')
                    
                    # Check if it's SVG
                    if 'svg' in content_type.lower() or data.startswith(b'<svg'):
                        logger.info(f"SVG detected, converting to PNG: {url}")
                        preview_url = self.get_svg_preview_url(url)
                        
                        async with session.get(preview_url, timeout=30) as png_response:
                            if png_response.status == 200:
                                png_data = await png_response.read()
                                self.stats['svg_converted'] += 1
                                return png_data, 'svg_converted', url
                            else:
                                logger.warning(f"SVG conversion failed: {png_response.status}")
                                return None, 'error', url
                    else:
                        return data, 'image', url
                else:
                    logger.warning(f"Download failed: {response.status}")
                    return None, 'error', url
                    
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return None, 'error', url

    async def analyze_image(self, session: aiohttp.ClientSession, 
                           image_data: bytes, url: str, content_type: str) -> Dict[str, Any]:
        """Analyze image with GPT-4o"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }

        base64_image = base64.b64encode(image_data).decode('utf-8')

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this image for Bosch brand compliance. Provide a detailed analysis including:

1. **Detailed Description**: What objects, text, and visual elements are visible?
2. **Brand Elements**: 
   - Logo detection (present/absent, type, color, position)
   - Colors used (provide hex codes if possible)
   - Typography (font family, sizes, styles)
3. **Asset Type**: Categorize as 'logo', 'marketing_material', 'product_image', 'illustration', or 'other'
4. **Brand Compliance Score**: Rate from 0-100 based on Bosch brand guidelines
5. **Technical Analysis**: Quality, style, and professional appearance

Return the analysis in structured JSON format."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1500
        }

        try:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Parse JSON response
                    try:
                        analysis = json.loads(content)
                        tokens_used = result['usage']['total_tokens']
                        self.stats['tokens_used'] += tokens_used
                        
                        return {
                            'analysis': analysis,
                            'tokens_used': tokens_used,
                            'model_used': 'gpt-4o',
                            'status': 'success'
                        }
                    except json.JSONDecodeError:
                        # If JSON parsing fails, create structured response
                        return {
                            'analysis': {
                                'detailed_description': {'text': content},
                                'brand_elements': {'logo': {'present': False}},
                                'asset_type': 'other',
                                'brand_compliance': 50,
                                'technical_analysis': {'quality': 'unknown'}
                            },
                            'tokens_used': result['usage']['total_tokens'],
                            'model_used': 'gpt-4o',
                            'status': 'success'
                        }
                else:
                    error_text = await response.text()
                    logger.error(f"OpenAI API error: {response.status} - {error_text}")
                    return {'status': 'error', 'error': f"API error: {response.status}"}
                    
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {'status': 'error', 'error': str(e)}

    def save_image_to_database(self, image_info: Dict[str, Any], 
                              analysis_result: Dict[str, Any]) -> bool:
        """Save image analysis results to database"""
        try:
            with self.conn.cursor() as cursor:
                # Check if image already exists
                cursor.execute(
                    "SELECT id FROM image_analysis_results WHERE original_url = %s",
                    (image_info['url'],)
                )
                existing = cursor.fetchone()
                
                if existing:
                    logger.info(f"Image already analyzed: {image_info['url']}")
                    return True
                
                # Extract analysis data
                analysis = analysis_result.get('analysis', {})
                brand_elements = analysis.get('brand_elements', {})
                logo_detected = brand_elements.get('logo', {}).get('present', False)
                compliance_score = analysis.get('brand_compliance', 0)
                asset_category = analysis.get('asset_type', 'other')
                
                # Insert new record
                cursor.execute("""
                    INSERT INTO image_analysis_results (
                        original_url, processed_url, image_type, content_type,
                        file_size, width, height, analysis_result, logo_detected,
                        brand_elements, compliance_score, asset_category,
                        source_context, brand_id, status, tokens_used, model_used
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    image_info['url'],
                    image_info['url'],  # processed_url same as original for now
                    analysis_result.get('image_type', 'image'),
                    'image/jpeg',  # Default content type
                    len(image_info.get('image_data', b'')),
                    image_info.get('width'),
                    image_info.get('height'),
                    json.dumps(analysis),
                    logo_detected,
                    json.dumps(brand_elements),
                    compliance_score,
                    asset_category,
                    image_info.get('source_context', ''),
                    self.brand_id,
                    'analyzed',
                    analysis_result.get('tokens_used', 0),
                    analysis_result.get('model_used', 'gpt-4o')
                ))
                
                self.conn.commit()
                
                if logo_detected:
                    self.stats['logos_detected'] += 1
                
                logger.info(f"Saved image analysis to database: {image_info['url']}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            self.conn.rollback()
            return False

    async def process_images_batch(self, images: List[Dict[str, Any]], 
                                  max_images: int = 50) -> Dict[str, Any]:
        """Process images in batch with database storage"""
        logger.info(f"Starting batch processing of {min(len(images), max_images)} images")
        
        self.stats['start_time'] = datetime.now()
        
        async with aiohttp.ClientSession() as session:
            for i, image_info in enumerate(images[:max_images]):
                if i % 10 == 0:
                    logger.info(f"Processing image {i+1}/{min(len(images), max_images)}")
                
                try:
                    # Download image
                    image_data, image_type, original_url = await self.download_image(
                        session, image_info['url']
                    )
                    
                    if image_data is None:
                        logger.warning(f"Failed to download: {original_url}")
                        self.stats['errors'] += 1
                        continue
                    
                    # Store image data for database
                    image_info['image_data'] = image_data
                    image_info['image_type'] = image_type
                    
                    # Analyze image
                    analysis_result = await self.analyze_image(
                        session, image_data, original_url, image_type
                    )
                    
                    if analysis_result['status'] == 'success':
                        # Save to database
                        if self.save_image_to_database(image_info, analysis_result):
                            self.stats['successful'] += 1
                        else:
                            self.stats['errors'] += 1
                    else:
                        logger.error(f"Analysis failed for {original_url}: {analysis_result.get('error')}")
                        self.stats['errors'] += 1
                    
                    self.stats['processed'] += 1
                    
                    # Small delay to avoid rate limiting
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error processing image {image_info['url']}: {e}")
                    self.stats['errors'] += 1
        
        self.stats['end_time'] = datetime.now()
        return self.stats

    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get current processing statistics"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get database statistics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_images,
                        COUNT(CASE WHEN status = 'analyzed' THEN 1 END) as analyzed_images,
                        COUNT(CASE WHEN status = 'error' THEN 1 END) as error_images,
                        COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_images,
                        COUNT(CASE WHEN logo_detected = true THEN 1 END) as logos_detected,
                        AVG(compliance_score) as avg_compliance_score,
                        SUM(tokens_used) as total_tokens_used
                    FROM image_analysis_results
                    WHERE brand_id = %s
                """, (self.brand_id,))
                
                db_stats = cursor.fetchone()
                
                return {
                    'database_stats': dict(db_stats) if db_stats else {},
                    'processing_stats': self.stats
                }
                
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {'error': str(e)}

async def main():
    """Main function to run batch image processing"""
    processor = BatchImageProcessor()
    
    try:
        # Connect to database
        processor.connect_db()
        
        # Extract all image URLs
        logger.info("Extracting image URLs from JSON files...")
        images = processor.extract_all_image_urls()
        
        if not images:
            logger.warning("No images found to process")
            return
        
        # Process images in batch
        logger.info(f"Processing {len(images)} images...")
        stats = await processor.process_images_batch(images, max_images=10000)  # Process all available images
        
        # Print final statistics
        logger.info("\n=== BATCH PROCESSING COMPLETE ===")
        logger.info(f"Total images: {stats['total_images']}")
        logger.info(f"Processed: {stats['processed']}")
        logger.info(f"Successful: {stats['successful']}")
        logger.info(f"Errors: {stats['errors']}")
        logger.info(f"SVG converted: {stats['svg_converted']}")
        logger.info(f"Logos detected: {stats['logos_detected']}")
        logger.info(f"Total tokens used: {stats['tokens_used']}")
        
        if stats['start_time'] and stats['end_time']:
            duration = (stats['end_time'] - stats['start_time']).total_seconds()
            logger.info(f"Duration: {duration:.1f} seconds")
            logger.info(f"Speed: {stats['processed']/duration:.2f} images/second")
        
        # Get database statistics
        db_stats = processor.get_processing_statistics()
        logger.info(f"\nDatabase statistics: {db_stats}")
        
    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
    finally:
        processor.disconnect_db()

if __name__ == "__main__":
    asyncio.run(main())
