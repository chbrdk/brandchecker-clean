#!/usr/bin/env python3
"""
Optimiert Brand-Daten vor der Indexierung:
- Entfernt Duplikate
- Strukturiert Farben
- Bereinigt Text
- Splittet komplexe Einträge
"""

import json
import re
from collections import defaultdict
from typing import Dict, List, Set, Any
import logging
import os

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrandDataOptimizer:
    def __init__(self):
        self.color_patterns = {
            'hex': r'#([0-9a-fA-F]{6})',
            'rgb': r'RGB\s*(\d+),\s*(\d+),\s*(\d+)',
            'cmyk': r'CMYK\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)',
            'pantone': r'PMS\s*(\d+)',
            'ral': r'RAL\s*(\d+)',
            'rgb_simple': r'RGB(\d+,\s*\d+,\s*\d+)',
            'cmyk_simple': r'CMYK(\d+,\s*\d+,\s*\d+,\s*\d+)'
        }
        
        self.known_colors = {
            '#007bc0': 'Bosch Blau 50',
            '#ed0007': 'Bosch Rot',
            '#71767c': 'Bosch Grau 50',
            '#000000': 'Schwarz',
            '#ffffff': 'Weiß'
        }
    
    def extract_colors(self, text: str) -> List[Dict[str, str]]:
        """Extrahiert alle Farben aus einem Text"""
        colors = []
        
        # Hex-Farben
        hex_matches = re.findall(self.color_patterns['hex'], text)
        for hex_color in hex_matches:
            hex_value = f"#{hex_color}"
            color_name = self.known_colors.get(hex_value, f"Color {hex_value}")
            colors.append({
                'type': 'hex',
                'value': hex_value,
                'name': color_name,
                'context': text[:100] + '...' if len(text) > 100 else text
            })
        
        # RGB-Farben (verschiedene Formate)
        rgb_matches = re.findall(self.color_patterns['rgb'], text)
        for r, g, b in rgb_matches:
            rgb_value = f"RGB({r}, {g}, {b})"
            colors.append({
                'type': 'rgb',
                'value': rgb_value,
                'name': f"RGB Color {r},{g},{b}",
                'context': text[:100] + '...' if len(text) > 100 else text
            })
        
        # RGB-Farben (einfaches Format)
        rgb_simple_matches = re.findall(self.color_patterns['rgb_simple'], text)
        for rgb_values in rgb_simple_matches:
            rgb_value = f"RGB({rgb_values})"
            colors.append({
                'type': 'rgb',
                'value': rgb_value,
                'name': f"RGB Color {rgb_values}",
                'context': text[:100] + '...' if len(text) > 100 else text
            })
        
        # CMYK-Farben
        cmyk_matches = re.findall(self.color_patterns['cmyk'], text)
        for c, m, y, k in cmyk_matches:
            cmyk_value = f"CMYK({c}, {m}, {y}, {k})"
            colors.append({
                'type': 'cmyk',
                'value': cmyk_value,
                'name': f"CMYK Color {c},{m},{y},{k}",
                'context': text[:100] + '...' if len(text) > 100 else text
            })
        
        # CMYK-Farben (einfaches Format)
        cmyk_simple_matches = re.findall(self.color_patterns['cmyk_simple'], text)
        for cmyk_values in cmyk_simple_matches:
            cmyk_value = f"CMYK({cmyk_values})"
            colors.append({
                'type': 'cmyk',
                'value': cmyk_value,
                'name': f"CMYK Color {cmyk_values}",
                'context': text[:100] + '...' if len(text) > 100 else text
            })
        
        # Pantone-Farben
        pantone_matches = re.findall(self.color_patterns['pantone'], text)
        for pantone in pantone_matches:
            pantone_value = f"PMS {pantone}"
            colors.append({
                'type': 'pantone',
                'value': pantone_value,
                'name': f"Pantone {pantone}",
                'context': text[:100] + '...' if len(text) > 100 else text
            })
        
        # RAL-Farben
        ral_matches = re.findall(self.color_patterns['ral'], text)
        for ral in ral_matches:
            ral_value = f"RAL {ral}"
            colors.append({
                'type': 'ral',
                'value': ral_value,
                'name': f"RAL {ral}",
                'context': text[:100] + '...' if len(text) > 100 else text
            })
        
        return colors
    
    def clean_text(self, text: str) -> str:
        """Bereinigt Text von überflüssigen Zeichen"""
        if not text:
            return ""
        
        # Entferne überflüssige Leerzeichen
        text = re.sub(r'\s+', ' ', text)
        
        # Entferne Sonderzeichen am Anfang/Ende
        text = text.strip()
        
        # Entferne zu kurze Texte
        if len(text) < 3:
            return ""
        
        return text
    
    def split_complex_entries(self, text: str) -> List[str]:
        """Splittet komplexe Einträge in einzelne Teile"""
        if not text:
            return []
        
        # Splitte bei bestimmten Mustern
        split_patterns = [
            r'HEX#',  # Vor Hex-Farben
            r'RGB\d+',  # Vor RGB-Werten
            r'CMYK\d+',  # Vor CMYK-Werten
            r'PMS\d+',  # Vor Pantone-Werten
            r'RAL\d+',  # Vor RAL-Werten
        ]
        
        parts = [text]
        for pattern in split_patterns:
            new_parts = []
            for part in parts:
                if re.search(pattern, part):
                    # Splitte bei dem Muster
                    split_result = re.split(f'({pattern})', part)
                    new_parts.extend([s for s in split_result if s.strip()])
                else:
                    new_parts.append(part)
            parts = new_parts
        
        # Bereinige die Teile
        cleaned_parts = [self.clean_text(part) for part in parts]
        return [part for part in cleaned_parts if part]
    
    def optimize_html_data(self, data: Dict) -> Dict[str, Any]:
        """Optimiert HTML-Daten"""
        logger.info("Optimiere HTML-Daten...")
        
        optimized = {
            'pages': [],
            'colors': [],
            'fonts': [],
            'duplicates_removed': 0,
            'entries_split': 0
        }
        
        seen_texts = set()
        color_entries = []
        
        # Verarbeite guideline_pages
        if 'guideline_pages' in data:
            guideline_pages = data['guideline_pages']
            logger.info(f"Verarbeite {len(guideline_pages)} Guideline-Seiten...")
            
            for page_url, page_data in guideline_pages.items():
                if not isinstance(page_data, dict):
                    continue
                
                # Verarbeite Titel
                if 'title' in page_data:
                    title = page_data['title']
                    if title and title not in seen_texts:
                        seen_texts.add(title)
                        colors = self.extract_colors(title)
                        if colors:
                            color_entries.extend(colors)
                        
                        optimized['pages'].append({
                            'content': title,
                            'source': 'page_title',
                            'url': page_data.get('url', ''),
                            'original_length': len(title),
                            'has_colors': len(colors) > 0
                        })
                
                # Verarbeite Sektionen
                if 'sections' in page_data:
                    for section in page_data['sections']:
                        if isinstance(section, dict) and 'text' in section:
                            text = section['text']
                            if text and text not in seen_texts:
                                seen_texts.add(text)
                                
                                # Splitte komplexe Einträge
                                split_parts = self.split_complex_entries(text)
                                if len(split_parts) > 1:
                                    optimized['entries_split'] += len(split_parts)
                                
                                # Extrahiere Farben
                                colors = self.extract_colors(text)
                                if colors:
                                    color_entries.extend(colors)
                                
                                # Füge bereinigte Teile hinzu
                                for part in split_parts:
                                    if part and len(part) > 3:
                                        optimized['pages'].append({
                                            'content': part,
                                            'source': 'section',
                                            'level': section.get('level', ''),
                                            'url': page_data.get('url', ''),
                                            'original_length': len(text),
                                            'has_colors': len(colors) > 0
                                        })
                
                # Verarbeite Paragraphs
                if 'paragraphs' in page_data:
                    for paragraph in page_data['paragraphs']:
                        if isinstance(paragraph, str) and paragraph not in seen_texts:
                            seen_texts.add(paragraph)
                            
                            # Splitte komplexe Einträge
                            split_parts = self.split_complex_entries(paragraph)
                            if len(split_parts) > 1:
                                optimized['entries_split'] += len(split_parts)
                            
                            # Extrahiere Farben
                            colors = self.extract_colors(paragraph)
                            if colors:
                                color_entries.extend(colors)
                            
                            # Füge bereinigte Teile hinzu
                            for part in split_parts:
                                if part and len(part) > 3:
                                    optimized['pages'].append({
                                        'content': part,
                                        'source': 'paragraph',
                                        'url': page_data.get('url', ''),
                                        'original_length': len(paragraph),
                                        'has_colors': len(colors) > 0
                                    })
                
                # Verarbeite ListItems
                if 'listItems' in page_data:
                    for item in page_data['listItems']:
                        if isinstance(item, str) and item not in seen_texts:
                            seen_texts.add(item)
                            
                            # Splitte komplexe Einträge
                            split_parts = self.split_complex_entries(item)
                            if len(split_parts) > 1:
                                optimized['entries_split'] += len(split_parts)
                            
                            # Extrahiere Farben
                            colors = self.extract_colors(item)
                            if colors:
                                color_entries.extend(colors)
                            
                            # Füge bereinigte Teile hinzu
                            for part in split_parts:
                                if part and len(part) > 3:
                                    optimized['pages'].append({
                                        'content': part,
                                        'source': 'list_item',
                                        'url': page_data.get('url', ''),
                                        'original_length': len(item),
                                        'has_colors': len(colors) > 0
                                    })
        
        # Verarbeite sections direkt (falls vorhanden)
        if 'sections' in data:
            sections = data['sections']
            logger.info(f"Verarbeite {len(sections)} direkte Sektionen...")
            
            for section in sections:
                if isinstance(section, dict) and 'text' in section:
                    text = section['text']
                    if text and text not in seen_texts:
                        seen_texts.add(text)
                        
                        # Splitte komplexe Einträge
                        split_parts = self.split_complex_entries(text)
                        if len(split_parts) > 1:
                            optimized['entries_split'] += len(split_parts)
                        
                        # Extrahiere Farben
                        colors = self.extract_colors(text)
                        if colors:
                            color_entries.extend(colors)
                        
                        # Füge bereinigte Teile hinzu
                        for part in split_parts:
                            if part and len(part) > 3:
                                optimized['pages'].append({
                                    'content': part,
                                    'source': 'direct_section',
                                    'level': section.get('level', ''),
                                    'original_length': len(text),
                                    'has_colors': len(colors) > 0
                                })
        
        # Verarbeite paragraphs direkt (falls vorhanden)
        if 'paragraphs' in data:
            paragraphs = data['paragraphs']
            logger.info(f"Verarbeite {len(paragraphs)} direkte Absätze...")
            
            for paragraph in paragraphs:
                if isinstance(paragraph, str) and paragraph not in seen_texts:
                    seen_texts.add(paragraph)
                    
                    # Splitte komplexe Einträge
                    split_parts = self.split_complex_entries(paragraph)
                    if len(split_parts) > 1:
                        optimized['entries_split'] += len(split_parts)
                    
                    # Extrahiere Farben
                    colors = self.extract_colors(paragraph)
                    if colors:
                        color_entries.extend(colors)
                    
                    # Füge bereinigte Teile hinzu
                    for part in split_parts:
                        if part and len(part) > 3:
                            optimized['pages'].append({
                                'content': part,
                                'source': 'paragraph',
                                'original_length': len(paragraph),
                                'has_colors': len(colors) > 0
                            })
        
        # Verarbeite list_items direkt (falls vorhanden)
        if 'list_items' in data:
            list_items = data['list_items']
            logger.info(f"Verarbeite {len(list_items)} Listenelemente...")
            
            for item in list_items:
                if isinstance(item, str) and item not in seen_texts:
                    seen_texts.add(item)
                    
                    # Splitte komplexe Einträge
                    split_parts = self.split_complex_entries(item)
                    if len(split_parts) > 1:
                        optimized['entries_split'] += len(split_parts)
                    
                    # Extrahiere Farben
                    colors = self.extract_colors(item)
                    if colors:
                        color_entries.extend(colors)
                    
                    # Füge bereinigte Teile hinzu
                    for part in split_parts:
                        if part and len(part) > 3:
                            optimized['pages'].append({
                                'content': part,
                                'source': 'list_item',
                                'original_length': len(item),
                                'has_colors': len(colors) > 0
                            })
        
        # Verarbeite listItems (camelCase) direkt (falls vorhanden)
        if 'listItems' in data:
            list_items = data['listItems']
            logger.info(f"Verarbeite {len(list_items)} Listenelemente (camelCase)...")
            
            for item in list_items:
                if isinstance(item, str) and item not in seen_texts:
                    seen_texts.add(item)
                    
                    # Splitte komplexe Einträge
                    split_parts = self.split_complex_entries(item)
                    if len(split_parts) > 1:
                        optimized['entries_split'] += len(split_parts)
                    
                    # Extrahiere Farben
                    colors = self.extract_colors(item)
                    if colors:
                        color_entries.extend(colors)
                    
                    # Füge bereinigte Teile hinzu
                    for part in split_parts:
                        if part and len(part) > 3:
                            optimized['pages'].append({
                                'content': part,
                                'source': 'list_item',
                                'original_length': len(item),
                                'has_colors': len(colors) > 0
                            })
        
        # Verarbeite alle Einträge auf der obersten Ebene nach Farben
        logger.info("Suche nach Farben in allen Einträgen...")
        for key, value in data.items():
            if isinstance(value, (str, list)):
                if isinstance(value, str):
                    self._process_text_for_colors(value, seen_texts, color_entries, optimized, f"top_level_{key}")
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, str):
                            self._process_text_for_colors(item, seen_texts, color_entries, optimized, f"top_level_{key}_{i}")
    
    def _process_text_for_colors(self, text: str, seen_texts: set, color_entries: list, optimized: dict, source: str):
        """Verarbeitet Text auf Farben"""
        if not text or text in seen_texts:
            return
        
        seen_texts.add(text)
        
        # Splitte komplexe Einträge
        split_parts = self.split_complex_entries(text)
        if len(split_parts) > 1:
            optimized['entries_split'] += len(split_parts)
        
        # Extrahiere Farben
        colors = self.extract_colors(text)
        if colors:
            color_entries.extend(colors)
        
        # Füge bereinigte Teile hinzu
        for part in split_parts:
            if part and len(part) > 3:
                optimized['pages'].append({
                    'content': part,
                    'source': source,
                    'original_length': len(text),
                    'has_colors': len(colors) > 0
                })
        
        # Dedupliziere Farben
        unique_colors = {}
        for color in color_entries:
            key = f"{color['type']}:{color['value']}"
            if key not in unique_colors:
                unique_colors[key] = color
            else:
                # Kombiniere Kontexte
                unique_colors[key]['context'] += f" | {color['context'][:50]}"
        
        optimized['colors'] = list(unique_colors.values())
        
        logger.info(f"Optimiert: {len(optimized['pages'])} Einträge, {len(optimized['colors'])} Farben")
        logger.info(f"Entfernt: {optimized['duplicates_removed']} Duplikate")
        logger.info(f"Gesplittet: {optimized['entries_split']} Einträge")
        
        return optimized
    
    def optimize_graphql_data(self, data: Dict) -> Dict[str, Any]:
        """Optimiert GraphQL-Daten"""
        logger.info("Optimiere GraphQL-Daten...")
        
        optimized = {
            'brands': [],
            'assets': [],
            'duplicates_removed': 0
        }
        
        # Verarbeite Brands
        if 'data' in data and 'brands' in data['data']:
            for brand in data['data']['brands']:
                if isinstance(brand, dict):
                    optimized['brands'].append({
                        'id': brand.get('id'),
                        'name': brand.get('name'),
                        'description': self.clean_text(brand.get('description', '')),
                        'created_at': brand.get('createdAt'),
                        'updated_at': brand.get('updatedAt')
                    })
        
        # Verarbeite Assets
        if 'data' in data and 'assetLibraries' in data['data']:
            for library in data['data']['assetLibraries']:
                if isinstance(library, dict) and 'assets' in library:
                    for asset in library['assets']:
                        if isinstance(asset, dict):
                            optimized['assets'].append({
                                'id': asset.get('id'),
                                'name': asset.get('name'),
                                'type': asset.get('type'),
                                'url': asset.get('url'),
                                'description': self.clean_text(asset.get('description', '')),
                                'library_id': library.get('id')
                            })
        
        logger.info(f"Optimiert: {len(optimized['brands'])} Brands, {len(optimized['assets'])} Assets")
        return optimized
    
    def save_optimized_data(self, html_data: Dict, graphql_data: Dict, output_dir: str = "shared/JSON/optimized"):
        """Speichert optimierte Daten"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Speichere HTML-Daten
        html_file = os.path.join(output_dir, "html_optimized.json")
        with open(html_file, 'w', encoding='utf-8') as f:
            json.dump(html_data, f, indent=2, ensure_ascii=False)
        logger.info(f"HTML-Daten gespeichert: {html_file}")
        
        # Speichere GraphQL-Daten
        graphql_file = os.path.join(output_dir, "graphql_optimized.json")
        with open(graphql_file, 'w', encoding='utf-8') as f:
            json.dump(graphql_data, f, indent=2, ensure_ascii=False)
        logger.info(f"GraphQL-Daten gespeichert: {graphql_file}")
        
        # Erstelle Statistiken
        stats = {
            'html_optimization': {
                'original_entries': len(html_data.get('pages', [])) if html_data else 0,
                'colors_found': len(html_data.get('colors', [])) if html_data else 0,
                'duplicates_removed': html_data.get('duplicates_removed', 0) if html_data else 0,
                'entries_split': html_data.get('entries_split', 0) if html_data else 0
            },
            'graphql_optimization': {
                'brands': len(graphql_data.get('brands', [])) if graphql_data else 0,
                'assets': len(graphql_data.get('assets', [])) if graphql_data else 0,
                'duplicates_removed': graphql_data.get('duplicates_removed', 0) if graphql_data else 0
            }
        }
        
        stats_file = os.path.join(output_dir, "optimization_stats.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        logger.info(f"Statistiken gespeichert: {stats_file}")
        
        return html_file, graphql_file, stats_file

def main():
    """Hauptfunktion"""
    logger.info("Starte Brand-Daten-Optimierung...")
    
    optimizer = BrandDataOptimizer()
    
    # Lade HTML-Daten
    html_file = "shared/JSON/html.json"
    if os.path.exists(html_file):
        logger.info(f"Lade HTML-Daten: {html_file}")
        with open(html_file, 'r', encoding='utf-8') as f:
            html_data = json.load(f)
        
        optimized_html = optimizer.optimize_html_data(html_data)
    else:
        logger.warning(f"HTML-Datei nicht gefunden: {html_file}")
        optimized_html = {'pages': [], 'colors': [], 'duplicates_removed': 0, 'entries_split': 0}
    
    # Lade GraphQL-Daten
    graphql_file = "shared/JSON/graphql.json"
    if os.path.exists(graphql_file):
        logger.info(f"Lade GraphQL-Daten: {graphql_file}")
        with open(graphql_file, 'r', encoding='utf-8') as f:
            graphql_data = json.load(f)
        
        optimized_graphql = optimizer.optimize_graphql_data(graphql_data)
    else:
        logger.warning(f"GraphQL-Datei nicht gefunden: {graphql_file}")
        optimized_graphql = {'brands': [], 'assets': [], 'duplicates_removed': 0}
    
    # Speichere optimierte Daten
    html_output, graphql_output, stats_output = optimizer.save_optimized_data(
        optimized_html, optimized_graphql
    )
    
    logger.info("Brand-Daten-Optimierung abgeschlossen!")
    logger.info(f"Optimierte HTML-Daten: {html_output}")
    logger.info(f"Optimierte GraphQL-Daten: {graphql_output}")
    logger.info(f"Statistiken: {stats_output}")

if __name__ == "__main__":
    main()
