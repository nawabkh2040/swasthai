# 🏥 SwasthAI Chat MVP

**AI-Powered Medical Assistant for Rural Healthcare**

SwasthAI Chat is an intelligent, accessible medical support system designed to help people in rural India get instant health guidance through a friendly AI chatbot powered by **LangChain + LangGraph**.

---
🌐 Live Demo: https://www.swasthai.live/chat
---
## 🎯 Project Overview

This MVP (Minimum Viable Product) is the first working version of the larger **SwasthAI Rural Healthcare System**. It demonstrates how AI technology can make healthcare more accessible, especially in areas with limited medical infrastructure.

### Key Features

✅ **User Authentication** - Secure signup and login system with JWT tokens  
✅ **AI Medical Assistant** - Powered by LangChain + LangGraph for intelligent, context-aware conversations  
✅ **Conversation Memory** - AI remembers context and previous messages  
✅ **Chat History** - All conversations are saved and can be revisited  
✅ **Multiple AI Providers** - Support for OpenAI (GPT-3.5) or Google Gemini  
✅ **Rural-Friendly Design** - Simple, clean interface designed for everyone  
✅ **Privacy & Security** - User data stored securely in local SQLite database  
✅ **24/7 Availability** - Get health guidance anytime, anywhere  

---

## 💻 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | High-performance Python web framework |
| **Frontend** | Jinja2 + HTML/CSS/JS | Server-side rendering with responsive design |
| **Database** | SQLite3 | Lightweight local database for users and messages |
| **AI Framework** | LangChain + LangGraph | Advanced AI reasoning and conversation management |
| **AI Models** | OpenAI GPT-3.5 / Google Gemini | Natural language processing |
| **Authentication** | JWT (JSON Web Tokens) | Secure user sessions |

---

## 📦 Installation & Setup

### Prerequisites

- **Python 3.13** (or 3.11+)
- **Virtual Environment** (recommended)
- **OpenAI API Key** or **Google Gemini API Key**

### Step 1: Clone the Repository

```bash
git clone https://github.com/nawabkh2040-cloud/swasthai.git
cd swasthai
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv SwasthAI

# Activate it (Windows)
SwasthAI\Scripts\activate

# Activate it (Linux/Mac)
source SwasthAI/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the `.env` file and edit it:

```bash
cp .env .env.local
```

2. Open `.env` and add your API key:

```env
# For OpenAI (Recommended)
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# OR for Google Gemini
# AI_PROVIDER=gemini
# GOOGLE_API_KEY=your-gemini-api-key-here

# Change this to a strong secret key
SECRET_KEY=your-super-secret-key-minimum-32-characters-long
```

**Get API Keys:**
- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Google Gemini**: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### Step 5: Run the Application

```bash
python main.py
```

The server will start at: **http://localhost:8000**

---

## 🚀 Usage Guide

### 1. **Access the Application**
   - Open your browser and go to `http://localhost:8000`

### 2. **Create an Account**
   - Click "Sign Up"
   - Enter your full name, username, and password
   - Click "Create Account"

### 3. **Start Chatting**
   - You'll be automatically logged in and redirected to the chat page
   - The AI assistant will greet you
   - Type your health-related questions
   - Get instant, helpful responses!

### 4. **Example Questions**
   - "I have a headache and mild fever since yesterday"
   - "What are the symptoms of dengue?"
   - "How can I prevent dehydration in summer?"
   - "My child has a persistent cough, what should I do?"

---

## 🧠 How LangChain + LangGraph Works

### Why LangChain?

**LangChain** allows the AI to:
- 🧩 **Chain thoughts** - Break down complex medical queries into steps
- 🔗 **Connect knowledge** - Use multiple sources of information
- 🎯 **Stay focused** - Maintain context throughout the conversation
- 🛠️ **Use tools** - Potentially integrate with medical databases (future)

### Why LangGraph?

**LangGraph** provides:
- 🗺️ **Conversation flow** - Manages the dialogue like a mind map
- 📊 **State management** - Tracks what has been discussed
- 🔄 **Context awareness** - Remembers previous messages
- 🎨 **Explainable AI** - Clear reasoning paths

Together, they create a **smart, reliable, and context-aware** medical assistant!

---

## 📁 Project Structure

```
swasthai/
├── main.py                 # FastAPI application entry point
├── ai_agent.py            # LangChain + LangGraph AI agent
├── auth.py                # JWT authentication logic
├── config.py              # Configuration settings
├── database.py            # SQLAlchemy database models
├── schemas.py             # Pydantic data models
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (IMPORTANT!)
├── swasthai.db           # SQLite database (auto-created)
│
├── templates/             # Jinja2 HTML templates
│   ├── index.html        # Landing page
│   ├── signup.html       # Signup page
│   ├── login.html        # Login page
│   └── chat.html         # Chat interface
│
└── static/                # Static assets
    ├── css/
    │   └── style.css     # Styling
    └── js/
        ├── chat.js       # Chat functionality
        ├── login.js      # Login logic
        └── signup.js     # Signup logic
```

---

## 🔒 Security Features

- ✅ **Password Hashing** - Using bcrypt for secure password storage
- ✅ **JWT Tokens** - Stateless authentication with expiration
- ✅ **SQL Injection Protection** - SQLAlchemy ORM prevents attacks
- ✅ **Input Validation** - Pydantic models validate all user inputs
- ✅ **Environment Variables** - Sensitive data not hardcoded

---

## 🌟 Future Enhancements

### Phase 2 Features
- 🎥 **Video Consultations** - Connect with verified doctors
- 🏥 **ABHA Integration** - Link with Ayushman Bharat Health ID
- 🗣️ **Voice Input** - Speak your symptoms instead of typing
- 🌐 **Multi-Language** - Hindi, English, and regional languages
- 📱 **WhatsApp Bot** - Chat via WhatsApp for wider reach

### Phase 3 Features
- 📋 **Health Records** - Store and manage digital health records
- 💊 **Prescription Generation** - AI-assisted prescriptions
- 📊 **Health Analytics** - Track health trends over time
- 🏪 **Medicine Delivery** - Integration with pharmacy services
- 📱 **Progressive Web App** - Offline-first mobile experience

---

## 🐛 Troubleshooting

### Issue: "OPENAI_API_KEY not set"
**Solution:** Make sure you've created a `.env` file and added your API key.

### Issue: "Cannot connect to database"
**Solution:** The database is created automatically. Check write permissions in the project folder.

### Issue: "Port 8000 already in use"
**Solution:** Change the port in `.env`:
```env
PORT=8001
```

### Issue: "Module not found"
**Solution:** Make sure your virtual environment is activated and dependencies are installed:
```bash
SwasthAI\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/signup` | Create new user account |
| `POST` | `/api/login` | Login and get JWT token |
| `GET` | `/api/user` | Get current user info |
| `POST` | `/api/chat` | Send message to AI assistant |
| `GET` | `/api/messages` | Get chat history |
| `DELETE` | `/api/messages` | Clear chat history |
| `GET` | `/api/greeting` | Get AI greeting message |

---

## 👥 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **LangChain** - For the amazing AI framework
- **FastAPI** - For the modern web framework
- **OpenAI / Google** - For powerful language models
- **Rural healthcare workers** - For inspiring this project

---

## 📞 Contact & Support

