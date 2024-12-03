from dotenv import load_dotenv
import yagmail
import os

# .env 파일 강제 로드
load_dotenv()

def send_email(recipient, subject, body, attachment):
    sender = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        raise ValueError(".env파일에 이메일 주소와 비밀번호가 올바르게 입력되었는지 확인하세요.")
    
    print(f"Sender: {sender}, Password: {'***' if password else 'Not Found'}")  # 디버깅용 출력

    try:
        yag = yagmail.SMTP(sender, password)
        yag.send(to=recipient, subject=subject, contents=body, attachments=attachment)
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise
