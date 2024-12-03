import yagmail
import os

def send_email(recipient, subject, body, attachment):
    sender = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    yag = yagmail.SMTP(sender, password)
    yag.send(to=recipient, subject=subject, contents=body, attachments=attachment)
    print(f"Email sent to {recipient}")
