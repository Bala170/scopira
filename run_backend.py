import sys
import os

# Add the project root and backend directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, 'backend')
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

# Change to project root directory
os.chdir(project_root)

# Set environment variables
os.environ['PYTHONPATH'] = backend_dir + os.pathsep + project_root

# Import and run the app
# We need to change to backend directory to run the app
os.chdir(backend_dir)
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)