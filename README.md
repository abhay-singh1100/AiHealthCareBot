# HealthAI - AI-Driven Healthcare Chatbot

## 🏥 Project Overview
A 24/7 AI-powered healthcare assistant that provides instant medical guidance and reduces communication gaps between patients and healthcare providers.

## ✨ Features
- **AI-Powered Chat**: Instant, intelligent responses to medical queries
- **Medical Knowledge Access**: Reliable information from healthcare sources
- **24/7 Availability**: Round-the-clock preliminary guidance
- **Personalized Interaction**: Adapts responses based on user input
- **Secure Communication**: Maintains data privacy and confidentiality

## 🛠️ Technology Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **AI Model**: Qwen (Generative AI)
- **Database**: SQLite for user data and chat history

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 8GB RAM minimum
- Stable internet connection

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure
```
HealthAI/
├── app.py                 # Main Flask application
├── models/
│   ├── qwen_model.py     # Qwen AI model integration
│   └── medical_db.py     # Medical knowledge database
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── chat.js       # Frontend JavaScript
├── templates/
│   └── index.html        # Main chat interface
├── data/
│   └── medical_knowledge.json  # Medical knowledge base
└── requirements.txt      # Python dependencies
```

## 🔒 Privacy & Security
- All conversations are encrypted
- No personal data is stored permanently
- HIPAA-compliant data handling
- Secure API endpoints

## ⚠️ Disclaimer
This application provides preliminary medical guidance only and should not replace professional medical consultation.
