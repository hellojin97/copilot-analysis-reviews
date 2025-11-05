"""
CSV 파일을 SQLite 데이터베이스에 로드하는 스크립트
Python 표준 라이브러리만 사용
"""
import os
import sqlite3
import csv
from datetime import datetime


def create_database_and_tables(db_path):
    """데이터베이스 생성 및 테이블 생성"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # customers 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age_group TEXT NOT NULL,
            gender TEXT NOT NULL,
            join_date DATE NOT NULL
        )
    """)
    
    # products 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    """)
    
    # reviews 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id TEXT PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            review_text TEXT NOT NULL,
            review_date DATE NOT NULL,
            sentiment TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    """)
    
    conn.commit()
    return conn


def load_customers_from_csv(conn, csv_path):
    """customers.csv를 customers 테이블에 로드"""
    print(f"Loading customers from {csv_path}...")
    
    cursor = conn.cursor()
    count = 0
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO customers (customer_id, name, age_group, gender, join_date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                int(row['customer_id']),
                row['name'],
                row['age_group'],
                row['gender'],
                row['join_date']
            ))
            count += 1
    
    conn.commit()
    print(f"✓ {count}개의 고객 데이터가 성공적으로 로드되었습니다.")


def load_products_from_csv(conn, csv_path):
    """products.csv를 products 테이블에 로드"""
    print(f"Loading products from {csv_path}...")
    
    cursor = conn.cursor()
    count = 0
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO products (product_id, product_name, category, price)
                VALUES (?, ?, ?, ?)
            """, (
                int(row['product_id']),
                row['product_name'],
                row['category'],
                int(row['price'])
            ))
            count += 1
    
    conn.commit()
    print(f"✓ {count}개의 상품 데이터가 성공적으로 로드되었습니다.")


def load_reviews_from_csv(conn, csv_path):
    """reviews.csv를 reviews 테이블에 로드"""
    print(f"Loading reviews from {csv_path}...")
    
    cursor = conn.cursor()
    count = 0
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO reviews (review_id, customer_id, product_id, rating, review_text, review_date, sentiment)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row['review_id'],
                int(row['customer_id']),
                int(row['product_id']),
                int(row['rating']),
                row['review_text'],
                row['review_date'],
                row['sentiment']
            ))
            count += 1
    
    conn.commit()
    print(f"✓ {count}개의 리뷰 데이터가 성공적으로 로드되었습니다.")


def get_table_count(conn, table_name):
    """테이블의 레코드 수 조회"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]


def main():
    """메인 함수"""
    print("=" * 60)
    print("CSV 데이터를 데이터베이스에 로드합니다.")
    print("=" * 60)
    
    # 현재 스크립트의 디렉토리
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # data 디렉토리 생성
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 데이터베이스 파일 경로
    db_path = os.path.join(data_dir, 'reviews.db')
    
    # 기존 데이터베이스 파일이 있으면 삭제 (새로 시작)
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"기존 데이터베이스 삭제: {db_path}")
    
    # 데이터베이스 및 테이블 생성
    print("\n데이터베이스 테이블을 생성합니다...")
    conn = create_database_and_tables(db_path)
    print("✓ 테이블 생성 완료")
    
    # CSV 파일 경로
    csv_dir = os.path.join(base_dir, 'csv')
    customers_csv = os.path.join(csv_dir, 'customers.csv')
    products_csv = os.path.join(csv_dir, 'products.csv')
    reviews_csv = os.path.join(csv_dir, 'reviews.csv')
    
    # CSV 파일 로드
    print("\n" + "=" * 60)
    load_customers_from_csv(conn, customers_csv)
    
    print("\n" + "=" * 60)
    load_products_from_csv(conn, products_csv)
    
    print("\n" + "=" * 60)
    load_reviews_from_csv(conn, reviews_csv)
    
    # 결과 확인
    print("\n" + "=" * 60)
    print("데이터 로드 결과 요약")
    print("=" * 60)
    print(f"고객 수: {get_table_count(conn, 'customers')}명")
    print(f"상품 수: {get_table_count(conn, 'products')}개")
    print(f"리뷰 수: {get_table_count(conn, 'reviews')}개")
    print("\n✓ 모든 데이터가 성공적으로 로드되었습니다!")
    print(f"데이터베이스 위치: {db_path}")
    
    # 연결 종료
    conn.close()


if __name__ == '__main__':
    main()
