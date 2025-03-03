import os
from pathlib import Path
from gmail_oauth import send_email_oauth, setup_oauth_credentials

def test_oauth_email():
    """Test sending an email using OAuth authentication"""
    print("=" * 60)
    print("LEGAL SOLVER - GMAIL OAUTH TEST")
    print("=" * 60)
    
    # Check if credentials.json exists
    if not Path('credentials.json').exists():
        print("\n❌ ERROR: credentials.json file not found!")
        print("You need to set up OAuth credentials first.")
        setup_oauth_credentials()
        return False
    
    print("\nThis test will send an email to yourself using Gmail OAuth authentication.")
    print("A browser window will open for you to sign in to your Google account.")
    print("You'll need to authorize the application to send emails on your behalf.")
    
    recipient = input("\nEnter your email address to receive the test email: ")
    
    # Create test email content
    subject = "Legal Solver - OAuth Email Test"
    html_content = """
    <html>
    <body>
        <h2>Gmail OAuth Test</h2>
        <p>This is a test email from the Legal Solver application using OAuth authentication.</p>
        <p>If you're receiving this email, your Gmail OAuth setup is working correctly!</p>
        <p>You can now use the Legal Solver application with secure email notifications.</p>
    </body>
    </html>
    """
    
    print("\nAttempting to send test email...")
    print("A browser window will open for authentication if needed.")
    
    # Send the test email
    success = send_email_oauth(recipient, subject, html_content)
    
    if success:
        print("\n✅ SUCCESS: Test email sent successfully!")
        print(f"Please check {recipient} for the test email.")
        print("Your Gmail OAuth setup is working correctly.")
        return True
    else:
        print("\n❌ ERROR: Failed to send test email.")
        print("Please check the error messages above for more information.")
        return False

if __name__ == "__main__":
    test_oauth_email() 