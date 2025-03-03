import json
import os
from email_service import send_emails_for_analysis
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_service():
    """Test the email service functionality"""
    print("Testing email service...")
    
    # Load sample IPC sections
    try:
        with open("ipc_sections.json", "r", encoding="utf-8") as file:
            ipc_data = json.load(file)
    except FileNotFoundError:
        print("IPC sections file not found")
        return
    
    # Create sample analysis results (first 3 sections)
    sample_results = ipc_data[:3]
    
    # Sample user and document info
    user_id = 1  # Replace with an actual user ID from your database
    document_name = "Test Document.pdf"
    file_path = os.path.abspath("test_document.txt")
    
    # Create a test document if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("This is a test document for email functionality testing.")
    
    # Send test emails
    success, departments = send_emails_for_analysis(
        user_id, document_name, file_path, sample_results
    )
    
    # Print results
    if success:
        print(f"Emails sent successfully to departments: {', '.join(departments)}")
    else:
        print("Failed to send emails")

def test_email_config():
    """Test email configuration with Hostinger"""
    print("\n" + "=" * 60)
    print("LEGAL SOLVER - EMAIL CONFIGURATION TEST")
    print("=" * 60)
    
    # Use hardcoded email configuration
    sender_email = "notification@agentsdistrict.com"
    sender_password = "LegalSolver@123"
    smtp_server = "smtp.hostinger.com"
    smtp_port = 465
    
    print(f"\n🔍 Testing connection to {smtp_server} with account: {sender_email}")
    
    # Create secure SSL context
    context = ssl.create_default_context()
    
    try:
        # Connect to SMTP server
        print(f"Connecting to {smtp_server} on port {smtp_port}...")
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            print("✓ Connected to SMTP server")
            print("Attempting to log in with provided credentials...")
            
            # Try to login
            server.login(sender_email, sender_password)
            print("✅ SUCCESS: Authentication successful!")
            
            # Ask if user wants to send a test email
            recipient = input("\nEnter an email address to send a test email to: ")
            
            # Create test email
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient
            message["Subject"] = "Legal Solver - Email Configuration Test"
            
            # Email body
            body = """
            <html>
            <body>
                <h2>Email Configuration Test</h2>
                <p>This is a test email from the Legal Solver application.</p>
                <p>If you're receiving this email, your email configuration is working correctly!</p>
                <p>You can now use the Legal Solver application with email notifications.</p>
            </body>
            </html>
            """
            message.attach(MIMEText(body, "html"))
            
            # Send email
            print(f"Sending test email to {recipient}...")
            server.sendmail(sender_email, recipient, message.as_string())
            print("✅ Test email sent successfully!")
            
            return True
            
    except smtplib.SMTPAuthenticationError:
        print("❌ ERROR: Authentication failed")
        print("\nPossible reasons:")
        print("1. Incorrect email address or password")
        print("2. SMTP server settings are incorrect")
        print("3. Your email provider has security restrictions")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_department_emails():
    """Test sending emails to departments"""
    print("\n" + "=" * 60)
    print("LEGAL SOLVER - DEPARTMENT EMAIL TEST")
    print("=" * 60)
    
    try:
        from email_service import load_department_emails, send_email
        
        # Load department emails
        departments = load_department_emails()
        if not departments:
            print("❌ ERROR: No departments found in department_emails.json")
            return False
        
        print(f"Found {len(departments)} departments:")
        for dept in departments:
            print(f"- {dept['department']}: {dept['email']}")
        
        # Ask which department to test
        print("\nWhich department would you like to test?")
        for i, dept in enumerate(departments):
            print(f"{i+1}. {dept['department']}")
        
        choice = int(input("Enter number (or 0 for all): "))
        
        if choice == 0:
            test_depts = departments
        elif 1 <= choice <= len(departments):
            test_depts = [departments[choice-1]]
        else:
            print("Invalid choice")
            return False
        
        # Test sending emails
        success_count = 0
        for dept in test_depts:
            dept_name = dept["department"]
            dept_email = dept["email"]
            
            print(f"\nTesting email to {dept_name} ({dept_email})...")
            
            # Create test email
            subject = f"Legal Solver - Test Email for {dept_name}"
            body = f"""
            <html>
            <body>
                <h2>Department Email Test</h2>
                <p>This is a test email for the {dept_name} department.</p>
                <p>If you're receiving this email, the department email configuration is working correctly!</p>
            </body>
            </html>
            """
            
            # Send email
            if send_email(dept_email, subject, body):
                print(f"✅ Email sent successfully to {dept_name}")
                success_count += 1
            else:
                print(f"❌ Failed to send email to {dept_name}")
        
        if success_count == len(test_depts):
            print("\n✅ All department emails sent successfully!")
            return True
        elif success_count > 0:
            print(f"\n⚠️ {success_count} out of {len(test_depts)} department emails sent successfully")
            return True
        else:
            print("\n❌ Failed to send any department emails")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("Which test would you like to run?")
    print("1. Test email configuration")
    print("2. Test department emails")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        test_email_config()
    elif choice == "2":
        test_department_emails()
    else:
        print("Invalid choice") 