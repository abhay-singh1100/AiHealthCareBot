# HealthAI Configuration File

# Application Settings
APP_NAME = "HealthAI"
APP_VERSION = "1.0.0"
DEBUG = True
HOST = "0.0.0.0"
PORT = 5000

# AI Model Settings
AI_MODEL_NAME = "Qwen/Qwen-7B-Chat"
AI_MODEL_DEVICE = "auto"  # auto, cpu, cuda
AI_MAX_LENGTH = 200
AI_TEMPERATURE = 0.7

# Database Settings
DATABASE_PATH = "healthai.db"
MEDICAL_KNOWLEDGE_PATH = "data/medical_knowledge.json"

# Security Settings
SECRET_KEY = "your-secret-key-change-this-in-production"
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# Privacy Settings
ENABLE_CONVERSATION_STORAGE = True
CONVERSATION_RETENTION_DAYS = 30
ENABLE_ANALYTICS = False

# Medical Disclaimer
MEDICAL_DISCLAIMER = "⚠️ **Important**: This is preliminary guidance only. Please consult a healthcare professional for proper medical advice, especially for serious symptoms."

# Emergency Keywords
EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "stroke", "difficulty breathing",
    "severe bleeding", "unconscious", "emergency", "911", "ambulance",
    "suicidal", "self harm", "overdose", "severe allergic reaction"
]

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE = 30
RATE_LIMIT_ENABLED = True

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "healthai.log"
ENABLE_REQUEST_LOGGING = True
