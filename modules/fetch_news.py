import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
import logging
from datetime import datetime

def fetch_news(limit: int = 10, keyword_filter: Optional[List[str]] = None) -> List[Dict]:
    """뉴이버 뉴스 수집"""
    try:
        logging.info("뉴스 수집 시작")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Accept-Language": "ko-KR,ko;q=0.9"
        }
        
        response = requests.get("https://news.naver.com/section/104", headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        seen_links = set()
        
        # 디스 아이템 찾기 (HTML 구조에 맞게 수정된 선택자)
        selectors = [
            "ul.sa_list li.sa_item",                 # 메인 리스트
            "ul._SECTION_HEADLINE_LIST_CONTENT li",  # 헤드라인
            "ul._SECTION_CONTENT li"                 # 일반 기사
        ]
        
        for selector in selectors:
            items = soup.select(selector)
            logging.debug(f"선택자 '{selector}' 결과: {len(items)}개")
            
            for item in items:
                try:
                    # 제목과 링크 찾기
                    title_tag = item.select_one("a.sa_text_title strong.sa_text_strong")
                    if not title_tag:
                        continue
                        
                    title = title_tag.get_text(strip=True)
                    
                    # 링크 찾기
                    link_tag = item.select_one("a.sa_text_title")
                    if not link_tag:
                        continue
                        
                    link = link_tag.get('href', '')
                    if not link.startswith('http'):
                        link = f"https://news.naver.com{link}"
                        
                    if not title or len(title) < 5 or link in seen_links:
                        continue
                        
                    # 언론사 찾기
                    press_tag = item.select_one("div.sa_text_press")
                    press = press_tag.get_text(strip=True) if press_tag else "Unknown"
                    
                    seen_links.add(link)
                    articles.append({
                        "title": title,
                        "link": link,
                        "press": press,
                        "category": "세계",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    logging.debug(f"기사 추가됨: {title}")
                    
                    if len(articles) >= limit:
                        break
                        
                except Exception as e:
                    logging.error(f"기사 항목 처리 중 오류: {e}")
                    continue
                    
            if len(articles) >= limit:
                break
                
        if not articles:
            logging.warning("기사를 찾을 수 없습니다.")
        else:
            logging.info(f"총 {len(articles)}개의 기사 수집 완료")
            
        return articles[:limit]
        
    except Exception as e:
        logging.error(f"뉴스 수집 실패: {e}")
        return []
