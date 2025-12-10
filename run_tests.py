#!/usr/bin/env python3
"""
Test runner for Scopira platform
"""

import subprocess
import sys
import os

def run_ml_tests():
    """Run ML component tests"""
    print("Running ML Component Tests...")
    try:
        result = subprocess.run([sys.executable, 'ml/test_ml.py'], 
                              cwd='.', capture_output=True, text=True)
        if result.returncode == 0:
            print("[SUCCESS] ML tests passed")
            return True
        else:
            print("[ERROR] ML tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error running ML tests: {e}")
        return False

def run_frontend_tests():
    """Run frontend tests"""
    print("Running Frontend Tests...")
    try:
        result = subprocess.run([sys.executable, 'frontend/test_frontend.py'], 
                              cwd='.', capture_output=True, text=True)
        if result.returncode == 0:
            print("[SUCCESS] Frontend tests passed")
            return True
        else:
            print("[ERROR] Frontend tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error running frontend tests: {e}")
        return False

def run_backend_tests():
    """Run backend API tests"""
    print("Running Backend API Tests...")
    try:
        result = subprocess.run([sys.executable, 'backend/test_api.py'], 
                              cwd='.', capture_output=True, text=True)
        if result.returncode == 0:
            print("[SUCCESS] Backend tests passed")
            return True
        else:
            print("[ERROR] Backend tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error running backend tests: {e}")
        return False

def main():
    """Run all tests"""
    print("Running All Scopira Tests\n")
    
    # Check if we're in the right directory
    if not os.path.exists('ml') or not os.path.exists('frontend') or not os.path.exists('backend'):
        print("[ERROR] Please run this script from the root of the Scopira project directory")
        return False
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if run_ml_tests():
        tests_passed += 1
    
    if run_frontend_tests():
        tests_passed += 1
    
    # Backend tests require the server to be running, so we'll skip them in this automated test
    print("Skipping backend API tests (requires server to be running)")
    print("To test backend API, start the server with 'python backend/app.py' and run 'python backend/test_api.py'")
    
    print(f"\nTest Results: {tests_passed}/{total_tests} test suites passed")
    
    if tests_passed == total_tests:
        print("[SUCCESS] All tests passed!")
        return True
    else:
        print("[WARNING] Some tests failed or were skipped")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)