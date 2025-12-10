import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
app.config['UPLOAD_FOLDER'] = '../uploads'

# Simple in-memory data for testing
users_data = {
    1: {
        'id': 1,
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '123-456-7890',
        'location': 'Test City',
        'profession': 'Software Developer',
        'headline': 'Test User Profile',
        'summary': 'This is a test user profile'
    }
}

# Store passwords separately (in production, these should be hashed)
passwords = {
    1: 'testpass123'
}

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return {'message': 'Scopira Backend API - Working!'}

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ('username', 'email', 'password', 'first_name', 'last_name')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists (simple check in memory)
    for user_id, user in users_data.items():
        if user['email'] == data['email']:
            return jsonify({'error': 'Email already registered'}), 400
        if user['username'] == data['username']:
            return jsonify({'error': 'Username already exists'}), 400
    
    # Create new user ID
    new_user_id = max(users_data.keys()) + 1 if users_data else 1
    
    # Create new user
    new_user = {
        'id': new_user_id,
        'username': data['username'],
        'email': data['email'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'phone': '',
        'location': '',
        'profession': data.get('profession', ''),
        'headline': f"{data['first_name']} {data['last_name']}",
        'summary': ''
    }
    
    # Store password (in production, this should be hashed)
    # For simplicity, we'll just store it in a separate dict
    if 'passwords' not in globals():
        global passwords
        passwords = {}
    passwords[new_user_id] = data['password']
    
    # Save to in-memory storage
    users_data[new_user_id] = new_user
    
    return jsonify({'message': 'User registered successfully', 'user': new_user}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Find user by email
    user_found = None
    user_id = None
    for uid, user in users_data.items():
        if user['email'] == data['email']:
            user_found = user
            user_id = uid
            break
    
    if not user_found:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Check password (in production, this should be hashed comparison)
    if 'passwords' not in globals():
        global passwords
        passwords = {}
    
    stored_password = passwords.get(user_id, '')
    if stored_password != data['password']:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    return jsonify({'message': 'Login successful', 'user': user_found}), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = users_data.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user}), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user = users_data.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update user data
    for field in ['first_name', 'last_name', 'email', 'phone', 'location', 'headline', 'summary', 'profession']:
        if field in data:
            user[field] = data[field]
    
    users_data[user_id] = user
    
    return jsonify({'message': 'Profile updated successfully', 'user': user}), 200

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    print("Starting Scopira Backend API...")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    app.run(debug=True, host='0.0.0.0', port=5000)