from app import create_app
from extensions import db
from models.simple_models import User

app = create_app()

with app.app_context():
    # Check if tables exist
    print("📋 Checking database state...")
    
    # Try to create a user directly
    try:
        user = User(
            username="test",
            email="test@test.com", 
            first_name="Test",
            last_name="User"
        )
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        print("✅ User created successfully!")
        
        # Verify we can query it
        found_user = User.query.filter_by(email="test@test.com").first()
        print(f"✅ User found: {found_user.first_name} {found_user.last_name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")