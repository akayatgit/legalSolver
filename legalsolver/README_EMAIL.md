# Email Functionality in Legal Solver

This document provides information about the email functionality in the Legal Solver application.

## Overview

The Legal Solver application includes email functionality that:
1. Sends notifications to relevant departments when a document is analyzed
2. Sends acknowledgment emails to users when their documents are processed

## Email Configuration

The application is pre-configured with the following Hostinger email settings:

- Email Address: notification@agentsdistrict.com
- SMTP Server: smtp.hostinger.com
- SMTP Port: 465 (SSL)

These settings are hardcoded in the application and do not require any additional setup.

## Department Email Addresses

The application uses a JSON file to store department email addresses. The default file is created automatically if it doesn't exist, with the following departments:

- Women Protection Cell: wpc@example.com
- Cyber Crime: cybercrime@example.com
- Anti-Corruption Bureau: acb@example.com
- Narcotics Control Bureau: ncb@example.com

You should modify these email addresses to match your actual department contacts. Edit the `department_emails.json` file directly.

## Testing Email Functionality

To test if the email configuration is working correctly:

```
python test_email.py
```

This script will:
1. Test the email configuration by connecting to the SMTP server
2. Allow you to send a test email
3. Test sending emails to department addresses

## Troubleshooting

If you encounter issues with email sending:

1. **Connection Errors**
   - Check your internet connection
   - Verify that your firewall isn't blocking the connection
   - Ensure the SMTP server is accessible from your network

2. **Email Not Received**
   - Check spam/junk folders
   - Verify that the recipient email address is correct
   - Check if there are sending limits on the email account

## Email Templates

The application uses HTML email templates for:
1. Department notifications
2. User acknowledgments

These templates can be customized in the `email_service.py` file if needed.

## Security Considerations

- The email credentials are hardcoded in the application for simplicity
- In a production environment, consider implementing additional security measures
- Regularly monitor the email account for any suspicious activity 