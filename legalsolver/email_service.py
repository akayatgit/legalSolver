import os
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from db_connection import get_user_by_id

# Email configuration - Use hardcoded values for Hostinger
SENDER_EMAIL = "notification@agentsdistrict.com"
SENDER_PASSWORD = "LegalSolver@123"
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465

# For testing purposes, you can set these directly if environment variables are not available
# But in production, always use environment variables
# if SENDER_PASSWORD == "your_password":
#     print("WARNING: Using default email password. Set EMAIL_PASSWORD environment variable for security.")

def load_department_emails():
    """Load department email IDs from JSON file"""
    try:
        with open("department_emails.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Department emails file not found")
        # Create default department emails file
        default_departments = [
            {"department": "Women Protection Cell", "email": "wpc@example.com"},
            {"department": "Cyber Crime", "email": "cybercrime@example.com"},
            {"department": "Anti-Corruption Bureau", "email": "acb@example.com"},
            {"department": "Narcotics Control Bureau", "email": "ncb@example.com"}
        ]
        with open("department_emails.json", "w", encoding="utf-8") as file:
            json.dump(default_departments, file, indent=4)
        print("Created default department_emails.json file")
        return default_departments

def get_department_email(department_name):
    """Get email ID for a specific department"""
    departments = load_department_emails()
    for dept in departments:
        if dept["department"] == department_name:
            return dept["email"]
    return None

def send_email(recipient_email, subject, body, attachment_path=None):
    """Send email with optional attachment"""
    # Check if email credentials are set
    # if SENDER_PASSWORD == "your_password":
    #     print("ERROR: Default email password is being used. Set EMAIL_PASSWORD environment variable.")
    #     return False
        
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient_email
    message["Subject"] = subject
    
    # Attach body text
    message.attach(MIMEText(body, "html"))
    
    # Attach file if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as file:
            attachment = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
            attachment["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            message.attach(attachment)
    
    # Create secure SSL context
    context = ssl.create_default_context()
    
    try:
        # Connect to SMTP server
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
            print(f"Email sent successfully to {recipient_email}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Email authentication failed. Check your email and password.")
        return False
    except smtplib.SMTPException as e:
        print(f"ERROR: SMTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error sending email: {e}")
        return False

def create_department_email_body(user_name, document_name, analysis_results, department):
    """Create email body for department notification"""
    relevant_sections = [section for section in analysis_results if section.get("department") == department]
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .container {{ padding: 20px; }}
            .header {{ background-color: #4b6cb7; color: white; padding: 10px; text-align: center; }}
            .section {{ margin-bottom: 20px; border-left: 4px solid #4b6cb7; padding-left: 15px; }}
            .footer {{ font-size: 12px; color: #666; margin-top: 30px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>New Legal Document Requiring Attention</h2>
            </div>
            
            <p>Dear {department} Department,</p>
            
            <p>A new document has been submitted by <b>{user_name}</b> that requires your attention. The document has been analyzed and found to contain content related to IPC sections under your department's jurisdiction.</p>
            
            <h3>Document Details:</h3>
            <p><b>Document Name:</b> {document_name}</p>
            
            <h3>Relevant IPC Sections:</h3>
    """
    
    for section in relevant_sections:
        html += f"""
            <div class="section">
                <p><b>Section {section.get('section')}</b> - Priority: {section.get('priority')}</p>
                <p>{section.get('description', {}).get('en', '')}</p>
                <p><b>Suggested Action:</b> {section.get('suggestion', '')}</p>
            </div>
        """
    
    html += f"""
            <p>Please review the attached document and take appropriate action as per the guidelines.</p>
            
            <p>Regards,<br>Legal Solver System</p>
            
            <div class="footer">
                <p>This is an automated email from the Legal Solver System. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def create_user_acknowledgment_email(user_name, document_name, departments):
    """Create email body for user acknowledgment"""
    departments_str = ", ".join(departments)
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .container {{ padding: 20px; }}
            .header {{ background-color: #4b6cb7; color: white; padding: 10px; text-align: center; }}
            .content {{ margin: 20px 0; }}
            .footer {{ font-size: 12px; color: #666; margin-top: 30px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Document Submission Acknowledgment</h2>
            </div>
            
            <div class="content">
                <p>Dear {user_name},</p>
                
                <p>Thank you for submitting your document <b>"{document_name}"</b> to the Legal Solver System.</p>
                
                <p>We are pleased to inform you that your document has been successfully analyzed and forwarded to the following department(s) for further action:</p>
                
                <ul>
                    <li><b>{departments_str}</b></li>
                </ul>
                
                <p>The concerned department(s) will review your document and take appropriate action as per the guidelines. You may be contacted for further information if required.</p>
                
                <p>Please keep this email for your reference.</p>
                
                <p>Regards,<br>Legal Solver Team</p>
            </div>
            
            <div class="footer">
                <p>This is an automated email from the Legal Solver System. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_emails_for_analysis(user_id, document_name, file_path, analysis_results):
    """Send emails to relevant departments and user based on analysis results"""
    # Debug information
    print(f"Starting email process for document: {document_name}")
    print(f"Analysis results type: {type(analysis_results)}")
    
    # Ensure analysis_results is a list (handle both JSON strings and objects)
    if isinstance(analysis_results, str):
        try:
            print("Parsing JSON string analysis results")
            analysis_results = json.loads(analysis_results)
            print(f"Parsed analysis results: {analysis_results}")
        except json.JSONDecodeError as e:
            print(f"Error parsing analysis results JSON: {e}")
            return False, []
    
    # Get unique departments from analysis results
    departments = set(section.get("department") for section in analysis_results if section.get("department"))
    print(f"Detected departments: {departments}")
    
    # Get user information
    user = get_user_by_id(user_id)
    if not user:
        print(f"User with ID {user_id} not found")
        return False, []
    
    user_name = user.get("full_name") or user.get("name") or user.get("username")
    user_email = user.get("email")
    print(f"User: {user_name}, Email: {user_email}")
    
    sent_departments = []
    
    # Send emails to departments
    for department in departments:
        print(f"Processing department: {department}")
        dept_email = get_department_email(department)
        print(f"Department email: {dept_email}")
        
        if dept_email:
            email_body = create_department_email_body(user_name, document_name, analysis_results, department)
            subject = f"Legal Document Requiring {department} Attention - {document_name}"
            
            try:
                print(f"Sending email to {department} at {dept_email}")
                success = send_email(dept_email, subject, email_body, file_path)
                print(f"Email sending result: {success}")
                
                if success:
                    sent_departments.append(department)
                    print(f"Successfully sent email to {department}")
                else:
                    print(f"Failed to send email to {department}")
            except Exception as e:
                print(f"Error sending email to {department}: {e}")
    
    # Send acknowledgment email to user if they have an email address
    if user_email and sent_departments:
        try:
            print(f"Sending acknowledgment email to user at {user_email}")
            ack_email_body = create_user_acknowledgment_email(user_name, document_name, sent_departments)
            subject = f"Document Submission Acknowledgment - {document_name}"
            send_email(user_email, subject, ack_email_body)
        except Exception as e:
            print(f"Error sending acknowledgment email to user: {e}")
    
    print(f"Email process completed. Sent to departments: {sent_departments}")
    return bool(sent_departments), sent_departments 