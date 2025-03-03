import os
import requests
from flask import Flask, session
from app import app

def test_file_upload():
    """Test the file upload functionality"""
    print("Testing file upload functionality...")
    
    # Create a test file
    test_file_path = "test_document.txt"
    with open(test_file_path, "w") as f:
        f.write("This is a test document for upload testing.")
    
    try:
        # Set up the test client
        with app.test_client() as client:
            # Log in first (required for upload)
            client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)
            
            # Test file upload
            with open(test_file_path, 'rb') as f:
                response = client.post(
                    '/upload',
                    data={
                        'document': (f, 'test_document.txt')
                    },
                    content_type='multipart/form-data',
                    follow_redirects=True
                )
            
            # Check response
            if response.status_code == 200:
                print("✅ File upload test successful!")
                print(f"Response status code: {response.status_code}")
            else:
                print("❌ File upload test failed!")
                print(f"Response status code: {response.status_code}")
                print(f"Response data: {response.data.decode('utf-8')}")
    
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print(f"Removed test file: {test_file_path}")

if __name__ == "__main__":
    test_file_upload() 