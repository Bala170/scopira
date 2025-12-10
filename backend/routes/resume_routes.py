from flask import Blueprint, request, jsonify
from models.resume import Resume
from models.db import db
import os
import json
from werkzeug.utils import secure_filename
from utils.resume_analyzer import ResumeAnalyzer

# Try to import resume parser, but don't fail if ML dependencies are missing
try:
    import sys
    import os as sys_os
    sys.path.append(sys_os.path.join(sys_os.path.dirname(__file__), '..', '..', 'ml', 'scripts'))
    from resume_parser import ResumeParser
    PARSER_AVAILABLE = True
except ImportError:
    PARSER_AVAILABLE = False
    print("Warning: Resume parser not available - ML dependencies may be missing")

bp = Blueprint('resumes', __name__, url_prefix='/api/resumes')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze resume content provided in JSON format.
    Expected JSON: {
        "summary": "...",
        "experience": [...],
        "education": [...],
        "skills": [...] or "skill1, skill2"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        analyzer = ResumeAnalyzer()
        analysis_result = analyzer.analyze(data)
        return jsonify(analysis_result), 200
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return jsonify({'error': 'Failed to analyze resume'}), 500

@bp.route('/upload', methods=['POST'])
def upload_resume():
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file has a filename
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file extension is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed.'}), 400
    
    # Get user_id from form data
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    try:
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Create upload directory if it doesn't exist
        upload_dir = '../uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Save file
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        # Parse resume to extract skills
        skills = []
        try:
            if PARSER_AVAILABLE:
                parser = ResumeParser()
                if filename.endswith('.pdf'):
                    parsed_data = parser.parse_pdf(file_path)
                elif filename.endswith('.docx'):
                    parsed_data = parser.parse_docx(file_path)
                else:
                    parsed_data = parser.extract_info(open(file_path, 'r').read())
                
                skills = parsed_data.get('skills', [])
            else:
                print("Resume parser not available - skipping skill extraction")
        except Exception as e:
            print(f"Error parsing resume: {str(e)}")
            # Continue with empty skills if parsing fails
        
        # Create resume record
        resume = Resume(
            user_id=user_id,
            file_path=file_path,
            original_filename=filename,
            skills=json.dumps(skills) if skills else None
        )
        
        # Save to database
        db.session.add(resume)
        db.session.commit()
        
        return jsonify({'message': 'Resume uploaded successfully', 'resume': resume.to_dict()}), 201
    
    except Exception as e:
        return jsonify({'error': f'Failed to upload resume: {str(e)}'}), 500

@bp.route('/<int:user_id>', methods=['GET'])
def get_user_resumes(user_id):
    resumes = Resume.query.filter_by(user_id=user_id).all()
    return jsonify({'resumes': [resume.to_dict() for resume in resumes]}), 200