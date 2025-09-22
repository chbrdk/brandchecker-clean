#!/usr/bin/env python3
"""
Script to embed Bosch colors JSON into the Knowledge Database
"""

import json
import requests
import os
import sys
from pathlib import Path

def load_bosch_colors(file_path: str) -> dict:
    """Load Bosch colors from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {file_path}: {e}")
        sys.exit(1)

def embed_bosch_colors(bosch_colors_data: dict, api_url: str = "http://localhost:8000") -> bool:
    """Embed Bosch colors into knowledge database"""
    try:
        url = f"{api_url}/knowledge/embed-bosch-colors"
        
        payload = {
            "bosch_colors": bosch_colors_data
        }
        
        print(f"🔗 Sending request to: {url}")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successfully embedded {result.get('chunks_saved', 0)} Bosch color chunks")
            print(f"📊 Chunk IDs: {result.get('chunk_ids', [])[:5]}...")  # Show first 5 IDs
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {api_url}")
        print("💡 Make sure the Brandchecker service is running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_bosch_colors_embedding(api_url: str = "http://localhost:8000") -> bool:
    """Test if Bosch colors were embedded successfully"""
    try:
        url = f"{api_url}/knowledge/bosch-colors"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            total_colors = result.get('total', 0)
            print(f"✅ Found {total_colors} Bosch colors in knowledge base")
            return total_colors > 0
        else:
            print(f"❌ Error testing Bosch colors: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Bosch colors: {e}")
        return False

def main():
    """Main function"""
    print("🎨 Bosch Colors Embedding Script")
    print("=" * 40)
    
    # Check if file path is provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Default path
        file_path = "/Users/m4mini/Desktop/bosch_colors.json"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        print("💡 Usage: python embed_bosch_colors.py [path/to/bosch_colors.json]")
        sys.exit(1)
    
    # Load Bosch colors
    print(f"📁 Loading Bosch colors from: {file_path}")
    bosch_colors = load_bosch_colors(file_path)
    
    # Count colors
    total_colors = 0
    for family, variants in bosch_colors.items():
        if isinstance(variants, dict):
            total_colors += len(variants)
    
    print(f"🎨 Found {total_colors} Bosch colors in {len(bosch_colors)} families")
    
    # Embed colors
    print("\n🚀 Embedding Bosch colors into knowledge database...")
    success = embed_bosch_colors(bosch_colors)
    
    if success:
        print("\n✅ Bosch colors embedded successfully!")
        
        # Test embedding
        print("\n🔍 Testing embedding...")
        test_success = test_bosch_colors_embedding()
        
        if test_success:
            print("🎉 Bosch colors are now available in the knowledge database!")
            print("\n📊 You can now:")
            print("  - Search for Bosch colors: GET /knowledge/bosch-colors")
            print("  - Get specific color: GET /knowledge/bosch-colors?hex_code=#e30613")
            print("  - Use in AI queries: POST /knowledge/query")
        else:
            print("⚠️  Warning: Could not verify embedding")
    else:
        print("❌ Failed to embed Bosch colors")
        sys.exit(1)

if __name__ == "__main__":
    main()
