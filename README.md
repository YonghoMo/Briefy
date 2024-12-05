# 🌏 Briefy: Daily World News Briefing

매일 아침, 주요 세계 뉴스를 요약하여 이메일로 받아보세요.

## 📌 주요 기능

- **자동 뉴스 수집**: 네이버 뉴스의 세계 섹션에서 최신 기사를 자동으로 수집
- **스마트 요약**: 각 기사의 핵심 내용을 3-5문장으로 추출
- **PDF 생성**: 깔끔한 레이아웃의 PDF 문서 자동 생성
- **이메일 전송**: GitHub Actions를 통한 매일 오전 8시 자동 전송
- **키워드 필터링**: 관심 있는 국가/주제 기반 필터링 (예: 중국, 미국, 일본, 러시아)

## 🛠 기술 스택

- **Python 3.11.6**
- **BeautifulSoup4**: 뉴스 크롤링
- **FPDF2**: PDF 문서 생성
- **GitHub Actions**: 자동화된 실행
- **Yagmail**: 이메일 전송

## ⚙️ 설치 방법

1. **저장소 Fork**

   - 이 저장소의 우측 상단 "Fork" 버튼 클릭
   - 자신의 GitHub 계정에 복사본 생성

2. **Gmail 앱 비밀번호 생성**

   - Gmail 계정의 2단계 인증 활성화
   - 앱 비밀번호 생성 (Gmail 설정 → 보안 → 앱 비밀번호)

3. **GitHub Secrets 설정**

   - Fork한 저장소의 Settings → Secrets and variables → Actions
   - "New repository secret" 클릭하여 두 개의 secret 추가:
     - `EMAIL_USERNAME`: 뉴스를 받을 Gmail 주소
     - `EMAIL_PASSWORD`: Gmail 앱 비밀번호

4. **GitHub Actions 활성화**
   - Actions 탭으로 이동
   - "I understand my workflows, go ahead and enable them" 클릭
   - "Daily News Summary" 워크플로우 활성화

## 📊 출력 예시

- **PDF 형식**:
  - 기사 제목
  - 출처 및 시간
  - 3-5문장 요약
  - 원문 링크

## 🔍 주요 기능 설명

1. **뉴스 수집**:

- 네이버 뉴스의 세계 섹션에서 최신 기사를 자동으로 수집
- 중복된 기사는 자동으로 필터링
- 각 기사의 제목, 링크, 언론사, 작성 시간 등의 메타데이터 추출
- 사용자가 지정한 키워드(국가/주제)에 따라 필터링 가능

2. **기사 요약**:

- 각 기사의 본문에서 핵심 문장을 3-5개 추출
- 기사 길이에 따라 동적으로 요약 길이 조정
  - 2000자 이상: 5문장
  - 1000-2000자: 4문장
  - 1000자 미만: 3문장
- 광고, 기자 정보, 저작권 등 불필요한 내용 자동 제거

3. **PDF 생성**:

- 깔끔한 레이아웃의 PDF 문서 자동 생성
- 기사별 구분선으로 가독성 향상
- 각 기사마다 포함되는 정보:
  - 제목 (굵은 글씨)
  - 언론사 및 작성 시간
  - 요약된 본문 내용
  - 클릭 가능한 원문 링크

4. **자동화**:

- GitHub Actions를 통한 자동 실행
- 매일 오전 8시(한국 시간)에 정기적으로 실행
- 실행 결과는 GitHub Actions 로그에서 확인 가능
- 오류 발생 시 자동 로깅

## 📝 라이선스

MIT License

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## 📬 문의

- 이메일: ahdydgh123@gmail.com
- GitHub: https://github.com/YonghoMo

---

**Note**:

- Gmail 사용 시 반드시 2단계 인증을 설정하고 앱 비밀번호를 생성하여 사용하세요.
- GitHub Actions는 매일 UTC 23:00 (한국 시간 08:00)에 자동으로 실행됩니다.
- 문제가 발생하면 Actions 탭에서 실행 로그를 확인할 수 있습니다.
