import json
import os
from typing import Dict, List, Any, Optional

class MedicalKnowledgeBase:
    def __init__(self):
        """Initialize the medical knowledge base."""
        self.knowledge_file = "data/medical_knowledge.json"
        self.knowledge_data = self._load_medical_data()
    
    def _load_medical_data(self) -> Dict[str, Any]:
        """Load medical knowledge from JSON file."""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading medical data: {e}")
                return self._create_default_knowledge()
        else:
            return self._create_default_knowledge()
    
    def _create_default_knowledge(self) -> Dict[str, Any]:
        """Create default medical knowledge base."""
        default_data = {
            "symptoms": {
                "headache": {
                    "description": "Pain or discomfort in the head or neck area",
                    "common_causes": ["Tension", "Migraine", "Dehydration", "Stress", "Eye strain"],
                    "self_care": ["Rest in a dark room", "Apply cold compress", "Stay hydrated", "Over-the-counter pain relievers"],
                    "when_to_see_doctor": ["Severe headache", "Headache with fever", "Sudden onset", "Headache after head injury"]
                },
                "fever": {
                    "description": "Elevated body temperature above normal (98.6°F/37°C)",
                    "common_causes": ["Viral infections", "Bacterial infections", "Inflammatory conditions"],
                    "self_care": ["Rest", "Stay hydrated", "Cool compress", "Over-the-counter fever reducers"],
                    "when_to_see_doctor": ["Fever above 103°F (39.4°C)", "Fever lasting more than 3 days", "Fever with rash"]
                },
                "cough": {
                    "description": "Reflex action to clear airways of mucus and irritants",
                    "common_causes": ["Common cold", "Flu", "Allergies", "Asthma", "Smoking"],
                    "self_care": ["Stay hydrated", "Use humidifier", "Honey and warm liquids", "Avoid irritants"],
                    "when_to_see_doctor": ["Persistent cough", "Cough with blood", "Cough with chest pain"]
                },
                "chest_pain": {
                    "description": "Pain or discomfort in the chest area",
                    "common_causes": ["Heart conditions", "Muscle strain", "Acid reflux", "Anxiety"],
                    "self_care": ["Rest", "Avoid strenuous activity", "Monitor symptoms"],
                    "when_to_see_doctor": ["Severe chest pain", "Pain radiating to arm/jaw", "Shortness of breath", "Call 911 immediately"]
                },
                "abdominal_pain": {
                    "description": "Pain or discomfort in the stomach or belly area",
                    "common_causes": ["Indigestion", "Gas", "Food poisoning", "Appendicitis", "Gallstones"],
                    "self_care": ["Rest", "Avoid solid foods", "Stay hydrated", "Apply heat"],
                    "when_to_see_doctor": ["Severe pain", "Pain with vomiting", "Pain lasting more than 24 hours"]
                }
            },
            "conditions": {
                "common_cold": {
                    "symptoms": ["Runny nose", "Sneezing", "Sore throat", "Cough", "Mild fever"],
                    "duration": "7-10 days",
                    "treatment": ["Rest", "Hydration", "Saline nasal spray", "Over-the-counter medications"],
                    "prevention": ["Hand washing", "Avoid close contact with sick people", "Boost immune system"]
                },
                "influenza": {
                    "symptoms": ["High fever", "Body aches", "Fatigue", "Cough", "Headache"],
                    "duration": "1-2 weeks",
                    "treatment": ["Rest", "Hydration", "Antiviral medications", "Symptom relief"],
                    "prevention": ["Annual flu vaccine", "Hand hygiene", "Avoid crowds during flu season"]
                },
                "hypertension": {
                    "symptoms": ["Often asymptomatic", "Headaches", "Shortness of breath", "Nosebleeds"],
                    "management": ["Low-sodium diet", "Regular exercise", "Weight management", "Medication"],
                    "monitoring": ["Regular blood pressure checks", "Lifestyle modifications", "Medical follow-up"]
                },
                "diabetes": {
                    "symptoms": ["Increased thirst", "Frequent urination", "Fatigue", "Blurred vision"],
                    "management": ["Blood sugar monitoring", "Healthy diet", "Regular exercise", "Medication"],
                    "complications": ["Heart disease", "Kidney damage", "Nerve damage", "Eye problems"]
                }
            },
            "emergency_signs": [
                "Severe chest pain",
                "Difficulty breathing",
                "Loss of consciousness",
                "Severe bleeding",
                "Signs of stroke (facial drooping, arm weakness, speech difficulty)",
                "Severe allergic reaction",
                "High fever with rash",
                "Severe abdominal pain"
            ],
            "first_aid": {
                "choking": "Perform Heimlich maneuver or back blows",
                "bleeding": "Apply direct pressure, elevate if possible",
                "burns": "Cool with water, don't use ice, cover loosely",
                "fainting": "Lay person flat, elevate legs, check breathing"
            }
        }
        
        # Save default data to file
        os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)
        
        return default_data
    
    def get_symptom_info(self, symptom: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific symptom."""
        return self.knowledge_data.get("symptoms", {}).get(symptom.lower())
    
    def get_condition_info(self, condition: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific medical condition."""
        return self.knowledge_data.get("conditions", {}).get(condition.lower())
    
    def search_symptoms(self, query: str) -> List[str]:
        """Search for symptoms matching the query."""
        query_lower = query.lower()
        matching_symptoms = []
        
        for symptom, info in self.knowledge_data.get("symptoms", {}).items():
            if (query_lower in symptom or 
                query_lower in info.get("description", "").lower() or
                any(query_lower in cause.lower() for cause in info.get("common_causes", []))):
                matching_symptoms.append(symptom)
        
        return matching_symptoms
    
    def get_emergency_signs(self) -> List[str]:
        """Get list of emergency warning signs."""
        return self.knowledge_data.get("emergency_signs", [])
    
    def get_first_aid_info(self, situation: str) -> Optional[str]:
        """Get first aid information for a specific situation."""
        return self.knowledge_data.get("first_aid", {}).get(situation.lower())
    
    def assess_urgency(self, symptoms: List[str]) -> str:
        """Assess the urgency level based on symptoms."""
        emergency_signs = self.get_emergency_signs()
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if any(emergency in symptom_lower for emergency in emergency_signs):
                return "emergency"
        
        # Check for moderate urgency symptoms
        moderate_symptoms = ["fever", "persistent cough", "severe pain", "dizziness", "nausea"]
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if any(moderate in symptom_lower for moderate in moderate_symptoms):
                return "moderate"
        
        return "low"
    
    def get_recommendations(self, symptoms: List[str]) -> Dict[str, Any]:
        """Get recommendations based on symptoms."""
        urgency = self.assess_urgency(symptoms)
        
        recommendations = {
            "urgency_level": urgency,
            "immediate_actions": [],
            "self_care": [],
            "when_to_seek_help": []
        }
        
        if urgency == "emergency":
            recommendations["immediate_actions"].append("Call 911 or go to emergency room immediately")
        elif urgency == "moderate":
            recommendations["immediate_actions"].append("Schedule appointment with healthcare provider")
            recommendations["self_care"].extend(["Rest", "Stay hydrated", "Monitor symptoms"])
        else:
            recommendations["self_care"].extend(["Rest", "Stay hydrated", "Over-the-counter medications if appropriate"])
            recommendations["when_to_seek_help"].append("If symptoms worsen or persist for more than a few days")
        
        return recommendations
