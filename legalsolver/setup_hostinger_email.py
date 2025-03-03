import os
import sys
import getpass

def setup_hostinger_email():
    """Set up Hostinger email configuration"""
    print("\n" + "=" * 60)
    print("LEGAL SOLVER - HOSTINGER EMAIL SETUP")
    print("=" * 60)
    
    # Get email credentials
    email = input("\nEnter your Hostinger email address: ")
    password = getpass.getpass("Enter your Hostinger email password: ")
    
    # Get SMTP settings (with defaults)
    smtp_server = input("\nEnter SMTP server (default: smtp.hostinger.com): ") or "smtp.hostinger.com"
    smtp_port = input("Enter SMTP port (default: 465): ") or "465"
    
    # Set environment variables for current session
    os.environ["EMAIL_USER"] = email
    os.environ["EMAIL_PASSWORD"] = password
    os.environ["SMTP_SERVER"] = smtp_server
    os.environ["SMTP_PORT"] = smtp_port
    
    print("\nEmail configuration set for current session.")
    
    # Provide instructions for permanent setup
    print("\nTo make these settings permanent, you need to set environment variables:")
    
    if sys.platform.startswith('win'):
        # Windows instructions
        print("\nFor Windows (Command Prompt):")
        print(f'setx EMAIL_USER "{email}"')
        print(f'setx EMAIL_PASSWORD "{password}"')
        print(f'setx SMTP_SERVER "{smtp_server}"')
        print(f'setx SMTP_PORT "{smtp_port}"')
        
        print("\nFor Windows (PowerShell):")
        print(f'[Environment]::SetEnvironmentVariable("EMAIL_USER", "{email}", "User")')
        print(f'[Environment]::SetEnvironmentVariable("EMAIL_PASSWORD", "{password}", "User")')
        print(f'[Environment]::SetEnvironmentVariable("SMTP_SERVER", "{smtp_server}", "User")')
        print(f'[Environment]::SetEnvironmentVariable("SMTP_PORT", "{smtp_port}", "User")')
    else:
        # Linux/Mac instructions
        print("\nFor Linux/Mac (add to ~/.bashrc or ~/.zshrc):")
        print(f'export EMAIL_USER="{email}"')
        print(f'export EMAIL_PASSWORD="{password}"')
        print(f'export SMTP_SERVER="{smtp_server}"')
        print(f'export SMTP_PORT="{smtp_port}"')
    
    # Ask if user wants to test the configuration
    test_config = input("\nWould you like to test the email configuration now? (y/n): ")
    if test_config.lower() == 'y':
        try:
            from test_email import test_email_config
            test_email_config()
        except ImportError:
            print("Test module not found. You can test the configuration later with:")
            print("python test_email.py")
    
    print("\nSetup complete!")

if __name__ == "__main__":
    setup_hostinger_email() 