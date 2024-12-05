import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional
import re

def fetch_article(url: str) -> Optional[str]:
    """
    네이버 뉴스 기사의 본문 내용을 추출하는 함수
    
    Args:
        url (str): 네이버 뉴스 기사의 URL
        
    Returns:
        Optional[str]: 성공 시 기사 본문 텍스트, 실패 시 None
        
    Note:
        - 다양한 네이버 뉴스 페이지 레이아웃에 대응
        - 불필요한 요소(기자 정보, 저작권 등)를 제거
        - 텍스트 정리(공백 정리, 앞뒤 공백 제거)
        - 너무 짧은 본문은 오류로 처리
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 네이버 뉴스 본문 선택자 업데이트
        content_selectors = [
            "#dic_area",                # 일반 기사
            "#articeBody",              # 스포츠 기사
            "#newsEndContents",         # 연예 기사
            "#article_body",            # 일부 기사
            "#newsct_article"           # 새로운 형식
        ]
        
        content = None
        for selector in content_selectors:
            content_tag = soup.select_one(selector)
            if content_tag:
                # 불필요한 요소 제거
                for tag in content_tag.select(".reporter_area, .copyright, .link_news, script, style"):
                    tag.decompose()
                    
                content = content_tag.get_text(strip=True)
                break
                
        if not content:
            logging.error(f"기사 본문을 찾을 수 없습니다: {url}")
            return None
            
        # 텍스트 정리
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        if len(content) < 100:
            logging.warning(f"기사 본문이 너무 짧습니다: {url}")
            return None
            
        logging.debug(f"기사 본문 추출 성공 (길이: {len(content)}자)")
        return content
        
    except Exception as e:
        logging.error(f"기사 가져오기 실패: {url} - {e}")
        return None
