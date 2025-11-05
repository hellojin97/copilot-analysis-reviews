# 🎯 프로젝트 5단계 로드맵 및 진행 상황

## 📊 프로젝트 개요

**목표**: 부정 키워드 빈도 집계 + 고객-키워드 유사도 기반 추천 시스템 구축

**데이터**: 
- 1,000명 고객
- 100개 상품
- 4,000개 리뷰 (Positive 50%, Negative 30%, Neutral 20%)

---

## 📋 5단계 로드맵

### ✅ **Phase 1: 데이터 분석 및 준비** (완료)

**목표**: 텍스트 정제 및 키워드 추출 시스템 구축

**완료 항목**:
- ✅ CSV → SQLite 데이터베이스 로드
- ✅ `text_cleaner.py` 모듈 구현
  - 한글 형태소 분석 (kiwipiepy)
  - 명사/키워드 추출
  - 감성 키워드 분류
  - 불용어 처리
- ✅ 4,000개 리뷰 키워드 통계 분석

**결과물**:
- `load_csv_to_db_simple.py`
- `text_cleaner.py`
- `test_text_cleaner_with_db.py`
- `data/reviews.db`

---

### ✅ **Phase 2: 부정 리뷰 분석 시스템** (완료)

**목표**: 개선이 필요한 상품 식별

**구현 내용**:
- ✅ 제품별 부정 키워드 빈도 집계
- ✅ 문제점 카테고리별 분류 (품질/배송/가격/서비스/성능/사용성)
- ✅ Top 5 개선 우선순위 상품 자동 리스트업
- ✅ JSON/CSV 리포트 생성

**핵심 함수**:
1. `analyze_negative_keywords_by_product()` - 제품별 부정 키워드 집계
2. `categorize_problems()` - 문제점 카테고리화
3. `get_improvement_priority_products()` - Top N 우선순위 리스트
4. `generate_improvement_report()` - 개선 리포트 생성

**결과물**:
- `analyze_negative_reviews.py`
- `reports/improvement_priority_top5.json`
- `reports/improvement_priority_top5.csv`

**분석 결과**:

| 순위 | 제품명 | 카테고리 | 부정키워드 | 부정리뷰 | 평균별점 | 주요문제 |
|------|--------|----------|------------|----------|----------|----------|
| 1 | 전기히터 | 가전 | 59개 | 24개 (47.1%) | 2.8★ | 실망(12), 아쉬움(9), 망가짐(8) |
| 2 | 냉장고 양문형 | 가전 | 48개 | 19개 (31.7%) | 3.27★ | 실망(9), 소음(9), 시끄러움(6) |
| 3 | 수영복 | 패션 | 46개 | 17개 (39.5%) | 3.16★ | 실망(10), 별로(7), 망가짐(5) |
| 4 | 히터 | 가전 | 46개 | 21개 (41.2%) | 3.04★ | 실망(10), 불편(9), 아쉬움(8) |
| 5 | 무선 충전 패드 | 디지털 | 45개 | 17개 (36.2%) | 3.3★ | 아쉬움(12), 나쁨(7) |

---

### ✅ **Phase 3: 추천 시스템 기초 구축** (완료)

**목표**: 고객 맞춤 상품 추천 엔진

**구현 내용**:
- ✅ 고객 프로필 생성 (긍정 리뷰 기반)
- ✅ 상품 프로필 생성 (긍정 리뷰 기반)
- ✅ 코사인 유사도 계산 알고리즘
- ✅ Top N 추천 상품 반환 API
- ✅ 프로필 캐싱 (성능 최적화)

**핵심 함수**:
1. `build_customer_profile()` - 고객 키워드 프로필 생성
2. `build_product_profile()` - 상품 키워드 프로필 생성
3. `calculate_similarity()` - 코사인 유사도 계산
4. `recommend_products()` - 추천 상품 반환

**알고리즘**:
```
유사도(customer, product) = cos(θ) = (A·B) / (||A|| × ||B||)
- A: 고객 키워드 벡터
- B: 상품 키워드 벡터
- 가중치: 5점 리뷰 = 1.5배, 4점 리뷰 = 1.0배
```

