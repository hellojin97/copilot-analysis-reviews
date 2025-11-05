# CSV to Database 프로젝트

CSV 파일을 SQLite 데이터베이스에 로드하는 프로젝트입니다.

## 프로젝트 구조

```text
110305-analysis-reviews/
├── csv/                         # CSV 데이터 파일
│   ├── customers.csv           # 고객 데이터 (1,000명)
│   ├── products.csv            # 상품 데이터 (100개)
│   └── reviews.csv             # 리뷰 데이터 (4,000개)
├── data/                        # 데이터베이스 저장 디렉토리
│   └── reviews.db              # SQLite 데이터베이스
├── load_csv_to_db_simple.py    # CSV → DB 로드 스크립트 (표준 라이브러리)
├── load_csv_to_db.py           # CSV → DB 로드 스크립트 (Flask + SQLAlchemy)
├── query_db_examples.py        # 데이터베이스 조회 예제
├── requirements.txt            # Python 패키지 의존성
└── README.md                   # 프로젝트 설명서
```

## 데이터베이스 스키마

### 1. customers 테이블

- `customer_id` (INTEGER, PRIMARY KEY): 고객 ID
- `name` (TEXT): 고객 이름
- `age_group` (TEXT): 연령대 (20대, 30대, 40대, 50대)
- `gender` (TEXT): 성별 (M: 남성, F: 여성)
- `join_date` (DATE): 가입일

### 2. products 테이블

- `product_id` (INTEGER, PRIMARY KEY): 상품 ID
- `product_name` (TEXT): 상품명
- `category` (TEXT): 카테고리 (가전, 패션, 디지털)
- `price` (INTEGER): 가격

### 3. reviews 테이블

- `review_id` (TEXT, PRIMARY KEY): 리뷰 ID
- `customer_id` (INTEGER, FOREIGN KEY): 고객 ID
- `product_id` (INTEGER, FOREIGN KEY): 상품 ID
- `rating` (INTEGER): 평점 (1-5)
- `review_text` (TEXT): 리뷰 내용
- `review_date` (DATE): 리뷰 작성일
- `sentiment` (TEXT): 감성 분석 결과 (Positive, Negative, Neutral)

## 사용 방법

### 1. CSV 데이터를 데이터베이스에 로드

```powershell
# 표준 라이브러리만 사용하는 방법 (추천)
python load_csv_to_db_simple.py
```

실행 결과:

```text
============================================================
CSV 데이터를 데이터베이스에 로드합니다.
============================================================
데이터베이스 테이블을 생성합니다...
✓ 테이블 생성 완료

============================================================
Loading customers from ...\csv\customers.csv...
✓ 1000개의 고객 데이터가 성공적으로 로드되었습니다.

============================================================
Loading products from ...\csv\products.csv...
✓ 100개의 상품 데이터가 성공적으로 로드되었습니다.

============================================================
Loading reviews from ...\csv\reviews.csv...
✓ 4000개의 리뷰 데이터가 성공적으로 로드되었습니다.

============================================================
데이터 로드 결과 요약
============================================================
고객 수: 1000명
상품 수: 100개
리뷰 수: 4000개

✓ 모든 데이터가 성공적으로 로드되었습니다!
데이터베이스 위치: ...\data\reviews.db
```

### 2. 데이터베이스 조회 예제 실행

```powershell
python query_db_examples.py
```

다음과 같은 예제 조회를 실행합니다:

- 전체 고객 수 조회
- 카테고리별 상품 수 조회
- 평점별 리뷰 분포 조회
- 감성 분석 결과 조회
- 평균 평점이 가장 높은 상품 TOP 5
- 성별 고객 수 조회
- 연령대별 평균 평점

### 3. Flask + SQLAlchemy를 사용하는 방법

Flask와 SQLAlchemy를 사용하려면:

```powershell
# 패키지 설치
pip install Flask Flask-SQLAlchemy pandas

# 스크립트 실행
python load_csv_to_db.py
```

## 데이터베이스 접근 예제

### Python에서 직접 접근

```python
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('data/reviews.db')
cursor = conn.cursor()

# 쿼리 실행
cursor.execute("SELECT * FROM customers LIMIT 5")
results = cursor.fetchall()

for row in results:
    print(row)

# 연결 종료
conn.close()
```

### SQLAlchemy ORM 사용

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/reviews.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # ... 다른 컬럼들

with app.app_context():
    # 모든 고객 조회
    customers = Customer.query.all()
    
    # 특정 고객 조회
    customer = Customer.query.filter_by(customer_id=1).first()
    
    # 이름으로 검색
    results = Customer.query.filter(Customer.name.like('%김%')).all()
```

## 보안 주의사항

1. **SQL 인젝션 방지**
   - 파라미터화된 쿼리 또는 ORM 사용
   - 사용자 입력을 직접 SQL 문자열에 삽입하지 않음

2. **사용자 입력 검증**
   - 모든 외부 입력은 유효성 검사 필수
   - 파일 업로드 시 `secure_filename()` 사용

3. **비밀 정보 관리**
   - 데이터베이스 비밀번호는 환경 변수로 관리
   - 소스 코드에 하드코딩 금지

## 데이터 통계

### 데이터 로드 결과

- **고객 수**: 1,000명
- **상품 수**: 100개
- **리뷰 수**: 4,000개

### 카테고리별 상품 분포

- **가전**: 40개 (40%)
- **패션**: 30개 (30%)
- **디지털**: 30개 (30%)

### 평점 분포

- **5점**: 982개 (24.6%)
- **4점**: 1,018개 (25.5%)
- **3점**: 800개 (20.0%)
- **2점**: 625개 (15.6%)
- **1점**: 575개 (14.4%)

### 감성 분석 결과

- **Positive (긍정)**: 2,000개 (50.0%)
- **Negative (부정)**: 1,200개 (30.0%)
- **Neutral (중립)**: 800개 (20.0%)

## 참고 사항

- SQLite 데이터베이스는 `data/reviews.db` 파일에 저장됩니다.
- 스크립트를 다시 실행하면 기존 데이터베이스가 삭제되고 새로 생성됩니다.
- 데이터베이스 파일은 DB Browser for SQLite 등의 도구로 직접 확인할 수 있습니다.

## 라이센스

이 프로젝트는 교육 목적으로 작성되었습니다.
