"""
Test script to verify Gemini API connectivity
"""

import requests
import json

def test_gemini_api():
    """Test the Gemini API connection"""
    
    api_key = "AIzaSyDVEE344Kj_5nZkWWJqYKwLaRahybAXLwk"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # First, let's try with Gemini 1.5 Pro which is more stable
    model_names = [
        "gemini-1.5-pro",
        "gemini-2.5-pro"  
    ]
    
    for model_name in model_names:
        print(f"🧪 Testing {model_name}...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        
        # Simple test prompt
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Rate this resume from 1-10: Python developer with 2 years experience."
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 100,
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            
            print(f"📊 API Response Status: {response.status_code}")
            
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    ai_response = candidate['content']['parts'][0]['text']
                    
                    print(f"✅ {model_name} API Connection Successful!")
                    print("🤖 Sample AI Response:")
                    print("-" * 50)
                    print(ai_response)
                    print("-" * 50)
                    print()
                    return True
                    
            print(f"❌ {model_name} - No proper response content")
            print(f"Response structure: {json.dumps(response_data, indent=2)[:300]}...")
            print()
            
        except Exception as e:
            print(f"❌ {model_name} Error: {str(e)}")
            print()
            continue
    
    print("📝 API Tests completed. If no model worked:")
    print("  • Check API key validity")
    print("  • Verify network connectivity")  
    print("  • Check API quotas and limits")
    print()
    print("💡 The application will work with fallback features:")
    print("   ✓ Resume text extraction and cleaning")
    print("   ✓ Keyword-based resume comparison")
    print("   ✓ Skills and contact extraction")
    print("   ✓ Interactive web interface")
    
    return False

if __name__ == "__main__":
    print("🧪 GEMINI API CONNECTIVITY TEST")
    print("=" * 50)
    test_gemini_api()
