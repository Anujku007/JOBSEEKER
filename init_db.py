from app import create_app
from extensions import db
from models.simple_models import User, Job, SavedJob
from werkzeug.security import generate_password_hash

def init_database():
    app = create_app()
    
    with app.app_context():
        try:
            print("🗑️ Dropping existing tables...")
            db.drop_all()
            
            print("📦 Creating new tables...")
            db.create_all()
            
            # Create test user
            print("👤 Creating test user...")
            test_user = User(
                email='test@jobseeker.com',
                first_name='Test',
                last_name='User'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            
            # Create test jobs
            print("💼 Creating test jobs...")
            jobs_data = [
                {
                    'title': 'Python Developer',
                    'company': 'TechCorp',
                    'location': 'San Francisco, CA',
                    'job_type': 'full-time',
                    'description': 'We are looking for a Python developer with Flask experience to build amazing web applications.',
                    'remote': True
                },
                {
                    'title': 'Backend Engineer', 
                    'company': 'StartupXYZ',
                    'location': 'New York, NY',
                    'job_type': 'full-time',
                    'description': 'Join our backend team to build scalable APIs and microservices.',
                    'remote': False
                },
                {
                    'title': 'Data Scientist',
                    'company': 'DataWorks',
                    'location': 'Remote',
                    'job_type': 'full-time',
                    'description': 'Looking for Data Scientist with Python, ML, and data analysis skills.',
                    'remote': True
                }
            ]
            
            for job_data in jobs_data:
                job = Job(**job_data)
                db.session.add(job)
            
            db.session.commit()
            
            print("✅ Database initialized successfully!")
            print("✅ Test user: test@jobseeker.com / password123")
            print("✅ 3 test jobs created")
            print("🎉 You can now run: python app.py")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    init_database()