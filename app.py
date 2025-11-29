from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import sqlite3
import os
from datetime import datetime
from models.qwen_model import QwenMedicalAssistant
from models.medical_db import MedicalKnowledgeBase
from models.conversation_manager import ConversationManager
from models.free_ai_model import FreeAIModel

app = Flask(__name__)
CORS(app)

# Initialize AI models - Free AI is lightweight and always available
print("🤖 Initializing AI Models...")
free_ai = FreeAIModel()  # Free, lightweight AI for general chat
ai_assistant = QwenMedicalAssistant()  # Optional, heavier model

# Initialize medical knowledge base
medical_db = MedicalKnowledgeBase()

# Initialize conversation manager with free AI
conversation_manager = ConversationManager(ai_model=free_ai)

# Database setup
def init_db():
    conn = sqlite3.connect('healthai.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            message TEXT,
            response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Use conversation manager for intelligent Q&A
        conversation_result = conversation_manager.process_message(session_id, user_message)
        
        # Store conversation in database
        store_conversation(session_id, user_message, conversation_result.get('response', ''))
        
        # Prepare response with conversation state
        response_data = {
            'response': conversation_result.get('response', ''),
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'stage': conversation_result.get('stage', 'general'),
            'next_question': conversation_result.get('next_question'),
            'medications': conversation_result.get('medications', []),
            'recommendations': conversation_result.get('recommendations', [])
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/medical-info/<symptom>')
def get_medical_info(symptom):
    try:
        info = medical_db.get_symptom_info(symptom.lower())
        return jsonify({'info': info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def store_conversation(session_id, message, response):
    conn = sqlite3.connect('healthai.db')
    cursor = conn.cursor()
    
    # Ensure session exists
    cursor.execute('INSERT OR IGNORE INTO chat_sessions (session_id) VALUES (?)', (session_id,))
    
    # Store message and response
    cursor.execute('''
        INSERT INTO messages (session_id, message, response)
        VALUES (?, ?, ?)
    ''', (session_id, message, response))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("🏥 HealthAI Chatbot starting...")
    print("📱 Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
