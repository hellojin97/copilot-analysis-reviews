# 📧 이메일 대시보드 리포트 전송 가이드

## 🎯 개요

JSON 형태의 분석 결과를 아름다운 HTML 대시보드로 변환하여 이메일로 자동 전송합니다.

---

## 🚀 빠른 시작

### 방법 1: 원클릭 전송 (추천) ⭐

API 서버 없이 바로 실행:

```bash
python send_email_report.py
```

**특징**:
- ✅ API 서버 불필요
- ✅ 데이터 직접 수집
- ✅ HTML 리포트 자동 생성
- ✅ 이메일 자동 전송
- ✅ JSON 원본 데이터 첨부

---

### 방법 2: API 서버를 통한 전송

1. **API 서버 실행**
```bash
python api_server.py
```

2. **이메일 전송 요청**
```bash
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/send-report?recipient_email=your@email.com" -Method Post
```

또는 Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/send-report",
    params={
        "recipient_email": "your@email.com",
        "attach_raw_data": True
    }
)
print(response.json())
```

---

## 📊 이메일 리포트 내용

### 1. 전체 통계 대시보드
- 📈 총 고객 수, 상품 수, 리뷰 수
- ⭐ 평균 별점
- 😊😞😐 감성 분포 (긍정/부정/중립)

### 2. 개선 우선순위 상품 Top 5
- 🚨 부정 리뷰 비율 높은 상품
- 🔑 주요 문제점 키워드
- 📊 카테고리별 분류

### 3. 추천 시스템 샘플
- 🎁 고객 맞춤 추천 상품
- 📈 유사도 점수
- ⭐ 평균 별점 및 리뷰 수

### 4. 첨부 파일
- 📎 `dashboard_data.json` - 원본 JSON 데이터

---

## 🎨 HTML 리포트 미리보기

리포트는 다음과 같은 형태로 생성됩니다:

```
┌─────────────────────────────────────────────────┐
│  📊 리뷰 분석 대시보드 리포트                      │
│  생성일: 2025년 11월 05일                         │
└─────────────────────────────────────────────────┘

📈 전체 통계
┌──────────┬──────────┬──────────┬──────────┐
│ 총 고객수 │ 총 상품수 │ 총 리뷰수 │ 평균 별점 │
│  1,000명  │  100개   │ 4,000개  │  3.2★   │
└──────────┴──────────┴──────────┴──────────┘

감성 분포
┌────────────┬────────────┬────────────┐
│  😊 긍정    │  😞 부정    │  😐 중립    │
│  2,000개   │  1,200개   │   800개    │
│   50.0%    │   30.0%    │   20.0%    │
└────────────┴────────────┴────────────┘

🚨 개선 우선순위 상품 Top 5
┌────┬──────────┬────────┬────────┬────────┐
│순위│  상품명   │카테고리│평균별점│부정비율│
├────┼──────────┼────────┼────────┼────────┤
│ 1  │전기히터  │  가전  │ 2.8★  │ 47.1% │
│    │ 주요 문제: 실망(12), 망가짐(8)      │
├────┼──────────┼────────┼────────┼────────┤
│ ... 
```

---

## ⚙️ 설정 변경

### 이메일 주소 변경

`send_email_report.py` 파일 수정:

```python
# 이메일 설정
SENDER_EMAIL = "your@gmail.com"        # 송신자
APP_PASSWORD = "your app password"      # Gmail 앱 비밀번호
RECIPIENT_EMAIL = "recipient@gmail.com" # 수신자
```

### Gmail 앱 비밀번호 생성 방법

1. Google 계정 설정 → 보안
2. 2단계 인증 활성화
3. 앱 비밀번호 생성
4. "메일" 선택 후 생성된 비밀번호 복사

---

## 📁 생성된 파일

```
email_reporter.py          # 이메일 리포터 클래스
send_email_report.py       # 원클릭 전송 스크립트
api_server.py              # FastAPI 서버 (이메일 엔드포인트 추가)
```

---

## 🔧 커스터마이징

### 1. HTML 템플릿 수정

`email_reporter.py`의 `generate_html_report()` 함수에서 HTML 수정:

```python
def generate_html_report(self, data: Dict) -> str:
    # HTML 템플릿 커스터마이징
    html_content = f"""
    <!DOCTYPE html>
    <html>
    ...
    """
    return html_content
