#!/usr/bin/env python3
"""
Test script for the 4-Gram Finder application
"""

import requests
import json

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working:", data)
            return True
        else:
            print("❌ Health endpoint failed:", response.status_code)
            return False
    except Exception as e:
        print("❌ Health endpoint error:", e)
        return False

def test_four_gram_extraction():
    """Test the 4-gram extraction endpoint"""
    test_sentences = [
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is a subset of artificial intelligence",
        "Natural language processing helps computers understand human language"
    ]
    
    for sentence in test_sentences:
        try:
            response = requests.post(
                "http://localhost:8000/extract-four-grams",
                headers={"Content-Type": "application/json"},
                json={"sentence": sentence}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 4-gram extraction for '{sentence[:30]}...':")
                print(f"   Found {data['total_grams']} 4-grams")
                for i, gram in enumerate(data['four_grams'][:3], 1):
                    print(f"   {i}. {gram}")
                if len(data['four_grams']) > 3:
                    print(f"   ... and {len(data['four_grams']) - 3} more")
                print()
            else:
                print(f"❌ 4-gram extraction failed for '{sentence[:30]}...':", response.status_code)
                
        except Exception as e:
            print(f"❌ 4-gram extraction error for '{sentence[:30]}...':", e)

def test_error_handling():
    """Test error handling"""
    test_cases = [
        {"sentence": ""},  # Empty sentence
        {"sentence": "Short"},  # Too few words
        {"sentence": "Only three words"}  # Exactly 3 words
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(
                "http://localhost:8000/extract-four-grams",
                headers={"Content-Type": "application/json"},
                json=test_case
            )
            
            if response.status_code == 400:
                data = response.json()
                print(f"✅ Error handling working for '{test_case['sentence']}': {data['detail']}")
            else:
                print(f"❌ Expected error but got status {response.status_code} for '{test_case['sentence']}'")
                
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")

def main():
    print("🧪 Testing 4-Gram Finder Application")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("❌ Application is not running properly")
        return
    
    print("\n📝 Testing 4-gram extraction:")
    test_four_gram_extraction()
    
    print("\n⚠️  Testing error handling:")
    test_error_handling()
    
    print("\n🎉 Testing completed!")
    print("\n🌐 You can now open http://localhost:8000 in your browser to use the application!")

if __name__ == "__main__":
    main()