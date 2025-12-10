from models.db import db
from datetime import datetime

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # JSON fields for structured data
    skills = db.Column(db.Text)  # JSON: {"technical": [], "soft": []}
    experience = db.Column(db.Text)  # JSON list of objects
    education = db.Column(db.Text)  # JSON list of objects
    projects = db.Column(db.Text)  # JSON list of objects
    certifications = db.Column(db.Text)  # JSON list of objects
    preferences = db.Column(db.Text) # JSON object
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skills': self.skills,
            'experience': self.experience,
            'education': self.education,
            'projects': self.projects,
            'certifications': self.certifications,
            'preferences': self.preferences,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
