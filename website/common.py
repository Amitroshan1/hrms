from flask import flash, current_app
from flask_mail import Message,Mail
import requests
from .auth import refresh_access_token




def verify_oauth2_and_send_email(user, subject, body, recipient_email, cc_emails=None):
    try:
        access_token = refresh_access_token(user)  # Function to get a valid OAuth2 token

        if not access_token:
            flash("Failed to authenticate with Microsoft. Please re-login.", 'error')
            return False

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        email_data = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": body
                },
                "toRecipients": [{"emailAddress": {"address": recipient_email}}],
                "ccRecipients": [{"emailAddress": {"address": email}} for email in (cc_emails or [])]
            },
            "saveToSentItems": "true"
        }

        response = requests.post(
            "https://graph.microsoft.com/v1.0/me/sendMail",
            headers=headers,
            json=email_data
        )

        if response.status_code == 202:
            return True
        else:
            flash(f"Error sending email: {response.json()}", 'error')
            return False

    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return False



def send_email_from_company(user_email,Passoword,subject, body, recipient_email, cc_emails=None):
    
    try:
        current_app.config.update(
                MAIL_USERNAME=user_email,
                MAIL_PASSWORD=Passoword,
                MAIL_DEFAULT_SENDER=user_email
            )
        

        mail = Mail(current_app)

        msg=Message(subject, recipients=[recipient_email], body=body)

        if cc_emails:
                if isinstance(cc_emails, str):
                    cc_emails = [cc_emails]  
                msg.cc = cc_emails

                
        mail.send(msg)
        return True
    except Exception as e:
            flash(f"Error sending email: {str(e)}", 'error')
            return False

