import os
import json
from email_service import send_emails_for_analysis, get_department_email, load_department_emails

def test_email_debug():
    """Debug the email sending functionality"""
    print("Debugging email sending functionality...")
    
    # Test analysis results with a department
    test_analysis = [
        {
            "section": "509",
            "keywords": ["Word", "Gesture", "Intrusion upon the privacy of a woman", "Insult", "Modesty"],
            "description": {
                "en": "Word, gesture or act intended to insult the modesty of a woman...",
                "ta": "ஒரு பெண்ணின் அடக்கத்தை அவமதிக்கும் நோக்கில் வார்த்தை, சைகை அல்லது செயல்..."
            },
            "department": "Women Protection Cell",
            "priority": "Medium",
            "suggestion": "Record the victim's statement, gather evidence of the insult, and initiate legal proceedings."
        }
    ]
    
    # Check if department_emails.json exists
    if os.path.exists("department_emails.json"):
        print("✅ department_emails.json file exists")
    else:
        print("❌ department_emails.json file not found")
        # Create the file with default values
        departments = [
            {"department": "Police", "email": "policepetitionhub123@gmail.com"},
            {"department": "Women Protection Cell", "email": "womenprotectioncell52@gmail.com"},
            {"department": "Economic Offences Wing", "email": "economicoffenceswing2@gmail.com"}
        ]
        with open("department_emails.json", "w", encoding="utf-8") as f:
            json.dump(departments, f, indent=2)
        print("Created department_emails.json with default values")
    
    # Test loading department emails
    departments = load_department_emails()
    print(f"Loaded departments: {departments}")
    
    # Test getting department email
    dept_email = get_department_email("Women Protection Cell")
    print(f"Women Protection Cell email: {dept_email}")
    
    # Test sending emails
    print("\nTesting email sending with test analysis results...")
    success, sent_depts = send_emails_for_analysis(
        user_id=1,  # Test user ID
        document_name="test_document.txt",
        file_path="test_document.txt",
        analysis_results=test_analysis
    )
    
    print(f"Email sending success: {success}")
    print(f"Sent departments: {sent_depts}")
    
    # Test with JSON string
    print("\nTesting email sending with JSON string...")
    json_analysis = json.dumps(test_analysis)
    success, sent_depts = send_emails_for_analysis(
        user_id=1,  # Test user ID
        document_name="test_document.txt",
        file_path="test_document.txt",
        analysis_results=json_analysis
    )
    
    print(f"Email sending success (JSON): {success}")
    print(f"Sent departments (JSON): {sent_depts}")

if __name__ == "__main__":
    test_email_debug() 