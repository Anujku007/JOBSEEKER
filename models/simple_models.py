from extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    saved_jobs = db.relationship('SavedJob', backref='user', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        print(f"🔐 Password set for {self.email}")
    
    def check_password(self, password):
        if not self.password_hash:
            print("❌ No password hash set for user")
            return False
        result = check_password_hash(self.password_hash, password)
        print(f"🔐 Password check for {self.email}: {result}")
        return result

    def __repr__(self):
        return f'<User {self.email}>'


class SavedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.String(100), nullable=False)  # String ID from API

    # Store job details directly (denormalized)
    job_title = db.Column(db.String(200), nullable=False)
    job_company = db.Column(db.String(100), nullable=False)
    job_location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50))
    job_salary = db.Column(db.String(100))
    job_description = db.Column(db.Text)
    job_url = db.Column(db.String(500))
    job_posted_date = db.Column(db.String(50))
    job_remote = db.Column(db.Boolean, default=False)
    job_source = db.Column(db.String(100))
    
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Ensure a user can't save the same job multiple times
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='unique_user_job'),)

    def __repr__(self):
        return f'<SavedJob {self.job_id} for user {self.user_id}>'


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.String(100), nullable=False)  # String ID from API

    # Store job details directly (denormalized)
    job_title = db.Column(db.String(200), nullable=False)
    job_company = db.Column(db.String(100), nullable=False)
    job_location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50))
    job_salary = db.Column(db.String(100))
    job_description = db.Column(db.Text)
    job_url = db.Column(db.String(500))
    job_posted_date = db.Column(db.String(50))
    job_remote = db.Column(db.Boolean, default=False)
    job_source = db.Column(db.String(100))

    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Applied')
    notes = db.Column(db.Text)

    # NEW: resume file path (relative to your static/uploads or uploads/resumes folder)
    resume_file = db.Column(db.String(255), nullable=True)

    # Ensure a user can't apply to the same job multiple times
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='unique_user_job_application'),)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'status': self.status,
            'notes': self.notes,
            'resume_file': self.resume_file,
            'job': {
                'id': self.job_id,
                'title': self.job_title,
                'company': self.job_company,
                'location': self.job_location,
                'job_type': self.job_type,
                'salary': self.job_salary,
                'description': self.job_description,
                'url': self.job_url,
                'posted_date': self.job_posted_date,
                'remote': self.job_remote,
                'source': self.job_source
            }
        }

    def __repr__(self):
        return f'<Application {self.job_id} by user {self.user_id}>'
