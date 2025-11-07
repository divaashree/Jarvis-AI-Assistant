# engine/helpers/email_helper.py

import smtplib
from engine.config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email_directly(recipient, subject, body):
    """Sends an email directly from the backend using SMTP."""
    
    # Check if credentials are set
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return "Email credentials are not set up in the config file."

    try:
        # Format the message
        message = f"Subject: {subject}\n\n{body}"

        # Connect and send (using a 'with' statement handles closing the connection)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, message.encode('utf-8'))
        
        return f"Email sent successfully to {recipient}."

    except Exception as e:
        print(f"Email sending failed: {e}")
        return "Sorry, I couldn't send the email. Please check the terminal for errors."