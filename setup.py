#!/usr/bin/env python3
"""
Setup script for Scopira platform
"""

import subprocess
import sys
import os

def install_backend_dependencies():
    """Install backend Python dependencies"""
    print("Installing backend dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'], check=True)
        print("Backend dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing backend dependencies: {e}")
        return False
    return True

def install_ml_dependencies():
    """Install ML Python dependencies"""
    print("Installing ML dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'ml/requirements.txt'], check=True)
        print("ML dependencies installed successfully")
        
        # Install spaCy English model
        print("Installing spaCy English model...")
        subprocess.run([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'], check=True)
        print("spaCy English model installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing ML dependencies: {e}")
        return False
    return True

def install_database_dependencies():
    """Install database Python dependencies"""
    print("Installing database dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'database/requirements.txt'], check=True)
        print("Database dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing database dependencies: {e}")
        return False
    return True

def setup_frontend():
    """Setup frontend dependencies"""
    print("Setting up frontend dependencies...")
    try:
        # Change to frontend directory
        os.chdir('frontend')
        # Install npm dependencies (if package.json exists)
        if os.path.exists('package.json'):
            subprocess.run(['npm', 'install'], check=True)
            print("Frontend dependencies installed successfully")
        else:
            print("No package.json found, skipping npm install")
        
        # Change back to root directory
        os.chdir('..')
    except subprocess.CalledProcessError as e:
        print(f"Error setting up frontend: {e}")
        return False
    except Exception as e:
        print(f"Error changing directory: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("Setting up Scopira platform...")
    
    # Install backend dependencies
    if not install_backend_dependencies():
        return False
    
    # Install ML dependencies
    if not install_ml_dependencies():
        return False
    
    # Install database dependencies
    if not install_database_dependencies():
        return False
    
    # Setup frontend
    if not setup_frontend():
        return False
    
    print("\nSetup completed successfully!")
    print("\nTo run the development servers:")
    print("1. Make sure PostgreSQL is installed and running")
    print("2. Create the database by running: python database/init_db.py")
    print("3. Start the development servers: python run_dev.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)