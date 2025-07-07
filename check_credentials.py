import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# The scope for sending emails. If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def verify_credentials():
    """
    Verifies the user's credentials for the Gmail API.
    Triggers the OAuth 2.0 flow if credentials are not found or expired.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Credentials have expired. Refreshing...")
            creds.refresh(Request())
        else:
            print("No valid credentials found. Starting OAuth flow...")
            if not os.path.exists("credentials.json"):
                print("Error: 'credentials.json' not found. Please download it from the Google Cloud Console.")
                return
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            print("'token.json' created successfully.")

    if creds and creds.valid:
        print("\nCredentials verified successfully!")
        print("Ready to send emails.")
    else:
        print("\nFailed to verify credentials.")

if __name__ == "__main__":
    verify_credentials()
