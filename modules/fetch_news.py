import requests
from bs4 import BeautifulSoup

def fetch_news():
    URL = "https://news.naver.com/section/105"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        for item in soup.select("a.sa_text_title"):
            title = " ".join([tag.text.strip() for tag in item.select("strong")])
            if not title:
                title = "No Title"

            link = item.get("href", "")
            if link and not link.startswith("http"):
                link = f"{link}"
            elif not link:
                link = "No Link"

            articles.append({"title": title, "link": link})

        return articles
    except requests.RequestException as e:
        print(f"Failed to fetch news: {e}")
        return []
