from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a simple app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobseeker.db'
app.config['SECRET_KEY'] = 'dev-key-change-in-production'

db = SQLAlchemy(app)

# Simple models for initialization
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    remote = db.Column(db.Boolean, default=False)

class SavedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_database():
    with app.app_context():
        # Drop and create all tables
        db.drop_all()
        db.create_all()
        
        # Create test user
        from werkzeug.security import generate_password_hash
        test_user = User(
            email='test@jobseeker.com',
            first_name='Test',
            last_name='User',
            password_hash=generate_password_hash('password123')
        )
        db.session.add(test_user)
        db.session.commit()
        
        print("✅ Database initialized successfully!")
        print("✅ Test user: test@jobseeker.com / password123")

if __name__ == '__main__':
    init_database()