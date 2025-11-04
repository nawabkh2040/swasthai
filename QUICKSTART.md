# 🚀 Quick Start Guide - SwasthAI Chat MVP

Get up and running in 5 minutes!

---

## ⚡ Super Quick Setup (Windows PowerShell)

```powershell
# 1. Navigate to project directory
cd c:\Users\arman\Downloads\swasth-ai\swasthai

# 2. Run setup script
.\setup.ps1

# 3. Edit .env and add your API key
notepad .env

# 4. Start the application
.\run.ps1
```

---

## 📋 Manual Setup (Step by Step)

### 1️⃣ Install Dependencies

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2️⃣ Configure API Key

```powershell
# Copy example file
copy .env.example .env

# Edit and add your API key
# Choose either OpenAI OR Gemini
```

**For OpenAI:**
```env
OPENAI_API_KEY=sk-your-key-here
AI_PROVIDER=openai
```

**For Gemini (Free):**
```env
GOOGLE_API_KEY=your-key-here
AI_PROVIDER=gemini
```

### 3️⃣ Run Application

```powershell
python main.py
```

### 4️⃣ Open Browser

Navigate to: **http://localhost:8000**

---

## 🎯 First Time User Flow

1. **Click "Get Started"** → Sign up page
2. **Fill in details:**
   - Full Name: Your name
   - Username: Choose a unique username
   - Password: At least 6 characters
3. **Click "Create Account"** → Automatically logged in
4. **Start chatting** with the AI assistant!

---

## 💬 Example Conversations

### General Health Query
```
You: "I have a mild fever and body ache"

AI: "I understand you're not feeling well. A mild fever with 
body ache can have several causes:

1. Viral infection (most common)
2. Flu
3. Fatigue or overexertion

Recommendations:
- Rest well
- Drink plenty of water
- Take paracetamol if needed
- Monitor your temperature

If fever goes above 102°F or persists for more than 3 days, 
please consult a doctor."
```

### Emergency Situation
```
You: "Severe chest pain and difficulty breathing"

AI: "⚠️ URGENT: These symptoms require immediate medical 
attention!

Please:
1. Call emergency services (108 or 102) NOW
2. Don't drive yourself
3. Stay calm and sit upright
4. Loosen tight clothing

This could be serious - please seek help immediately."
```

---

## 🔑 Important Features

### Chat History
- All your conversations are saved
- Access them anytime you login
- Messages are stored securely

### Clear Chat
- Click the 🗑️ icon to clear history
- Warning: This cannot be undone

### Logout
- Click the 🚪 icon to logout safely
- Your data remains secure

---

## ⚙️ Configuration Options

### Change Port
Edit `.env`:
```env
PORT=8001
```

### Change Session Duration
Edit `.env`:
```env
ACCESS_TOKEN_EXPIRE_MINUTES=720  # 12 hours
```

### Switch AI Provider
Edit `.env`:
```env
AI_PROVIDER=gemini  # or openai
```

---

## 🐛 Common Issues

### Problem: Can't install requirements
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Then try again
pip install -r requirements.txt
```

### Problem: Import errors
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\activate

# Verify installation
pip list
```

### Problem: API key not working
```
# Check .env file exists
dir .env

# Verify key format (no quotes, no spaces)
# OpenAI: starts with "sk-"
# Gemini: 39 characters long
```

### Problem: Database locked
```powershell
# Delete database and restart
del swasthai.db
python main.py
```

---

## 📚 API Endpoints Reference

### Public Endpoints
- `GET /` - Home page
- `GET /signup` - Signup page
- `GET /login` - Login page
- `GET /health` - Health check

### Authentication
- `POST /api/signup` - Create account
- `POST /api/login` - Login

### Protected Endpoints (Requires Token)
- `GET /api/user` - Get user info
- `GET /api/messages` - Get chat history
- `POST /api/chat` - Send message
- `DELETE /api/messages` - Clear history
- `GET /api/greeting` - Get welcome message

---

## 🧪 Testing the AI

Test AI agent independently:

```powershell
python ai_agent.py
```

This will:
1. Initialize the agent
2. Show greeting message
3. Process a sample query
4. Display response

---

## 📱 Mobile Testing

### On Same Network
1. Find your computer's IP address:
```powershell
ipconfig
# Look for IPv4 Address (e.g., 192.168.1.5)
```

2. Update `.env`:
```env
HOST=0.0.0.0
```

3. Restart server

4. On mobile, open: `http://YOUR-IP:8000`

---

## 🎨 Customization

### Change App Name
Edit `config.py`:
```python
APP_NAME: str = "Your Custom Name"
```

### Modify AI Behavior
Edit `ai_agent.py` - Update `MEDICAL_ASSISTANT_PROMPT`

### Change Styling
Edit `static/css/style.css`

### Modify Templates
Edit files in `templates/` folder

---

## 📊 Usage Stats

Check your database:

```powershell
# Install SQLite browser
# or use Python

python
>>> from database import *
>>> init_db()
>>> from sqlalchemy.orm import Session
>>> db = SessionLocal()
>>> user_count = db.query(User).count()
>>> message_count = db.query(Message).count()
>>> print(f"Users: {user_count}, Messages: {message_count}")
```

---

## 🔄 Updates

### Pull Latest Changes
```powershell
git pull origin main
pip install -r requirements.txt --upgrade
```

### Reset Database
```powershell
del swasthai.db
python main.py  # Auto-creates new database
```

---

## 🆘 Getting Help

1. Check `README.md` for detailed documentation
2. Check `DEPLOYMENT.md` for deployment help
3. Review error messages in terminal
4. Test with `python ai_agent.py`

---

## 🎓 Learning Resources

### FastAPI
- Docs: https://fastapi.tiangolo.com
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### LangChain
- Docs: https://python.langchain.com
- Guide: https://python.langchain.com/docs/get_started

### LangGraph
- Docs: https://langchain-ai.github.io/langgraph/

---

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] API key added
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000
- [ ] Can create an account
- [ ] Can send messages to AI
- [ ] AI responds correctly

---

**Congratulations! You're ready to use SwasthAI Chat! 🎉**

Built with ❤️ for Rural India 🇮🇳
