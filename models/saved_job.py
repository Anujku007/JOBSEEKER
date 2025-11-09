from .user import db
from datetime import datetime

class SavedJob(db.Model):
    __tablename__ = 'saved_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    saved_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Unique constraint to prevent duplicate saves
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='unique_user_job'),)
    
    def __repr__(self):
        return f'<SavedJob user:{self.user_id} job:{self.job_id}>'