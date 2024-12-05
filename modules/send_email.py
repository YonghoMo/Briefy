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
    """
    이메일을 전송하는 함수
    
    Args:
        recipient (str): 수신자 이메일 주소
        subject (str): 이메일 제목
        body (str): 이메일 본문
        attachment (Optional[str]): 첨부 파일 경로 (선택사항)
        
    Returns:
        bool: 이메일 전송 성공 시 True, 실패 시 False
        
    Note:
        - Gmail SMTP를 사용하여 이메일 전송
        - 환경 변수에서 발신자 이메일과 비밀번호를 가져옴
        - 첨부 파일이 있는 경우 절대 경로로 변환하여 첨부
        - 오류 발생 시 자세한 로그 기록
    """
    try:
        sender = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")

        if not all([sender, password]):
            raise ValueError("이메일 설정이 올바르지 않습니다.")

        yag = yagmail.SMTP(sender, password)
        
        contents = [body]
        if attachment and os.path.exists(attachment):
            full_path = os.path.abspath(attachment)
            contents.append(full_path)
            logging.info(f"첨부파일 추가: {full_path}")
        else:
            logging.warning(f"첨부파일을 찾을 수 없음: {attachment}")

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
