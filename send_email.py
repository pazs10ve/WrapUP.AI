import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import base64

load_dotenv()

def send_summary_email(to_email, summary_text, summary_file_path):
    """
    Sends the meeting summary using the Brevo API.
    """
    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')

    if not configuration.api_key['api-key']:
        raise ValueError("BREVO_API_KEY environment variable not set.")

    # Create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Read and encode the attachment
    try:
        with open(summary_file_path, 'rb') as f:
            attachment_content = base64.b64encode(f.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Attachment file not found at {summary_file_path}")
        return None

    # Define email parameters
    sender = {"name": "WrapUp.AI", "email": "summary@wrapup.ai"}
    to = [{"email": to_email}]
    subject = "Your Meeting Summary from WrapUp.AI"
    html_content = f"""\
    <html>
        <body>
            <h2>Here is your meeting summary:</h2>
            <pre style='font-family: monospace; white-space: pre-wrap; padding: 10px; border: 1px solid #eee; background-color: #f9f9f9;'>{summary_text}</pre>
            <p>The full summary is also attached to this email.</p>
            <p>Thank you for using WrapUp.AI!</p>
        </body>
    </html>
    """
    attachment = [{
        "content": attachment_content,
        "name": os.path.basename(summary_file_path)
    }]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content,
        attachment=attachment
    )

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Successfully sent email via Brevo.")
        print(api_response)
        return api_response
    except ApiException as e:
        print(f"Exception when calling TransactionalEmailsApi->send_transac_email: {e}")
        return None

