# FastAPI REST API 서버 실행 가이드

## 🚀 서버 실행 방법

### 방법 1: Python으로 직접 실행
```bash
python api_server.py
```

### 방법 2: uvicorn으로 실행
```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

---

## 📖 API 문서 확인

서버 실행 후 브라우저에서 아래 주소로 접속:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🧪 API 테스트 (PowerShell)

### 1. 헬스 체크
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get | ConvertTo-Json
```

### 2. 전체 통계 조회
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/stats/overview" -Method Get | ConvertTo-Json -Depth 5
```

### 3. 고객 추천 (고객 ID: 100)
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/recommend/100?top_n=5" -Method Get | ConvertTo-Json -Depth 10
```

### 4. 부정 리뷰 분석 (Top 5)
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/negative-analysis?top_n=5" -Method Get | ConvertTo-Json -Depth 10
```

### 5. 상품 프로필 조회 (상품 ID: 39)
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/product/39/profile" -Method Get | ConvertTo-Json -Depth 5
```

### 6. 고객 프로필 조회 (고객 ID: 100)
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/customer/100/profile" -Method Get | ConvertTo-Json -Depth 5
```

---

## 🐍 Python으로 API 호출

```python
import requests

# 고객 추천
response = requests.get(
    "http://localhost:8000/api/v1/recommend/100",
    params={"top_n": 5, "exclude_purchased": True}
)
print(response.json())

# 부정 리뷰 분석
response = requests.get(
    "http://localhost:8000/api/v1/negative-analysis",
    params={"top_n": 5}
)
print(response.json())
```

---

## 📊 주요 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | `/health` | 헬스 체크 |
| GET | `/api/v1/recommend/{customer_id}` | 고객 맞춤 추천 |
| GET | `/api/v1/negative-analysis` | 부정 리뷰 분석 |
| GET | `/api/v1/product/{product_id}/profile` | 상품 프로필 |
| GET | `/api/v1/customer/{customer_id}/profile` | 고객 프로필 |
| GET | `/api/v1/stats/overview` | 전체 통계 |

---

## ✅ 구현 완료 사항

### Phase 3 추천 시스템 → REST API 변환

**구현된 API 기능**:
- ✅ 고객 맞춤 상품 추천 (코사인 유사도 기반)
- ✅ 부정 리뷰 분석 및 개선 우선순위
- ✅ 상품/고객 키워드 프로필 조회
- ✅ 전체 통계 대시보드 데이터
- ✅ FastAPI 자동 문서화 (Swagger/ReDoc)
- ✅ Pydantic 모델 기반 유효성 검증
- ✅ 에러 핸들링 및 HTTP 상태 코드
- ✅ JSON 형식 응답

**기술 스택**:
- FastAPI 0.115+
- uvicorn (ASGI 서버)
- Pydantic (데이터 검증)
- recommendation_system.py (Phase 3 로직)
- analyze_negative_reviews.py (Phase 2 로직)

---

## 🎯 API 응답 예시

### 고객 추천 API
```json
{
  "customer_id": 100,
  "recommendations": [
    {
      "product_id": 45,
      "product_name": "커피머신",
      "category": "가전",
      "similarity_score": 0.8102,
      "average_rating": 3.21,
      "review_count": 39,
      "top_keywords": [
        {"keyword": "좋", "weight": 0.1234}
      ]
    }
  ],
  "total_count": 5,
  "generated_at": "2025-11-05T12:34:56"
}
```

### 부정 리뷰 분석 API
```json
{
  "generated_at": "2025-11-05T12:34:56",
  "total_products_analyzed": 5,
  "improvement_priority_list": [
    {
      "product_id": 39,
      "product_name": "전기히터",
      "category": "가전",
      "total_negative_keyword_count": 59,
      "negative_ratio": 47.1,
      "top_negative_keywords": [
        {"keyword": "실망", "count": 12}
      ]
    }
  ]
}
```

---

## 💡 활용 시나리오

### 1. 고객 맞춤 추천
- E-commerce 사이트에서 "당신을 위한 추천" 섹션
- 이메일 마케팅 개인화

### 2. 품질 개선
- 개선 우선순위 대시보드
- 제품 개발팀 주간 리포트

### 3. 데이터 분석
- BI 도구와 연동 (Tableau, PowerBI)
- 실시간 모니터링 대시보드

---

## 📌 다음 단계

### Phase 4: Streamlit 대시보드
- API를 호출하여 시각화
- 인터랙티브 UI 제공

### Phase 5: 고도화
- JWT 인증 추가
- Rate Limiting
- Redis 캐싱
- Docker 컨테이너화

---

## 🎉 완료!

Phase 3 추천 시스템이 FastAPI REST API로 성공적으로 변환되었습니다!
이제 다양한 클라이언트(웹, 모바일, 대시보드)에서 JSON 형태로 데이터를 받아 활용할 수 있습니다.
