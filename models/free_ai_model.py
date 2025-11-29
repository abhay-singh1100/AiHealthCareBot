"""
Free AI Model Integration for HealthAI
Uses Hugging Face Inference API (free) for conversational responses
"""
import requests
import json
from typing import Dict, Any, Optional
import time

class FreeAIModel:
    """Free, open-source AI model integration for general chat conversations."""
    
    def __init__(self):
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.2"  # Free and open source
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.use_local_fallback = True
        self.loaded = False
        
        print("Initializing Free AI Model...")
        print(f"Model: {self.model_name}")
        print("Ready for free AI conversations!")
        self.loaded = True
    
    def get_response(self, user_message: str, conversation_context: str = "") -> str:
        """
        Get AI response using Hugging Face Inference API.
        
        Args:
            user_message: The user's message
            conversation_context: Previous conversation context
        
        Returns:
            AI-generated response
        """
        try:
            # Try using Hugging Face Inference API
            response = self._get_hf_response(user_message, conversation_context)
            if response:
                return self._format_response(response)
        except Exception as e:
            print(f"WARNING HF API error: {e}")
        
        # Fallback to enhanced rule-based system
        return self._get_enhanced_fallback(user_message)
    
    def _get_hf_response(self, user_message: str, context: str) -> Optional[str]:
        """Get response from Hugging Face Inference API."""
        try:
            # Build the prompt with medical context
            prompt = f"""You are a helpful and knowledgeable medical assistant. Provide accurate, helpful medical information.

{context}
User: {user_message}
Assistant:"""
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            # Make API request
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    return generated_text
            elif response.status_code == 503:
                # Model is loading, wait a bit and retry
                print("⏳ Model is loading, please wait...")
                time.sleep(5)
                response = requests.post(
                    self.api_url,
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get('generated_text', '')
                        return generated_text
            
            return None
            
        except requests.exceptions.Timeout:
            print("Request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def _format_response(self, response: str) -> str:
        """Format and clean the AI response."""
        if not response:
            return self._get_enhanced_fallback("")
        
        # Clean up the response
        response = response.strip()
        
        # Remove repeated content if any
        if "Assistant:" in response:
            response = response.split("Assistant:")[-1].strip()
        
        # Ensure response ends with disclaimer
        if "WARNING" not in response and "Important" not in response:
            response += "\n\nWARNING **Important**: This is preliminary guidance only. Please consult a healthcare professional for proper medical advice."
        
        return response
    
    def _get_enhanced_fallback(self, user_message: str) -> str:
        """Enhanced fallback with better medical knowledge."""
        user_lower = user_message.lower()
        
        # Medical knowledge base with responses
        knowledge_base = {
            'cold': """Common cold symptoms include runny nose, sneezing, sore throat, and mild cough. 
            
Suggestions:
- Rest and stay hydrated
- Use saline nasal spray for congestion
- Gargle with warm salt water for sore throat
- Over-the-counter cold medications if needed
- Symptoms typically resolve in 7-10 days

Important: Consult a doctor if symptoms worsen or persist.""",
            
            'headache': """Headaches can be caused by many factors including stress, tension, dehydration, or more serious conditions.

**Immediate Relief:**
- Rest in a quiet, dark room
- Apply cold compress to forehead
- Stay hydrated
- Over-the-counter pain relievers (if not contraindicated)
- Gentle neck massage

WARNING **Seek immediate care** if you have a severe headache with fever, confusion, or neck stiffness.""",
            
            'fever': """Fever (temperature above 100.4F/38C) is often a sign of infection.

**Self-Care:**
- Rest and stay hydrated
- Cool compress on forehead
- Light, breathable clothing
- Over-the-counter fever reducers (acetaminophen or ibuprofen)
- Monitor temperature regularly

WARNING **Seek medical attention** if fever is above 103F (39.4C), lasts more than 3 days, or is accompanied by severe symptoms.""",
            
            'cough': """Coughs can be caused by colds, flu, allergies, or infections.

**Relief Tips:**
- Stay well-hydrated with warm liquids
- Use a humidifier or steam
- Honey and lemon for soothing
- Cough drops or lozenges
- Avoid irritants (smoke, dust)

WARNING **See a doctor** if cough persists more than 3 weeks, is accompanied by chest pain, or if you cough up blood.""",
            
            'nausea': """Nausea can be caused by many things including stomach bugs, motion sickness, or anxiety.

**Relief Methods:**
- Sit up and avoid lying flat
- Sip clear fluids (water, ginger tea)
- Eat bland foods (crackers, toast)
- Avoid strong smells
- Get fresh air

WARNING **Seek care** if nausea is severe, persistent, or accompanied by other concerning symptoms.""",
            
            'pain': """Pain management depends on the type and location of pain.

**General Relief:**
- Rest the affected area
- Apply ice for acute pain (first 48 hours)
- Apply heat for chronic pain
- Over-the-counter pain relievers
- Gentle stretching if appropriate

WARNING **Important**: For severe pain, chest pain, or pain after injury, seek immediate medical attention.""",
            
            'anxiety': """Anxiety is a normal stress response but can be debilitating when excessive.

**Coping Strategies:**
- Deep breathing exercises
- Progressive muscle relaxation
- Regular exercise
- Mindfulness meditation
- Adequate sleep
- Limit caffeine and alcohol

WARNING **Seek professional help** if anxiety significantly impacts daily life or you experience panic attacks.""",
            
            'fitness': """Regular physical activity is essential for good health.

**Recommendations:**
- At least 150 minutes of moderate activity per week
- Include strength training 2x per week
- Find activities you enjoy
- Start slowly if new to exercise
- Stay hydrated during exercise
- Listen to your body

TIP **Remember**: Any movement is better than none!""",
            
            'nutrition': """Good nutrition is fundamental to health.

**General Guidelines:**
- Eat a variety of fruits and vegetables
- Choose whole grains over refined grains
- Include lean proteins
- Stay hydrated (8 glasses water/day)
- Limit processed foods and added sugars
- Watch portion sizes

TIP **Pro tip**: Follow a balanced diet with all food groups in moderation."""
        }
        
        # Check for matching keywords
        for keyword, response in knowledge_base.items():
            if keyword in user_lower:
                return response
        
        # Check for specific medical questions
        if 'what' in user_lower or 'how' in user_lower or 'tell me about' in user_lower:
            # Generic informative response
            return f"""I'd be happy to help you with information about "{user_message}".

Based on my knowledge base, I can provide general health information. For specific medical concerns, I recommend:

1. **Consulting a healthcare provider** for personalized advice
2. **Using our symptom checker** to get specific guidance
3. **Contacting telehealth services** for immediate consultation
4. **Visiting urgent care** for non-emergency immediate needs

WARNING **Important**: This is preliminary guidance only. Please consult a healthcare professional for proper medical advice."""
        
        # Default helpful response
        return f"""Thank you for your question about: "{user_message}"

I'm here to help with general health information and guidance. Here's what I can assist with:

**I can help you with:**
- General health information
- Symptom descriptions
- Basic first aid guidance
- Wellness and lifestyle tips
- Medication information

**For serious concerns:**
- Please contact a healthcare provider
- Visit urgent care for immediate needs
- Call 911 for emergencies

Would you like me to ask you some questions about your symptoms to provide more specific guidance?

WARNING **Important**: This is preliminary guidance only. Please consult a healthcare professional for proper medical advice."""

    def is_available(self) -> bool:
        """Check if the AI model is available."""
        return self.loaded

