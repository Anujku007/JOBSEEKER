from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    saved_jobs = db.relationship('SavedJob', backref='user', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    remote = db.Column(db.Boolean, default=False)
    salary = db.Column(db.String(100))
    source = db.Column(db.String(100))
    job_url = db.Column(db.String(500))
    posted_date = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    saved_by = db.relationship('SavedJob', backref='job', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'

class SavedJob(db.Model):
    __tablename__ = 'saved_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure a user can't save the same job multiple times
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='unique_user_job'),)
    
    def __repr__(self):
        return f'<SavedJob user:{self.user_id} job:{self.job_id}>'

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Applied')
    cover_letter = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Application user:{self.user_id} job:{self.job_id} status:{self.status}>'

def create_sample_data():
    """Function to create sample data for testing"""
    # Check if sample user already exists
    if not User.query.filter_by(email='test@example.com').first():
        # Create sample user
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        db.session.add(user)
        
        # Create sample jobs
        jobs = [
            Job(
                title='Senior Python Developer',
                company='Tech Corp Inc',
                location='New York, NY',
                description='We are looking for an experienced Python developer to join our team...',
                type='Full-time',
                remote=True,
                salary='$120,000 - $140,000',
                source='LinkedIn',
                job_url='https://example.com/job1',
                posted_date='2 days ago'
            ),
            Job(
                title='Frontend React Developer',
                company='Startup XYZ',
                location='San Francisco, CA',
                description='Join our dynamic team as a Frontend Developer working with React...',
                type='Full-time',
                remote=False,
                salary='$100,000 - $130,000',
                source='Indeed',
                job_url='https://example.com/job2',
                posted_date='1 week ago'
            ),
            Job(
                title='DevOps Engineer',
                company='Cloud Solutions Ltd',
                location='Remote',
                description='We need a DevOps engineer to help scale our infrastructure...',
                type='Contract',
                remote=True,
                salary='$90 - $120/hr',
                source='Glassdoor',
                job_url='https://example.com/job3',
                posted_date='3 days ago'
            )
        ]
        
        for job in jobs:
            db.session.add(job)
        
        db.session.commit()
        print("Sample data created successfully!")