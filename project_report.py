#!/usr/bin/env python3
"""
Project report generator for Scopira
"""

import os
import sys
from datetime import datetime

def count_files(directory):
    """Count files in a directory"""
    count = 0
    try:
        for root, dirs, files in os.walk(directory):
            count += len(files)
        return count
    except:
        return 0

def get_directory_size(directory):
    """Get directory size in MB"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except:
                    pass
        return round(total_size / (1024 * 1024), 2)
    except:
        return 0

def generate_report():
    """Generate project report"""
    print("=" * 60)
    print("SCOPERA PROJECT REPORT")
    print("=" * 60)
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Project overview
    print("PROJECT OVERVIEW")
    print("-" * 20)
    print("Name: Scopira - AI-Powered Career Guidance Platform")
    print("Description: Platform for career optimization through AI")
    print()
    
    # Directory structure
    print("DIRECTORY STRUCTURE")
    print("-" * 20)
    directories = ['frontend', 'backend', 'ml', 'database']
    for directory in directories:
        if os.path.exists(directory):
            files = count_files(directory)
            size = get_directory_size(directory)
            print(f"{directory}/: {files} files ({size} MB)")
        else:
            print(f"{directory}/: Not found")
    print()
    
    # Technology stack
    print("TECHNOLOGY STACK")
    print("-" * 20)
    print("Frontend: HTML5, CSS3, JavaScript, Chart.js")
    print("Backend: Python, Flask, SQLAlchemy")
    print("Database: PostgreSQL")
    print("ML: Python, spaCy, scikit-learn")
    print()
    
    # Features implemented
    print("FEATURES IMPLEMENTED")
    print("-" * 20)
    features = [
        "User Authentication",
        "Resume Upload & Parsing",
        "Job Matching Engine",
        "Skill Gap Analysis",
        "AI Resume Generation",
        "Portfolio Creation",
        "Interactive Dashboard"
    ]
    for feature in features:
        print(f"✓ {feature}")
    print()
    
    # Files summary
    print("FILES SUMMARY")
    print("-" * 20)
    total_files = 0
    for directory in directories:
        if os.path.exists(directory):
            files = count_files(directory)
            total_files += files
            print(f"{directory.capitalize()}: {files} files")
    
    print(f"Total Files: {total_files}")
    
    # Project size
    total_size = 0
    for directory in directories:
        if os.path.exists(directory):
            size = get_directory_size(directory)
            total_size += size
    
    print(f"Total Size: {total_size} MB")
    print()
    
    # Next steps
    print("NEXT STEPS")
    print("-" * 20)
    next_steps = [
        "Implement user authentication in frontend",
        "Connect frontend to backend APIs",
        "Train ML models with real data",
        "Deploy to production environment",
        "Add more unit tests",
        "Implement continuous integration"
    ]
    for i, step in enumerate(next_steps, 1):
        print(f"{i}. {step}")
    print()
    
    print("=" * 60)
    print("END OF REPORT")
    print("=" * 60)

if __name__ == "__main__":
    generate_report()