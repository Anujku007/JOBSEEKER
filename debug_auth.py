from app import create_app
from extensions import db
from models.simple_models import User

def debug_auth():
    app = create_app()
    
    with app.app_context():
        print("🔍 AUTHENTICATION DEBUG REPORT")
        print("=" * 50)
        
        # Check database connection
        try:
            db.session.execute('SELECT 1')
            print("✅ Database connection: OK")
        except Exception as e:
            print(f"❌ Database connection: FAILED - {e}")
            return
        
        # Check tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Database tables: {tables}")
        
        # Check users
        users = User.query.all()
        print(f"👥 Total users: {len(users)}")
        
        for user in users:
            print(f"   - {user.email} (ID: {user.id})")
            print(f"     Username: {user.username}")
            print(f"     Name: {user.first_name} {user.last_name}")
            print(f"     Has password: {bool(user.password_hash)}")
            
            # Test password checking
            if user.password_hash:
                test_passwords = ['password123', 'wrongpassword']
                for pwd in test_passwords:
                    result = user.check_password(pwd)
                    print(f"     Password '{pwd}': {'✅ CORRECT' if result else '❌ WRONG'}")
        
        # Check if we can create a test user
        print("\n🧪 Testing user creation...")
        try:
            test_user = User(
                username="debuguser",
                email="debug@example.com", 
                first_name="Debug",
                last_name="User"
            )
            test_user.set_password("debug123")
            
            db.session.add(test_user)
            db.session.commit()
            print("✅ User creation: SUCCESS")
            
            # Verify the new user
            new_user = User.query.filter_by(email="debug@example.com").first()
            if new_user and new_user.check_password("debug123"):
                print("✅ Password verification: SUCCESS")
            else:
                print("❌ Password verification: FAILED")
                
            # Clean up
            db.session.delete(new_user)
            db.session.commit()
            print("✅ Cleanup: SUCCESS")
            
        except Exception as e:
            print(f"❌ User creation: FAILED - {e}")
            db.session.rollback()

if __name__ == "__main__":
    debug_auth()