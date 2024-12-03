import requests
from bs4 import BeautifulSoup
from transformers import pipeline

def fetch_article(link):
    """
    Fetches the main content of a news article given its link and summarizes it to 3 sentences.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, "html.parser")

        # 본문 내용 추출
        article = soup.select_one("article#dic_area")
        if not article:
            print("No article content found.")
            return "No Content Available"

        paragraphs = article.find_all(["p", "div"], recursive=True)
        content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        # 본문 내용이 짧으면 요약하지 않음
        sentence_count = len(content.split("."))
        if sentence_count <= 3:
            return content  # 3문장 이하면 그대로 반환

        # 긴 기사 내용 요약 (최대 3문장)
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(content, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    except requests.RequestException as e:
        print(f"Failed to fetch article content: {e}")
        return "No Content Available"
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return "Error summarizing this article."
