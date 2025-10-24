from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import sqlite3
import os
from datetime import datetime
from models.qwen_model import QwenMedicalAssistant
from models.medical_db import MedicalKnowledgeBase

app = Flask(__name__)
CORS(app)

# Initialize AI model and medical knowledge base
ai_assistant = QwenMedicalAssistant()
medical_db = MedicalKnowledgeBase()

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
        
        # Get AI response
        ai_response = ai_assistant.get_response(user_message)
        
        # Store conversation in database
        store_conversation(session_id, user_message, ai_response)
        
        return jsonify({
            'response': ai_response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
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
