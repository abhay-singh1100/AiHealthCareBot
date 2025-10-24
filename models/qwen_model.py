import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import re
from typing import List, Dict, Any

class QwenMedicalAssistant:
    def __init__(self):
        """Initialize the Qwen AI model for medical assistance."""
        self.model_name = "Qwen/Qwen-7B-Chat"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🤖 Loading Qwen model on {self.device}...")
        
        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
                
            print("✅ Qwen model loaded successfully!")
            
        except Exception as e:
            print(f"⚠️ Could not load Qwen model: {e}")
            print("🔄 Falling back to rule-based responses...")
            self.model = None
            self.tokenizer = None
    
    def get_response(self, user_input: str) -> str:
        """Generate a medical response using Qwen AI or fallback system."""
        try:
            if self.model and self.tokenizer:
                return self._generate_ai_response(user_input)
            else:
                return self._generate_fallback_response(user_input)
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._generate_fallback_response(user_input)
    
    def _generate_ai_response(self, user_input: str) -> str:
        """Generate response using Qwen AI model."""
        # Create medical context prompt
        medical_prompt = f"""You are a helpful medical assistant. Provide accurate, helpful medical information while always reminding users to consult healthcare professionals for serious concerns.

User Question: {user_input}

Medical Assistant Response:"""
        
        # Tokenize input
        inputs = self.tokenizer.encode(medical_prompt, return_tensors="pt").to(self.device)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=inputs.shape[1] + 200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the assistant's response
        if "Medical Assistant Response:" in response:
            response = response.split("Medical Assistant Response:")[-1].strip()
        
        # Add medical disclaimer
        disclaimer = "\n\n⚠️ **Important**: This is preliminary guidance only. Please consult a healthcare professional for proper medical advice, especially for serious symptoms."
        
        return response + disclaimer
    
    def _generate_fallback_response(self, user_input: str) -> str:
        """Generate fallback response using rule-based system."""
        user_input_lower = user_input.lower()
        
        # Common medical queries and responses
        responses = {
            'headache': "Headaches can have various causes. Try rest, hydration, and over-the-counter pain relief. If severe or persistent, consult a doctor.",
            'fever': "For adults, fever above 100.4°F (38°C) may indicate infection. Rest, stay hydrated, and monitor symptoms. Seek medical attention if fever persists.",
            'cough': "Coughs can be due to colds, allergies, or infections. Stay hydrated, use humidifiers, and avoid irritants. See a doctor if cough persists or worsens.",
            'pain': "Pain management depends on the type and location. Rest, ice/heat therapy, and over-the-counter pain relievers may help. Consult a doctor for severe pain.",
            'cold': "Common cold symptoms include runny nose, sneezing, and congestion. Rest, stay hydrated, and use saline nasal sprays. Symptoms usually resolve in 7-10 days.",
            'flu': "Flu symptoms include fever, body aches, and fatigue. Rest, stay hydrated, and consider antiviral medication if caught early. Seek medical attention if symptoms worsen.",
            'anxiety': "Anxiety can be managed with breathing exercises, regular exercise, and stress management techniques. Consider speaking with a mental health professional.",
            'depression': "Depression is a serious condition. Reach out to mental health professionals, maintain social connections, and consider therapy or medication.",
            'diabetes': "Diabetes management requires monitoring blood sugar, following a healthy diet, regular exercise, and medication adherence. Regular check-ups are essential.",
            'hypertension': "High blood pressure management includes lifestyle changes (diet, exercise, stress reduction) and medication as prescribed by your doctor."
        }
        
        # Find matching response
        for keyword, response in responses.items():
            if keyword in user_input_lower:
                return f"{response}\n\n⚠️ **Important**: This is preliminary guidance only. Please consult a healthcare professional for proper medical advice."
        
        # General response for unmatched queries
        return f"""I understand you're asking about: "{user_input}"

While I can provide general health information, I recommend:
1. Consulting with a healthcare professional for accurate diagnosis
2. Visiting urgent care for immediate concerns
3. Calling emergency services (911) for life-threatening situations

⚠️ **Important**: This is preliminary guidance only. Please consult a healthcare professional for proper medical advice."""

    def analyze_symptoms(self, symptoms: List[str]) -> Dict[str, Any]:
        """Analyze a list of symptoms and provide preliminary assessment."""
        analysis = {
            'urgency_level': 'low',
            'recommended_actions': [],
            'common_causes': [],
            'warning_signs': []
        }
        
        # Simple symptom analysis logic
        urgent_symptoms = ['chest pain', 'difficulty breathing', 'severe headache', 'loss of consciousness']
        moderate_symptoms = ['fever', 'persistent cough', 'abdominal pain', 'dizziness']
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if any(urgent in symptom_lower for urgent in urgent_symptoms):
                analysis['urgency_level'] = 'high'
                analysis['recommended_actions'].append('Seek immediate medical attention')
            elif any(moderate in symptom_lower for moderate in moderate_symptoms):
                if analysis['urgency_level'] == 'low':
                    analysis['urgency_level'] = 'moderate'
                analysis['recommended_actions'].append('Schedule a doctor appointment')
        
        return analysis
