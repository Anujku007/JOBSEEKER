from app import create_app
from extensions import db
from models.simple_models import User

def test_user_methods():
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing User model methods...")
        
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
        
        # Test set_password method
        print("🔐 Testing set_password method...")
        test_user.set_password("password123")
        
        db.session.add(test_user)
        db.session.commit()
        print("✅ User created with password")
        
        # Test check_password method
        print("🔐 Testing check_password method...")
        found_user = User.query.filter_by(email="test@example.com").first()
        
        if found_user.check_password("password123"):
            print("✅ Correct password works!")
        else:
            print("❌ Correct password failed!")
        
        if not found_user.check_password("wrongpassword"):
            print("✅ Wrong password correctly rejected!")
        else:
            print("❌ Wrong password was accepted!")
        
        print("🎯 User model methods test complete!")

if __name__ == "__main__":
    test_user_methods()