from fpdf import FPDF
import logging
import os
from typing import List, Dict, Optional
from datetime import datetime

class NewsPDF(FPDF):
    """
    뉴스 요약을 위한 사용자 정의 PDF 클래스
    FPDF를 상속받아 한글 폰트 지원과 헤더/푸터를 구현
    """
    
    def __init__(self):
        """
        PDF 클래스 초기화
        부모 클래스 초기화 및 폰트 설정 수행
        """
        super().__init__()
        self._check_fonts()
        
    def _check_fonts(self):
        """
        한글 폰트 파일 존재 여부 확인 및 폰트 초기화
        
        Raises:
            FileNotFoundError: 필요한 폰트 파일이 없는 경우
        """
        # fonts 디렉토리가 없으면 생성
        if not os.path.exists('fonts'):
            os.makedirs('fonts')
            
        # 필요한 폰트 파일 목록
        font_files = {
            'regular': 'malgun.ttf',     # 기본 맑은 고딕
            'bold': 'malgunbd.ttf'       # 굵은 맑은 고딕
        }
        
        # 폰트 파일 존재 여부 확인
        for font_type, font_file in font_files.items():
            font_path = os.path.join('fonts', font_file)
            if not os.path.exists(font_path):
                raise FileNotFoundError(f"폰트 파일이 없습니다: {font_path}")
                
        # PDF에 폰트 추가 (유니코드 지원 활성화)
        self.add_font('Malgun', '', os.path.join('fonts', 'malgun.ttf'), uni=True)
        self.add_font('Malgun', 'B', os.path.join('fonts', 'malgunbd.ttf'), uni=True)
        
    def header(self):
        """
        PDF 문서의 모든 페이지 상단에 표시될 헤더 정의
        """
        self.set_font('Malgun', '', 8)
        self.cell(0, 10, '일일 세계 뉴스 요약', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        """
        PDF 문서의 모든 페이지 하단에 표시될 푸터 정의
        페이지 번호를 포함
        """
        self.set_y(-15)  # 페이지 하단에서 15mm 위치
        self.set_font('Malgun', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_news_pdf(articles: List[Dict], date: str) -> Optional[str]:
    """
    뉴스 기사 목록을 PDF 문서로 생성하는 함수
    
    Args:
        articles (List[Dict]): 뉴스 기사 정보를 담은 딕셔너리 리스트
            각 딕셔너리는 다음 키를 포함:
            - title: 기사 제목
            - press: 언론사
            - category: 카테고리
            - timestamp: 시간
            - summary: 요약문
            - link: 원문 링크
        date (str): PDF 파일명에 포함될 날짜 문자열
        
    Returns:
        Optional[str]: 성공 시 생성된 PDF 파일명, 실패 시 None
        
    Note:
        - A4 용지 크기 사용
        - 기사별로 제목, 메타 정보, 요약문, 링크를 포함
        - 기사 사이에 구분선 추가
        - 긴 URL은 자동으로 축약
    """
    try:
        # PDF 객체 생성 및 기본 설정
        pdf = NewsPDF()
        # A4 기본 여백 설정 (좌, 우 각각 10mm)
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.add_page()
        
        # 문서 제목 추가
        pdf.set_font('Malgun', 'B', 16)
        pdf.cell(0, 10, f'{date} 세계 뉴스 요약', 0, 1, 'C')
        pdf.ln(10)
        
        # 각 기사 정보 추가
        for idx, article in enumerate(articles, 1):
            # 기사 제목 (굵은 글씨, 12pt)
            pdf.set_font('Malgun', 'B', 12)
            pdf.multi_cell(0, 10, f"{idx}. {article['title']}")
            
            # 메타 정보 (회색, 9pt)
            pdf.set_font('Malgun', '', 9)
            pdf.set_text_color(100, 100, 100)  # 회색
            meta = f"출처: {article['press']} | 카테고리: {article['category']} | 시간: {article['timestamp']}"
            effective_width = pdf.w - 20  # 좌우 여백을 제외한 유효 너비
            pdf.set_x(10)  # 시작 위치를 왼쪽 여백으로 설정
            pdf.cell(effective_width, 5, meta, 0, 1, 'L')
            pdf.ln(5)
            
            # 요약문 (검은색, 10pt)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Malgun', '', 10)
            pdf.set_x(10)
            pdf.multi_cell(0, 10, article['summary'])
            
            # 링크 (파란색, 클릭 가능)
            pdf.set_text_color(0, 0, 255)  # 파란색
            pdf.set_x(10)
            # 긴 URL 자동 축약 (80자 초과시)
            if len(article['link']) > 80:
                shortened_link = article['link'][:77] + "..."
            else:
                shortened_link = article['link']
            pdf.cell(effective_width, 5, shortened_link, 0, 1, 'L', link=article['link'])
            pdf.set_text_color(0, 0, 0)  # 색상 초기화
            
            # 구분선 추가 (마지막 기사 제외)
            if idx < len(articles):
                pdf.ln(5)
                pdf.line(10, pdf.get_y(), pdf.w - 10, pdf.get_y())
                pdf.ln(10)
        
        # PDF 파일 저장
        filename = f'news_summary_{date}.pdf'
        pdf.output(filename)
        logging.info(f"PDF 생성 완료: {filename}")
        return filename
        
    except Exception as e:
        logging.error(f"PDF 생성 실패: {e}")
        return None
