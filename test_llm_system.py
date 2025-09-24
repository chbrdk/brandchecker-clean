#!/usr/bin/env python3
"""
Test Script for Brand Guidelines LLM System
Tests the complete LLM integration with OpenAI models
"""

import os
import sys
import json
import requests
import time
from typing import Dict, Any

def test_api_endpoint(url: str, data: Dict[str, Any] = None, method: str = "GET") -> Dict[str, Any]:
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

def test_llm_system():
    """Test the complete LLM system"""
    print("🚀 Testing Brand Guidelines LLM System")
    print("=" * 50)
    
    # Configuration
    base_url = "http://localhost:8001"
    brand_id = "9a933c7f-bd87-400f-b13a-b3bce7c822d8"  # Bosch brand ID
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    result = test_api_endpoint(f"{base_url}/health")
    if "error" not in result:
        print("✅ Health check passed")
        print(f"   Status: {result.get('status')}")
    else:
        print(f"❌ Health check failed: {result['error']}")
        return False
    
    # Test 2: Get Brands
    print("\n2. Testing Get Brands...")
    result = test_api_endpoint(f"{base_url}/api/brands")
    if "error" not in result:
        print("✅ Get brands passed")
        brands = result.get('brands', [])
        print(f"   Found {len(brands)} brands")
        for brand in brands:
            print(f"   - {brand['name']} (ID: {brand['id']})")
    else:
        print(f"❌ Get brands failed: {result['error']}")
    
    # Test 3: Get Brand Assets
    print(f"\n3. Testing Get Brand Assets for {brand_id}...")
    result = test_api_endpoint(f"{base_url}/api/brand/{brand_id}/assets")
    if "error" not in result:
        print("✅ Get brand assets passed")
        assets = result.get('assets', [])
        print(f"   Found {len(assets)} assets")
        if assets:
            print(f"   Sample asset: {assets[0]['title']}")
    else:
        print(f"❌ Get brand assets failed: {result['error']}")
    
    # Test 4: Get Brand Guidelines
    print(f"\n4. Testing Get Brand Guidelines for {brand_id}...")
    result = test_api_endpoint(f"{base_url}/api/brand/{brand_id}/guidelines")
    if "error" not in result:
        print("✅ Get brand guidelines passed")
        guidelines = result.get('guidelines', [])
        print(f"   Found {len(guidelines)} guideline pages")
        if guidelines:
            print(f"   Sample guideline: {guidelines[0]['title']}")
    else:
        print(f"❌ Get brand guidelines failed: {result['error']}")
    
    # Test 5: Check Embedding Status
    print("\n5. Testing Embedding Status...")
    result = test_api_endpoint(f"{base_url}/api/embeddings/status")
    if "error" not in result:
        print("✅ Get embedding status passed")
        status_data = result.get('embedding_status', [])
        for status in status_data:
            print(f"   Brand: {status['brand_name']}")
            print(f"   Chunks: {status['chunk_count']}")
            print(f"   Embedded: {status['embedded_count']}")
            if status['chunk_count'] > 0:
                coverage = (status['embedded_count'] / status['chunk_count']) * 100
                print(f"   Coverage: {coverage:.1f}%")
    else:
        print(f"❌ Get embedding status failed: {result['error']}")
    
    # Test 6: Semantic Search (if embeddings exist)
    print(f"\n6. Testing Semantic Search...")
    search_query = "Welche Farben sind für Bosch Corporate erlaubt?"
    search_data = {
        "query": search_query,
        "brand_id": brand_id,
        "limit": 5
    }
    
    result = test_api_endpoint(f"{base_url}/api/search", search_data, "POST")
    if "error" not in result:
        print("✅ Semantic search passed")
        results = result.get('results', [])
        print(f"   Found {len(results)} results for: '{search_query}'")
        for i, res in enumerate(results[:3]):
            print(f"   {i+1}. Score: {res['similarity_score']:.3f} - {res['content'][:100]}...")
    else:
        print(f"❌ Semantic search failed: {result['error']}")
        print("   This might be because embeddings haven't been generated yet.")
    
    # Test 7: Ask Question (LLM Integration)
    print(f"\n7. Testing LLM Question Answering...")
    question = "Welche Schriftarten darf ich für Bosch verwenden?"
    question_data = {
        "question": question,
        "brand_id": brand_id,
        "limit": 5
    }
    
    result = test_api_endpoint(f"{base_url}/api/ask", question_data, "POST")
    if "error" not in result:
        print("✅ LLM question answering passed")
        answer = result.get('answer', '')
        print(f"   Question: {question}")
        print(f"   Answer: {answer[:200]}...")
        sources = result.get('sources', [])
        print(f"   Used {len(sources)} sources")
    else:
        print(f"❌ LLM question answering failed: {result['error']}")
        print("   This might be because:")
        print("   1. OpenAI API key is not set")
        print("   2. Embeddings haven't been generated")
        print("   3. GPT-5 model is not available (will use fallback)")
    
    # Test 8: Compliance Check
    print(f"\n8. Testing Compliance Check...")
    compliance_data = {
        "content": "Ich verwende die Farbe #FF0000 (Rot) für mein Bosch-Logo.",
        "brand_id": brand_id,
        "check_type": "colors"
    }
    
    result = test_api_endpoint(f"{base_url}/api/compliance/check", compliance_data, "POST")
    if "error" not in result:
        print("✅ Compliance check passed")
        score = result.get('compliance_score', 0)
        assessment = result.get('assessment', '')
        print(f"   Compliance Score: {score:.2f}")
        print(f"   Assessment: {assessment[:200]}...")
    else:
        print(f"❌ Compliance check failed: {result['error']}")
    
    print("\n" + "=" * 50)
    print("🎉 LLM System Test Completed!")
    print("\nNext Steps:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
    print("2. Generate embeddings: docker-compose exec llm-api-service python /app/embedding_service.py")
    print("3. Optimize indexes: docker-compose exec brandchecker-python python /app/optimize_indexes.py")
    print("4. Test the system again!")

if __name__ == "__main__":
    test_llm_system()
