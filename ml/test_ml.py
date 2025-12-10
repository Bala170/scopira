#!/usr/bin/env python3
"""
Test script for ML components
"""

import sys
import os

# Add parent directory to path to import ML modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ml.scripts.resume_parser import ResumeParser
from ml.scripts.job_matcher import JobMatcher
from ml.scripts.skill_gap_analyzer import SkillGapAnalyzer
from ml.scripts.resume_generator import ResumeGenerator

def test_resume_parser():
    """Test the resume parser component"""
    print("Testing Resume Parser...")
    
    # Create a sample resume text
    sample_resume = """
    John Doe
    Data Scientist
    john.doe@example.com
    (555) 123-4567
    San Francisco, CA
    
    PROFESSIONAL SUMMARY
    Experienced data scientist with 5+ years in machine learning and statistical analysis.
    
    SKILLS
    Python, Machine Learning, SQL, Data Visualization, TensorFlow, Scikit-learn
    
    PROFESSIONAL EXPERIENCE
    Senior Data Scientist, TechCorp (2022-Present)
    - Developed machine learning models that improved customer retention by 25%
    - Led a team of 3 junior data scientists
    
    Data Scientist, DataSystems Ltd (2020-2022)
    - Built predictive models for sales forecasting
    - Created interactive dashboards using Tableau
    
    EDUCATION
    M.S. in Data Science, University of California (2019)
    B.S. in Computer Science, Stanford University (2017)
    """
    
    # Test the parser
    parser = ResumeParser()
    
    # Since we don't have actual files, we'll test the extract_info method directly
    parsed_data = parser.extract_info(sample_resume)
    
    print("Parsed entities:", parsed_data.get('entities', {}))
    print("Parsed skills:", parsed_data.get('skills', []))
    print("Experience sections:", len(parsed_data.get('experience', [])))
    print("Resume Parser test completed.\n")

def test_job_matcher():
    """Test the job matcher component"""
    print("Testing Job Matcher...")
    
    matcher = JobMatcher()
    
    # Sample user profile and job descriptions
    user_profile = "Experienced Python developer with skills in machine learning and data analysis"
    job_descriptions = [
        "Looking for Python developer with machine learning experience",
        "Seeking Java developer with Spring framework experience",
        "Need data scientist with Python and statistics background"
    ]
    
    # Calculate similarities
    similarities = matcher.calculate_similarity(user_profile, job_descriptions)
    
    for i, score in enumerate(similarities):
        print(f"Job {i+1} similarity score: {score:.3f}")
    
    # Test skill matching
    user_skills = ['Python', 'Machine Learning', 'SQL']
    job_requirements = [
        {
            'id': 1,
            'skills': ['Python', 'Machine Learning', 'Deep Learning']
        },
        {
            'id': 2,
            'skills': ['Java', 'Spring', 'Hibernate']
        }
    ]
    
    matches = matcher.match_user_to_jobs(user_skills, job_requirements)
    for match in matches:
        print(f"Job {match['job_id']} match score: {match['match_score']:.2f}")
        print(f"  Matched skills: {match['matched_skills']}")
        print(f"  Missing skills: {match['missing_skills']}")
    
    print("Job Matcher test completed.\n")

def test_skill_gap_analyzer():
    """Test the skill gap analyzer component"""
    print("Testing Skill Gap Analyzer...")
    
    analyzer = SkillGapAnalyzer()
    
    # Sample data
    user_skills = ['Python', 'SQL', 'Data Analysis']
    job_requirements = {
        'skills': [
            {'name': 'Python', 'importance': 5},
            {'name': 'Machine Learning', 'importance': 4},
            {'name': 'SQL', 'importance': 3},
            {'name': 'Deep Learning', 'importance': 2}
        ]
    }
    
    # Analyze gaps
    gaps = analyzer.analyze_gaps(user_skills, job_requirements)
    
    print(f"Match percentage: {gaps['match_percentage']:.1f}%")
    print(f"Matched skills: {[skill['name'] for skill in gaps['matched_skills']]}")
    print(f"Missing skills: {[skill['name'] for skill in gaps['missing_skills']]}")
    print(f"Recommendations: {len(gaps['recommendations'])} learning resources suggested")
    
    print("Skill Gap Analyzer test completed.\n")

def test_resume_generator():
    """Test the resume generator component"""
    print("Testing Resume Generator...")
    
    generator = ResumeGenerator()
    
    # Sample data
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+1 (555) 123-4567',
        'skills': ['Python', 'Machine Learning', 'Data Analysis', 'SQL'],
        'experience': [
            'Senior Data Analyst, Tech Corp (2020-Present)\n- Led data analysis initiatives\n- Developed machine learning models',
            'Data Analyst, Startup Inc (2018-2020)\n- Performed statistical analysis\n- Created data visualizations'
        ],
        'education': [
            'M.S. in Data Science, University (2018)',
            'B.S. in Computer Science, College (2016)'
        ]
    }
    
    job_data = {
        'title': 'Senior Data Scientist',
        'company': 'Innovative AI Company',
        'requirements': [
            {'name': 'Python'},
            {'name': 'Machine Learning'},
            {'name': 'Deep Learning'}
        ]
    }
    
    # Generate resume
    resume = generator.generate_ats_friendly_resume(user_data, job_data)
    print("Generated resume preview:")
    print(resume[:500] + "..." if len(resume) > 500 else resume)
    
    print("Resume Generator test completed.\n")

def main():
    """Run all ML component tests"""
    print("Running ML Component Tests\n")
    
    try:
        test_resume_parser()
        test_job_matcher()
        test_skill_gap_analyzer()
        test_resume_generator()
        
        print("All ML component tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)