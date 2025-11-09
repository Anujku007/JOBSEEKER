from .user import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text)
    website = db.Column(db.String(500))
    logo_url = db.Column(db.String(500))
    industry = db.Column(db.String(100))
    size = db.Column(db.String(50))  # 1-10, 11-50, 51-200, 201-500, 501-1000, 1000+
    founded_year = db.Column(db.Integer)
    headquarters = db.Column(db.String(200))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    jobs = db.relationship('Job', backref='company_ref', lazy=True)
    
    def __repr__(self):
        return f'<Company {self.name}>'