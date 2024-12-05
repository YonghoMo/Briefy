# 필요한 라이브러리 임포트
import os                  # 환경 변수 및 파일 시스템 작업용
import time               # 시간 지연 및 스케줄링 관련 기능용
import schedule          # 정기적인 작업 스케줄링을 위한 라이브러리
import logging           # 로그 기록을 위한 라이브러리
from datetime import datetime  # 날짜 및 시간 처리용

# 사용자 정의 모듈 임포트
from modules.fetch_news import fetch_news           # 뉴스 데이터 수집 모듈
from modules.fetch_article import fetch_article     # 개별 기사 내용 수집 모듈
from modules.summarize import summarize_article     # 기사 요약 모듈
from modules.create_pdf import create_news_pdf      # PDF 생성 모듈
from modules.send_email import send_email          # 이메일 전송 모듈

# 로깅 설정
# level=logging.INFO: 정보성 메시지부터 기록
# format: 로그 메시지의 형식 지정 (시간 - 로그레벨 - 메시지)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # 콘솔에 로그 출력
)

def process_articles(articles):
    """
    수집된 뉴스 기사들을 처리하고 요약하는 함수
    
    Args:
        articles (list): 처리할 뉴스 기사 목록
        
    Returns:
        list: 요약된 기사 정보를 담은 딕셔너리 리스트
    """
    summarized_articles = []
    
    for article in articles:
        try:
            logging.info(f"처리 중인 기사: {article['title']}")
            
            # 기사 본문 수집
            content = fetch_article(article['link'])
            if not content:
                logging.warning(f"기사 내용을 가져올 수 없음: {article['title']}")
                continue

            # 기사 요약 생성
            summary = summarize_article(content)
            if not summary:
                logging.warning(f"기사 요약 실패: {article['title']}")
                continue

            # 요약된 기사 정보 저장
            summarized_articles.append({
                "title": article["title"],
                "summary": summary,
                "link": article["link"],
                "press": article.get("press", "Unknown"),  # 언론사 정보가 없을 경우 "Unknown" 사용
                "category": article.get("category", "세계"),  # 카테고리 정보가 없을 경우 "세계" 사용
                "timestamp": article.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            })
            
            time.sleep(1)  # API 요청 제한을 피하기 위한 지연
            
        except Exception as e:
            logging.error(f"기사 처리 중 오류 발생: {e}")
            continue

    return summarized_articles

def job():
    """
    일일 뉴스 요약 작업을 실행하는 메인 함수
    - 뉴스 수집
    - 기사 요약
    - PDF 생성
    - 이메일 전송
    을 순차적으로 수행
    """
    try:
        logging.info("일일 뉴스 요약 작업 시작")
        
        # 환경 변수에서 이메일 수신자 정보 가져오기
        recipient = os.getenv("EMAIL_USERNAME")
        if not recipient:
            logging.error("이메일 수신자가 설정되지 않았습니다")
            return
            
        # 현재 날짜 문자열 생성 (YYYYMMDD 형식)
        today = datetime.now().strftime("%Y%m%d")
        
        # 최대 10개의 뉴스 기사 수집
        articles = fetch_news(limit=10)
        if not articles:
            logging.error("뉴스를 가져올 수 없습니다")
            return
            
        # 수집된 기사 처리 및 요약
        summarized = process_articles(articles)
        if not summarized:
            logging.error("뉴스 요약을 생성할 수 없습니다")
            return
            
        # PDF 파일명 생성
        pdf_filename = f"news_summary_{today}.pdf"
        
        # 요약된 뉴스로 PDF 생성
        if not create_news_pdf(summarized, today):
            logging.error("PDF를 생성할 수 없습니다")
            return
            
        # 이메일 전목과 본문 설정
        subject = f"{today} 세계 뉴스 요약"
        body = "안녕하세요,\n\n오늘의 세계 뉴스 요약을 보내드립니다.\n자세한 내용은 첨부된 PDF를 확인해 주세요."
        
        # 이메일 전송
        if not send_email(recipient, subject, body, pdf_filename):
            logging.error("이메일 전송에 실패했습니다")
            return
            
        logging.info("일일 뉴스 요약 작업 완료")
        
    except Exception as e:
        logging.error(f"작업 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    # 필수 환경 변수 존재 여부 확인
    required_env_vars = ["EMAIL_USERNAME", "EMAIL_PASSWORD"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logging.error(f"필수 환경 변수가 설정되지 않음: {', '.join(missing_vars)}")
        exit(1)

    # 프로그램 시작 시 즉시 작업 실행
    job()
    
    # 매일 오전 8시에 실행되도록 스케줄 설정
    schedule.every().day.at("08:00").do(job)
    
    # 스케줄러 무한 루프 실행
    logging.info("스케줄러 실행 중...")
    while True:
        schedule.run_pending()  # 예약된 작업 실행
        time.sleep(60)  # 1분마다 스케줄 확인

