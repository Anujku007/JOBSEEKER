import os
import sqlite3
from app import create_app
from extensions import db

def force_reset():
    app = create_app()
    
    with app.app_context():
        print("🚀 Starting forced database reset...")
        
        # Get database path from config
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"📁 Database URI: {db_uri}")
        
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            print(f"📍 Database path: {db_path}")
            
            # Force delete database file
            if os.path.exists(db_path):
                os.remove(db_path)
                print(f"🗑️  Deleted: {db_path}")
            else:
                print(f"ℹ️  Database file not found at: {db_path}")
        
        # Recreate all tables
        print("🔄 Creating new tables...")
        db.drop_all()
        db.create_all()
        
        # Verify the User table has correct columns
        print("🔍 Verifying table structure...")
        if db_uri.startswith('sqlite:///'):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check User table columns
            cursor.execute("PRAGMA table_info(user)")
            columns = cursor.fetchall()
            print("📊 User table columns:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")
            
            conn.close()
        
        print("✅ Force reset complete!")
        print("🎯 Now try: python app.py")

if __name__ == "__main__":
    force_reset()