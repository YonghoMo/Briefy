from fpdf import FPDF

def create_pdf(summarized_articles, filename="news_summary.pdf"):
    """
    Creates a PDF file from summarized articles.
    Each article includes the title, summary, and a link to the full article.
    """
    pdf = FPDF()
    pdf.add_page()

    # 한글 폰트 추가 (기본 폰트와 굵기 폰트 모두 등록)
    pdf.add_font('Malgun', '', './malgun.ttf', uni=True)
    pdf.add_font('Malgun', 'B', './malgunbd.ttf', uni=True)

    if not summarized_articles:
        summarized_articles = [{"title": "No Title", "summary": "No content available to summarize.", "link": "No Link"}]

    for idx, article in enumerate(summarized_articles, start=1):
        title = article.get("title", "No Title")
        summary = article.get("summary", "No Summary")
        link = article.get("link", "No Link")  # 기본값 추가

        # 제목 추가
        pdf.set_font('Malgun', 'B', size=14)
        pdf.cell(0, 10, f"Article {idx}: {title}", ln=True)

        # 링크 추가
        pdf.set_font('Malgun', style='U', size=12)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 10, link, ln=True, link=link)

        # 요약 내용 추가
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Malgun', '', size=12)
        pdf.multi_cell(0, 10, f"Summary:\n{summary}\n")

    pdf.output(filename, "F")
    print(f"PDF created: {filename}")
