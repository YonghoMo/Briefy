import os
import time
import schedule
import logging
from datetime import datetime
from modules.fetch_news import fetch_news
from modules.fetch_article import fetch_article
from modules.summarize import summarize_article
from modules.create_pdf import create_news_pdf
from modules.send_email import send_email

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def process_articles(articles):
    """기사 처리 및 요약"""
    summarized_articles = []
    
    for article in articles:
        try:
            logging.info(f"처리 중인 기사: {article['title']}")
            
            content = fetch_article(article['link'])
            if not content:
                logging.warning(f"기사 내용을 가져올 수 없음: {article['title']}")
                continue

            summary = summarize_article(content)
            if not summary:
                logging.warning(f"기사 요약 실패: {article['title']}")
                continue

            summarized_articles.append({
                "title": article["title"],
                "summary": summary,
                "link": article["link"],
                "press": article.get("press", "Unknown"),
                "category": article.get("category", "세계"),
                "timestamp": article.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            })
            
            time.sleep(1)  # API 요청 제한 방지
            
        except Exception as e:
            logging.error(f"기사 처리 중 오류 발생: {e}")
            continue

    return summarized_articles

def job():
    """메인 작업 실행"""
    try:
        logging.info("일일 뉴스 요약 작업 시작")
        
        # 수신자 이메일 가져오기
        recipient = os.getenv("EMAIL_USERNAME")
        if not recipient:
            logging.error("이메일 수신자가 설정되지 않았습니다")
            return
            
        # 오늘 날짜
        today = datetime.now().strftime("%Y%m%d")
        
        # 뉴스 수집 및 처리
        articles = fetch_news(limit=10)
        if not articles:
            logging.error("뉴스를 가져올 수 없습니다")
            return
            
        summarized = process_articles(articles)
        if not summarized:
            logging.error("뉴스 요약을 생성할 수 없습니다")
            return
            
        # PDF 파일명 통일
        pdf_filename = f"news_summary_{today}.pdf"
        
        # PDF 생성
        if not create_news_pdf(summarized, today):
            logging.error("PDF를 생성할 수 없습니다")
            return
            
        # 이메일 전송
        subject = f"{today} 세계 뉴스 요약"
        body = "안녕하세요,\n\n오늘의 세계 뉴스 요약을 보내드립니다.\n자세한 내용은 첨부된 PDF를 확인해 주세요."
        
        if not send_email(recipient, subject, body, pdf_filename):
            logging.error("이메일 전송에 실패했습니다")
            return
            
        logging.info("일일 뉴스 요약 작업 완료")
        
    except Exception as e:
        logging.error(f"작업 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    # 환경 변수 확인
    required_env_vars = ["EMAIL_USERNAME", "EMAIL_PASSWORD"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logging.error(f"필수 환경 변수가 설정되지 않음: {', '.join(missing_vars)}")
        exit(1)

    # 즉시 실행
    job()
    # 스케줄러 설정 (매일 오전 8시)
    schedule.every().day.at("08:00").do(job)
    
    logging.info("스케줄러 실행 중...")
    while True:
        schedule.run_pending()
        time.sleep(60)

