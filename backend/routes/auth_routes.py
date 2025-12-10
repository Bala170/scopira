from flask import Blueprint, request, jsonify
from models.user import User
from models.db import db

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ('username', 'email', 'password', 'first_name', 'last_name')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        profession=data.get('profession')
    )
    user.set_password(data['password'])
    
    # Save to database
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not data or 'password' not in data:
        return jsonify({'error': 'Password is required'}), 400
    
    # Find user by email or username
    user = None
    if 'email' in data:
        user = User.query.filter_by(email=data['email']).first()
    elif 'username' in data:
        user = User.query.filter_by(username=data['username']).first()
    else:
        return jsonify({'error': 'Email or username required'}), 400

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email/username or password'}), 401
    
    return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200