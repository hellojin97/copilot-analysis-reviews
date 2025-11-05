# 🚀 FastAPI 추천 시스템 REST API 가이드

## 📋 개요

Phase 3 추천 시스템을 FastAPI 기반 RESTful API로 제공합니다.
고객 맞춤 추천, 부정 리뷰 분석, 프로필 조회 등의 기능을 JSON 형태로 반환합니다.

---

## 🛠️ 설치 및 실행

### 1. 필요 패키지 설치
```bash
pip install fastapi uvicorn[standard]
```

### 2. API 서버 실행
```bash
python api_server.py
```

또는

```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

### 3. 서버 접속
- **API 서버**: http://localhost:8000
- **Swagger UI 문서**: http://localhost:8000/docs
- **ReDoc 문서**: http://localhost:8000/redoc

---

## 📡 API 엔드포인트

### 1. 헬스 체크

#### `GET /`
루트 엔드포인트 - API 상태 확인

**응답 예시**:
```json
{
  "status": "running",
  "message": "리뷰 분석 및 추천 시스템 API가 정상 작동 중입니다.",
  "timestamp": "2025-11-05T10:30:00.123456"
}
```

#### `GET /health`
헬스 체크 엔드포인트

**응답 예시**:
```json
{
  "status": "healthy",
  "message": "모든 시스템이 정상입니다.",
  "timestamp": "2025-11-05T10:30:00.123456"
}
```

---

### 2. 고객 맞춤 추천

#### `GET /api/v1/recommend/{customer_id}`
고객에게 맞춤 상품을 추천합니다.

**경로 파라미터**:
- `customer_id` (int, required): 고객 ID

**쿼리 파라미터**:
- `top_n` (int, optional): 추천할 상품 개수 (기본값: 5, 최소: 1, 최대: 20)
- `exclude_purchased` (bool, optional): 이미 리뷰 작성한 상품 제외 (기본값: true)

**요청 예시**:
```bash
curl "http://localhost:8000/api/v1/recommend/100?top_n=5&exclude_purchased=true"
```

**응답 예시**:
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
        {"keyword": "좋", "weight": 0.1234},
        {"keyword": "만족", "weight": 0.0987},
        {"keyword": "드리", "weight": 0.0765}
      ]
    },
    {
      "product_id": 78,
      "product_name": "양말 5족세트",
      "category": "패션",
      "similarity_score": 0.8071,
      "average_rating": 3.4,
      "review_count": 48,
      "top_keywords": [
        {"keyword": "하", "weight": 0.1456},
        {"keyword": "드리", "weight": 0.1123}
      ]
    }
  ],
  "total_count": 2,
  "generated_at": "2025-11-05T10:30:00.123456"
}
```

**에러 응답 (404)**:
```json
{
  "detail": "고객 ID 999에 대한 추천 결과가 없습니다. 긍정 리뷰가 없거나 고객이 존재하지 않을 수 있습니다."
}
```

---

### 3. 부정 리뷰 분석

#### `GET /api/v1/negative-analysis`
부정 리뷰를 분석하여 개선 우선순위 상품을 반환합니다.

**쿼리 파라미터**:
- `top_n` (int, optional): 분석할 상품 개수 (기본값: 5, 최소: 1, 최대: 50)

**요청 예시**:
```bash
curl "http://localhost:8000/api/v1/negative-analysis?top_n=5"
```

**응답 예시**:
```json
{
  "generated_at": "2025-11-05T10:30:00.123456",
  "total_products_analyzed": 5,
  "improvement_priority_list": [
    {
      "product_id": 39,
      "product_name": "전기히터",
      "category": "가전",
      "total_negative_keyword_count": 59,
      "negative_review_count": 24,
      "total_review_count": 51,
      "average_rating": 2.8,
      "negative_ratio": 47.1,
      "top_negative_keywords": [
        {"keyword": "실망", "count": 12},
        {"keyword": "아쉽", "count": 9},
        {"keyword": "망가지", "count": 8}
      ],
      "problem_categories": {
        "품질": [
          {"keyword": "망가지", "count": 8}
        ],
        "배송": [
          {"keyword": "배송", "count": 1},
          {"keyword": "늦", "count": 1}
        ]
      }
    }
  ]
}
```

