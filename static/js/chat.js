// HealthAI Chat Interface JavaScript

class HealthAIChat {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.isLoading = false;
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        
        this.initializeEventListeners();
        this.setWelcomeTime();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    initializeEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key press
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Input change for enabling/disabling send button
        this.messageInput.addEventListener('input', () => {
            this.updateSendButton();
            this.autoResizeTextarea();
        });
        
        // Quick action buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const symptom = e.currentTarget.dataset.symptom;
                this.sendQuickMessage(symptom);
            });
        });
        
        // Clear chat button
        document.getElementById('clearChat').addEventListener('click', () => {
            this.clearChat();
        });
    }

    setWelcomeTime() {
        const welcomeTimeElement = document.getElementById('welcomeTime');
        if (welcomeTimeElement) {
            welcomeTimeElement.textContent = this.formatTime(new Date());
        }
    }

    updateSendButton() {
        const hasText = this.messageInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText || this.isLoading;
    }

    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.updateSendButton();
        this.autoResizeTextarea();
        
        // Show loading
        this.showLoading();
        
        try {
            // Send to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Add bot response to chat
            this.addMessage(data.response, 'bot');
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('I apologize, but I encountered an error. Please try again or contact support if the problem persists.', 'bot');
        } finally {
            this.hideLoading();
        }
    }

    sendQuickMessage(symptom) {
        const quickMessages = {
            'headache': 'I have a headache. Can you help me understand what might be causing it?',
            'fever': 'I have a fever. What should I do?',
            'cough': 'I have a persistent cough. What could be the cause?',
            'pain': 'I\'m experiencing pain. Can you provide some guidance?'
        };
        
        const message = quickMessages[symptom];
        if (message) {
            this.messageInput.value = message;
            this.updateSendButton();
            this.sendMessage();
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.innerHTML = this.formatMessage(text);
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.formatTime(new Date());
        
        content.appendChild(messageText);
        content.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatMessage(text) {
        // Convert line breaks to <br>
        text = text.replace(/\n/g, '<br>');
        
        // Format bold text
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Format italic text
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Format warning messages
        text = text.replace(/⚠️/g, '<span style="color: #e74c3c;">⚠️</span>');
        
        // Format emergency keywords
        const emergencyKeywords = ['emergency', '911', 'urgent', 'immediately'];
        emergencyKeywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
            text = text.replace(regex, `<span style="color: #e74c3c; font-weight: bold;">${keyword}</span>`);
        });
        
        return text;
    }

    formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showLoading() {
        this.isLoading = true;
        this.loadingOverlay.classList.add('show');
        this.updateSendButton();
    }

    hideLoading() {
        this.isLoading = false;
        this.loadingOverlay.classList.remove('show');
        this.updateSendButton();
    }

    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            // Keep only the welcome message
            const messages = this.chatMessages.querySelectorAll('.message');
            messages.forEach((message, index) => {
                if (index > 0) { // Keep the first message (welcome)
                    message.remove();
                }
            });
            
            // Generate new session ID
            this.sessionId = this.generateSessionId();
            
            // Show confirmation
            this.addMessage('Chat history cleared. How can I help you today?', 'bot');
        }
    }

    // Utility method to check for emergency keywords
    checkForEmergency(message) {
        const emergencyKeywords = [
            'chest pain', 'heart attack', 'stroke', 'difficulty breathing',
            'severe bleeding', 'unconscious', 'emergency', '911', 'ambulance'
        ];
        
        const messageLower = message.toLowerCase();
        return emergencyKeywords.some(keyword => messageLower.includes(keyword));
    }

    // Method to highlight emergency messages
    highlightEmergency(messageElement) {
        messageElement.style.border = '2px solid #e74c3c';
        messageElement.style.animation = 'glow 1s infinite alternate';
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new HealthAIChat();
});

// Add some helpful utility functions
window.HealthAIUtils = {
    // Format medical terms
    formatMedicalTerm: function(term) {
        return term.charAt(0).toUpperCase() + term.slice(1).toLowerCase();
    },
    
    // Validate medical input
    validateInput: function(input) {
        if (!input || input.trim().length === 0) {
            return { valid: false, message: 'Please enter a message.' };
        }
        
        if (input.length > 1000) {
            return { valid: false, message: 'Message is too long. Please keep it under 1000 characters.' };
        }
        
        return { valid: true };
    },
    
    // Get current timestamp
    getTimestamp: function() {
        return new Date().toISOString();
    }
};
