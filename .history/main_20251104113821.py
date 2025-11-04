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
    return ErrorResponse(error=exc.detail, detail=str(exc.status_code))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