---

### 4. 상품 프로필 조회

#### `GET /api/v1/product/{product_id}/profile`
특정 상품의 키워드 프로필을 조회합니다.

**경로 파라미터**:
- `product_id` (int, required): 상품 ID

**요청 예시**:
```bash
curl "http://localhost:8000/api/v1/product/39/profile"
```

**응답 예시**:
```json
{
  "product_id": 39,
  "total_keywords": 45,
  "top_keywords": [
    {"keyword": "좋", "weight": 0.1234},
    {"keyword": "만족", "weight": 0.0987},
    {"keyword": "브랜드", "weight": 0.0876},
    {"keyword": "추천", "weight": 0.0765}
  ],
  "generated_at": "2025-11-05T10:30:00.123456"
}
```

---

### 5. 고객 프로필 조회

#### `GET /api/v1/customer/{customer_id}/profile`
특정 고객의 키워드 프로필을 조회합니다.

**경로 파라미터**:
- `customer_id` (int, required): 고객 ID

**요청 예시**:
```bash
curl "http://localhost:8000/api/v1/customer/100/profile"
```

**응답 예시**:
```json
{
  "customer_id": 100,
  "total_keywords": 17,
  "top_keywords": [
    {"keyword": "좋", "weight": 0.2345},
    {"keyword": "만족", "weight": 0.1876},
    {"keyword": "추천", "weight": 0.1234}
  ],
  "generated_at": "2025-11-05T10:30:00.123456"
}
```

---

### 6. 전체 통계 조회

#### `GET /api/v1/stats/overview`
리뷰 데이터 전체 통계를 조회합니다.

**요청 예시**:
```bash
curl "http://localhost:8000/api/v1/stats/overview"
```

**응답 예시**:
```json
{
  "overview": {
    "total_customers": 1000,
    "total_products": 100,
    "total_reviews": 4000,
    "average_rating": 3.2
  },
  "sentiment_distribution": {
    "positive": {
      "count": 2000,
      "percentage": 50.0
    },
    "negative": {
      "count": 1200,
      "percentage": 30.0
    },
    "neutral": {
      "count": 800,
      "percentage": 20.0
    }
  },
  "generated_at": "2025-11-05T10:30:00.123456"
}
```

---

## 🔧 Python 코드 예제

### 1. requests 라이브러리 사용

```python
import requests

# 고객 추천 조회
response = requests.get(
    "http://localhost:8000/api/v1/recommend/100",
    params={"top_n": 5, "exclude_purchased": True}
)

if response.status_code == 200:
    data = response.json()
    print(f"고객 {data['customer_id']}의 추천 상품:")
    for rec in data['recommendations']:
        print(f"  - {rec['product_name']} (유사도: {rec['similarity_score']:.4f})")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### 2. 부정 리뷰 분석 조회

```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/negative-analysis",
    params={"top_n": 10}
)

if response.status_code == 200:
    data = response.json()
    print(f"개선 우선순위 상품 Top {data['total_products_analyzed']}:")
    for idx, product in enumerate(data['improvement_priority_list'], 1):
        print(f"{idx}. {product['product_name']}")
        print(f"   부정 키워드: {product['total_negative_keyword_count']}개")
        print(f"   부정 비율: {product['negative_ratio']}%")
```

### 3. 통계 조회

```python
import requests

response = requests.get("http://localhost:8000/api/v1/stats/overview")
data = response.json()

