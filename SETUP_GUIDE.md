# 🚀 Quick Setup Guide - SwasthAI Chat MVP

## ⚠️ Current Issue

Your Gemini API key is not working with the available models. You have two options:

## Option 1: Use OpenAI (Recommended)

OpenAI is more stable and widely supported.

### Steps:

1. **Get OpenAI API Key**:
   - Go to: https://platform.openai.com/api-keys
   - Sign up or log in
   - Click "Create new secret key"
   - Copy the key (starts with `sk-...`)

2. **Update `.env` file**:
   ```env
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. **Restart the server**:
   ```powershell
   # Press Ctrl+C to stop the current server
   # Then run:
   C:/Users/arman/Downloads/swasth-ai/swasthai/SwasthAI/Scripts/python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Option 2: Fix Gemini API Key

Your current Gemini key might be:
- Invalid or expired
- Not have access to newer models
- Have billing issues

### Steps:

1. **Get a NEW Gemini API Key**:
   - Go to: https://aistudio.google.com/app/apikey
   - Create a new API key
   - Copy it

2. **Update `.env` file**:
   ```env
   AI_PROVIDER=gemini
   GOOGLE_API_KEY=YOUR-NEW-KEY-HERE
   ```

3. **Restart the server**

## 🎯 Which One to Choose?

| Feature | OpenAI (GPT-3.5) | Google Gemini |
|---------|------------------|---------------|
| Reliability | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good |
| Setup | Easy | Medium |
| Cost | $0.50 / 1M tokens | Free (with limits) |
| Response Quality | Excellent | Excellent |
| **Recommendation** | ✅ **Best for production** | Good for testing |

## 💡 Quick Test

Once configured, try these test questions in the chat:

1. "I have a headache and mild fever"
2. "What are symptoms of dengue?"
3. "How to prevent dehydration?"

## 📞 Need Help?

If you continue to face issues:
1. Check that your API key is correctly copied (no extra spaces)
2. Ensure you have credits/billing enabled
3. Try creating a completely new API key

---

**Current Status**: Server is running, but AI model needs proper API key configuration.
