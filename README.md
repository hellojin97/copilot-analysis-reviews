# 📊 리뷰 분석 및 추천 시스템

> 고객 리뷰 데이터 기반 부정 키워드 분석 및 AI 추천 시스템

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 목차

1. [프로젝트 소개](#-프로젝트-소개)
2. [주요 기능](#-주요-기능)
3. [프로젝트 구조](#-프로젝트-구조)
4. [설치 및 설정](#-설치-및-설정)
5. [사용법](#-사용법)
6. [REST API 가이드](#-rest-api-가이드)
7. [이메일 대시보드](#-이메일-대시보드)
8. [GitHub Actions 자동화](#-github-actions-자동화)
9. [기술 스택](#-기술-스택)
10. [데이터 통계](#-데이터-통계)

---

## 🎯 프로젝트 소개

이 프로젝트는 **1,000명의 고객**이 작성한 **100개 상품**에 대한 **4,000개의 리뷰**를 분석하여:

- 📉 **부정 리뷰 분석**: 개선이 필요한 상품을 자동으로 식별
- 🎁 **AI 추천 시스템**: 고객 취향 기반 상품 추천
- 📧 **자동 리포트**: HTML 대시보드를 이메일로 전송
- 🌐 **REST API**: JSON 형태로 분석 결과 제공
- 📊 **시각화**: 차트 및 워드클라우드 생성

### 핵심 가치

1. **자동화된 품질 개선**: 부정 리뷰를 분석하여 우선순위 상품 자동 도출
2. **개인화된 추천**: 고객의 긍정 리뷰 키워드 기반 맞춤 추천
3. **실시간 모니터링**: API를 통한 실시간 데이터 조회
4. **의사결정 지원**: 경영진을 위한 시각화된 이메일 리포트

---

## ✨ 주요 기능

### 1. 부정 리뷰 분석 시스템
- 제품별 부정 키워드 빈도 집계
- 6가지 문제 카테고리 자동 분류 (품질/배송/가격/서비스/성능/사용성)
- Top N 개선 우선순위 상품 리스트

### 2. AI 추천 시스템
- 코사인 유사도 기반 상품 추천
- 고객별 맞춤 추천 (이미 구매한 상품 제외)
- 실시간 추천 API

### 3. REST API 서버
- FastAPI 기반 고성능 API
- Swagger UI 자동 문서화
- JSON 형태의 응답

### 4. 이메일 대시보드
- HTML 형식의 아름다운 리포트
- 차트 및 그래프 포함
- 원클릭 전송 지원

### 5. GitHub Actions 자동화
- 수동 워크플로우 트리거
- 자동 이메일 발송
- 스케줄링 지원

---

## 📁 프로젝트 구조

```
📁 프로젝트 루트/
├── 📁 src/                     # 핵심 분석 로직
│   ├── text_cleaner.py        # 텍스트 전처리 및 정제
│   ├── analyze_negative_reviews.py  # 부정 리뷰 분석
│   ├── recommendation_system.py     # 추천 시스템
│   └── chart_generator.py     # 차트 생성 및 시각화
│
├── 📁 api/                     # REST API 서버
│   ├── api_server.py          # FastAPI 서버
│   └── test_api.py            # API 테스트
│
├── 📁 emailer/                 # 이메일 리포터
│   ├── email_reporter.py      # HTML 이메일 생성
│   └── send_email_report.py   # 이메일 발송 스크립트
│
├── 📁 scripts/                 # 유틸리티 스크립트
│   ├── load_csv_to_db_simple.py    # CSV → SQLite 로드
│   └── test_text_cleaner_with_db.py # 텍스트 정제 테스트
│
├── 📁 csv/                     # 원본 데이터
│   ├── customers.csv          # 고객 데이터 (1,000명)
│   ├── products.csv           # 상품 데이터 (100개)
│   └── reviews.csv            # 리뷰 데이터 (4,000개)
│
├── 📁 data/                    # 데이터베이스
│   └── reviews.db             # SQLite 데이터베이스
│
├── 📁 cache/                   # 캐시 파일
│   └── product_profiles.pkl   # 상품 프로필 캐시
│
├── 📁 reports/                 # 분석 리포트
│
├── 📁 .github/workflows/      # GitHub Actions
│   └── send-email-report.yml  # 이메일 자동화 워크플로우
│
├── 📄 requirements.txt         # Python 패키지 의존성
└── 📄 README.md               # 프로젝트 문서
```

---

## ⚙️ 설치 및 설정

### 1. 저장소 클론

```bash
git clone https://github.com/hellojin97/copilot-analysis-reviews.git
cd copilot-analysis-reviews
```

### 2. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

**주요 패키지**:
- `kiwipiepy==0.21.0` - 한글 형태소 분석
- `scikit-learn==1.6.1` - 코사인 유사도 계산
- `fastapi` - REST API 서버
- `matplotlib`, `seaborn`, `wordcloud` - 시각화

### 4. 데이터베이스 생성

```bash
python scripts/load_csv_to_db_simple.py
```

**실행 결과**:
```
✓ 1000개의 고객 데이터가 성공적으로 로드되었습니다.
✓ 100개의 상품 데이터가 성공적으로 로드되었습니다.
✓ 4000개의 리뷰 데이터가 성공적으로 로드되었습니다.
```

---

## 🚀 사용법

### 1. 부정 리뷰 분석

```bash
python -m src.analyze_negative_reviews
```

### 2. 추천 시스템 실행

```python
from src.recommendation_system import RecommendationSystem

recommender = RecommendationSystem()
recommender.load_profiles()

# 고객 ID 100에게 상품 5개 추천
recommendations = recommender.recommend_products(
    customer_id=100,
    top_n=5,
    exclude_purchased=True
)

for rec in recommendations:
    print(f"{rec['product_name']}: {rec['similarity_score']:.4f}")
```

### 3. 이메일 리포트 전송

#### 환경변수 설정

**1단계: `.env` 파일 생성**

프로젝트 루트에 `.env` 파일을 생성하고 이메일 정보를 입력하세요:

```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# Windows
copy .env.example .env
```

`.env` 파일 내용:
```env
SENDER_EMAIL=your@gmail.com
APP_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@gmail.com
```

**2단계: Gmail 앱 비밀번호 생성**

1. Google 계정 → 보안
2. 2단계 인증 활성화
3. 앱 비밀번호 생성
4. "메일" 선택 후 생성된 16자리 비밀번호 복사

**3단계: 이메일 발송**

```bash
# Windows PowerShell (환경변수로 직접 설정)
$env:SENDER_EMAIL="your@gmail.com"
$env:APP_PASSWORD="your_app_password"
$env:RECIPIENT_EMAIL="recipient@gmail.com"
python -m emailer.send_email_report

# Linux/Mac (환경변수로 직접 설정)
export SENDER_EMAIL="your@gmail.com"
export APP_PASSWORD="your_app_password"
export RECIPIENT_EMAIL="recipient@gmail.com"
python -m emailer.send_email_report

# .env 파일 사용 (권장)
python -m emailer.send_email_report
```

**참고**: `.env` 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다.

---

## 🌐 REST API 가이드

### API 서버 실행

```bash
python -m api.api_server
```

또는

```bash
uvicorn api.api_server:app --reload --host 0.0.0.0 --port 8000
```

### API 문서 확인

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 엔드포인트

#### 1. 헬스 체크

```bash
GET /health
```

#### 2. 고객 맞춤 추천

```bash
GET /api/v1/recommend/{customer_id}?top_n=5
```

#### 3. 부정 리뷰 분석

```bash
GET /api/v1/negative-analysis?top_n=5
```

#### 4. 전체 통계 조회

```bash
GET /api/v1/stats/overview
```

### Python에서 API 호출

```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/recommend/100",
    params={"top_n": 5}
)
print(response.json())
```

---

## 📧 이메일 대시보드

### 원클릭 전송

```bash
python -m emailer.send_email_report
```

**포함 내용**:
- ✅ 전체 통계 대시보드
- ✅ 개선 우선순위 상품 Top 5
- ✅ 추천 시스템 샘플
- ✅ 5가지 차트 (감성 분포, 개선 우선순위, 별점 비교, 워드클라우드, 추천 산점도)
- ✅ 한글 폰트 완벽 지원

### Gmail 앱 비밀번호 생성

1. Google 계정 설정 → 보안
2. 2단계 인증 활성화
3. 앱 비밀번호 생성
4. "메일" 선택 후 생성된 비밀번호 복사

---

## 🤖 GitHub Actions 자동화

### 1. GitHub Secrets 등록

GitHub 저장소 → Settings → Secrets and variables → Actions

**등록할 Secrets**:
- `SENDER_EMAIL`: 송신자 이메일 주소
- `APP_PASSWORD`: Gmail 앱 비밀번호

### 2. Workflow 수동 실행

1. GitHub 저장소 → **Actions** 탭
2. **Send Dashboard Email Report** 선택
3. **Run workflow** 버튼 클릭
4. (선택) 수신자 이메일 입력
5. **Run workflow** 실행

### 자동 스케줄 실행 (선택사항)

매일 자동 실행하려면 `.github/workflows/send-email-report.yml`에 추가:

```yaml
on:
  workflow_dispatch:  # 수동 실행
  schedule:
    - cron: '0 0 * * *'  # 매일 자정 (UTC)
```

---

## 🛠️ 기술 스택

### 언어 및 프레임워크
- **Python**: 3.12.11
- **FastAPI**: REST API 서버
- **SQLite**: 데이터베이스

### 주요 라이브러리
| 라이브러리 | 버전 | 용도 |
|-----------|------|------|
| kiwipiepy | 0.21.0 | 한글 형태소 분석 |
| scikit-learn | 1.6.1 | 코사인 유사도 계산 |
| FastAPI | 0.115+ | REST API 서버 |
| matplotlib | 3.10.7 | 차트 생성 |
| seaborn | 0.13.2 | 통계 시각화 |
| wordcloud | 1.9.4 | 워드클라우드 |

### 알고리즘
- **코사인 유사도**: 고객-상품 키워드 벡터 유사도 계산
- **TF-IDF**: 키워드 가중치 계산
- **형태소 분석**: Kiwi (한국어 Intelligent Word Identifier)

---

## 📊 데이터 통계

### 데이터 규모
- **고객 수**: 1,000명
- **상품 수**: 100개
- **리뷰 수**: 4,000개

### 카테고리별 상품 분포
- **가전**: 40개 (40%)
- **패션**: 30개 (30%)
- **디지털**: 30개 (30%)

### 감성 분석 결과
| 감성 | 리뷰 수 | 비율 |
|------|---------|------|
| 긍정 (Positive) | 2,000개 | 50.0% |
| 부정 (Negative) | 1,200개 | 30.0% |
| 중립 (Neutral) | 800개 | 20.0% |

### 개선 우선순위 Top 5

| 순위 | 제품명 | 카테고리 | 부정 비율 | 평균 별점 |
|------|--------|----------|-----------|-----------|
| 1 | 전기히터 | 가전 | 47.1% | 2.8★ |
| 2 | 냉장고 양문형 | 가전 | 31.7% | 3.27★ |
| 3 | 수영복 | 패션 | 39.5% | 3.16★ |
| 4 | 히터 | 가전 | 41.2% | 3.04★ |
| 5 | 무선 충전 패드 | 디지털 | 36.2% | 3.3★ |

---

## 🔒 보안 고려사항

### 1. SQL 인젝션 방지
- ✅ SQLAlchemy ORM 사용
- ✅ 파라미터화된 쿼리
- ❌ f-string으로 SQL 생성 금지

### 2. 비밀 정보 관리
- ✅ 환경변수 사용 (`.env`)
- ✅ GitHub Secrets 활용
- ❌ 하드코딩 금지

---

## 🐛 문제 해결

### 1. 이메일 전송 실패
- Gmail 앱 비밀번호 재생성
- 2단계 인증 활성화 확인

### 2. 한글 깨짐
- ✅ 이미 해결됨 (Malgun Gothic 폰트 사용)

### 3. API 연결 실패
- API 서버 실행 확인
- 포트 충돌 확인 (8000번)

---

## 📞 문의 및 기여

### 버그 리포트
GitHub Issues에 버그 리포트를 등록해주세요.

### 기여 방법
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 🎉 완료!

**실행 방법**:
```bash
# 로컬 실행
python -m emailer.send_email_report

# GitHub Actions
GitHub → Actions → Send Dashboard Email Report → Run workflow
```

**Happy Analyzing!** 🚀

---

**Made with ❤️ by hellojin97**
