import sys
import os

# Add the current directory and backend directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

# Set the Python path environment variable
os.environ['PYTHONPATH'] = current_dir

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a minimal Flask app for database initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scopira.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)  # JSON string of required skills
    location = db.Column(db.String(100))
    salary_range = db.Column(db.String(50))
    posted_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    active = db.Column(db.Boolean, default=True)

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(100), nullable=False)
    parsed_data = db.Column(db.Text)  # JSON string of parsed resume data
    skills = db.Column(db.Text)  # JSON string of extracted skills
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Parsed resume fields
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    summary = db.Column(db.Text)

class UserJobMatch(db.Model):
    __tablename__ = 'user_job_matches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    match_score = db.Column(db.Float)  # Between 0 and 1
    matched_skills = db.Column(db.Text)  # JSON string of matched skills
    missing_skills = db.Column(db.Text)  # JSON string of missing skills
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    create_tables()