**Project Lead**: [@nawabkh2040-cloud](https://github.com/nawabkh2040-cloud)

**Issues**: [GitHub Issues](https://github.com/nawabkh2040-cloud/swasthai/issues)

---

## 💡 Vision

**To make healthcare accessible, intelligent, and empathetic — enabling every Indian village to get medical support through technology that listens, understands, and helps.**

---

Made with ❤️ for Rural India 🇮🇳
| **Database** | SQLite3 | Lightweight local database |
| **AI Engine** | LangChain + LangGraph | Advanced conversation flow and reasoning |
| **LLM Provider** | OpenAI GPT-3.5 / Google Gemini | Language model for medical guidance |
| **Authentication** | JWT (JSON Web Tokens) | Secure user authentication |
| **Styling** | Custom CSS | Clean, accessible, mobile-friendly UI |

---

## 🧠 How It Works

### The AI Agent Architecture

```
User Message
    ↓
[LangGraph State Machine]
    ↓
System Prompt (Medical Assistant Context)
    ↓
Conversation History (Last 10 messages)
    ↓
[LangChain + LLM (OpenAI/Gemini)]
    ↓
Context-Aware Medical Response
    ↓
Save to Database
    ↓
Display to User
```

### Why LangChain + LangGraph?

- **LangChain**: Provides powerful tools for building conversational AI with memory, reasoning, and tool integration
- **LangGraph**: Enables complex conversation flows with state management and decision-making capabilities
- **Result**: More intelligent, context-aware, and reliable medical guidance

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **OpenAI API Key** OR **Google Gemini API Key** (free alternative)

### Step 1: Clone the Repository

```powershell
cd c:\Users\arman\Downloads\swasth-ai\swasthai
```

### Step 2: Create Virtual Environment (Recommended)

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the example environment file:
```powershell
copy .env.example .env
```

2. Edit `.env` file and add your API key:

**Option A: Using OpenAI (Paid)**
```
OPENAI_API_KEY=sk-your-openai-api-key-here
AI_PROVIDER=openai
```

**Option B: Using Google Gemini (Free)**
```
GOOGLE_API_KEY=your-google-api-key-here
AI_PROVIDER=gemini
```

**Get Your API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Google Gemini: https://makersuite.google.com/app/apikey

### Step 5: Run the Application

```powershell
python main.py
```

or

```powershell
uvicorn main:app --reload
```

### Step 6: Open in Browser

Navigate to: **http://localhost:8000**

---

## 📱 Usage Guide

### 1. Create an Account
- Click "Get Started" on the home page
- Enter your full name, username, and password
- Click "Create Account"

### 2. Start Chatting
- You'll be automatically logged in and redirected to the chat page
- Type your health question in the message box
- The AI assistant will respond with helpful guidance

### 3. Example Questions
- "I have a headache and mild fever since yesterday"
- "My child has diarrhea, what should I do?"
- "I got a small cut while cooking, how to treat it?"
- "What are symptoms of dehydration?"

### 4. Features
- **Clear Chat**: Click the trash icon to clear your conversation history
- **Logout**: Click the door icon to logout
- **Auto-Save**: All messages are automatically saved

---

## 📁 Project Structure

```
swasthai/
├── main.py                 # Main FastAPI application
├── config.py              # Configuration settings
├── database.py            # Database models and setup
├── auth.py                # Authentication utilities (JWT)
├── schemas.py             # Pydantic models for validation
├── ai_agent.py            # LangChain + LangGraph AI agent
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore            # Git ignore file
├── README.md             # This file
│
├── templates/            # Jinja2 HTML templates
│   ├── index.html       # Home page
│   ├── signup.html      # Signup page
│   ├── login.html       # Login page
│   └── chat.html        # Chat interface
│
└── static/              # Static assets
    ├── css/
    │   └── style.css    # Main stylesheet
    └── js/
        ├── signup.js    # Signup page logic
        ├── login.js     # Login page logic
        └── chat.js      # Chat page logic
```

---

## 🔒 Security Features

- **Password Hashing**: Passwords are hashed using bcrypt before storage
- **JWT Authentication**: Secure token-based authentication
- **Session Management**: 24-hour session expiry
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Input Validation**: Pydantic models validate all user input

---

## 🎨 Design Philosophy

### Built for Rural Users

1. **Simple Language**: No complex medical jargon
2. **Clean Interface**: Minimal, distraction-free design
3. **Mobile-First**: Works perfectly on phones
4. **Low Bandwidth**: Lightweight pages, no heavy images
5. **Intuitive**: Anyone can use it without training

### Color Scheme

- **Primary Blue (#2563eb)**: Trust and healthcare
- **Green (#10b981)**: Health and wellness
- **White (#ffffff)**: Clean and professional
- **Gray Tones**: Easy on the eyes

---

## 🧪 Testing the AI Agent

You can test the AI agent independently:

```powershell
python ai_agent.py
```

This will:
- Initialize the agent
- Show a greeting message
- Process a test query
- Display the AI response

---

## 🐛 Troubleshooting

### Problem: "OpenAI API key not set"
**Solution**: Make sure you've created a `.env` file and added your API key

### Problem: "Module not found"
**Solution**: Activate virtual environment and run `pip install -r requirements.txt`

### Problem: Port 8000 already in use
**Solution**: Change the PORT in `.env` file or run with: `uvicorn main:app --port 8001`

### Problem: Database errors
**Solution**: Delete `swasthai.db` file and restart the application

### Problem: Can't access from other devices
**Solution**: Change HOST in `.env` to `0.0.0.0` and access via your IP address

---

## 🚀 Future Enhancements

This is just the MVP! Planned features for future versions:

### Phase 2
- [ ] Video/Audio consultations with real doctors
- [ ] Voice input and output (speech recognition)
- [ ] Multi-language support (Hindi, Bengali, Tamil, etc.)
- [ ] WhatsApp chatbot integration

### Phase 3
- [ ] Health record storage and management
- [ ] Integration with Ayushman Bharat Health ID (ABHA)
- [ ] PDF prescription generation
- [ ] Appointment booking system

### Phase 4
- [ ] Doctor dashboard for rural healthcare workers
- [ ] Analytics and health insights
- [ ] Offline support (Progressive Web App)
- [ ] Emergency service integration

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🤝 Contributing

This is an MVP project. Contributions are welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is created for educational and humanitarian purposes.

---

## 👥 Team

**SwasthAI Team** - Making healthcare accessible for every Indian village

---

## 🙏 Acknowledgments

- **LangChain**: For powerful AI conversation tools
- **FastAPI**: For the excellent web framework
- **OpenAI/Google**: For providing AI capabilities
- **Rural India**: The inspiration for this project

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Create an issue on GitHub

---

## 💡 Vision

**"To make healthcare accessible, intelligent, and empathetic — enabling every Indian village to get medical support through technology that listens, understands, and helps."**

---

**Built with ❤️ for Rural India** 🇮🇳
Chat with an AI medical assistant  Get symptom-based health guidance in Hindi/English  Store chat history in a local SQLite3 database
