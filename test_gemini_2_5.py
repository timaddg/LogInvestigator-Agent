#!/usr/bin/env python3
"""
Test script to verify Gemini 2.5 Pro is working correctly.
"""

import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

def test_gemini_2_5():
    """Test Gemini 2.5 Pro model."""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("Please set your Gemini API key in the .env file")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with Gemini 2.5 Pro
        model_name = "gemini-2.5-pro"
        print(f"🧪 Testing {model_name}...")
        
        # Create model instance
        model = genai.GenerativeModel(model_name)
        
        # Simple test prompt
        test_prompt = "Hello! Please respond with 'Gemini 2.5 Pro is working correctly!' and nothing else."
        
        print("📤 Sending test request...")
        response = model.generate_content(test_prompt)
        
        if response and response.text:
            print("✅ Gemini 2.5 Pro is working correctly!")
            print(f"📝 Response: {response.text.strip()}")
            return True
        else:
            print("❌ No response received from Gemini 2.5 Pro")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini 2.5 Pro: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Gemini 2.5 Pro Configuration")
    print("=" * 50)
    
    success = test_gemini_2_5()
    
    print("=" * 50)
    if success:
        print("🎉 All tests passed! Gemini 2.5 Pro is ready to use.")
    else:
        print("💥 Tests failed. Please check your configuration.")
    
    sys.exit(0 if success else 1) 