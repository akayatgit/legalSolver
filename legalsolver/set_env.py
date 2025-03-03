import os
import sys

def set_email_credentials():
    """Set email credentials as environment variables"""
    email = input("Enter email address: ")
    password = input("Enter email password or app password: ")
    
    # Set environment variables
    os.environ["EMAIL_USER"] = email
    os.environ["EMAIL_PASSWORD"] = password
    
    print("Environment variables set successfully!")
    print("Note: These will only be available in the current terminal session.")
    
    # If on Windows, provide instructions for setting permanently
    if sys.platform.startswith('win'):
        print("\nTo set these permanently on Windows, use:")
        print(f'setx EMAIL_USER "{email}"')
        print(f'setx EMAIL_PASSWORD "{password}"')
    # If on Linux/Mac
    else:
        print("\nTo set these permanently on Linux/Mac, add to your ~/.bashrc or ~/.zshrc:")
        print(f'export EMAIL_USER="{email}"')
        print(f'export EMAIL_PASSWORD="{password}"')

if __name__ == "__main__":
    set_email_credentials() 