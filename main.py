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
        
        # 뉴스 수집
        articles = fetch_news(
            limit=10,
            keyword_filter=["우크라이나", "중국", "미국", "일본", "러시아"]
        )
        
        if not articles:
            logging.error("뉴스를 가져오는데 실패했습니다")
            return

        # 기사 처리 및 요약
        summarized_articles = process_articles(articles)
        
        if not summarized_articles:
            logging.error("처리된 기사가 없습니다")
            return

        # PDF 생성
        pdf_filename = f"news_summary_{datetime.now().strftime('%Y%m%d')}.pdf"
        create_news_pdf(summarized_articles, pdf_filename)

        # 이메일 전송
        recipient = os.getenv("EMAIL_USERNAME")
        if not recipient:
            logging.error("이메일 수신자가 설정되지 않았습니다")
            return

        send_email(
            recipient=recipient,
            subject=f"일일 세계 뉴스 요약 ({datetime.now().strftime('%Y-%m-%d')})",
            body="안녕하세요,\n\n오늘의 세계 뉴스 요약을 첨부파일로 보내드립니다.\n\n감사합니다.",
            attachment=pdf_filename
        )
        
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

