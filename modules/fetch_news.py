import requests
from bs4 import BeautifulSoup

def fetch_news():
    URL = "https://news.ycombinator.com/"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.select(".titleline > a"):
        title = item.text.strip()
        link = item["href"]
        articles.append({"title": title, "link": link})
    
    return articles
