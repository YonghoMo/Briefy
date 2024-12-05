from dotenv import load_dotenv
import yagmail
import os
import logging
from typing import Optional

# .env 파일 강제 로드
load_dotenv()

def send_email(
    recipient: str,
    subject: str,
    body: str,
    attachment: Optional[str] = None
) -> bool:
    """이메일 전송"""
    try:
        sender = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")

        if not all([sender, password]):
            raise ValueError("이메일 설정이 올바르지 않습니다.")

        yag = yagmail.SMTP(sender, password)
        
        contents = [body]
        if attachment and os.path.exists(attachment):
            contents.append(attachment)

        yag.send(
            to=recipient,
            subject=subject,
            contents=contents
        )
        
        logging.info(f"이메일 전송 완료: {recipient}")
        return True

    except Exception as e:
        logging.error(f"이메일 전송 실패: {e}")
        return False
