from fpdf import FPDF
import logging
import os
from typing import List, Dict, Optional
from datetime import datetime

class NewsPDF(FPDF):
    def __init__(self):
        super().__init__()
        self._check_fonts()
        
    def _check_fonts(self):
        """폰트 확인 및 초기화"""
        if not os.path.exists('fonts'):
            os.makedirs('fonts')
            
        font_files = {
            'regular': 'malgun.ttf',
            'bold': 'malgunbd.ttf'
        }
        
        for font_type, font_file in font_files.items():
            font_path = os.path.join('fonts', font_file)
            if not os.path.exists(font_path):
                raise FileNotFoundError(f"폰트 파일이 없습니다: {font_path}")
                
        self.add_font('Malgun', '', os.path.join('fonts', 'malgun.ttf'), uni=True)
        self.add_font('Malgun', 'B', os.path.join('fonts', 'malgunbd.ttf'), uni=True)
        
    def header(self):
        self.set_font('Malgun', '', 8)
        self.cell(0, 10, '일일 세계 뉴스 요약', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Malgun', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_news_pdf(articles: List[Dict], date: str) -> Optional[str]:
    """뉴스 요약 PDF 생성"""
    try:
        pdf = NewsPDF()
        # A4 기본 여백 설정 (좌, 우 각각 10mm)
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.add_page()
        
        # 제목
        pdf.set_font('Malgun', 'B', 16)
        pdf.cell(0, 10, f'{date} 세계 뉴스 요약', 0, 1, 'C')
        pdf.ln(10)
        
        # 기사들
        for idx, article in enumerate(articles, 1):
            # 제목
            pdf.set_font('Malgun', 'B', 12)
            pdf.multi_cell(0, 10, f"{idx}. {article['title']}")
            
            # 메타 정보 - 여백 조정
            pdf.set_font('Malgun', '', 9)
            pdf.set_text_color(100, 100, 100)
            meta = f"출처: {article['press']} | 카테고리: {article['category']} | 시간: {article['timestamp']}"
            effective_width = pdf.w - 20  # 좌우 여백
            pdf.set_x(10)  # 시작 위치를 왼쪽 여백으로 명시적 설정
            pdf.cell(effective_width, 5, meta, 0, 1, 'L')
            pdf.ln(5)
            
            # 요약문
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Malgun', '', 10)
            pdf.set_x(10)  # 시작 위치 재설정
            pdf.multi_cell(0, 10, article['summary'])
            
            # 링크 - 여백 조정
            pdf.set_text_color(0, 0, 255)
            pdf.set_x(10)  # 시작 위치 재설정
            if len(article['link']) > 80:  # 링크가 너무 길 경우
                shortened_link = article['link'][:77] + "..."
            else:
                shortened_link = article['link']
            pdf.cell(effective_width, 5, shortened_link, 0, 1, 'L', link=article['link'])
            pdf.set_text_color(0, 0, 0)
            
            # 구분선 (마지막 기사 제외)
            if idx < len(articles):
                pdf.ln(5)
                pdf.line(10, pdf.get_y(), pdf.w - 10, pdf.get_y())  # 여기도 w 속성 사용
                pdf.ln(10)
        
        filename = f'news_summary_{date}.pdf'
        pdf.output(filename)
        logging.info(f"PDF 생성 완료: {filename}")
        return filename
        
    except Exception as e:
        logging.error(f"PDF 생성 실패: {e}")
        return None
