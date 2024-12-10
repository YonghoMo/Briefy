
---

# Briefy - Daily News Summarizer

**Briefy**는 뉴스 크롤링, 본문 요약, PDF 생성 및 이메일 전송 기능을 제공하는 Python 프로젝트입니다. 매일 주요 뉴스 기사를 수집하고 요약하여 PDF 형식으로 저장한 뒤, 지정된 이메일로 전송합니다.

---

## 📋 목차
- [프로젝트 소개](#프로젝트-소개)
- [주요 기능](#주요-기능)
- [설치 및 실행](#설치-및-실행)
- [GitHub Actions를 통한 자동화](#github-actions를-통한-자동화)
- [사용 방법](#사용-방법)
- [프로젝트 구조](#프로젝트-구조)
- [참고 자료](#참고-자료)

---

## 📖 프로젝트 소개

이 프로젝트는 Naver 뉴스 섹션에서 기사를 크롤링하고, 기사 본문을 요약하여 매일 요약본을 PDF로 생성한 뒤 이메일로 자동 전송하는 프로그램입니다.

---

## ✨ 주요 기능
1. **뉴스 크롤링**:
   - 네이버 IT 뉴스 섹션에서 주요 기사 제목과 링크를 가져옵니다.
2. **본문 요약**:
   - 각 기사 내용을 최대 3줄로 요약합니다.
3. **PDF 생성**:
   - 제목, 요약, 기사 링크를 포함한 PDF 파일을 생성합니다.
4. **이메일 전송**:
   - 생성된 PDF 파일을 이메일 첨부파일로 전송합니다.
5. **자동 실행**:
   - 매일 정해진 시간에 작업을 실행합니다.
6. **GitHub Actions를 통한 자동화**:
   - 클라우드 환경에서 주기적으로 실행되도록 설정 가능합니다.

---

## 🛠 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone https://github.com/your-username/briefy.git
cd briefy
```

### 2. 가상환경 생성 및 활성화
```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. 필수 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
- 프로젝트 루트 디렉토리에 `.env` 파일 생성:
  ```env
  EMAIL_USERNAME=your_email@gmail.com
  EMAIL_PASSWORD=your_password
  ```
- 이메일 전송을 위해 Gmail 앱 비밀번호를 생성해야 합니다.

### 5. 프로그램 실행
```bash
python main.py
```

---

## 🚀 GitHub Actions를 통한 자동화

GitHub Actions를 사용하면 서버를 유지하거나 매일 로컬에서 실행할 필요 없이, 클라우드 환경에서 이 프로젝트를 자동으로 실행할 수 있습니다.

### 설정 방법

1. **GitHub Actions 워크플로 파일 생성**:
   - 프로젝트 디렉토리에서 `.github/workflows/briefy.yml` 파일 생성.
   - 아래 내용을 추가:
     ```yaml
     name: Run Briefy Daily

     on:
       schedule:
         # 매일 오전 8시에 실행
         - cron: '0 8 * * *'
       workflow_dispatch:  # 수동 실행 가능
     
     jobs:
       run_briefy:
         runs-on: ubuntu-latest
         
         steps:
         - name: Checkout repository
           uses: actions/checkout@v3
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt
         
         - name: Run main script
           env:
             EMAIL_USERNAME: ${{ secrets.EMAIL_USERNAME }}
             EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
           run: |
             python main.py
     ```

2. **GitHub Secrets 설정**:
   - GitHub 리포지토리의 **Settings > Secrets and variables > Actions > New repository secret**로 이동.
   - 아래 두 가지 환경 변수를 추가:
     - `EMAIL_USERNAME`: 이메일 주소
     - `EMAIL_PASSWORD`: 이메일 비밀번호 (또는 앱 비밀번호)

3. **자동화 확인**:
   - 워크플로가 매일 설정된 시간에 실행됩니다.
   - 필요 시 수동으로 실행하려면 **Actions** 탭에서 워크플로를 선택 후 실행.

---

## 📝 사용 방법

1. `main.py`를 실행하면 다음 작업이 수행됩니다:
   - 뉴스 크롤링 및 요약.
   - PDF 파일 생성.
   - 이메일 전송.

2. GitHub Actions를 통한 자동화:
   - 설정된 크론 스케줄에 따라 GitHub Actions에서 자동 실행됩니다.
   - 워크플로 실행 로그는 GitHub **Actions** 탭에서 확인 가능합니다.

---

## 📂 프로젝트 구조

```
Briefy/
├── main.py                # 프로그램 실행 파일
├── requirements.txt       # 필수 라이브러리 목록
├── .env                   # 환경 변수 파일 (이메일 정보)
├── .github/
│   └── workflows/
│       └── briefy.yml     # GitHub Actions 워크플로 설정 파일
├── modules/
│   ├── fetch_news.py      # 뉴스 크롤링 모듈
│   ├── fetch_article.py   # 기사 본문 크롤링 모듈
│   ├── summarize.py       # 본문 요약 모듈
│   ├── create_pdf.py      # PDF 생성 모듈
│   └── send_email.py      # 이메일 전송 모듈
└── README.md              # 프로젝트 설명 파일
```

---

## 📎 참고 자료

1. [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
2. [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
3. [FPDF Documentation](https://pyfpdf.github.io/fpdf2/)
4. [Python Schedule](https://schedule.readthedocs.io/en/stable/)
5. [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 📬 문의
- **개발자**: Yongho Mo
- **이메일**: ahdydgh123@gmail.com
- **GitHub**: [Yongho Mo](https://github.com/YonghoMo)

---
