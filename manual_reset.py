import os
from sqlalchemy import inspect

def manual_reset():
    """Safely reset the database and recreate schema + test data"""

    from app import create_app
    from extensions import db
    from models.simple_models import User

    app = create_app()

    with app.app_context():
        try:
            # Detect actual DB path from SQLAlchemy URI
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if db_uri.startswith('sqlite:///'):
                db_path = db_uri.replace('sqlite:///', '')
            elif db_uri == 'sqlite:///:memory:':
                print("ℹ️ Using in-memory database - no file to delete")
                db_path = None
            else:
                db_path = 'instance/jobseeker.db'  # Common Flask default
            
            # Delete DB file if it exists and we're using file-based SQLite
            if db_path and os.path.exists(db_path):
                os.remove(db_path)
                print(f"🗑️  Deleted database file: {db_path}")
            elif db_path:
                print(f"ℹ️  Database file not found: {db_path}")

            # Recreate schema
            print("🔄 Creating new database with correct schema...")
            db.create_all()

            # Create test user
            test_user = User(
                username="testuser",
                email="test@example.com",
                first_name="Test",
                last_name="User"
            )
            test_user.set_password("password123")
            
            db.session.add(test_user)
            db.session.commit()
            print("👤 Test user created successfully.")

            # Verify tables
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Database tables: {tables}")

            # Verify users
            users = User.query.all()
            print(f"👥 Total users: {len(users)}")
            for user in users:
                print(f"   - {user.email} (ID: {user.id})")

            print("✅ Database reset complete!")

        except Exception as e:
            print(f"❌ Error during reset: {e}")
            db.session.rollback()

if __name__ == "__main__":
    manual_reset()