```

### 2. 데이터 범위 조정

Top 5 대신 Top 10으로 변경:

```python
# send_email_report.py
priority_products = analyzer.get_improvement_priority_products(top_n=10)
```

### 3. 추천 고객 변경

```python
# send_email_report.py
for customer_id in [100, 50, 200, 300]:  # 원하는 고객 ID 추가
```

---

## 🔄 자동화 스케줄링

### Windows 작업 스케줄러

1. **작업 스케줄러** 열기
2. **기본 작업 만들기**
3. **트리거**: 매일 오전 9시
4. **작업**: 프로그램 시작
   - 프로그램: `C:\...\\.venv\Scripts\python.exe`
   - 인수: `send_email_report.py`
   - 시작 위치: `C:\Users\...\110305-analysis-reviews`

### Cron (Linux/Mac)

```bash
# 매일 오전 9시 실행
0 9 * * * cd /path/to/project && .venv/bin/python send_email_report.py
```

---

## 📊 사용 사례

### 1. 일일 리포트
매일 아침 팀에게 리뷰 분석 결과 공유

### 2. 주간 리포트
매주 월요일 경영진에게 주간 리포트

### 3. 즉시 리포트
긴급 이슈 발생 시 즉시 관련 부서에 전송

### 4. 다중 수신자
여러 팀원에게 동시 전송

```python
# 여러 이메일 주소로 전송
recipients = [
    "team1@company.com",
    "team2@company.com",
    "manager@company.com"
]

for recipient in recipients:
    reporter.send_email(
        recipient_email=recipient,
        subject=subject,
        html_content=html_content
    )
```

---

## 🎯 주요 특징

### ✅ 완료된 기능
- [x] HTML 대시보드 자동 생성
- [x] Gmail SMTP 이메일 전송
- [x] JSON 원본 데이터 첨부
- [x] 반응형 HTML 디자인
- [x] 그라디언트 카드 UI
- [x] API 서버 통합
- [x] 원클릭 전송 스크립트

### 🎨 디자인 특징
- 💎 프로페셔널한 그라디언트 디자인
- 📱 모바일 반응형 레이아웃
- 🎨 색상 코딩 (긍정=녹색, 부정=빨강, 중립=회색)
- 📊 테이블 및 카드 레이아웃
- ⭐ 직관적인 통계 시각화

---

## 🔒 보안 고려사항

### 1. 앱 비밀번호 관리

**하드코딩 대신 환경변수 사용** (권장):

```python
import os

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
```

`.env` 파일 생성:
```
SENDER_EMAIL=your@gmail.com
APP_PASSWORD=your_app_password
```

### 2. .gitignore 설정

민감한 정보 제외:
```
.env
send_email_report.py  # 이메일 정보 포함 시
```

---

## 🐛 문제 해결

### 1. 이메일 전송 실패

**증상**: `SMTPAuthenticationError`

**해결**:
- Gmail 앱 비밀번호 재생성
- 2단계 인증 활성화 확인
- "보안 수준이 낮은 앱" 설정 확인

### 2. API 연결 실패

**증상**: `ConnectionError`

**해결**:
- API 서버가 실행 중인지 확인
- `send_email_report.py` 사용 (서버 불필요)

### 3. 한글 깨짐

**증상**: 이메일 본문 한글 깨짐

**해결**:
- UTF-8 인코딩 확인 (`charset='utf-8'`)
- 이미 적용되어 있음

---

## 📞 API 엔드포인트

### POST `/api/v1/send-report`

이메일 리포트 전송

**파라미터**:
- `recipient_email` (required): 수신자 이메일
- `attach_raw_data` (optional): JSON 첨부 여부

**응답**:
```json
{
  "status": "success",
  "message": "이메일이 성공적으로 전송되었습니다.",
  "recipient": "user@example.com",
  "sent_at": "2025-11-05T10:30:00"
}
```

---

## 🎉 완료!

이제 JSON 분석 결과가 아름다운 HTML 대시보드로 변환되어 자동으로 이메일로 전송됩니다!

**실행 명령**:
```bash
python send_email_report.py
```

**결과**:
- ✅ 전체 통계 대시보드
- ✅ 개선 우선순위 Top 5
- ✅ 추천 시스템 샘플
- ✅ JSON 원본 데이터 첨부
- ✅ 프로페셔널한 HTML 디자인

**이메일함을 확인하세요!** 📬
