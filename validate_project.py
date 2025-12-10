#!/usr/bin/env python3
"""
Project structure validator for Scopira
"""

import os
import sys

def validate_directory_structure():
    """Validate the project directory structure"""
    print("Validating Project Structure...")
    print("=" * 40)
    
    # Expected directories
    expected_dirs = [
        'frontend',
        'backend',
        'ml',
        'database',
        'uploads'
    ]
    
    # Expected files in root
    expected_root_files = [
        'README.md',
        'DOCUMENTATION.md',
        '.gitignore',
        'setup.py',
        'run_dev.py',
        'run_tests.py',
        'project_report.py',
        'validate_project.py',
        '.env.example',
        'docker-compose.yml',
        'Makefile'
    ]
    
    # Check directories
    print("Checking directories...")
    missing_dirs = []
    for directory in expected_dirs:
        if os.path.exists(directory):
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ (MISSING)")
            missing_dirs.append(directory)
    
    # Check root files
    print("\nChecking root files...")
    missing_files = []
    for file in expected_root_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            missing_files.append(file)
    
    # Check frontend structure
    print("\nChecking frontend structure...")
    frontend_files = [
        'index.html',
        'dashboard.html',
        'jobs.html',
        'portfolio.html',
        'profile.html',
        'css/style.css',
        'js/main.js'
    ]
    
    missing_frontend = []
    for file in frontend_files:
        file_path = os.path.join('frontend', file)
        if os.path.exists(file_path):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            missing_frontend.append(file)
    
    # Check backend structure
    print("\nChecking backend structure...")
    backend_files = [
        'app.py',
        'requirements.txt',
        'models/__init__.py',
        'models/db.py',
        'models/user.py',
        'models/resume.py',
        'models/job.py',
        'models/user_job_match.py',
        'routes/__init__.py',
        'routes/auth_routes.py',
        'routes/resume_routes.py',
        'routes/job_routes.py',
        'routes/portfolio_routes.py'
    ]
    
    missing_backend = []
    for file in backend_files:
        file_path = os.path.join('backend', file)
        if os.path.exists(file_path):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            missing_backend.append(file)
    
    # Check ML structure
    print("\nChecking ML structure...")
    ml_files = [
        'scripts/resume_parser.py',
        'scripts/job_matcher.py',
        'scripts/skill_gap_analyzer.py',
        'scripts/resume_generator.py',
        'requirements.txt'
    ]
    
    missing_ml = []
    for file in ml_files:
        file_path = os.path.join('ml', file)
        if os.path.exists(file_path):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            missing_ml.append(file)
    
    # Check database structure
    print("\nChecking database structure...")
    db_files = [
        'schemas/schema.sql',
        'init_db.py',
        'requirements.txt'
    ]
    
    missing_db = []
    for file in db_files:
        file_path = os.path.join('database', file)
        if os.path.exists(file_path):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            missing_db.append(file)
    
    # Summary
    print("\n" + "=" * 40)
    print("VALIDATION SUMMARY")
    print("=" * 40)
    
    total_missing = len(missing_dirs) + len(missing_files) + len(missing_frontend) + \
                   len(missing_backend) + len(missing_ml) + len(missing_db)
    
    if total_missing == 0:
        print("🎉 All project structure requirements met!")
        return True
    else:
        print(f"❌ {total_missing} items missing from project structure:")
        if missing_dirs:
            print(f"  Directories: {', '.join(missing_dirs)}")
        if missing_files:
            print(f"  Root files: {', '.join(missing_files)}")
        if missing_frontend:
            print(f"  Frontend files: {', '.join(missing_frontend)}")
        if missing_backend:
            print(f"  Backend files: {', '.join(missing_backend)}")
        if missing_ml:
            print(f"  ML files: {', '.join(missing_ml)}")
        if missing_db:
            print(f"  Database files: {', '.join(missing_db)}")
        return False

def main():
    """Main validation function"""
    print("Scopira Project Structure Validator")
    print("=" * 40)
    
    success = validate_directory_structure()
    
    if success:
        print("\n✅ Project structure validation PASSED")
        return True
    else:
        print("\n❌ Project structure validation FAILED")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)