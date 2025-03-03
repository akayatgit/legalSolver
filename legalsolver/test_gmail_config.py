import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail_connection():
    """Test Gmail connection with current credentials"""
    # Get email credentials from environment variables
    sender_email = os.environ.get("EMAIL_USER", "")
    sender_password = os.environ.get("EMAIL_PASSWORD", "")
    
    # Check if credentials are set
    if not sender_email or not sender_password or sender_password == "your_app_password":
        print("\n❌ ERROR: Email credentials not properly set")
        print("Please set the EMAIL_USER and EMAIL_PASSWORD environment variables")
        print("See GMAIL_APP_PASSWORD_GUIDE.md for instructions")
        return False
    
    print(f"\n🔍 Testing connection to Gmail with account: {sender_email}")
    print("Attempting to connect to Gmail SMTP server...")
    
    # Create secure SSL context
    context = ssl.create_default_context()
    
    try:
        # Connect to SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            print("✓ Connected to Gmail SMTP server")
            print("Attempting to log in with provided credentials...")
            
            # Try to login
            server.login(sender_email, sender_password)
            print("✅ SUCCESS: Authentication successful!")
            print("Your Gmail App Password is correctly configured")
            
            # Ask if user wants to send a test email
            send_test = input("\nWould you like to send a test email to yourself? (y/n): ")
            if send_test.lower() == 'y':
                # Create test email
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = sender_email  # Send to self
                message["Subject"] = "Legal Solver - Gmail Configuration Test"
                
                # Email body
                body = """
                <html>
                <body>
                    <h2>Gmail Configuration Test</h2>
                    <p>This is a test email from the Legal Solver application.</p>
                    <p>If you're receiving this email, your Gmail App Password is correctly configured!</p>
                    <p>You can now use the Legal Solver application with email notifications.</p>
                </body>
                </html>
                """
                message.attach(MIMEText(body, "html"))
                
                # Send email
                print(f"Sending test email to {sender_email}...")
                server.sendmail(sender_email, sender_email, message.as_string())
                print("✅ Test email sent successfully!")
            
            return True
            
    except smtplib.SMTPAuthenticationError:
        print("❌ ERROR: Authentication failed")
        print("\nPossible reasons:")
        print("1. You're using your regular Gmail password instead of an App Password")
        print("2. The App Password is incorrect or has been revoked")
        print("3. The Gmail account email address is incorrect")
        print("\nPlease check GMAIL_APP_PASSWORD_GUIDE.md for instructions on setting up an App Password")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("LEGAL SOLVER - GMAIL APP PASSWORD CONFIGURATION TEST")
    print("=" * 60)
    
    success = test_gmail_connection()
    
    if not success:
        print("\nFor detailed instructions on setting up Gmail App Password:")
        print("1. Read the GMAIL_APP_PASSWORD_GUIDE.md file")
        print("2. Visit https://myaccount.google.com/apppasswords to generate an App Password")
        
    print("\nTest completed.") 