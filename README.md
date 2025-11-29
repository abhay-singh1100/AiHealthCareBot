# HealthAI - AI-Driven Healthcare Chatbot

## 🏥 Project Overview
A 24/7 AI-powered healthcare assistant that provides instant medical guidance and reduces communication gaps between patients and healthcare providers.

## ✨ Key Features

### 🤖 **Intelligent AI Chat**
- **FREE AI Model**: Lightweight, open-source AI for any health question
- **Multi-turn Conversations**: Interactive Q&A about symptoms
- **Medication Suggestions**: Personalized recommendations with dosage info
- **No API Keys Required**: Completely free to use

### 🏥 **Medical Features**
- **Symptom Analysis**: Ask detailed questions to understand your symptoms
- **Follow-up Questions**: Intelligent Q&A system for accurate assessment
- **Medication Guidance**: Get medication suggestions with proper dosages
- **Health Information**: Comprehensive knowledge base

### 🔒 **Privacy & Security**
- All conversations are encrypted
- No personal data stored permanently
- HIPAA-compliant data handling
- Secure API endpoints

## 🛠️ Technology Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **AI Models**: 
  - Free AI Model (Mistral via Hugging Face - FREE)
  - Qwen Model (Optional - Local)
- **Database**: SQLite for chat history

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Internet connection (for AI features)
- 4GB RAM minimum (for basic usage)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd HealthAI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```
   Or use the startup script:
   ```bash
   ./start_healthai.sh  # Linux/Mac
   start_healthai.bat   # Windows
   ```

4. Open your browser and navigate to `http://localhost:5000`

## 🎯 How to Use

### Basic Usage
1. **Start a conversation**: Type any health question or symptom
2. **Answer questions**: The chatbot will ask follow-up questions
3. **Get suggestions**: Receive medication and self-care recommendations
4. **Medical disclaimer**: Always consult healthcare professionals

### Example Conversations

**User**: "I have a headache"  
**Bot**: Asks about duration, pain level, triggers, and previous treatments  
**Result**: Provides specific medication suggestions with dosages

**User**: "What should I eat when I have a cold?"  
**Bot**: AI-powered response about nutrition during illness

**User**: "How to reduce stress?"  
**Bot**: Comprehensive advice with coping strategies

## 📁 Project Structure
```
HealthAI/
├── app.py                        # Main Flask application
├── models/
│   ├── free_ai_model.py         # 🆕 Free AI model (Mistral)
│   ├── conversation_manager.py  # 🆕 Multi-turn conversation logic
│   ├── qwen_model.py            # Optional Qwen AI model
│   └── medical_db.py            # Medical knowledge database
├── static/
│   ├── css/
│   │   └── style.css            # Styling (with medication cards)
│   └── js/
│       └── chat.js              # Frontend JavaScript (enhanced)
├── templates/
│   └── index.html               # Main chat interface
├── data/
│   └── medical_knowledge.json   # Medical knowledge base
├── test_free_ai.py              # 🆕 Test script for AI
└── requirements.txt             # Python dependencies
```

## 🔥 New Features

### AI-Powered Chat
- **Free AI Model**: Uses Hugging Face Inference API (FREE)
- **No API Keys**: No registration or keys required
- **Smart Fallback**: Enhanced knowledge base when AI is slow
- **General Questions**: Answer ANY health question

### Interactive Symptom Analysis
- **Follow-up Questions**: 3-4 intelligent questions per symptom
- **Medication Cards**: Beautiful UI for medication suggestions
- **Dosage Information**: Proper dosing recommendations
- **Self-care Tips**: Additional recommendations

## 📚 Documentation
- `CHATBOT_IMPROVEMENTS.md` - New chatbot features
- `AI_MODEL_INTEGRATION.md` - AI model setup guide
- `PROJECT_SUMMARY.md` - Detailed project overview

## 🔒 Privacy & Security
- All conversations are encrypted
- No personal data is stored permanently
- HIPAA-compliant data handling
- Secure API endpoints

## ⚠️ Disclaimer
This application provides preliminary medical guidance only and should not replace professional medical consultation.
