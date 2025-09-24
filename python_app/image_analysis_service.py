#!/usr/bin/env python3
"""
Finaler Bildanalyse-Service für Brandchecker
- GPT-4o für Bildanalyse (GPT-5 deaktiviert)
- Vollständige SVG-Unterstützung
- Detaillierte Bildbeschreibungen
- Produktionsreif mit Fehlerbehandlung
"""

import json
import os
import asyncio
import aiohttp
from datetime import datetime
import base64
import logging
from urllib.parse import urlparse, parse_qs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageAnalysisService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.semaphore = asyncio.Semaphore(2)
        
        # Nur GPT-4o verwenden (GPT-5 deaktiviert)
        self.model = 'gpt-4o'
        
        # Statistiken
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'errors': 0,
            'svg_converted': 0,
            'logos_detected': 0,
            'start_time': None,
            'end_time': None
        }
    
    def get_svg_preview_url(self, svg_url: str) -> str:
        """Konvertiert SVG-URL zu PNG-Preview"""
        parsed = urlparse(svg_url)
        query_params = parse_qs(parsed.query)
        
        query_params['format'] = ['png']
        query_params['width'] = ['800']
        query_params['quality'] = ['100']
        
        new_query = '&'.join([f"{k}={v[0]}" for k, v in query_params.items()])
        preview_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
        
        return preview_url
    
    def is_svg_url(self, url: str) -> bool:
        """Prüft ob URL auf SVG zeigt"""
        return '.svg' in url.lower() or 'format=svg' in url.lower() or 'image/svg' in url.lower()
    
    async def download_image(self, session: aiohttp.ClientSession, url: str) -> tuple[bytes, str, str]:
        """Lädt Bild herunter mit SVG-Konvertierung"""
        try:
            # Versuche zuerst die Original-URL
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    data = await response.read()
                    content_type = response.headers.get('content-type', 'image')
                    logger.info(f"Downloaded image: {len(data)} bytes, {content_type}")
                    
                    # Prüfe ob es SVG ist
                    if 'svg' in content_type.lower() or data.startswith(b'<svg'):
                        logger.info(f"SVG detected, converting to PNG: {url}")
                        preview_url = self.get_svg_preview_url(url)
                        
                        async with session.get(preview_url, timeout=30) as png_response:
                            if png_response.status == 200:
                                png_data = await png_response.read()
                                logger.info(f"SVG converted to PNG: {len(png_data)} bytes")
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
                           image_data: bytes, url: str, content_type: str) -> dict:
        """Analysiert Bild mit GPT-4o"""
        
        # Optimierter Prompt für detaillierte Bildanalyse
        prompt = """Analysiere dieses Bild aus den Bosch Brand Guidelines sehr detailliert:

**DETAILLIERTE BESCHREIBUNG:**
- Beschreibe jeden sichtbaren Bereich und jedes Element im Detail
- Identifiziere alle Personen, Objekte, Texte und grafischen Elemente
- Analysiere die Komposition und das Layout

**BRAND-ELEMENTE:**
- Bosch-Logo vorhanden? (Typ, Farbe, Position, Qualität)
- Bosch-Farben verwendet? (spezifische HEX-Werte: #007bc0, #ed0007, #71767c)
- Bosch-Typography? (Schriftarten, Größen, Gewichte)

**ASSET-KATEGORISIERUNG:**
- Asset-Typ: Logo, Icon, Produktbild, Marketing-Material, Illustration, Avatar
- Verwendungszweck und Zielgruppe
- Brand-Compliance-Bewertung (0-100 Punkte)

**TECHNISCHE ANALYSE:**
- Bildqualität und -schärfe
- Design-Stil und Ästhetik
- Hauptfarben (mit HEX-Werten wenn möglich)

Antworte als strukturiertes JSON mit deutschen Beschreibungen."""
        
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        try:
            logger.info(f"Analyzing with {self.model}")
            
            payload = {
                "model": self.model,
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }],
                "max_completion_tokens": 1500
            }
            
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=self.headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    tokens_used = data.get('usage', {}).get('total_tokens', 0)
                    
                    # Parse JSON
                    try:
                        if content.startswith("```json"):
                            content = content[7:]
                        if content.endswith("```"):
                            content = content[:-3]
                        
                        analysis_json = json.loads(content.strip())
                    except json.JSONDecodeError:
                        analysis_json = {
                            "raw_analysis": content,
                            "parse_error": "Could not parse JSON"
                        }
                    
                    # Prüfe auf Logo-Erkennung
                    logo_detected = self.detect_logo(analysis_json)
                    
                    if logo_detected:
                        self.stats['logos_detected'] += 1
                    
                    logger.info(f"Success with {self.model}: {len(content)} chars, {tokens_used} tokens")
                    
                    return {
                        "url": url,
                        "original_url": url,
                        "content_type": content_type,
                        "model_used": self.model,
                        "analysis": analysis_json,
                        "logo_detected": logo_detected,
                        "tokens_used": tokens_used,
                        "status": "success",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                else:
                    error_text = await response.text()
                    logger.error(f"API error: {response.status} - {error_text}")
                    return {
                        "url": url,
                        "content_type": content_type,
                        "error": f"API error: {response.status}",
                        "status": "error",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
        except Exception as e:
            logger.error(f"Error analyzing {url}: {e}")
            return {
                "url": url,
                "content_type": content_type,
                "error": str(e),
                "status": "error",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def detect_logo(self, analysis_json: dict) -> bool:
        """Erkennt ob ein Logo in der Analyse gefunden wurde"""
        if not isinstance(analysis_json, dict):
            return False
        
        # Verschiedene Felder für Logo-Erkennung prüfen
        logo_keywords = ['logo', 'bosch', 'brand', 'symbol']
        
        for field in ['brand_elemente', 'logo', 'Logo', 'brand_elements', 'asset_typ', 'detailed_description']:
            if field in analysis_json:
                field_data = analysis_json[field]
                
                if isinstance(field_data, dict):
                    # Prüfe Keys und Values
                    for key, value in field_data.items():
                        if any(keyword in key.lower() for keyword in logo_keywords):
                            if any(keyword in str(value).lower() for keyword in ['ja', 'true', 'vorhanden', 'present']):
                                return True
                
                elif isinstance(field_data, str):
                    if any(keyword in field_data.lower() for keyword in logo_keywords):
                        return True
        
        return False
    
    async def process_single_image(self, session: aiohttp.ClientSession, url: str) -> dict:
        """Verarbeitet ein einzelnes Bild komplett"""
        async with self.semaphore:
            try:
                logger.info(f"Processing: {url}")
                
                # Bild herunterladen
                image_data, content_type, original_url = await self.download_image(session, url)
                
                if not image_data:
                    self.stats['errors'] += 1
                    return {
                        "url": url,
                        "content_type": content_type,
                        "error": "Failed to download image",
                        "status": "error",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                
                # Bild analysieren
                result = await self.analyze_image(session, image_data, url, content_type)
                
                # Statistiken aktualisieren
                self.stats['total_processed'] += 1
                if result.get('status') == 'success':
                    self.stats['successful'] += 1
                    if content_type == 'svg_converted':
                        self.stats['svg_converted'] += 1
                else:
                    self.stats['errors'] += 1
                
                return result
                
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                self.stats['total_processed'] += 1
                self.stats['errors'] += 1
                return {
                    "url": url,
                    "error": str(e),
                    "status": "error",
                    "timestamp": datetime.utcnow().isoformat()
                }
    
    async def analyze_images(self, image_urls: list, max_images: int = None) -> list:
        """Analysiert alle Bilder"""
        if max_images:
            image_urls = image_urls[:max_images]
        
        logger.info(f"Starting image analysis of {len(image_urls)} images")
        self.stats['start_time'] = datetime.utcnow()
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.process_single_image(session, url) for url in image_urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        self.stats['end_time'] = datetime.utcnow()
        
        # Exception-Handling
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "url": image_urls[i],
                    "error": str(result),
                    "status": "error",
                    "timestamp": datetime.utcnow().isoformat()
                })
                self.stats['errors'] += 1
            else:
                processed_results.append(result)
        
        return processed_results
    
    def save_results(self, results: list, output_dir: str = "shared/JSON/analyzed") -> dict:
        """Speichert alle Ergebnisse"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Alle Ergebnisse
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(output_dir, f"image_analysis_{timestamp}.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Statistiken berechnen
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds() if self.stats['end_time'] else 0
        
        final_stats = {
            **self.stats,
            'duration_seconds': duration,
            'images_per_second': self.stats['successful'] / duration if duration > 0 else 0,
            'success_rate': (self.stats['successful'] / self.stats['total_processed'] * 100) if self.stats['total_processed'] > 0 else 0,
            'logo_detection_rate': (self.stats['logos_detected'] / self.stats['successful'] * 100) if self.stats['successful'] > 0 else 0
        }
        
        # Konvertiere datetime zu string für JSON
        if self.stats['start_time']:
            final_stats['start_time'] = self.stats['start_time'].isoformat()
        if self.stats['end_time']:
            final_stats['end_time'] = self.stats['end_time'].isoformat()
        
        stats_file = os.path.join(output_dir, f"image_analysis_stats_{timestamp}.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(final_stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Image analysis results saved:")
        logger.info(f"  - Results: {results_file}")
        logger.info(f"  - Statistics: {stats_file}")
        logger.info(f"Final Statistics: {final_stats}")
        
        return final_stats

async def main():
    """Hauptfunktion"""
    analyzer = ImageAnalysisService()
    
    # Lade Bild-URLs
    urls_file = "/shared/JSON/extracted/image_urls.json"
    if not os.path.exists(urls_file):
        logger.error(f"Image URLs file not found: {urls_file}")
        return
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        image_urls = json.load(f)
    
    logger.info(f"Loaded {len(image_urls)} image URLs")
    
    # Teste mit ersten 20 Bildern
    test_urls = image_urls[:20]
    logger.info(f"Starting analysis with {len(test_urls)} images")
    
    # Starte Analyse
    results = await analyzer.analyze_images(test_urls)
    
    # Speichere Ergebnisse
    stats = analyzer.save_results(results)
    
    # Zeige Zusammenfassung
    logger.info(f"\n=== IMAGE ANALYSIS SUMMARY ===")
    logger.info(f"Total processed: {stats['total_processed']}")
    logger.info(f"Successful: {stats['successful']}")
    logger.info(f"Errors: {stats['errors']}")
    logger.info(f"SVG converted: {stats['svg_converted']}")
    logger.info(f"Logos detected: {stats['logos_detected']}")
    logger.info(f"Success rate: {stats['success_rate']:.1f}%")
    logger.info(f"Logo detection rate: {stats['logo_detection_rate']:.1f}%")
    logger.info(f"Duration: {stats['duration_seconds']:.1f} seconds")
    logger.info(f"Speed: {stats['images_per_second']:.2f} images/second")

if __name__ == "__main__":
    asyncio.run(main())
