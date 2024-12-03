from modules.fetch_news import fetch_news
from modules.summarize import summarize_news
from modules.create_pdf import create_pdf
from modules.send_email import send_email
import schedule
import time

def job():
    print("Fetching news...")
    articles = fetch_news()
    print("Summarizing news...")
    summarized_articles = summarize_news(articles)
    print("Creating PDF...")
    create_pdf(summarized_articles)
    print("Sending email...")
    send_email(
        recipient="recipient_email@gmail.com",
        subject="Daily News Summary",
        body="Please find attached the daily news summary.",
        attachment="news_summary.pdf"
    )
    print("Job completed!")

# 스케줄 설정
schedule.every().day.at("08:00").do(job)

print("Scheduler is running...")
while True:
    schedule.run_pending()
    time.sleep(1)
