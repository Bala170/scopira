import requests
import json

BASE_URL = 'http://localhost:5000/api/auth'

def test_login():
    # 1. Register a test user (to ensure one exists)
    register_data = {
        'username': 'logintestuser',
        'email': 'logintest@example.com',
        'password': 'password123',
        'first_name': 'Login',
        'last_name': 'Test'
    }
    
    print("Attempting to register user...")
    try:
        reg_response = requests.post(f'{BASE_URL}/register', json=register_data)
        print(f"Register Status: {reg_response.status_code}")
        print(f"Register Response: {reg_response.text}")
    except Exception as e:
        print(f"Registration failed (might already exist): {e}")

    # 2. Try to login with email
    login_data = {
        'email': 'logintest@example.com',
        'password': 'password123'
    }
    
    print("\nAttempting to login with email...")
    try:
        login_response = requests.post(f'{BASE_URL}/login', json=login_data)
        print(f"Login Status: {login_response.status_code}")
        print(f"Login Response: {login_response.text}")
        
        if login_response.status_code == 200:
            print("SUCCESS: Login working correctly.")
        else:
            print("FAILURE: Login failed.")
            
    except Exception as e:
        print(f"Login request failed: {e}")

if __name__ == '__main__':
    test_login()
