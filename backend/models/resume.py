from models.db import db
from datetime import datetime

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(100), nullable=False)
    parsed_data = db.Column(db.Text)  # JSON string of parsed resume data
    skills = db.Column(db.Text)  # JSON string of extracted skills
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Parsed resume fields
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    summary = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'original_filename': self.original_filename,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'skills': self.skills
        }