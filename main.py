from modules.fetch_news import fetch_news
from modules.fetch_article import fetch_article
from modules.summarize import summarize_article
from modules.create_pdf import create_pdf
from modules.send_email import send_email
import schedule
import time

def job():
    print("Fetching news titles and links...")
    articles = fetch_news()  # 뉴스 제목과 링크 가져오기

    summarized_articles = []  # 요약된 기사를 저장할 리스트
    for article in articles:
        print(f"Fetching content for: {article['title']}")
        content = fetch_article(article['link'])  # 기사 본문 가져오기

        # 본문 내용이 없는 경우 처리
        if content == "No Content Available":
            summarized_articles.append({
                "title": article["title"],
                "summary": "No content available to summarize.",
                "link": article["link"]
            })
            continue

        print(f"Summarizing content for: {article['title']}")
        summary = summarize_article(content)  # 기사 요약하기
        summarized_articles.append({
            "title": article["title"],
            "summary": summary,
            "link": article["link"]
        })

    print("Creating PDF...")
    create_pdf(summarized_articles)  # PDF 생성

    print("Sending email...")
    send_email(
        # 본인의 이메일을 입력하세요.
        recipient="ahdydgh123@gmail.com",
        subject="Daily News Summary",
        body="Please find attached the daily news summary.",
        attachment="news_summary.pdf"
    )
    print("Job completed!")

# Immediate execution for testing
job()

# Scheduler for daily execution
schedule.every().day.at("08:00").do(job)

print("Scheduler is running...")
while True:
    schedule.run_pending()
    time.sleep(1)
