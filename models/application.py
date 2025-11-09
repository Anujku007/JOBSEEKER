from .user import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    cover_letter = db.Column(db.Text)
    status = db.Column(db.String(50), default='applied')  # applied, viewed, contacted, rejected, hired
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def get_status_display(self):
        status_map = {
            'applied': 'Applied',
            'viewed': 'Viewed',
            'contacted': 'Contacted',
            'rejected': 'Rejected',
            'hired': 'Hired'
        }
        return status_map.get(self.status, self.status)
    
    def __repr__(self):
        return f'<Application {self.user_id} for {self.job_id}>'