// Chat Page JavaScript
const token = localStorage.getItem('token');

// Redirect to login if no token
if (!token) {
    window.location.href = '/login';
}

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const chatForm = document.getElementById('chatForm');
const sendBtn = document.getElementById('sendBtn');
const userInfo = document.getElementById('userInfo');
const logoutBtn = document.getElementById('logoutBtn');
const clearChatBtn = document.getElementById('clearChatBtn');

let isLoading = false;

// Initialize
async function init() {
    await loadUserInfo();
    await loadChatHistory();
}

// Load user information
async function loadUserInfo() {
    try {
        const response = await fetch('/api/user', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            userInfo.textContent = user.full_name;
        } else if (response.status === 401) {
            // Token invalid, redirect to login
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error loading user info:', error);
    }
}

// Load chat history
async function loadChatHistory() {
    try {
        const response = await fetch('/api/messages', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Clear loading message
            chatMessages.innerHTML = '';
            
            if (data.messages.length === 0) {
                // Show welcome message
                await showGreeting();
            } else {
                // Display messages
                data.messages.forEach(msg => {
                    appendMessage(msg.content, msg.role, msg.created_at);
                });
            }
            
            scrollToBottom();
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
        chatMessages.innerHTML = '<p style="text-align:center; color: var(--danger-color);">Failed to load messages</p>';
    }
}

// Show greeting message
async function showGreeting() {
    try {
        const response = await fetch('/api/greeting', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            appendMessage(data.greeting, 'assistant');
        }
    } catch (error) {
        appendMessage('Hello! I am SwasthAI, your medical assistant. How can I help you today?', 'assistant');
    }
}

// Append message to chat
function appendMessage(content, role, timestamp = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;
    
    if (timestamp) {
        const time = document.createElement('div');
        time.className = 'message-time';
        time.textContent = formatTime(timestamp);
        bubble.appendChild(time);
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
}

// Format timestamp
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Show typing indicator
function showTypingIndicator() {
    const template = document.getElementById('typingTemplate');
    const indicator = template.content.cloneNode(true);
    indicator.firstElementChild.id = 'typingIndicator';
    chatMessages.appendChild(indicator);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Scroll to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send message
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isLoading) return;
    
    // Disable input
    isLoading = true;
    sendBtn.disabled = true;
    messageInput.disabled = true;
    
    // Append user message
    appendMessage(message, 'user');
    messageInput.value = '';
    autoResize();
    scrollToBottom();
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        removeTypingIndicator();
        
        if (response.ok) {
            const data = await response.json();
            appendMessage(data.response, 'assistant');
        } else {
            const error = await response.json();
            appendMessage(`Sorry, I encountered an error: ${error.detail}`, 'assistant');
        }
    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        appendMessage('Sorry, I could not process your message. Please try again.', 'assistant');
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
        scrollToBottom();
    }
});

// Auto-resize textarea
messageInput.addEventListener('input', autoResize);

function autoResize() {
    messageInput.style.height = 'auto';
    messageInput.style.height = messageInput.scrollHeight + 'px';
    
    // Enable/disable send button
    sendBtn.disabled = !messageInput.value.trim();
}

// Logout
logoutBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('token');
        window.location.href = '/login';
    }
});

// Clear chat history
clearChatBtn.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to clear all your chat history? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/messages', {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            chatMessages.innerHTML = '';
            await showGreeting();
            scrollToBottom();
        }
    } catch (error) {
        console.error('Error clearing chat:', error);
        alert('Failed to clear chat history');
    }
});

// Initialize on load
init();
