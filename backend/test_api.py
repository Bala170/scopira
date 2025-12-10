#!/usr/bin/env python3
"""
Test script for backend API
"""

import requests
import json
import os

# API base URL
BASE_URL = "http://localhost:5000/api"

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("Testing Authentication Endpoints...")
    
    # Test registration
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Register status code: {response.status_code}")
        if response.status_code == 201:
            print("Registration successful")
            user_data = response.json()
            print(f"User ID: {user_data.get('user', {}).get('id')}")
        else:
            print(f"Registration failed: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to backend server. Make sure it's running.")
        return False
    except Exception as e:
        print(f"Error during registration test: {e}")
        return False
    
    # Test login
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login status code: {response.status_code}")
        if response.status_code == 200:
            print("Login successful")
            user_data = response.json()
            print(f"Logged in user: {user_data.get('user', {}).get('username')}")
        else:
            print(f"Login failed: {response.text}")
    except Exception as e:
        print(f"Error during login test: {e}")
        return False
    
    print("Authentication endpoints test completed.\n")
    return True

def test_job_endpoints():
    """Test job-related endpoints"""
    print("Testing Job Endpoints...")
    
    try:
        # Test getting all jobs
        response = requests.get(f"{BASE_URL}/jobs")
        print(f"Get jobs status code: {response.status_code}")
        if response.status_code == 200:
            jobs_data = response.json()
            print(f"Retrieved {len(jobs_data.get('jobs', []))} jobs")
        else:
            print(f"Failed to get jobs: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to backend server. Make sure it's running.")
        return False
    except Exception as e:
        print(f"Error during job endpoints test: {e}")
        return False
    
    print("Job endpoints test completed.\n")
    return True

def test_portfolio_endpoints():
    """Test portfolio endpoints"""
    print("Testing Portfolio Endpoints...")
    
    try:
        # Test getting portfolio (using user ID 1 as example)
        response = requests.get(f"{BASE_URL}/portfolio/1")
        print(f"Get portfolio status code: {response.status_code}")
        if response.status_code == 200:
            portfolio_data = response.json()
            print("Portfolio retrieved successfully")
        else:
            print(f"Failed to get portfolio: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to backend server. Make sure it's running.")
        return False
    except Exception as e:
        print(f"Error during portfolio endpoints test: {e}")
        return False
    
    print("Portfolio endpoints test completed.\n")
    return True

def main():
    """Run all API tests"""
    print("Running Backend API Tests\n")
    
    # Check if backend server is running
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("Backend server doesn't seem to be running at the expected URL.")
            print("Please start the backend server with 'python backend/app.py'")
            return False
    except requests.exceptions.ConnectionError:
        print("Could not connect to backend server.")
        print("Please start the backend server with 'python backend/app.py'")
        return False
    except Exception as e:
        print(f"Error checking backend server: {e}")
        return False
    
    # Run tests
    try:
        test_auth_endpoints()
        test_job_endpoints()
        test_portfolio_endpoints()
        
        print("All API tests completed!")
        
    except Exception as e:
        print(f"Error during API testing: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)