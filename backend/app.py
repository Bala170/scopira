import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from flask import Flask, send_from_directory
from flask_cors import CORS
from models.db import db

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
app.config['UPLOAD_FOLDER'] = '../uploads'

# Database configuration - use PostgreSQL if DATABASE_URL is set, otherwise SQLite for development
database_url = os.environ.get('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scopira.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

# Import models to ensure they are registered with SQLAlchemy before create_all
from models.user import User
from models.job import Job
from models.resume import Resume
from models.user_job_match import UserJobMatch
from models.portfolio import Portfolio

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Import routes
from routes import auth_routes, resume_routes, job_routes, portfolio_routes, user_routes

# Register blueprints
app.register_blueprint(auth_routes.bp)
app.register_blueprint(resume_routes.bp)
app.register_blueprint(job_routes.bp)
app.register_blueprint(portfolio_routes.bp)
app.register_blueprint(user_routes.bp)

@app.route('/')
def index():
    return {'message': 'Scopira Backend API'}

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)