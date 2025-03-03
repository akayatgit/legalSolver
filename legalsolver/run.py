import os
import sys
from app import app

def run_application():
    """Run the Legal Solver application"""
    print("\n" + "=" * 60)
    print("LEGAL SOLVER - APPLICATION STARTUP")
    print("=" * 60)
    
    print("\nStarting Legal Solver application...")
    print("Email is pre-configured with the following settings:")
    print("- Email: notification@agentsdistrict.com")
    print("- SMTP Server: smtp.hostinger.com")
    print("- SMTP Port: 465")
    
    print("\nRunning application on http://127.0.0.1:5000")
    app.run(debug=True)

if __name__ == "__main__":
    run_application() 