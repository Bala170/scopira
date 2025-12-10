#!/usr/bin/env python3
"""
Development server runner for Scopira
"""

import subprocess
import threading
import time
import os
import sys

# Add the project root and backend directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, 'backend')
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

def run_backend():
    """Run the Flask backend server"""
    print("Starting Flask backend server...")
    try:
        # Get absolute paths
        project_root = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(project_root, 'backend')
        
        # Set Python path
        env = os.environ.copy()
        env['PYTHONPATH'] = backend_dir + os.pathsep + project_root
        
        # Run Flask app
        subprocess.run(['python', 'app.py'], cwd=backend_dir, env=env)
    except Exception as e:
        print(f"Error starting backend server: {e}")

def run_frontend():
    """Run the frontend development server"""
    print("Starting frontend development server...")
    try:
        # Get absolute paths
        project_root = os.path.dirname(os.path.abspath(__file__))
        frontend_dir = os.path.join(project_root, 'frontend')
        
        # Run Python HTTP server
        subprocess.run(['python', '-m', 'http.server', '8000'], cwd=frontend_dir)
    except Exception as e:
        print(f"Error starting frontend server: {e}")

if __name__ == "__main__":
    print("Starting Scopira development servers...")
    
    # Create threads for backend and frontend
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)
    
    # Start both servers
    backend_thread.start()
    frontend_thread.start()
    
    # Give the servers time to start
    time.sleep(3)
    
    print("\nServers started:")
    print("- Frontend: http://localhost:8000")
    print("- Backend: http://localhost:5000")
    print("\nPress Ctrl+C to stop the servers\n")
    
    try:
        # Wait for threads to complete
        backend_thread.join()
        frontend_thread.join()
    except KeyboardInterrupt:
        print("Stopping servers...")
    
    print("Development servers stopped.")