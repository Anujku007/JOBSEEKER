from app import create_app
from extensions import db
from models.simple_models import User

def test_login():
    app = create_app()
    
    with app.app_context():
        print("🚀 Starting login debug test...")
        
        # Delete any existing test user
        existing_user = User.query.filter_by(email="test@example.com").first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            print("🗑️  Deleted existing test user")
        
        # Create new test user
        test_user = User(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        test_user.set_password("password123")
        
        db.session.add(test_user)
        db.session.commit()
        print("👤 Created test user: test@example.com / password123")
        
        # Verify we can find and authenticate
        found_user = User.query.filter_by(email="test@example.com").first()
        if found_user:
            print(f"✅ User found: {found_user.email}")
            print(f"🔐 Testing password verification...")
            
            # Test correct password
            if found_user.check_password("password123"):
                print("✅ Correct password works!")
            else:
                print("❌ Correct password FAILED!")
            
            # Test wrong password
            if not found_user.check_password("wrongpassword"):
                print("✅ Wrong password correctly rejected!")
            else:
                print("❌ Wrong password was accepted!")
        else:
            print("❌ User not found after creation!")
        
        print("🎯 Debug test complete!")

if __name__ == "__main__":
    test_login()