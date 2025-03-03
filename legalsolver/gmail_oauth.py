import os
import pickle
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import webbrowser
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the token.pickle file
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Get an authorized Gmail API service instance."""
    creds = None
    # Token file stores the user's access and refresh tokens
    token_path = Path('token.pickle')
    
    # Check if token file exists
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Check if credentials.json exists
            if not Path('credentials.json').exists():
                print("ERROR: credentials.json file not found!")
                print("Please follow the setup instructions in the README to create OAuth credentials.")
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error building Gmail service: {e}")
        return None

def create_message(sender, to, subject, html_content, attachment_path=None):
    """Create a message for an email."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    # Attach HTML content
    msg = MIMEText(html_content, 'html')
    message.attach(msg)
    
    # Attach file if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as file:
            attachment = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
            attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            message.attach(attachment)
    
    # Encode message
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent! Message ID: {message['id']}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def send_email_oauth(to, subject, html_content, attachment_path=None):
    """Send email using Gmail OAuth authentication."""
    service = get_gmail_service()
    if not service:
        print("Failed to get Gmail service. Authentication may have failed.")
        return False
    
    try:
        # Get user's email from the service
        profile = service.users().getProfile(userId='me').execute()
        sender_email = profile['emailAddress']
        
        # Create and send message
        message = create_message(sender_email, to, subject, html_content, attachment_path)
        return send_message(service, 'me', message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def setup_oauth_credentials():
    """Guide the user through setting up OAuth credentials."""
    print("\n" + "=" * 60)
    print("GMAIL OAUTH SETUP GUIDE")
    print("=" * 60)
    
    print("\n1. Go to the Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create a new project or select an existing one")
    print("3. Navigate to 'APIs & Services' > 'Credentials'")
    print("4. Click 'Create Credentials' > 'OAuth client ID'")
    print("5. Select 'Desktop app' as the application type")
    print("6. Name it 'Legal Solver' and click 'Create'")
    print("7. Download the JSON file")
    print("8. Rename it to 'credentials.json' and place it in the legalsolver directory")
    
    print("\nWould you like to open the Google Cloud Console now? (y/n)")
    open_browser = input().lower()
    if open_browser == 'y':
        webbrowser.open("https://console.cloud.google.com/apis/credentials")
    
    print("\nOnce you've downloaded and placed the credentials.json file,")
    print("run the test_oauth.py script to verify your setup.")

if __name__ == "__main__":
    setup_oauth_credentials() 