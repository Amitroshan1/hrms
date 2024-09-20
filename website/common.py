from flask import flash, current_app
from flask_mail import Message,Mail



def verify_password_and_send_email(user, form_password, subject, body, recipient_email, cc_emails=None):
    if form_password:
        try:
            print(user.email,form_password)
            current_app.config.update(
                MAIL_USERNAME=user.email,
                MAIL_PASSWORD=form_password,
                MAIL_DEFAULT_SENDER=user.email
            )

            mail = Mail(current_app)

            print(cc_emails,type(cc_emails))
            msg = Message(subject, recipients=[recipient_email], body=body)

            
            if cc_emails and type(cc_emails)!=list:
                print('yes')
                if isinstance(cc_emails, str):
                    cc_emails = [cc_emails]  
                msg.cc = cc_emails
            else:
                print('no',cc_emails,type(cc_emails))
                msg.cc = cc_emails

            mail.send(msg)
            return True
        except Exception as e:
            flash(f"Error sending email: {str(e)}", 'error')
            return False
    else:
        flash('Incorrect password. Please try again.', 'error')
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

