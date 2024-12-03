from transformers import pipeline

def summarize_news(articles):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    for article in articles:
        summary = summarizer(article["title"], max_length=50, min_length=10, do_sample=False)
        article["summary"] = summary[0]["summary_text"]
    return articles
