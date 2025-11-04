require('dotenv').config();
const express = require('express');
const session = require('express-session');
const path = require('path');
const Database = require('better-sqlite3');
const bcrypt = require('bcryptjs');
const OpenAI = require('openai');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize Database
const db = new Database('swasthai.db');

// Create tables if they don't exist
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
  );

  CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
  CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
`);

// Initialize OpenAI
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
  secret: process.env.SESSION_SECRET || 'swasthai-secret-key-change-in-production',
  resave: false,
  saveUninitialized: false,
  cookie: { 
    secure: false, // Set to true in production with HTTPS
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  }
}));

// Authentication middleware
const requireAuth = (req, res, next) => {
  if (req.session && req.session.userId) {
    next();
  } else {
    res.status(401).json({ error: 'Authentication required' });
  }
};

// Routes

// Serve pages
app.get('/', (req, res) => {
  if (req.session.userId) {
    res.sendFile(path.join(__dirname, 'public', 'chat.html'));
  } else {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
  }
});

app.get('/signup', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'signup.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/chat', (req, res) => {
  if (req.session.userId) {
    res.sendFile(path.join(__dirname, 'public', 'chat.html'));
  } else {
    res.redirect('/login');
  }
});

// API Routes

// Signup
app.post('/api/signup', async (req, res) => {
  try {
    const { username, password, fullName } = req.body;

    if (!username || !password || !fullName) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    if (password.length < 6) {
      return res.status(400).json({ error: 'Password must be at least 6 characters' });
    }

    // Check if user exists
    const existingUser = db.prepare('SELECT id FROM users WHERE username = ?').get(username);
    if (existingUser) {
      return res.status(400).json({ error: 'Username already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insert user
    const result = db.prepare(
      'INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)'
    ).run(username, hashedPassword, fullName);

    req.session.userId = result.lastInsertRowid;
    req.session.username = username;
    req.session.fullName = fullName;

    res.json({ success: true, message: 'Account created successfully' });
  } catch (error) {
    console.error('Signup error:', error);
    res.status(500).json({ error: 'Server error during signup' });
  }
});

// Login
app.post('/api/login', async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    // Get user
    const user = db.prepare('SELECT * FROM users WHERE username = ?').get(username);
    if (!user) {
      return res.status(401).json({ error: 'Invalid username or password' });
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid username or password' });
    }

    req.session.userId = user.id;
    req.session.username = user.username;
    req.session.fullName = user.full_name;

    res.json({ success: true, message: 'Login successful' });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Server error during login' });
  }
});

// Logout
app.post('/api/logout', (req, res) => {
  req.session.destroy();
  res.json({ success: true });
});

// Get current user
app.get('/api/user', requireAuth, (req, res) => {
  res.json({
    id: req.session.userId,
    username: req.session.username,
    fullName: req.session.fullName
  });
});

// Get chat history
app.get('/api/messages', requireAuth, (req, res) => {
  try {
    const messages = db.prepare(
      'SELECT role, content, created_at FROM messages WHERE user_id = ? ORDER BY created_at ASC'
    ).all(req.session.userId);

    res.json({ messages });
  } catch (error) {
    console.error('Error fetching messages:', error);
    res.status(500).json({ error: 'Failed to fetch messages' });
  }
});

// Send message and get AI response
app.post('/api/chat', requireAuth, async (req, res) => {
  try {
    const { message } = req.body;
    const userId = req.session.userId;

    if (!message || message.trim().length === 0) {
      return res.status(400).json({ error: 'Message cannot be empty' });
    }

    // Save user message
    db.prepare(
      'INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)'
    ).run(userId, 'user', message);

    // Get recent conversation history (last 10 messages)
    const recentMessages = db.prepare(
      'SELECT role, content FROM messages WHERE user_id = ? ORDER BY created_at DESC LIMIT 10'
    ).all(userId).reverse();

    // Prepare messages for OpenAI
    const conversationHistory = [
      {
        role: 'system',
        content: `You are SwasthAI, a friendly and helpful medical assistant chatbot designed to help people, especially in rural areas, with health-related questions and concerns. 

Your responsibilities:
- Provide accurate, easy-to-understand health information
- Be empathetic and supportive
- Use simple language that anyone can understand
- For serious symptoms or emergencies, always advise consulting a doctor
- Never provide definitive diagnoses, but offer general guidance
- Be culturally sensitive and respectful
- Explain medical terms when you use them

Important guidelines:
- Always start by asking about symptoms or concerns if the user hasn't specified
- Provide practical advice when appropriate
- Recommend seeking professional medical help for serious issues
- Be encouraging and positive
- Keep responses concise but informative

Remember: You are not replacing doctors, but helping people understand their health better and know when to seek professional help.`
      },
      ...recentMessages
    ];

    // Get AI response
    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: conversationHistory,
      max_tokens: 500,
      temperature: 0.7,
    });

    const aiResponse = completion.choices[0].message.content;

    // Save AI response
    db.prepare(
      'INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)'
    ).run(userId, 'assistant', aiResponse);

    res.json({ 
      success: true, 
      response: aiResponse 
    });
  } catch (error) {
    console.error('Chat error:', error);
    
    // Provide helpful error message
    let errorMessage = 'Failed to get response';
    if (error.status === 401) {
      errorMessage = 'OpenAI API key is invalid. Please check your .env file.';
    } else if (error.code === 'ENOTFOUND') {
      errorMessage = 'Network error. Please check your internet connection.';
    }
    
    res.status(500).json({ error: errorMessage });
  }
});

// Clear chat history
app.delete('/api/messages', requireAuth, (req, res) => {
  try {
    db.prepare('DELETE FROM messages WHERE user_id = ?').run(req.session.userId);
    res.json({ success: true, message: 'Chat history cleared' });
  } catch (error) {
    console.error('Error clearing messages:', error);
    res.status(500).json({ error: 'Failed to clear chat history' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`🏥 SwasthAI Chat MVP is running on http://localhost:${PORT}`);
  console.log(`📊 Database: swasthai.db`);
  console.log(`🤖 AI Assistant: ${process.env.OPENAI_API_KEY ? 'Configured' : 'NOT CONFIGURED - Please add OPENAI_API_KEY to .env'}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  db.close();
  process.exit(0);
});
