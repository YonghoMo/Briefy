from transformers import pipeline

def summarize_article(content):
    """
    Summarizes a single article content.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    try:
        input_length = len(content.split())

        # 입력 길이가 너무 짧은 경우 그대로 반환
        if input_length < 30:
            print("Content too short to summarize. Returning as-is.")
            return content

        # 요약 길이 설정
        max_length = max(30, int(input_length * 0.3))  # 입력 길이에 비례한 요약 길이
        min_length = min(30, int(input_length * 0.2))  # 최소 길이는 입력 길이에 비례

        summary = summarizer(
            content,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        return summary[0]['summary_text']

    except Exception as e:
        print(f"Error summarizing article: {e}")
        return "Error summarizing this article."

