#!/usr/bin/env python3
"""
HealthAI Test Script
Tests the basic functionality of the HealthAI application
"""

import sys
import os
import json

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import flask_cors
        print("✅ Flask-CORS imported successfully")
    except ImportError as e:
        print(f"❌ Flask-CORS import failed: {e}")
        return False
    
    try:
        import sqlite3
        print("✅ SQLite3 imported successfully")
    except ImportError as e:
        print(f"❌ SQLite3 import failed: {e}")
        return False
    
    try:
        import torch
        print("✅ PyTorch imported successfully")
    except ImportError as e:
        print(f"⚠️ PyTorch import failed: {e}")
        print("   This is optional - the app will use fallback responses")
    
    try:
        import transformers
        print("✅ Transformers imported successfully")
    except ImportError as e:
        print(f"⚠️ Transformers import failed: {e}")
        print("   This is optional - the app will use fallback responses")
    
    return True

def test_medical_database():
    """Test the medical knowledge database."""
    print("\nTesting medical database...")
    
    try:
        with open('data/medical_knowledge.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'symptoms' in data and 'conditions' in data:
            print("✅ Medical knowledge database loaded successfully")
            print(f"   Found {len(data['symptoms'])} symptoms")
            print(f"   Found {len(data['conditions'])} conditions")
            return True
        else:
            print("❌ Medical knowledge database structure invalid")
            return False
            
    except FileNotFoundError:
        print("❌ Medical knowledge database file not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Medical knowledge database JSON error: {e}")
        return False

def test_models():
    """Test the AI models."""
    print("\nTesting AI models...")
    
    try:
        from models.medical_db import MedicalKnowledgeBase
        medical_db = MedicalKnowledgeBase()
        
        # Test symptom lookup
        headache_info = medical_db.get_symptom_info('headache')
        if headache_info:
            print("✅ Medical knowledge base working")
        else:
            print("❌ Medical knowledge base not working")
            return False
        
        # Test AI model (optional)
        try:
            from models.qwen_model import QwenMedicalAssistant
            ai_assistant = QwenMedicalAssistant()
            print("✅ AI model initialized (may use fallback)")
        except Exception as e:
            print(f"⚠️ AI model initialization failed: {e}")
            print("   App will use rule-based fallback responses")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_flask_app():
    """Test Flask application creation."""
    print("\nTesting Flask application...")
    
    try:
        from app import app
        print("✅ Flask application created successfully")
        
        # Test if we can create a test client
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page accessible")
            else:
                print(f"❌ Home page returned status {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🏥 HealthAI Application Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_medical_database,
        test_models,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo start the application:")
        print("  Windows: Run start_healthai.bat")
        print("  Linux/Mac: Run ./start_healthai.sh")
        print("  Manual: python app.py")
        print("\nThen open: http://localhost:5000")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("The application may still work with limited functionality.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
