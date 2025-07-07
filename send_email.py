import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

class EmailSender:
    """
    A class to handle sending emails using the Gmail API.
    """
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        """
        Initializes the EmailSender and authenticates with the Gmail API.
        """
        self.creds = self._get_credentials(credentials_path, token_path)
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _get_credentials(self, credentials_path, token_path):
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    def create_message(self, sender, to, subject, message_text):
        """
        Creates a MIME message for an email.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(self, user_id, message):
        """
        Sends the created message.
        """
        try:
            sent_message = self.service.users().messages().send(userId=user_id, body=message).execute()
            print(f"Message Id: {sent_message['id']}")
            return sent_message
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Send a meeting summary via email.")
    parser.add_argument("recipient", type=str, help="The recipient's email address.")
    parser.add_argument("summary_file", type=str, help="The path to the summary text file.")
    args = parser.parse_args()

    if not os.path.exists(args.summary_file):
        print(f"Error: Summary file not found at '{args.summary_file}'")
    else:
        try:
            with open(args.summary_file, 'r', encoding='utf-8') as f:
                summary_content = f.read()

            sender = EmailSender()
            subject = "Meeting Summary: WrapUp.AI Test"
            message = sender.create_message('me', args.recipient, subject, summary_content)
            sender.send_message('me', message)
            print(f"Email sent successfully to {args.recipient}.")

        except Exception as e:
            print(f"An error occurred: {e}")