**결과물**:
- `recommendation_system.py`
- `cache/product_profiles.pkl` (100개 상품 프로필)

**추천 예시 (고객 ID 100)**:
1. 커피머신 (유사도: 0.8102, 평균 3.21★)
2. 양말 5족세트 (유사도: 0.8071, 평균 3.4★)
3. 모자 베레 (유사도: 0.7917, 평균 2.88★)
4. 다리미 (유사도: 0.7661, 평균 3.34★)
5. 온수매트 (유사도: 0.7541, 평균 3.54★)

---

### ⏳ **Phase 4: 통합 대시보드** (진행 예정)

**목표**: 분석 결과를 시각적으로 제공

**구현 계획**:
- [ ] Streamlit 웹 애플리케이션 개발
- [ ] 메인 페이지: 전체 리뷰 통계 (긍정/부정/중립 비율)
- [ ] 개선 우선순위 페이지: Top 5 상품 + 워드클라우드
- [ ] 추천 시스템 페이지: 고객 ID 입력 → 추천 상품 목록
- [ ] 상품 상세 페이지: 제품별 키워드 분석 + 감성 트렌드

**예상 결과물**:
- `dashboard.py`
- Streamlit 인터랙티브 웹 대시보드 (4개 페이지)

**예상 소요 시간**: 2-3일

---

### ⏳ **Phase 5: 최적화 및 자동화** (진행 예정)

**목표**: 프로덕션 레벨 완성도

**구현 계획**:
- [ ] 성능 최적화
  - 키워드 캐싱
  - 데이터베이스 인덱싱
  - 벡터화 사전 계산
- [ ] 배치 프로세싱
  - 주기적 키워드 재분석 스케줄러
  - 신규 리뷰 자동 처리
- [ ] API 서버
  - Flask REST API
  - `/api/recommend` 추천 엔드포인트
  - `/api/negative-analysis` 분석 엔드포인트
- [ ] 테스트 코드
  - pytest 단위 테스트
  - 통합 테스트
- [ ] 문서화
  - API 문서 (Swagger)
  - 사용자 가이드

**예상 결과물**:
- `tests/` 디렉토리 (단위 테스트)
- `api_server.py` (Flask API)
- `scheduler.py` (배치 작업)
- `README_API.md` (API 문서)

**예상 소요 시간**: 1-2일

---

## 🛠️ 기술 스택

### 언어 및 프레임워크
- **Python**: 3.12.11
- **Database**: SQLite
- **Dashboard**: Streamlit (예정)
- **API**: Flask (예정)

### 주요 라이브러리
- **kiwipiepy**: 0.21.0 (한글 형태소 분석)
- **scikit-learn**: 1.6.1 (코사인 유사도 계산)
- **pandas**: 2.3.3 (데이터 처리)
- **numpy**: 2.3.4 (수치 계산)
- **matplotlib**: 3.10.7 (시각화)
- **seaborn**: 0.13.2 (통계 시각화)
- **wordcloud**: 1.9.4 (워드클라우드)
- **plotly**: 6.4.0 (인터랙티브 차트)

---

## 📁 프로젝트 구조

```
.
├── data/
│   └── reviews.db                          # SQLite 데이터베이스
├── csv/
│   ├── customers.csv                       # 고객 데이터
│   ├── products.csv                        # 상품 데이터
│   └── reviews.csv                         # 리뷰 데이터
├── reports/
│   ├── improvement_priority_top5.json      # 개선 우선순위 (JSON)
│   └── improvement_priority_top5.csv       # 개선 우선순위 (CSV)
├── cache/
│   └── product_profiles.pkl                # 상품 프로필 캐시
├── text_cleaner.py                         # 텍스트 정제 모듈
├── analyze_negative_reviews.py             # 부정 리뷰 분석 (Phase 2)
├── recommendation_system.py                # 추천 시스템 (Phase 3)
├── load_csv_to_db_simple.py               # CSV → DB 로드
├── query_db_examples.py                    # DB 쿼리 예제
└── test_text_cleaner_with_db.py           # 텍스트 정제 테스트
```

