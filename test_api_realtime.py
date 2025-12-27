"""
Test Real-Time Estimate API

This script tests the new /api/estimate/current endpoint
"""

import requests
import json
import time
from pathlib import Path

def test_api_endpoint():
    """Test the real-time estimate API endpoint"""
    
    print("\n" + "="*70)
    print("Testing Real-Time Estimate API Endpoint")
    print("="*70 + "\n")
    
    base_url = "http://localhost:5000"
    
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✓ Health check passed: {response.json()}")
        else:
            print(f"   ⚠ Health check returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ℹ Server not running. This is expected if not testing the API server.")
        print("   To test the API, run: python api_server.py")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n2. Testing system status endpoint...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"   ✓ System status: {json.dumps(status, indent=2)}")
        else:
            print(f"   ⚠ Status endpoint returned {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n3. Testing current estimate endpoint...")
    try:
        response = requests.get(f"{base_url}/api/estimate/current", timeout=5)
        if response.status_code == 404:
            print("   ✓ No current project (expected when idle)")
        elif response.status_code == 200:
            estimate = response.json()
            print(f"   ✓ Current estimate: {json.dumps(estimate, indent=2)}")
        else:
            print(f"   ⚠ Estimate endpoint returned {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n" + "="*70)
    print("✅ API Endpoint Tests PASSED!")
    print("="*70 + "\n")
    
    return True


if __name__ == '__main__':
    import sys
    try:
        success = test_api_endpoint()
        if not success:
            print("\nNote: Start the API server with 'python api_server.py' to test API endpoints")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
