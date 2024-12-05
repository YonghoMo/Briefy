from typing import Optional
import logging
import re

def summarize_article(text: str, summary_length: int = 3) -> Optional[str]:
    """
    뉴스 기사 텍스트를 요약하는 함수
    
    Args:
        text (str): 요약할 뉴스 기사 본문 텍스트
        summary_length (int): 기본 요약 문장 수 (기본값: 3)
        
    Returns:
        Optional[str]: 성공 시 요약된 텍스트, 실패 시 None
        
    Note:
        - 추출적 요약 방식 사용 (첫 3~5문장 추출)
        - 텍스트 길이에 따라 동적으로 요약 길이 조정
        - 불필요한 문장 필터링 (메타 정보, 광고 등)
        - 최소/최대 길이 제한 적용
        - 문장 정제 및 포맷팅 수행
    """
    try:
        if not text or len(text) < 100:
            logging.warning("텍스트가 너무 짧아 요약할 수 없습니다")
            return None
            
        # 문장 분리 (개선된 정규식)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # 문장 필터링 강화
        filtered_sentences = []
        for s in sentences:
            s = s.strip()
            if (30 <= len(s) <= 200 and  # 길이 제한
                not re.search(r'(제공|특파원|기자|저작권|구독|뉴스|기사|전재)', s) and
                not s.startswith(('▶', '■', '※', '☞', '#', '@'))):
                filtered_sentences.append(s)
        
        if not filtered_sentences:
            logging.warning("유효한 문장을 찾을 수 없습니다")
            return None
            
        # 원문 길이에 따른 동적 요약 길이 조정
        text_length = len(text)
        if text_length > 2000:
            summary_length = 5  # 긴 기사는 5문장
        elif text_length > 1000:
            summary_length = 4  # 중간 길이 기사는 4문장
        else:
            summary_length = 3  # 짧은 기사는 3문장
            
        # 최소 요약 길이 보장
        if len(filtered_sentences) <= summary_length:
            if len(filtered_sentences) < 2:  # 너무 짧은 경우
                return None
            return '. '.join(filtered_sentences) + '.'
            
        # 요약문 생성
        summary = '. '.join(filtered_sentences[:summary_length]) + '.'
        summary = re.sub(r'\.+', '.', summary)
        
        # 최종 요약문 길이 제한 및 최소 길이 보장
        if len(summary) > 1000:
            summary = summary[:997] + "..."
        elif len(summary) < 200:  # 요약문이 너무 짧은 경우
            # 추가 문장 포함
            additional_sentences = filtered_sentences[summary_length:summary_length+2]
            if additional_sentences:
                summary = '. '.join(filtered_sentences[:summary_length+2]) + '.'
                summary = re.sub(r'\.+', '.', summary)
        
        logging.debug(f"요약 완료 (원본: {len(text)}자, 요약: {len(summary)}자, 문장 수: {summary_length})")
        return summary
        
    except Exception as e:
        logging.error(f"텍스트 요약 실패: {e}")
        return None

