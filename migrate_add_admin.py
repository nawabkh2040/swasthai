"""
Migration script to add is_admin column to users table
Run this script once to update your existing database
"""

import sqlite3
import os

# Database path
DB_PATH = "swasthai.db"

def migrate_database():
    """Add is_admin column to users table"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database file '{DB_PATH}' not found!")
        print("Please make sure you're running this script from the correct directory.")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_admin' in columns:
            print("✅ Column 'is_admin' already exists in users table!")
            conn.close()
            return True
        
        # Add is_admin column with default value False
        print("📝 Adding 'is_admin' column to users table...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0
        """)
        
        conn.commit()
        print("✅ Successfully added 'is_admin' column!")
        
        # Show current table structure
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        print("\n📋 Current users table structure:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SwasthAI Database Migration - Add Admin Column")
    print("=" * 60)
    print()
    
    success = migrate_database()
    
    print()
    if success:
        print("✅ Migration completed successfully!")
        print()
        print("Next steps:")
        print("1. Run 'python create_admin.py' to create an admin user")
        print("2. Restart your FastAPI server")
        print("3. Login with admin credentials and access /admin")
    else:
        print("❌ Migration failed! Please check the errors above.")
    
    print("=" * 60)
