from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Database instance
db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User preferences
    preferred_location = db.Column(db.String(100))
    job_alerts = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)

class SavedJob(db.Model):
    __tablename__ = 'saved_jobs'
    
    # PRIMARY KEY IS REQUIRED - Add this line:
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.String(100), nullable=False)  # External job ID
    job_title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100))
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Store additional job details for quick access
    job_type = db.Column(db.String(50))
    salary = db.Column(db.String(100))
    remote = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job_title': self.job_title,
            'company': self.company,
            'location': self.location,
            'job_type': self.job_type,
            'salary': self.salary,
            'remote': self.remote,
            'source': self.source,
            'saved_at': self.saved_at.isoformat()
        }