---

## 🎯 주요 성과

### Phase 2: 부정 리뷰 분석
✅ **1,200개 부정 리뷰 분석 완료**
✅ **100개 제품의 부정 키워드 집계**
✅ **6가지 문제 카테고리 자동 분류**
  - 품질, 배송, 가격, 서비스, 성능, 사용성

### Phase 3: 추천 시스템
✅ **100개 상품 프로필 생성**
✅ **고객별 맞춤 추천 알고리즘 구현**
✅ **코사인 유사도 기반 추천 (최대 0.81 유사도)**
✅ **이미 구매한 상품 자동 제외**

---

## 📈 핵심 인사이트

### 1. 개선이 가장 시급한 제품
- **전기히터** (부정 비율 47.1%)
  - 주요 문제: 내구성 (망가짐 8회)
  - 개선 방향: 품질 관리 강화

### 2. 부정 리뷰 패턴
- 가전 제품: 소음, 발열 문제 빈번
- 패션 제품: 내구성, 품질 불만
- 디지털 제품: 성능, 사용성 이슈

### 3. 추천 시스템 효과
- 고객 선호 키워드 기반 유사 상품 추천
- 평균 유사도 0.5~0.8 (높은 관련성)
- Cold Start 문제: 리뷰 없는 고객은 추천 불가

---

## 🔄 다음 단계

### 즉시 시작 가능
1. **Phase 4 대시보드 개발**
   - Streamlit 설치 및 기본 구조 설정
   - 4개 페이지 레이아웃 디자인
   - Phase 2/3 결과 시각화

2. **워드클라우드 생성**
   - 긍정/부정 키워드 워드클라우드
   - 제품별 키워드 시각화

### 추후 진행
3. **Phase 5 최적화**
   - 성능 프로파일링
   - API 서버 구축
   - 자동화 스케줄러

---

## 💻 실행 방법

### Phase 2: 부정 리뷰 분석
```bash
python analyze_negative_reviews.py
```
→ `reports/improvement_priority_top5.json` 생성

### Phase 3: 추천 시스템
```bash
python recommendation_system.py
```
→ `cache/product_profiles.pkl` 생성 + 샘플 추천 출력

### 추천 시스템 API 사용 예제
```python
from recommendation_system import RecommendationSystem

recommender = RecommendationSystem()
recommender.load_profiles()  # 캐시 로드

# 고객 ID 100에게 상품 5개 추천
recommendations = recommender.recommend_products(
    customer_id=100, 
    top_n=5,
    exclude_purchased=True
)

for rec in recommendations:
    print(f"{rec['product_name']}: {rec['similarity_score']:.4f}")
```

---

## 📝 주요 학습 포인트

### 1. 한글 NLP
- kiwipiepy를 활용한 형태소 분석
- 한글 불용어 처리
- 감성 키워드 사전 구축

### 2. 추천 시스템
- 코사인 유사도 알고리즘
- 고객/상품 프로필링
- Cold Start 문제 대응

### 3. 데이터 분석
- 키워드 빈도 분석
- 카테고리별 문제점 분류
- 우선순위 자동 리스트업

### 4. 성능 최적화
- 프로필 캐싱 (pickle)
- 벡터화 사전 계산
- 데이터베이스 쿼리 최적화

---

## 🎉 결론

**Phase 1~3 완료** ✅
- 텍스트 정제 시스템 구축
- 부정 리뷰 분석 및 개선 우선순위 도출
- 고객 맞춤 추천 시스템 구현

**다음 목표**: Streamlit 대시보드 개발 (Phase 4)

전체적으로 체계적인 5단계 로드맵을 바탕으로 순조롭게 진행 중이며,
Phase 4 대시보드만 구현하면 실용적인 리뷰 분석 시스템이 완성됩니다! 🚀
