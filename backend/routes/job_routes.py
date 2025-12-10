from flask import Blueprint, request, jsonify
from models.job import Job
from models.user_job_match import UserJobMatch
from models.user import User
from models.resume import Resume
from models.portfolio import Portfolio
from models.db import db
import json

bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@bp.route('/', methods=['GET'])
def get_jobs():
    # Get query parameters for filtering
    location = request.args.get('location')
    title = request.args.get('title')
    
    # Build query
    query = Job.query.filter_by(active=True)
    
    if location:
        query = query.filter(Job.location.contains(location))
    
    if title:
        query = query.filter(Job.title.contains(title))
    
    jobs = query.all()
    
    return jsonify({'jobs': [job.to_dict() for job in jobs]}), 200

@bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify({'job': job.to_dict()}), 200

@bp.route('/matches/<int:user_id>', methods=['GET'])
def get_user_job_matches(user_id):
    matches = UserJobMatch.query.filter_by(user_id=user_id).join(Job).all()
    
    result = []
    for match in matches:
        match_data = match.to_dict()
        match_data['job'] = match.job.to_dict()
        result.append(match_data)
    
    return jsonify({'matches': result}), 200

@bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_job_recommendations(user_id):
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user skills from Portfolio or Resume
    user_skills = []
    
    # Try Portfolio first
    portfolio = Portfolio.query.filter_by(user_id=user_id).first()
    if portfolio and portfolio.skills:
        try:
            skills_data = json.loads(portfolio.skills)
            # Combine technical and soft skills if structured, or use as list if flat
            if isinstance(skills_data, dict):
                user_skills = (skills_data.get('technical', []) + skills_data.get('soft', []))
            elif isinstance(skills_data, list):
                user_skills = skills_data
        except json.JSONDecodeError:
            pass

    # If no skills from Portfolio, try Resume
    if not user_skills:
        resume = Resume.query.filter_by(user_id=user_id).first()
        if resume and resume.skills:
            try:
                user_skills = json.loads(resume.skills)
            except json.JSONDecodeError:
                pass
    
    # If still no skills, return general job listings
    if not user_skills:
        jobs = Job.query.filter_by(active=True).limit(10).all()
        recommendations = []
        for job in jobs:
            recommendations.append({
                'job_id': job.id,
                'job': job.to_dict(),
                'match_score': 0.5,  # Default match score
                'matched_skills': [],
                'missing_skills': []
            })
        return jsonify({'recommendations': recommendations}), 200
    
    # Get all active jobs
    jobs = Job.query.filter_by(active=True).all()
    
    # Calculate match scores for each job
    recommendations = []
    for job in jobs:
        # Get job requirements
        job_skills = []
        if job.requirements:
            try:
                job_requirements = json.loads(job.requirements)
                job_skills = job_requirements.get('skills', [])
            except json.JSONDecodeError:
                job_skills = []
        
        # Calculate match score based on skills
        if job_skills:
            # Normalize skills for comparison (lowercase)
            user_skills_norm = {s.lower() for s in user_skills}
            job_skills_norm = {s.lower() for s in job_skills}
            
            matched_skills = user_skills_norm & job_skills_norm
            match_score = len(matched_skills) / len(job_skills_norm) if len(job_skills_norm) > 0 else 0
            
            # Convert back to original case for display (best effort)
            matched_display = [s for s in user_skills if s.lower() in matched_skills]
            missing_display = [s for s in job_skills if s.lower() not in matched_skills]
        else:
            match_score = 0.5  # Default match score if no requirements specified
            matched_display = []
            missing_display = []
        
        recommendations.append({
            'job_id': job.id,
            'job': job.to_dict(),
            'match_score': match_score,
            'matched_skills': matched_display,
            'missing_skills': missing_display
        })
    
    # Sort by match score (descending)
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Return top 10 recommendations
    return jsonify({'recommendations': recommendations[:10]}), 200

@bp.route('/match', methods=['POST'])
def calculate_job_match():
    """Calculate match score between a user and a job"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    job_id = data.get('job_id')
    
    if not user_id or not job_id:
        return jsonify({'error': 'user_id and job_id are required'}), 400
    
    # Get user and job
    user = User.query.get(user_id)
    job = Job.query.get(job_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    # Get user skills from Portfolio or Resume
    user_skills = []
    
    # Try Portfolio first
    portfolio = Portfolio.query.filter_by(user_id=user_id).first()
    if portfolio and portfolio.skills:
        try:
            skills_data = json.loads(portfolio.skills)
            if isinstance(skills_data, dict):
                user_skills = (skills_data.get('technical', []) + skills_data.get('soft', []))
            elif isinstance(skills_data, list):
                user_skills = skills_data
        except json.JSONDecodeError:
            pass

    # If no skills from Portfolio, try Resume
    if not user_skills:
        resume = Resume.query.filter_by(user_id=user_id).first()
        if resume and resume.skills:
            try:
                user_skills = json.loads(resume.skills)
            except json.JSONDecodeError:
                pass
    
    # Get job requirements
    job_skills = []
    if job.requirements:
        try:
            job_requirements = json.loads(job.requirements)
            job_skills = job_requirements.get('skills', [])
        except json.JSONDecodeError:
            job_skills = []
    
    # Calculate match score
    if job_skills:
        user_skills_norm = {s.lower() for s in user_skills}
        job_skills_norm = {s.lower() for s in job_skills}
        
        matched_skills = user_skills_norm & job_skills_norm
        missing_skills = job_skills_norm - user_skills_norm
        match_score = len(matched_skills) / len(job_skills_norm)
    else:
        matched_skills = set()
        missing_skills = set()
        match_score = 0.5  # Default match score if no requirements specified
    
    # Save match to database
    user_job_match = UserJobMatch(
        user_id=user_id,
        job_id=job_id,
        match_score=match_score,
        matched_skills=json.dumps(list(matched_skills)),
        missing_skills=json.dumps(list(missing_skills))
    )
    
    db.session.add(user_job_match)
    db.session.commit()
    
    return jsonify({
        'match_id': user_job_match.id,
        'match_score': match_score,
        'matched_skills': list(matched_skills),
        'missing_skills': list(missing_skills)
    }), 201