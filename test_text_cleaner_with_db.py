"""
데이터베이스 리뷰 데이터로 텍스트 정제 테스트

실제 리뷰 데이터를 불러와서 텍스트 정제 기능을 테스트합니다.
"""
import sqlite3
from text_cleaner import KoreanTextCleaner


def test_with_real_reviews(limit: int = 10):
    """
    실제 리뷰 데이터로 텍스트 정제 테스트
    
    Args:
        limit (int): 테스트할 리뷰 개수
    """
    print("=" * 80)
    print(f"데이터베이스 리뷰 {limit}개 텍스트 정제 테스트")
    print("=" * 80)
    
    # 데이터베이스 연결
    db_path = 'data/reviews.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 리뷰 데이터 가져오기 (각 감성별로)
    query = """
    SELECT review_id, product_id, rating, review_text, sentiment
    FROM reviews
    WHERE sentiment = ?
    LIMIT ?
    """
    
    # 텍스트 정제기 초기화
    cleaner = KoreanTextCleaner()
    print()
    
    sentiments = ['Positive', 'Negative', 'Neutral']
    reviews_per_sentiment = limit // len(sentiments)
    
    for sentiment in sentiments:
        print(f"\n{'=' * 80}")
        print(f"[{sentiment} 리뷰 분석]")
        print(f"{'=' * 80}")
        
        cursor.execute(query, (sentiment, reviews_per_sentiment))
        reviews = cursor.fetchall()
        
        for idx, (review_id, product_id, rating, review_text, sentiment_label) in enumerate(reviews, 1):
            print(f"\n{'-' * 80}")
            print(f"리뷰 #{review_id} (상품 ID: {product_id}, 별점: {rating}, 감성: {sentiment_label})")
            print(f"{'-' * 80}")
            print(f"원본 리뷰:")
            print(f"  {review_text}")
            print()
            
            # 1. 명사 추출
            nouns = cleaner.extract_nouns(review_text)
            print(f"📌 명사 추출 ({len(nouns)}개):")
            print(f"  {', '.join(nouns[:15])}")  # 처음 15개만
            if len(nouns) > 15:
                print(f"  ... 외 {len(nouns) - 15}개")
            print()
            
            # 2. 키워드 추출
            keywords = cleaner.extract_keywords(review_text)
            print(f"🔑 키워드 추출 ({len(keywords)}개):")
            print(f"  {', '.join(keywords[:15])}")  # 처음 15개만
            if len(keywords) > 15:
                print(f"  ... 외 {len(keywords) - 15}개")
            print()
            
            # 3. 감성 키워드
            sentiment_keywords = cleaner.get_sentiment_keywords(review_text)
            print(f"😊 긍정 키워드: {', '.join(sentiment_keywords['positive']) if sentiment_keywords['positive'] else '없음'}")
            print(f"😞 부정 키워드: {', '.join(sentiment_keywords['negative']) if sentiment_keywords['negative'] else '없음'}")
    
    conn.close()
    
    print(f"\n{'=' * 80}")
    print("✓ 테스트 완료!")
    print(f"{'=' * 80}")


def analyze_keyword_statistics(top_n: int = 20):
    """
    전체 리뷰의 키워드 통계 분석
    
    Args:
        top_n (int): 상위 몇 개 키워드를 표시할지
    """
    print("\n" + "=" * 80)
    print("전체 리뷰 키워드 통계 분석")
    print("=" * 80)
    
    # 데이터베이스 연결
    db_path = 'data/reviews.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 모든 리뷰 가져오기
    cursor.execute("SELECT review_text, sentiment FROM reviews")
    reviews = cursor.fetchall()
    
    print(f"\n총 {len(reviews)}개 리뷰 분석 중...")
    
    # 텍스트 정제기 초기화
    cleaner = KoreanTextCleaner()
    
    # 감성별 키워드 수집
    sentiment_keywords = {
        'Positive': {},
        'Negative': {},
        'Neutral': {}
    }
    
    for review_text, sentiment in reviews:
        keywords = cleaner.extract_keywords(review_text)
        
        for keyword in keywords:
            if keyword in sentiment_keywords[sentiment]:
                sentiment_keywords[sentiment][keyword] += 1
            else:
                sentiment_keywords[sentiment][keyword] = 1
    
    # 감성별 상위 키워드 출력
    for sentiment, keywords_dict in sentiment_keywords.items():
        print(f"\n{'-' * 80}")
        print(f"[{sentiment} 리뷰 상위 키워드 TOP {top_n}]")
        print(f"{'-' * 80}")
        
        # 빈도순으로 정렬
        sorted_keywords = sorted(keywords_dict.items(), key=lambda x: x[1], reverse=True)
        
        for rank, (keyword, count) in enumerate(sorted_keywords[:top_n], 1):
            bar = '█' * min(50, count // 10)  # 시각화 바
            print(f"{rank:2d}. {keyword:15s} {count:4d}회  {bar}")
    
    conn.close()
    
    print(f"\n{'=' * 80}")
    print("✓ 통계 분석 완료!")
    print(f"{'=' * 80}")


if __name__ == '__main__':
    # 1. 샘플 리뷰로 상세 테스트
    test_with_real_reviews(limit=9)
    
    # 2. 전체 키워드 통계 분석
    analyze_keyword_statistics(top_n=20)
