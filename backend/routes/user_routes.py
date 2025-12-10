from flask import Blueprint, request, jsonify, current_app
from models.user import User
from models.db import db
import os
from werkzeug.utils import secure_filename

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@bp.route('/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        # Check if email is taken by another user
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({'error': 'Email already in use'}), 400
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    if 'location' in data:
        user.location = data['location']
    if 'headline' in data:
        user.headline = data['headline']
    if 'summary' in data:
        user.summary = data['summary']
    if 'profession' in data:
        user.profession = data['profession']
        
    db.session.commit()
    
    return jsonify({'message': 'Profile updated successfully', 'user': user.to_dict()}), 200

@bp.route('/<int:user_id>/upload-picture', methods=['POST'])
def upload_profile_picture(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        filename = secure_filename(f"profile_{user_id}_{file.filename}")
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Update user profile picture URL
        # Assuming the frontend can access uploads via /uploads/filename
        # We store the full URL or relative path. Let's store the relative path/filename.
        # Or better, the full URL if we know the domain, but relative is safer.
        # Let's store just the filename and construct the URL in the frontend or return the full URL here.
        
        user.profile_picture = f"/uploads/{filename}"
        db.session.commit()
        
        return jsonify({'message': 'Profile picture uploaded successfully', 'profile_picture': user.profile_picture}), 200

