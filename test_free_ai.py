"""
Test script for Free AI Model functionality
"""
from models.free_ai_model import FreeAIModel

def test_free_ai_model():
    """Test the free AI model with various queries."""
    print("=" * 60)
    print("Testing Free AI Model")
    print("=" * 60)
    
    # Initialize the AI model
    print("\n1. Initializing AI Model...")
    ai = FreeAIModel()
    
    # Test cases
    test_cases = [
        "What causes headaches?",
        "I have a fever, what should I do?",
        "Tell me about healthy eating habits",
        "How to relieve stress?",
    ]
    
    # Run tests
    for i, query in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"Test {i}: {query}")
        print('=' * 60)
        
        try:
            response = ai.get_response(query)
            print(f"\nResponse:\n{response}\n")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_free_ai_model()

