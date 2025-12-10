from flask import Blueprint, request, jsonify
from models.portfolio import Portfolio
from models.db import db
import json

bp = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')

@bp.route('/<int:user_id>', methods=['GET'])
def get_portfolio(user_id):
    portfolio = Portfolio.query.filter_by(user_id=user_id).first()
    
    if not portfolio:
        # Return empty structure if no portfolio exists
        return jsonify({'portfolio': {
            'user_id': user_id,
            'skills': '{"technical": [], "soft": []}',
            'experience': '[]',
            'education': '[]',
            'projects': '[]',
            'certifications': '[]',
            'preferences': '{}'
        }}), 200
    
    return jsonify({'portfolio': portfolio.to_dict()}), 200

@bp.route('/<int:user_id>', methods=['POST', 'PUT'])
def update_portfolio(user_id):
    data = request.get_json()
    
    portfolio = Portfolio.query.filter_by(user_id=user_id).first()
    
    if not portfolio:
        portfolio = Portfolio(user_id=user_id)
        db.session.add(portfolio)
    
    if 'skills' in data:
        portfolio.skills = json.dumps(data['skills']) if isinstance(data['skills'], (dict, list)) else data['skills']
    if 'experience' in data:
        portfolio.experience = json.dumps(data['experience']) if isinstance(data['experience'], list) else data['experience']
    if 'education' in data:
        portfolio.education = json.dumps(data['education']) if isinstance(data['education'], list) else data['education']
    if 'projects' in data:
        portfolio.projects = json.dumps(data['projects']) if isinstance(data['projects'], list) else data['projects']
    if 'certifications' in data:
        portfolio.certifications = json.dumps(data['certifications']) if isinstance(data['certifications'], list) else data['certifications']
    if 'preferences' in data:
        portfolio.preferences = json.dumps(data['preferences']) if isinstance(data['preferences'], dict) else data['preferences']
        
    db.session.commit()
    
    return jsonify({'message': 'Portfolio updated successfully', 'portfolio': portfolio.to_dict()}), 200