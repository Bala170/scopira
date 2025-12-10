from models.db import db
from datetime import datetime

class UserJobMatch(db.Model):
    __tablename__ = 'user_job_matches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    match_score = db.Column(db.Float)  # Between 0 and 1
    matched_skills = db.Column(db.Text)  # JSON string of matched skills
    missing_skills = db.Column(db.Text)  # JSON string of missing skills
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'match_score': self.match_score,
            'matched_skills': self.matched_skills,
            'missing_skills': self.missing_skills,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }