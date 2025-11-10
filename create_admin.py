"""
Create Admin User Script for SwasthAI
Run this to create your first admin account
"""
from database import SessionLocal, User
from auth import get_password_hash

def create_admin():
    """Create an admin user"""
    db = SessionLocal()
    
    print("🔐 Create SwasthAI Admin Account")
    print("=" * 50)
    
    username = input("Enter admin username: ").strip()
    full_name = input("Enter full name: ").strip()
    password = input("Enter password: ").strip()
    
    # Check if user exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        print(f"\n❌ User '{username}' already exists!")
        
        # Ask if want to make them admin
        make_admin = input("Make this user an admin? (yes/no): ").strip().lower()
        if make_admin == 'yes':
            existing_user.is_admin = True
            db.commit()
            print(f"✅ User '{username}' is now an admin!")
        db.close()
        return
    
    # Create new admin user
    hashed_password = get_password_hash(password)
    admin_user = User(
        username=username,
        full_name=full_name,
        hashed_password=hashed_password,
        is_admin=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print(f"\n✅ Admin user created successfully!")
    print(f"   Username: {username}")
    print(f"   Admin: Yes")
    print(f"\n🔗 Access admin panel at: http://localhost:8000/admin")
    print(f"   (Login with your credentials first)")
    
    db.close()

if __name__ == "__main__":
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
