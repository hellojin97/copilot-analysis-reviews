"""
추천 시스템 기초 구축 (Phase 3)

고객-키워드 유사도 기반 상품 추천 시스템을 구현합니다.
"""
import sqlite3
import pickle
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_cleaner import KoreanTextCleaner


class RecommendationSystem:
    """추천 시스템 클래스"""
    
    def __init__(self, db_path: str = 'data/reviews.db'):
        """
        RecommendationSystem 초기화
        
        Args:
            db_path (str): 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self.cleaner = KoreanTextCleaner()
        self.customer_profiles = {}
        self.product_profiles = {}
        self.vectorizer = None
        self.product_vectors = None
        self.product_ids = []
    
    def build_customer_profile(self, customer_id: int) -> Dict[str, float]:
        """
        고객 프로필 생성 (긍정 리뷰 기반)
        
        Args:
            customer_id (int): 고객 ID
            
        Returns:
            Dict[str, float]: {keyword: weight} 딕셔너리
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 고객의 긍정 리뷰 추출 (별점 4점 이상 또는 Positive 감성)
        query = """
        SELECT review_text, rating
        FROM reviews
        WHERE customer_id = ?
        AND (rating >= 4 OR sentiment = 'Positive')
        """
        
        cursor.execute(query, (customer_id,))
        positive_reviews = cursor.fetchall()
        
        conn.close()
        
        # 키워드 빈도 계산
        keyword_freq = defaultdict(int)
        
        for review_text, rating in positive_reviews:
            keywords = self.cleaner.extract_keywords(review_text)
            
            # 별점에 따라 가중치 부여 (5점: 1.5배, 4점: 1.0배)
            weight = 1.5 if rating == 5 else 1.0
            
            for keyword in keywords:
                keyword_freq[keyword] += weight
        
        # 정규화 (총합으로 나눔)
        total = sum(keyword_freq.values())
        if total > 0:
            keyword_profile = {k: v / total for k, v in keyword_freq.items()}
        else:
            keyword_profile = {}
        
        return keyword_profile
    
    def build_product_profile(self, product_id: int) -> Dict[str, float]:
        """
        상품 프로필 생성 (긍정 리뷰 기반)
        
        Args:
            product_id (int): 상품 ID
            
        Returns:
            Dict[str, float]: {keyword: weight} 딕셔너리
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 상품의 긍정 리뷰 추출
        query = """
        SELECT review_text, rating
        FROM reviews
        WHERE product_id = ?
        AND (rating >= 4 OR sentiment = 'Positive')
        """
        
        cursor.execute(query, (product_id,))
        positive_reviews = cursor.fetchall()
        
        conn.close()
        
        # 키워드 빈도 계산
        keyword_freq = defaultdict(int)
        
        for review_text, rating in positive_reviews:
            keywords = self.cleaner.extract_keywords(review_text)
            
            # 별점에 따라 가중치
            weight = 1.5 if rating == 5 else 1.0
            
            for keyword in keywords:
                keyword_freq[keyword] += weight
        
        # 정규화
        total = sum(keyword_freq.values())
        if total > 0:
            keyword_profile = {k: v / total for k, v in keyword_freq.items()}
        else:
            keyword_profile = {}
        
        return keyword_profile
    
    def build_all_product_profiles(self) -> Dict[int, Dict[str, float]]:
        """
        모든 상품의 프로필을 사전 계산
        
        Returns:
            Dict[int, Dict[str, float]]: {product_id: keyword_profile}
        """
        print("=" * 80)
        print("전체 상품 프로필 생성 중...")
        print("=" * 80)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 모든 상품 ID 가져오기
        cursor.execute("SELECT product_id FROM products")
        product_ids = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        print(f"총 {len(product_ids)}개 상품 프로필 생성 시작...")
        
        product_profiles = {}
        for idx, product_id in enumerate(product_ids, 1):
            product_profiles[product_id] = self.build_product_profile(product_id)
            
            if idx % 20 == 0:
                print(f"  진행률: {idx}/{len(product_ids)} ({idx/len(product_ids)*100:.1f}%)")
        
        print(f"✓ {len(product_profiles)}개 상품 프로필 생성 완료")
        
        self.product_profiles = product_profiles
        return product_profiles
    
    def calculate_similarity(self, customer_profile: Dict[str, float], 
                           product_profile: Dict[str, float]) -> float:
        """
        고객과 상품의 키워드 프로필 유사도 계산 (코사인 유사도)
        
        Args:
            customer_profile: 고객 키워드 프로필
            product_profile: 상품 키워드 프로필
            
        Returns:
            float: 유사도 (0~1)
        """
        # 전체 키워드 집합
        all_keywords = set(customer_profile.keys()) | set(product_profile.keys())
        
        if not all_keywords:
            return 0.0
        
        # 벡터 생성
        customer_vector = np.array([customer_profile.get(k, 0.0) for k in all_keywords])
        product_vector = np.array([product_profile.get(k, 0.0) for k in all_keywords])
        
        # 코사인 유사도 계산
        dot_product = np.dot(customer_vector, product_vector)
        norm_customer = np.linalg.norm(customer_vector)
        norm_product = np.linalg.norm(product_vector)
        
        if norm_customer == 0 or norm_product == 0:
            return 0.0
        
        similarity = dot_product / (norm_customer * norm_product)
        
        return similarity
    
    def get_purchased_products(self, customer_id: int) -> Set[int]:
        """
        고객이 이미 리뷰를 남긴 상품 ID 집합
        
        Args:
            customer_id (int): 고객 ID
            
        Returns:
            Set[int]: 구매(리뷰 작성) 상품 ID 집합
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT product_id
            FROM reviews
            WHERE customer_id = ?
        """, (customer_id,))
        
        purchased = {row[0] for row in cursor.fetchall()}
        
        conn.close()
        
        return purchased
    
    def recommend_products(self, customer_id: int, top_n: int = 5, 
                          exclude_purchased: bool = True) -> List[Dict]:
        """
        고객에게 상품 추천
        
        Args:
            customer_id (int): 고객 ID
            top_n (int): 추천할 상품 개수
            exclude_purchased (bool): 이미 리뷰 작성한 상품 제외 여부
            
        Returns:
            List[Dict]: 추천 상품 리스트
        """
        print(f"\n{'=' * 80}")
        print(f"고객 ID {customer_id}에게 상품 추천")
        print(f"{'=' * 80}")
        
        # 고객 프로필 생성
        customer_profile = self.build_customer_profile(customer_id)
        
        if not customer_profile:
            print("⚠️  고객의 긍정 리뷰가 없어 추천할 수 없습니다.")
            return []
        
        print(f"✓ 고객 프로필 생성 완료 (키워드: {len(customer_profile)}개)")
        
        # 이미 구매한 상품 제외
        purchased_products = self.get_purchased_products(customer_id) if exclude_purchased else set()
        
        # 전체 상품 프로필이 없으면 생성
        if not self.product_profiles:
            self.build_all_product_profiles()
        
        # 유사도 계산
        print(f"유사도 계산 중...")
        similarities = []
        
        for product_id, product_profile in self.product_profiles.items():
            # 이미 구매한 상품은 제외
            if product_id in purchased_products:
                continue
            
            # 상품에 프로필이 없으면 스킵 (리뷰가 없는 상품)
            if not product_profile:
                continue
            
            similarity = self.calculate_similarity(customer_profile, product_profile)
            similarities.append((product_id, similarity))
        
        # 유사도 기준 정렬
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # 상위 N개 추천
        top_recommendations = similarities[:top_n]
        
        # 상품 정보 조회
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        recommendations = []
        for product_id, similarity_score in top_recommendations:
            cursor.execute("""
                SELECT product_name, category, 
                       (SELECT AVG(rating) FROM reviews WHERE product_id = ?) as avg_rating,
                       (SELECT COUNT(*) FROM reviews WHERE product_id = ?) as review_count
                FROM products
                WHERE product_id = ?
            """, (product_id, product_id, product_id))
            
            result = cursor.fetchone()
            if result:
                product_name, category, avg_rating, review_count = result
                
                # 상품 주요 키워드
                product_keywords = sorted(
                    self.product_profiles[product_id].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
                
                recommendations.append({
                    'product_id': product_id,
                    'product_name': product_name,
                    'category': category,
                    'similarity_score': round(similarity_score, 4),
                    'average_rating': round(avg_rating, 2) if avg_rating else 0,
                    'review_count': review_count,
                    'top_keywords': [
                        {'keyword': k, 'weight': round(w, 4)} 
                        for k, w in product_keywords
                    ]
                })
        
        conn.close()
        
        print(f"✓ 추천 완료: {len(recommendations)}개 상품")
        
        return recommendations
    
    def save_profiles(self, customer_profile_path: str = 'cache/customer_profiles.pkl',
                     product_profile_path: str = 'cache/product_profiles.pkl'):
        """
        프로필을 파일로 저장 (캐싱)
        
        Args:
            customer_profile_path: 고객 프로필 저장 경로
            product_profile_path: 상품 프로필 저장 경로
        """
        import os
        os.makedirs('cache', exist_ok=True)
        
        # 상품 프로필 저장
        with open(product_profile_path, 'wb') as f:
            pickle.dump(self.product_profiles, f)
        
        print(f"✓ 상품 프로필 저장: {product_profile_path}")
    
    def load_profiles(self, product_profile_path: str = 'cache/product_profiles.pkl'):
        """
        저장된 프로필 로드
        
        Args:
            product_profile_path: 상품 프로필 파일 경로
        """
        import os
        
        if os.path.exists(product_profile_path):
            with open(product_profile_path, 'rb') as f:
                self.product_profiles = pickle.load(f)
            print(f"✓ 상품 프로필 로드: {len(self.product_profiles)}개")
        else:
            print("⚠️  저장된 프로필이 없습니다. 새로 생성합니다.")
            self.build_all_product_profiles()


def main():
    """메인 실행 함수"""
    print("=" * 80)
    print("추천 시스템 기초 구축 (Phase 3)")
    print("=" * 80)
    
    # 추천 시스템 초기화
    recommender = RecommendationSystem()
    
    # 전체 상품 프로필 생성
    recommender.build_all_product_profiles()
    
    # 프로필 저장
    recommender.save_profiles()
    
    # 테스트: 랜덤 고객에게 추천
    print("\n" + "=" * 80)
    print("추천 시스템 테스트")
    print("=" * 80)
    
    # 샘플 고객 ID (1, 50, 100)
    test_customer_ids = [1, 50, 100]
    
    for customer_id in test_customer_ids:
        recommendations = recommender.recommend_products(customer_id, top_n=5)
        
        if recommendations:
            print(f"\n고객 ID {customer_id}의 추천 상품:")
            print("-" * 80)
            for rank, rec in enumerate(recommendations, 1):
                print(f"{rank}. {rec['product_name']} ({rec['category']})")
                print(f"   유사도: {rec['similarity_score']:.4f} | "
                      f"평균 별점: {rec['average_rating']}★ | "
                      f"리뷰: {rec['review_count']}개")
                keywords = ', '.join([k['keyword'] for k in rec['top_keywords'][:3]])
                print(f"   주요 키워드: {keywords}")
    
    print("\n" + "=" * 80)
    print("✅ Phase 3 완료: 추천 시스템 구축 완료!")
    print("=" * 80)
    print("\n생성된 파일:")
    print("  - cache/product_profiles.pkl (상품 프로필 캐시)")


if __name__ == '__main__':
    main()
