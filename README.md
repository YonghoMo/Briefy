# 📚 Briefy: 뉴스 요약 크롤러 및 이메일 전송 프로그램

Briefy는 매일 최신 뉴스를 크롤링하고 요약하여 PDF로 정리한 후, 이메일로 자동 전송하는 Python 기반 프로그램입니다. 이 프로젝트는 정보 전달 과정을 간소화하고 사용자의 시간을 절약하는 데 초점을 맞추고 있습니다.

---

## 🌟 주요 기능

1. **뉴스 크롤링**:
   - 지정된 뉴스 웹사이트에서 제목과 본문을 자동으로 수집합니다.
2. **뉴스 요약**:
   - Hugging Face의 사전 학습된 요약 모델(`facebook/bart-large-cnn`)을 사용하여 뉴스를 요약합니다.
3. **PDF 생성**:
   - 요약된 뉴스를 PDF 형식으로 저장합니다.
4. **이메일 전송**:
   - PDF를 사용자 지정 이메일로 전송합니다.
5. **자동화**:
   - Python의 `schedule` 라이브러리를 사용하여 매일 지정된 시간에 실행됩니다.

---

## 🛠️ 기술 스택

- **언어**: Python
- **크롤링**: `requests`, `BeautifulSoup`
- **요약 모델**: Hugging Face Transformers (`facebook/bart-large-cnn`)
- **PDF 생성**: `fpdf`
- **이메일 전송**: `yagmail`
- **스케줄링**: `schedule`

---

## 🚀 설치 방법

1. **리포지토리 클론**
   ```bash
   git clone https://github.com/username/briefy.git
   cd briefy
   ```
2. **필수 라이브러리 설치**

   ```bash
   pip install -r requirements.txt
   ```

   **python 3.11.6, rust 1.83.0가 설치되어 있어야 하며 환경변수 설정이 올바르게 되어있어야 합니다.**

3. **환경 변수 설정**

   - 프로젝트 루트 디렉토리에 `.env` 파일을 생성합니다:

   ```bash
   EMAIL_USERNAME=your_email@gmail.com(이곳에 요악본 pdf를 받을 email을 작성하세요.)
   EMAIL_PASSWORD=your_password(이곳에 email 앱 비밀번호를 생성하여 작성하세요.)
   ```

   - 이메일 서비스(Gmail 등)의 앱 비밀번호를 사용해야 합니다.
   - Gmail 설정에서 보안 수준이 낮은 앱의 액세스를 허용하거나 앱 비밀번호를 생성하세요.

4. **스크립트 실행**
   ```bash
   python main.py
   ```

---

## 📝 사용 방법

### **자동 실행 설정**

- `main.py`는 기본적으로 매일 오전 8시에 실행되도록 설정되어 있습니다.
- 실행 시간을 변경하려면 `schedule.every().day.at("08:00").do(job)` 코드를 수정하세요.

### **결과 확인**

- 생성된 PDF는 프로젝트 디렉토리에 저장되며, 이메일로 전송됩니다.

---

## 📊 주요 결과

### **PDF 예시**

프로그램 실행 후 생성된 PDF 파일은 아래와 같은 내용을 포함합니다:

```
Title: ChatGPT가 IT 산업에 미치는 영향
Summary: ChatGPT는 인공지능 기술 혁신의 중심에 있으며, IT 산업의 주요 역할을 하고 있습니다.
Link: https://example.com
```

---

## 🕒 자동화 스케줄

- 기본 실행 시간: 매일 오전 8시.
- 실행 시간을 변경하려면 `main.py`에서 `schedule.every().day.at("08:00").do(job)` 부분을 수정하세요.

---

## 📎 참고 자료

```
Hugging Face Transformers
BeautifulSoup Documentation
FPDF Documentation
Python Schedule
```

---

📬 문의

```
개발자: Yongho Mo
이메일: ahdydgh123@gmail.com
GitHub: https://github.com/YonghoMo
```
