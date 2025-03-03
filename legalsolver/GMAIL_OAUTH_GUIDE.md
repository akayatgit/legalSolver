# Setting Up Gmail OAuth Authentication for Legal Solver

This guide will help you set up Gmail OAuth authentication for the Legal Solver application. OAuth is a more secure way to authenticate with Gmail and doesn't require App Passwords, even if you have 2-Factor Authentication (2FA) enabled.

## Why OAuth is Better Than App Passwords

- Works with all Google account types, including those with restrictions
- More secure than password-based authentication
- No need to create or manage App Passwords
- Provides a familiar Google sign-in experience
- Gives you control over what permissions you grant to the application

## Prerequisites

Before you begin, make sure you have:

1. A Google account
2. Python 3.6 or higher
3. The following Python packages installed:
   ```
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter "Legal Solver" as the project name
5. Click "Create"
6. Wait for the project to be created, then select it from the project dropdown

## Step 2: Enable the Gmail API

1. In the Google Cloud Console, navigate to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click on "Gmail API" in the results
4. Click "Enable"

## Step 3: Configure OAuth Consent Screen

1. In the Google Cloud Console, navigate to "APIs & Services" > "OAuth consent screen"
2. Select "External" as the user type (unless you have a Google Workspace account)
3. Click "Create"
4. Fill in the required information:
   - App name: "Legal Solver"
   - User support email: Your email address
   - Developer contact information: Your email address
5. Click "Save and Continue"
6. On the "Scopes" page, click "Add or Remove Scopes"
7. Add the scope: `https://www.googleapis.com/auth/gmail.send`
8. Click "Save and Continue"
9. On the "Test users" page, click "Add Users"
10. Add your email address as a test user
11. Click "Save and Continue"
12. Review your settings and click "Back to Dashboard"

## Step 4: Create OAuth Client ID

1. In the Google Cloud Console, navigate to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Desktop app" as the application type
4. Name it "Legal Solver Desktop"
5. Click "Create"
6. Click "Download JSON" to download your credentials
7. Rename the downloaded file to `credentials.json`
8. Move the `credentials.json` file to the `legalsolver` directory

## Step 5: Test the OAuth Setup

1. Run the test script:
   ```
   python test_oauth.py
   ```
2. A browser window will open asking you to sign in to your Google account
3. Sign in and grant the requested permissions
4. The script will send a test email to verify the setup

## Step 6: Using OAuth in the Application

Once you've completed the setup, the Legal Solver application will automatically use OAuth authentication for sending emails. The first time you run the application, it will open a browser window for authentication. After that, your credentials will be saved in a `token.pickle` file and reused.

## Troubleshooting

### "Invalid Client" Error

If you see an "invalid_client" error, make sure:
- You've downloaded the correct credentials.json file
- You've placed the credentials.json file in the legalsolver directory
- You've enabled the Gmail API for your project

### "Access Not Configured" Error

If you see an "Access Not Configured" error, make sure:
- You've enabled the Gmail API for your project
- You've waited a few minutes after enabling the API (it can take time to propagate)

### "Invalid Grant" Error

If you see an "invalid_grant" error:
- Delete the token.pickle file if it exists
- Run the test script again to generate a new token

### Other Issues

If you encounter other issues:
1. Check the Google Cloud Console for any error messages
2. Make sure you've added yourself as a test user in the OAuth consent screen
3. Try running the setup process again from the beginning 