# HealthAI - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 8GB RAM minimum (16GB recommended for AI model)
- 10GB free disk space
- Stable internet connection

### Installation Steps

#### Option 1: Automated Setup (Recommended)
**Windows:**
```bash
# Double-click start_healthai.bat
# OR run in Command Prompt:
start_healthai.bat
```

**Linux/Mac:**
```bash
# Make executable and run:
chmod +x start_healthai.sh
./start_healthai.sh
```

#### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python app.py

# 3. Open browser to http://localhost:5000
```

### Testing the Installation
```bash
# Run the test suite
python test_healthai.py
```

## 🔧 Configuration

### AI Model Settings
The application will automatically:
- Try to load the Qwen AI model
- Fall back to rule-based responses if the model fails to load
- Use CPU or GPU based on availability

### Medical Knowledge Base
- Located in `data/medical_knowledge.json`
- Contains symptoms, conditions, and emergency information
- Can be customized by editing the JSON file

### Database
- SQLite database: `healthai.db`
- Stores chat sessions and messages
- Automatically created on first run

## 🌐 Accessing the Application

1. **Start the server** using one of the methods above
2. **Open your web browser**
3. **Navigate to:** `http://localhost:5000`
4. **Start chatting** with the AI healthcare assistant!

## 📱 Features Available

### ✅ Working Features
- **AI-Powered Chat**: Intelligent responses to medical queries
- **Medical Knowledge Access**: Comprehensive symptom and condition database
- **24/7 Availability**: Always accessible
- **Responsive Design**: Works on desktop and mobile
- **Quick Actions**: Pre-defined symptom buttons
- **Emergency Detection**: Highlights urgent medical situations
- **Privacy Protection**: Secure conversation handling

### 🔄 Fallback Mode
If the Qwen AI model fails to load:
- Application uses rule-based responses
- Still provides helpful medical guidance
- All other features remain functional

## 🛠️ Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
pip install -r requirements.txt
```

**2. "Port already in use"**
- Change port in `app.py` (line with `app.run()`)
- Or kill the process using port 5000

**3. "AI model loading failed"**
- This is normal if you don't have enough RAM
- Application will use fallback responses
- Still fully functional

**4. "Database errors"**
- Delete `healthai.db` file
- Restart the application
- Database will be recreated

### Performance Optimization

**For Better AI Performance:**
- Install CUDA for GPU acceleration
- Increase RAM to 16GB+
- Use SSD storage

**For Basic Usage:**
- Current setup works fine
- Fallback responses are comprehensive
- No additional configuration needed

## 🔒 Security & Privacy

### Data Protection
- Conversations stored locally in SQLite
- No data sent to external servers
- Configurable retention periods
- HIPAA-compliant design

### Security Features
- Input validation and sanitization
- Rate limiting protection
- Secure session management
- Emergency keyword detection

## 📊 Monitoring & Logs

### Application Logs
- Logs saved to `healthai.log`
- Configurable log levels
- Request tracking available

### Health Monitoring
- Built-in health check endpoint
- Performance metrics
- Error tracking

## 🚀 Production Deployment

### For Production Use:
1. **Update `config.py`**:
   - Set `DEBUG = False`
   - Change `SECRET_KEY`
   - Configure proper logging

2. **Use Production WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up Reverse Proxy** (nginx/Apache)

4. **Configure SSL/HTTPS**

5. **Set up Monitoring**

## 📞 Support

### Getting Help
- Check the test suite: `python test_healthai.py`
- Review logs in `healthai.log`
- Check the README.md for detailed information

### Reporting Issues
- Include error messages
- Provide system specifications
- Include log files if available

## ⚠️ Important Disclaimers

### Medical Disclaimer
- This application provides preliminary guidance only
- Not a replacement for professional medical advice
- Always consult healthcare professionals for serious concerns
- Call 911 for emergencies

### Technical Disclaimer
- Use at your own risk
- Test thoroughly before production deployment
- Keep backups of important data
- Regular security updates recommended

---

**🎉 Congratulations! Your HealthAI application is ready to use!**

For questions or support, refer to the documentation or run the test suite for diagnostics.
