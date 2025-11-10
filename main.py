"""
SwasthAI Chat MVP - Main Application
FastAPI backend with LangChain/LangGraph AI agent
"""
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
import os

# Local imports
from config import settings
from database import get_db, init_db, User, Message
from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_admin,
    get_password_hash
)
from schemas import (
    UserSignup,
    UserLogin,
    Token,
    UserResponse,
    ChatMessage,
    ChatResponse,
    ChatHistoryResponse,
    MessageResponse,
    SuccessResponse,
    ErrorResponse
)
from ai_agent import get_agent

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered medical assistant for rural healthcare",
    version="1.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")

# Create templates and static directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)

try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    pass  # Static directory might be empty initially


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and AI agent on startup"""
    init_db()
    print(f"🚀 {settings.APP_NAME} is starting...")
    print(f"📊 Database: {settings.DATABASE_URL}")
    print(f"🤖 AI Provider: {settings.AI_PROVIDER.upper()}")
    
    try:
        # Test AI agent initialization
        agent = get_agent()
        print("✅ AI Agent initialized successfully")
    except Exception as e:
        print(f"⚠️  Warning: AI Agent initialization failed: {e}")
        print("   Please check your API keys in .env file")


# ==================== FRONTEND ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - redirect to chat or login"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Signup page"""
    return templates.TemplateResponse("signup.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Chat page (requires authentication via JS)"""
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/robots.txt")
async def robots():
    """Serve robots.txt for search engines"""
    from fastapi.responses import FileResponse
    return FileResponse("static/robots.txt", media_type="text/plain")


@app.get("/sitemap.xml")
async def sitemap():
    """Serve sitemap.xml for search engines"""
    from fastapi.responses import FileResponse
    return FileResponse("static/sitemap.xml", media_type="application/xml")


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About Us page"""
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact Us page"""
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/careers", response_class=HTMLResponse)
async def careers_page(request: Request):
    """Careers page"""
    return templates.TemplateResponse("careers.html", {"request": request})


@app.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    """Privacy Policy page"""
    return templates.TemplateResponse("privacy.html", {"request": request})


@app.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    """Terms of Service page"""
    return templates.TemplateResponse("terms.html", {"request": request})


@app.get("/disclaimer", response_class=HTMLResponse)
async def disclaimer_page(request: Request):
    """Medical Disclaimer page"""
    return templates.TemplateResponse("disclaimer.html", {"request": request})


@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request):
    """Help Center page"""
    return templates.TemplateResponse("help.html", {"request": request})


@app.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    """FAQs page"""
    return templates.TemplateResponse("faq.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    """Admin Dashboard page (requires admin authentication via JS)"""
    return templates.TemplateResponse("admin.html", {"request": request})


# ==================== API ROUTES ====================

@app.post("/api/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    Create a new user account
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    """
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/user", response_model=UserResponse)
async def get_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user


@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the AI assistant and get a response
    """
    try:
        # Get conversation history (last 10 messages)
        recent_messages = db.query(Message).filter(
            Message.user_id == current_user.id
        ).order_by(Message.created_at.desc()).limit(10).all()
        
        # Reverse to chronological order
        recent_messages.reverse()
        
        # Convert to format expected by AI agent
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in recent_messages
        ]
        
        # Get AI response
        agent = get_agent()
        ai_response = agent.chat(chat_message.message, conversation_history)
        
        # Save user message
        user_message = Message(
            user_id=current_user.id,
            role="user",
            content=chat_message.message
        )
        db.add(user_message)
        
        # Save AI response
        assistant_message = Message(
            user_id=current_user.id,
            role="assistant",
            content=ai_response
        )
        db.add(assistant_message)
        
        db.commit()
        
        return ChatResponse(response=ai_response)
    
    except ValueError as e:
        # API key not configured
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service not configured: {str(e)}"
        )
    except Exception as e:
        # Other errors
        print(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat message"
        )


@app.get("/api/messages", response_model=ChatHistoryResponse)
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get chat history for current user
    """
    messages = db.query(Message).filter(
        Message.user_id == current_user.id
    ).order_by(Message.created_at.asc()).all()
    
    return ChatHistoryResponse(
        messages=messages,
        total_messages=len(messages)
    )


@app.delete("/api/messages", response_model=SuccessResponse)
async def clear_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Clear all chat history for current user
    """
    db.query(Message).filter(Message.user_id == current_user.id).delete()
    db.commit()
    
    return SuccessResponse(message="Chat history cleared successfully")


@app.get("/api/greeting")
async def get_greeting(current_user: User = Depends(get_current_user)):
    """
    Get a personalized greeting from the AI assistant
    """
    agent = get_agent()
    greeting = agent.get_greeting()
    return {"greeting": greeting}


# ==================== ADMIN API ROUTES ====================

@app.get("/api/admin/users")
async def get_all_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all users (Admin only)
    """
    users = db.query(User).order_by(User.created_at.desc()).all()
    
    users_data = []
    for user in users:
        message_count = db.query(Message).filter(Message.user_id == user.id).count()
        users_data.append({
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat(),
            "total_messages": message_count
        })
    
    return {
        "users": users_data,
        "total_users": len(users_data)
    }


@app.get("/api/admin/users/{user_id}/messages")
async def get_user_messages(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all messages for a specific user (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    messages = db.query(Message).filter(
        Message.user_id == user_id
    ).order_by(Message.created_at.asc()).all()
    
    messages_data = [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat()
        }
        for msg in messages
    ]
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name
        },
        "messages": messages_data,
        "total_messages": len(messages_data)
    }


@app.get("/api/admin/stats")
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get platform statistics (Admin only)
    """
    total_users = db.query(User).count()
    total_messages = db.query(Message).count()
    total_admins = db.query(User).filter(User.is_admin == True).count()
    
    # Get recent users (last 7 days)
    from datetime import datetime, timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    new_users_week = db.query(User).filter(User.created_at >= seven_days_ago).count()
    
    return {
        "total_users": total_users,
        "total_messages": total_messages,
        "total_admins": total_admins,
        "new_users_this_week": new_users_week,
        "avg_messages_per_user": round(total_messages / total_users, 2) if total_users > 0 else 0
    }


@app.delete("/api/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Delete a user (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deleting yourself
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user.username} deleted successfully"}


# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "ai_provider": settings.AI_PROVIDER
    }


# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "detail": str(exc.status_code)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
