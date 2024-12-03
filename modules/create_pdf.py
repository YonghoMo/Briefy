from fpdf import FPDF

def create_pdf(articles, filename="news_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="News Summary", ln=True, align="C")

    for article in articles:
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, f"Title: {article['title']}\nSummary: {article['summary']}\nLink: {article['link']}")
    
    pdf.output(filename)
    print(f"PDF saved as {filename}")
