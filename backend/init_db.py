import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Change to the backend directory
os.chdir(backend_dir)

# Set the PYTHONPATH environment variable
os.environ['PYTHONPATH'] = backend_dir

from app import app
from models.db import db
from models.user import User
from models.job import Job
from models.resume import Resume
from models.user_job_match import UserJobMatch

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()