import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import sqlite3

class ConversationManager:
    """Manages conversational state and tracks symptom analysis flow."""
    
    def __init__(self, ai_model=None):
        self.conversation_states = {}  # session_id -> conversation_state
        self.current_session = None
        self.ai_model = ai_model  # Optional AI model for general chat
        self.load_medical_data()
    
    def load_medical_data(self):
        """Load medical knowledge for symptom analysis."""
        try:
            with open('data/medical_knowledge.json', 'r', encoding='utf-8') as f:
                self.medical_data = json.load(f)
        except:
            self.medical_data = {}
    
    def get_state(self, session_id: str) -> Dict[str, Any]:
        """Get conversation state for a session."""
        if session_id not in self.conversation_states:
            self.conversation_states[session_id] = {
                'stage': 'initial',  # initial, gathering_symptoms, suggesting
                'symptoms': [],
                'symptom_details': {},
                'follow_up_questions': [],
                'question_index': 0,
                'potential_conditions': [],
                'risk_level': 'low'
            }
        return self.conversation_states[session_id]
    
    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """Process user message and return appropriate response."""
        self.current_session = session_id
        state = self.get_state(session_id)
        user_message_lower = user_message.lower()
        
        # Detect if this is an initial symptom report
        detected_symptoms = self._detect_symptoms(user_message)
        
        if state['stage'] == 'initial' and detected_symptoms:
            # Start symptom gathering
            state['stage'] = 'gathering_symptoms'
            state['symptoms'] = detected_symptoms
            state['symptom_details'][detected_symptoms[0]] = user_message
            state['question_index'] = 1  # Increment to track that we've asked the first question
            
            # Ask first follow-up question
            follow_up = self._get_follow_up_question(detected_symptoms[0])
            
            return {
                'response': follow_up['response'],
                'next_question': follow_up.get('next_question'),
                'stage': state['stage'],
                'suggestions': follow_up.get('suggestions', [])
            }
        
        elif state['stage'] == 'gathering_symptoms':
            # Processing follow-up answers
            current_symptom = state['symptoms'][-1]
            state['symptom_details'][current_symptom] = user_message
            
            # Check if we should continue asking or start suggesting
            # Since we already asked question 0 in initial stage, we use question_index as-is
            question_index = state['question_index']
            max_questions = self._get_max_questions_for_symptom(current_symptom)
            
            if question_index < max_questions:
                # Ask next question (index 1, 2, 3, etc.)
                follow_up = self._get_next_follow_up(current_symptom, question_index)
                state['question_index'] += 1
                
                return {
                    'response': follow_up['response'],
                    'next_question': follow_up.get('next_question'),
                    'stage': state['stage'],
                    'suggestions': follow_up.get('suggestions', [])
                }
            else:
                # Done asking questions - start suggesting medications
                state['stage'] = 'suggesting'
                suggestions = self._generate_suggestions(state)
                state = self.conversation_states[session_id]  # Update state
                
                return {
                    'response': suggestions['response'],
                    'medications': suggestions.get('medications', []),
                    'recommendations': suggestions.get('recommendations', []),
                    'stage': state['stage']
                }
        
        elif state['stage'] == 'suggesting':
            # Check if user wants to start new analysis
            if any(keyword in user_message_lower for keyword in ['new', 'another', 'different', 'reset', 'start over']):
                state = self._reset_state(session_id)
                return {
                    'response': 'Okay, I\'m ready to help you with a new symptom or health concern. What would you like to ask about?',
                    'stage': 'initial'
                }
            else:
                # Provide general response
                return {
                    'response': self._generate_general_response(user_message),
                    'stage': state['stage']
                }
        
        else:
            # General conversation - use AI if available
            if detected_symptoms and state['stage'] == 'initial':
                response = self._generate_general_response(user_message)
                response += '\n\nWould you like me to ask you some questions to better understand your symptoms?'
            else:
                # Use AI for general questions
                response = self._generate_general_response(user_message)
            
            return {'response': response}
    
    def _detect_symptoms(self, message: str) -> List[str]:
        """Detect symptoms in user message."""
        symptoms = self.medical_data.get('symptoms', {})
        detected = []
        message_lower = message.lower()
        
        for symptom_key, symptom_data in symptoms.items():
            if symptom_key in message_lower:
                detected.append(symptom_key)
            elif any(cause.lower() in message_lower for cause in symptom_data.get('common_causes', [])):
                detected.append(symptom_key)
        
        return detected
    
    def _get_follow_up_question(self, symptom: str) -> Dict[str, Any]:
        """Get first follow-up question for a symptom."""
        questions_by_symptom = {
            'headache': {
                'questions': [
                    "How long have you been experiencing this headache? (hours/days)",
                    "Can you rate the pain on a scale of 1-10?",
                    "Does anything seem to trigger or worsen it?",
                    "Have you tried any pain relievers already?"
                ],
                'response': f"Thank you for describing your headache. Let me ask you a few questions to better understand your situation."
            },
            'fever': {
                'questions': [
                    "What is your current temperature? (if you know)",
                    "How long have you had the fever?",
                    "Do you have any other symptoms? (chills, body aches, cough)",
                    "Have you taken any fever reducers?"
                ],
                'response': "I understand you have a fever. Let me gather some important details."
            },
            'cough': {
                'questions': [
                    "How long have you been coughing?",
                    "Is it a dry cough or do you have mucus?",
                    "Does your cough worsen at certain times of day?",
                    "Have you been exposed to anyone who's been sick recently?"
                ],
                'response': "Thank you for mentioning your cough. I'd like to understand it better."
            },
            'abdominal_pain': {
                'questions': [
                    "Where exactly is the pain located? (upper/lower abdomen)",
                    "How would you describe the pain? (sharp, dull, cramping)",
                    "How long has it been going on?",
                    "Are there any activities that make it better or worse?"
                ],
                'response': "I see you're experiencing abdominal pain. Let me ask you some questions to help assess this."
            },
            'dizziness': {
                'questions': [
                    "When does the dizziness occur? (standing up, after eating, randomly)",
                    "Do you feel lightheaded or like the room is spinning?",
                    "How long do the episodes last?",
                    "Have you had any recent falls or injuries?"
                ],
                'response': "Thank you for mentioning dizziness. I need to ask you a few questions."
            }
        }
        
        default = {
            'questions': [
                "How long have you been experiencing this?",
                "How severe would you rate it on a scale of 1-10?",
                "Have you tried any treatments yet?",
                "Are there any other symptoms accompanying this?"
            ],
            'response': f"Thank you for describing your symptoms. Let me ask a few questions."
        }
        
        symptom_data = questions_by_symptom.get(symptom, default)
        
        return {
            'response': symptom_data['response'] + "\n\n" + symptom_data['questions'][0] + "\n\n**Please respond with your answer.**",
            'next_question': symptom_data['questions'][0]
        }
    
    def _get_next_follow_up(self, symptom: str, question_index: int) -> Dict[str, Any]:
        """Get next follow-up question."""
        questions_by_symptom = {
            'headache': [
                "How long have you been experiencing this headache? (hours/days)",
                "Can you rate the pain on a scale of 1-10?",
                "Does anything seem to trigger or worsen it?",
                "Have you tried any pain relievers already?"
            ],
            'fever': [
                "What is your current temperature? (if you know)",
                "How long have you had the fever?",
                "Do you have any other symptoms? (chills, body aches, cough)",
                "Have you taken any fever reducers?"
            ],
            'cough': [
                "How long have you been coughing?",
                "Is it a dry cough or do you have mucus?",
                "Does your cough worsen at certain times of day?",
                "Have you been exposed to anyone who's been sick recently?"
            ],
            'abdominal_pain': [
                "Where exactly is the pain located? (upper/lower abdomen)",
                "How would you describe the pain? (sharp, dull, cramping)",
                "How long has it been going on?",
                "Are there any activities that make it better or worse?"
            ],
            'dizziness': [
                "When does the dizziness occur? (standing up, after eating, randomly)",
                "Do you feel lightheaded or like the room is spinning?",
                "How long do the episodes last?",
                "Have you had any recent falls or injuries?"
            ]
        }
        
        default_questions = [
            "How long have you been experiencing this?",
            "How severe would you rate it on a scale of 1-10?",
            "Have you tried any treatments yet?",
            "Are there any other symptoms accompanying this?"
        ]
        
        questions = questions_by_symptom.get(symptom, default_questions)
        
        if question_index < len(questions):
            return {
                'response': questions[question_index] + "\n\n**Please provide your answer.**",
                'next_question': questions[question_index]
            }
        else:
            # Done with questions, start suggesting
            return self._generate_suggestions(self.conversation_states.get('current_session', {'symptoms': [symptom]}))
    
    def _get_max_questions_for_symptom(self, symptom: str) -> int:
        """Get maximum number of questions to ask for a symptom."""
        return 4  # Default to 4 questions
    
    def _generate_suggestions(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate medication suggestions based on gathered symptoms."""
        symptoms = state.get('symptoms', [])
        
        if not symptoms:
            return {
                'response': "Based on our conversation, I recommend consulting with a healthcare professional for personalized advice.",
                'medications': [],
                'recommendations': ["Consult with a healthcare professional"]
            }
        
        # Analyze symptoms and suggest medications
        suggested_medications = []
        recommendations = []
        
        for symptom in symptoms:
            symptom_info = self.medical_data.get('symptoms', {}).get(symptom, {})
            
            if symptom == 'headache':
                suggested_medications.extend([
                    {'name': 'Acetaminophen (Tylenol)', 'dosage': '500-1000mg', 'frequency': 'Every 4-6 hours', 'notes': 'For mild to moderate pain'},
                    {'name': 'Ibuprofen (Advil)', 'dosage': '200-400mg', 'frequency': 'Every 4-6 hours', 'notes': 'Anti-inflammatory, take with food'},
                ])
                recommendations.extend(['Rest in a dark room', 'Apply cold compress', 'Stay hydrated'])
            
            elif symptom == 'fever':
                suggested_medications.extend([
                    {'name': 'Acetaminophen (Tylenol)', 'dosage': '500-1000mg', 'frequency': 'Every 4-6 hours', 'notes': 'Reduces fever'},
                    {'name': 'Ibuprofen (Advil)', 'dosage': '200-400mg', 'frequency': 'Every 6-8 hours', 'notes': 'If fever persists'},
                ])
                recommendations.extend(['Rest', 'Stay hydrated', 'Use cool compresses', 'Light clothing'])
            
            elif symptom == 'cough':
                suggested_medications.extend([
                    {'name': 'Dextromethorphan (Cough Suppressant)', 'dosage': '15-30mg', 'frequency': 'Every 4-6 hours', 'notes': 'For dry cough'},
                    {'name': 'Guaifenesin (Expectorant)', 'dosage': '200-400mg', 'frequency': 'Every 4 hours', 'notes': 'For productive cough'},
                ])
                recommendations.extend(['Stay hydrated', 'Use humidifier', 'Honey and warm liquids'])
            
            elif symptom == 'abdominal_pain':
                suggested_medications.extend([
                    {'name': 'Antacids (Tums, Rolaids)', 'dosage': 'As directed', 'frequency': 'When needed', 'notes': 'For indigestion'},
                    {'name': 'Simethicone (Gas-X)', 'dosage': '40-125mg', 'frequency': 'After meals', 'notes': 'For gas'},
                ])
                recommendations.extend(['Avoid trigger foods', 'Small meals', 'Apply heat to abdomen'])
        
        # Create comprehensive response
        response = "Based on your symptoms and our conversation, here's what I recommend:\n\n"
        response += "**Suggested Medications:**\n"
        
        for med in suggested_medications:
            response += f"\n• {med['name']}\n"
            response += f"  - Dosage: {med['dosage']}\n"
            response += f"  - Frequency: {med['frequency']}\n"
            response += f"  - Note: {med['notes']}\n"
        
        response += "\n**Additional Recommendations:**\n"
        for rec in recommendations:
            response += f"• {rec}\n"
        
        response += "\n⚠️ **Important Disclaimer:**\n"
        response += "Please consult with a healthcare professional before taking any medications, especially if you:\n"
        response += "- Are pregnant or breastfeeding\n"
        response += "- Have existing medical conditions\n"
        response += "- Are taking other medications\n"
        response += "- Have allergies to medications"
        
        return {
            'response': response,
            'medications': suggested_medications,
            'recommendations': recommendations
        }
    
    def _generate_general_response(self, message: str) -> str:
        """Generate general response for non-symptom queries using AI if available."""
        # Try using AI model if available
        if self.ai_model and self.ai_model.is_available():
            try:
                ai_response = self.ai_model.get_response(message)
                return ai_response
            except Exception as e:
                print(f"AI model error: {e}, using fallback")
        
        # Fallback response
        return f"I understand you're asking about: {message}\n\n" + \
               "I can help you with symptom analysis and general health information. " + \
               "If you're experiencing any symptoms, please describe them and I'll guide you through some questions."
    
    def _reset_state(self, session_id: str) -> Dict[str, Any]:
        """Reset conversation state."""
        self.conversation_states[session_id] = {
            'stage': 'initial',
            'symptoms': [],
            'symptom_details': {},
            'follow_up_questions': [],
            'question_index': 0,
            'potential_conditions': [],
            'risk_level': 'low'
        }
        return self.conversation_states[session_id]

