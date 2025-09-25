#!/usr/bin/env python3
"""
Filter Working URLs - Extrahiert nur funktionierende URLs ohne AWS-Credentials
"""

import json
import os
import logging
from typing import Dict, List, Any, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def filter_working_urls():
    """Filtert nur funktionierende URLs ohne AWS-Credentials"""
    
    # Lade alle extrahierten URLs
    extracted_file = "/shared/JSON/extracted/image_urls.json"
    if not os.path.exists(extracted_file):
        logger.error(f"Extracted URLs file not found: {extracted_file}")
        return
    
    with open(extracted_file, 'r', encoding='utf-8') as f:
        all_urls = json.load(f)
    
    logger.info(f"Total URLs loaded: {len(all_urls)}")
    
    # Filtere URLs - nur Frontify CDN URLs ohne AWS-Credentials
    working_urls = []
    
    for url in all_urls:
        # Skip AWS signed URLs (they have expired credentials)
        if 'X-Amz-Credential' in url or 'X-Amz-Signature' in url or 'X-Amz-Algorithm' in url:
            continue
        
        # Skip URLs mit [AWS_SECRET_KEY_REMOVED]
        if '[AWS_SECRET_KEY_REMOVED]' in url:
            continue
        
        # Bevorzuge Frontify CDN URLs
        if 'cdn-assets-eu.frontify.com' in url:
            working_urls.append(url)
        elif 'frontify' in url and ('png' in url.lower() or 'jpg' in url.lower() or 'jpeg' in url.lower()):
            working_urls.append(url)
    
    logger.info(f"Working URLs (Frontify CDN only): {len(working_urls)}")
    
    # Speichere gefilterte URLs
    output_file = "/shared/JSON/extracted/working_urls.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(working_urls, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Working URLs saved to: {output_file}")
    
    # Erstelle Statistiken
    stats = {
        'total_urls': len(all_urls),
        'working_urls': len(working_urls),
        'filtered_out': len(all_urls) - len(working_urls),
        'filter_reasons': {
            'aws_credentials': sum(1 for url in all_urls if 'X-Amz-Credential' in url),
            'aws_signature': sum(1 for url in all_urls if 'X-Amz-Signature' in url),
            'aws_algorithm': sum(1 for url in all_urls if 'X-Amz-Algorithm' in url),
            'removed_keys': sum(1 for url in all_urls if '[AWS_SECRET_KEY_REMOVED]' in url)
        }
    }
    
    stats_file = "/shared/JSON/extracted/filter_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Filter statistics: {stats}")
    
    return working_urls

if __name__ == "__main__":
    filter_working_urls()
