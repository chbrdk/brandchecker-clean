#!/usr/bin/env python3
"""
Test script to verify connection between n8n and Python service
"""

import requests
import json

def test_python_service():
    """Test if Python service is accessible"""
    try:
        # Test health endpoint
        response = requests.get('http://localhost:8000/health', timeout=5)
        print(f"✅ Python Service Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Python Service Health Check Failed: {e}")
        return False

def test_n8n_service():
    """Test if n8n service is accessible"""
    try:
        # Test n8n endpoint
        response = requests.get('http://localhost:5680', timeout=5)
        print(f"✅ n8n Service Check: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ n8n Service Check Failed: {e}")
        return False

def test_internal_connection():
    """Test internal connection between containers"""
    try:
        # Test if n8n can reach Python service via container name
        response = requests.get('http://brandchecker-python:8000/health', timeout=5)
        print(f"✅ Internal Connection Test: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Internal Connection Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Brandchecker Container Connections...")
    print("=" * 50)
    
    python_ok = test_python_service()
    n8n_ok = test_n8n_service()
    internal_ok = test_internal_connection()
    
    print("=" * 50)
    print("📊 Test Results:")
    print(f"Python Service: {'✅ OK' if python_ok else '❌ FAILED'}")
    print(f"n8n Service: {'✅ OK' if n8n_ok else '❌ FAILED'}")
    print(f"Internal Connection: {'✅ OK' if internal_ok else '❌ FAILED'}")
    
    if python_ok and n8n_ok and internal_ok:
        print("\n🎉 All tests passed! Services are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the container configuration.") 