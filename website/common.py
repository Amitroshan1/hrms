from flask import flash, current_app
from flask_mail import Message,Mail
 

def verify_password_and_send_email(user, form_password, subject, body, recipient_email):
    
    
    if form_password:
        try:
            print(type(user.email),type(form_password))
            
            current_app.config.update(
                MAIL_USERNAME=user.email,
                MAIL_PASSWORD=form_password,
                MAIL_DEFAULT_SENDER=user.email
            )


            mail = Mail(current_app)

            print(subject,recipient_email,body)
            msg = Message(subject, recipients=[recipient_email], body=body)
            mail.send(msg)
            return True
        except Exception as e:
            flash(f"Error sending email: {str(e)}", 'error')
            return False
    else:
        flash('Incorrect password. Please try again.', 'error')
        return False
