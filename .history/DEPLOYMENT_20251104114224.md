# SwasthAI Chat MVP - Deployment Guide

This guide explains how to deploy SwasthAI Chat to popular cloud platforms.

---

## 🌐 Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Pros**: Easy setup, free tier, automatic deployments  
**Cons**: Cold starts on free tier

#### Steps:

1. Create a `render.yaml` file (see below)
2. Push code to GitHub
3. Connect GitHub repo to Render
4. Add environment variables in Render dashboard
5. Deploy!

**render.yaml**:
```yaml
services:
  - type: web
    name: swasthai-chat
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: OPENAI_API_KEY
        sync: false
      - key: AI_PROVIDER
        value: openai
```

---

### Option 2: Railway

**Pros**: Very simple, great free tier  
**Cons**: Limited free hours per month

#### Steps:

1. Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

2. Install Railway CLI:
```powershell
npm install -g @railway/cli
```

3. Login and deploy:
```powershell
railway login
railway init
railway up
```

---

### Option 3: Heroku

**Pros**: Reliable, well-documented  
**Cons**: No free tier anymore

#### Files Needed:

**Procfile**:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**runtime.txt**:
```
python-3.11.0
```

#### Steps:
```powershell
heroku login
heroku create swasthai-chat
git push heroku main
heroku config:set OPENAI_API_KEY=your-key-here
heroku open
```

---

### Option 4: Google Cloud Run

**Pros**: Serverless, scales to zero  
**Cons**: Requires Docker knowledge

#### Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### Deploy:
```powershell
gcloud builds submit --tag gcr.io/YOUR_PROJECT/swasthai
gcloud run deploy swasthai --image gcr.io/YOUR_PROJECT/swasthai --platform managed
```

---

### Option 5: DigitalOcean App Platform

**Pros**: Simple, good pricing  
**Cons**: Paid service

Create `.do/app.yaml`:
```yaml
name: swasthai-chat
services:
  - name: web
    github:
      repo: your-username/swasthai
      branch: main
    build_command: pip install -r requirements.txt
    run_command: uvicorn main:app --host 0.0.0.0 --port 8080
    envs:
      - key: OPENAI_API_KEY
        scope: RUN_TIME
        value: ${OPENAI_API_KEY}
```

---

## 🔒 Production Checklist

Before deploying to production:

### Security
- [ ] Change `SECRET_KEY` in .env to a strong random string
- [ ] Set `ALGORITHM` to HS256 (default is fine)
- [ ] Enable HTTPS on your hosting platform
- [ ] Set secure cookie settings (in `main.py`)
- [ ] Add CORS middleware if needed

### Database
- [ ] Consider upgrading to PostgreSQL for production
- [ ] Set up regular database backups
- [ ] Add database migration system (Alembic)

### Monitoring
- [ ] Add logging (Python logging module)
- [ ] Set up error tracking (Sentry)
- [ ] Monitor API usage and costs
- [ ] Add health check endpoint (already included at `/health`)

### Performance
- [ ] Enable database connection pooling
- [ ] Add caching for static assets
- [ ] Implement rate limiting
- [ ] Optimize database queries

### Configuration Changes

Update `main.py` for production:

```python
# Add CORS if needed
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update cookie settings for HTTPS
app.use(session({
    cookie: { 
        secure: True,  # Require HTTPS
        httpOnly: True,
        sameSite: 'lax'
    }
}))
```

---

## 📊 Upgrading to PostgreSQL

For production, replace SQLite with PostgreSQL:

1. Update `requirements.txt`:
```
psycopg2-binary==2.9.9
```

2. Update `config.py`:
```python
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/swasthai"
)
```

3. Most hosting platforms provide PostgreSQL databases automatically

---

## 💰 Cost Estimates

### Free Tier Options:
- **Render**: Free tier with limitations (cold starts)
- **Railway**: $5 free credit, then pay-as-you-go
- **Google Cloud Run**: Free tier (1M requests/month)

### AI API Costs:
- **OpenAI GPT-3.5**: ~$0.002 per conversation
- **Google Gemini**: Free tier available

### Estimated Monthly Cost (100 users, 10 chats/day):
- Hosting: $0-10
- AI API: $5-20
- Total: ~$5-30/month

---

## 🚀 Quick Deploy Commands

### Render
```powershell
# Push to GitHub
git add .
git commit -m "Initial deployment"
git push origin main

# Then connect repo in Render dashboard
```

### Railway
```powershell
railway login
railway init
railway up
railway open
```

### Docker (Any Platform)
```powershell
docker build -t swasthai .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key swasthai
```

---

## 📱 Post-Deployment

After deployment:

1. **Test thoroughly**: Create account, send messages, logout
2. **Monitor logs**: Check for errors
3. **Set up alerts**: Get notified of issues
4. **Update documentation**: Share the URL with users
5. **Collect feedback**: Improve based on user input

---

## 🆘 Troubleshooting Deployment Issues

### "Application Error" or "502 Bad Gateway"
- Check logs for Python errors
- Ensure all environment variables are set
- Verify PORT binding (use `$PORT` env variable)

### Database Connection Errors
- Ensure DATABASE_URL is correct
- Check firewall rules
- Verify database credentials

### AI API Errors
- Confirm API key is valid
- Check billing/quota limits
- Monitor API usage

### Slow Response Times
- Check if cold start is the issue
- Consider upgrading to paid tier
- Optimize database queries
- Enable caching

---

## 📞 Need Help?

- Review platform-specific documentation
- Check application logs
- Test locally first with same environment variables
- Ensure all dependencies are in requirements.txt

---

**Good luck with your deployment! 🚀**

Built with ❤️ for Rural India 🇮🇳