print(f"전체 고객: {data['overview']['total_customers']}명")
print(f"전체 상품: {data['overview']['total_products']}개")
print(f"전체 리뷰: {data['overview']['total_reviews']}개")
print(f"평균 별점: {data['overview']['average_rating']}★")
```

---

## 📝 PowerShell 예제

### 1. 고객 추천 조회
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/recommend/100?top_n=5" -Method Get | ConvertTo-Json -Depth 10
```

### 2. 부정 리뷰 분석
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/negative-analysis?top_n=5" -Method Get | ConvertTo-Json -Depth 10
```

### 3. 헬스 체크
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get | ConvertTo-Json
```

---

## 🌐 JavaScript/Fetch 예제

```javascript
// 고객 추천 조회
async function getRecommendations(customerId, topN = 5) {
  const response = await fetch(
    `http://localhost:8000/api/v1/recommend/${customerId}?top_n=${topN}`
  );
  const data = await response.json();
  
  console.log(`고객 ${data.customer_id}의 추천 상품:`);
  data.recommendations.forEach((rec, idx) => {
    console.log(`${idx + 1}. ${rec.product_name} (유사도: ${rec.similarity_score})`);
  });
}

getRecommendations(100, 5);
```

---

## 🚦 상태 코드

| 상태 코드 | 설명 |
|-----------|------|
| 200 | 성공 |
| 404 | 리소스를 찾을 수 없음 (고객/상품 없음, 리뷰 없음 등) |
| 422 | 유효성 검증 실패 (잘못된 파라미터) |
| 500 | 서버 내부 오류 |

---

## 📊 API 테스트 시나리오

### 시나리오 1: 신규 고객 추천
```bash
# 고객 ID 50에게 추천
curl "http://localhost:8000/api/v1/recommend/50?top_n=5"
```

### 시나리오 2: 개선 우선순위 Top 10 조회
```bash
curl "http://localhost:8000/api/v1/negative-analysis?top_n=10"
```

### 시나리오 3: 특정 상품 프로필 분석
```bash
# 전기히터 (ID: 39) 프로필 조회
curl "http://localhost:8000/api/v1/product/39/profile"
```

### 시나리오 4: 전체 통계 대시보드
```bash
curl "http://localhost:8000/api/v1/stats/overview"
```

---

## 🔒 에러 처리

모든 API는 에러 발생 시 다음 형식으로 응답합니다:

```json
{
  "error": "Error Type",
  "detail": "상세 에러 메시지",
  "timestamp": "2025-11-05T10:30:00.123456"
}
```

---

## 📖 Swagger UI 활용

1. 브라우저에서 http://localhost:8000/docs 접속
2. 각 엔드포인트 펼치기
3. "Try it out" 버튼 클릭
4. 파라미터 입력 후 "Execute" 클릭
5. 응답 확인

---

## 🎯 주요 기능

### ✅ 완료된 기능
- [x] 고객 맞춤 추천 API
- [x] 부정 리뷰 분석 API
- [x] 상품/고객 프로필 조회 API
- [x] 전체 통계 조회 API
- [x] 자동 API 문서 생성 (Swagger/ReDoc)
- [x] 에러 핸들링
- [x] 입력 유효성 검증

### 🔄 개선 가능 항목
- [ ] 인증/인가 (JWT 토큰)
- [ ] Rate Limiting
- [ ] 캐싱 (Redis)
- [ ] 로깅 개선
- [ ] CORS 설정
- [ ] Docker 컨테이너화

---

## 💡 팁

1. **자동 재시작**: `--reload` 옵션으로 코드 변경 시 자동 재시작
2. **포트 변경**: `--port 8080` 옵션으로 포트 변경 가능
3. **API 문서**: Swagger UI에서 직접 API 테스트 가능
4. **프로필 캐싱**: 서버 시작 시 자동으로 프로필 캐시 로드

---

## 📞 문의

API 관련 문의사항이나 버그 리포트는 GitHub Issues에 등록해주세요.
