"""
부정 리뷰 분석 시스템 (Phase 2)

제품별 부정 키워드를 집계하여 개선이 필요한 상품을 식별합니다.
"""
import sqlite3
import json
import csv
from collections import defaultdict
from typing import Dict, List, Tuple
from src.text_cleaner import KoreanTextCleaner


class NegativeReviewAnalyzer:
    """부정 리뷰 분석 클래스"""
    
    def __init__(self, db_path: str = 'data/reviews.db'):
        """
        NegativeReviewAnalyzer 초기화
        
        Args:
            db_path (str): 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self.cleaner = KoreanTextCleaner()
        
        # 문제점 카테고리 사전
        self.problem_categories = {
            '품질': ['고장', '망가지', '불량', '내구', '품질', '내구성', '튼튼', '약하', '부서지'],
            '배송': ['늦', '지연', '포장', '파손', '배송', '배달', '택배', '상자', '찌그러지'],
            '가격': ['비싸', '가성비', '가격', '비용', '돈', '저렴', '비싸다'],
            '서비스': ['불친절', '응답', '환불', '교환', '서비스', '고객센터', 'CS', '친절'],
            '성능': ['느리', '소음', '발열', '성능', '속도', '시끄럽', '뜨겁', '작동'],
            '사용성': ['불편', '복잡', '사용', '어렵', '불편하', '조작', '설명서']
        }
    
    def analyze_negative_keywords_by_product(self) -> Dict[int, Dict[str, int]]:
        """
        제품별 부정 키워드 빈도 집계
        
        Returns:
            Dict[int, Dict[str, int]]: {product_id: {keyword: count}}
        """
        print("=" * 80)
        print("제품별 부정 키워드 분석 시작")
        print("=" * 80)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 부정 리뷰 추출
        query = """
        SELECT review_id, product_id, review_text
        FROM reviews
        WHERE sentiment = 'Negative'
        """
        
        cursor.execute(query)
        negative_reviews = cursor.fetchall()
        
        print(f"\n총 {len(negative_reviews)}개의 부정 리뷰를 분석합니다...")
        
        # 제품별 부정 키워드 집계
        product_negative_keywords = defaultdict(lambda: defaultdict(int))
        
        for review_id, product_id, review_text in negative_reviews:
            # 부정 키워드 추출
            sentiment_keywords = self.cleaner.get_sentiment_keywords(review_text)
            negative_keywords = sentiment_keywords['negative']
            
            # 부정 키워드가 없으면 모든 키워드 추출
            if not negative_keywords:
                all_keywords = self.cleaner.extract_keywords(review_text)
                negative_keywords = all_keywords[:5]  # 상위 5개만
            
            # 제품별로 키워드 카운트
            for keyword in negative_keywords:
                product_negative_keywords[product_id][keyword] += 1
        
        conn.close()
        
        print(f"✓ {len(product_negative_keywords)}개 제품의 부정 키워드 분석 완료")
        
        return dict(product_negative_keywords)
    
    def categorize_problems(self, keywords: Dict[str, int]) -> Dict[str, List[Tuple[str, int]]]:
        """
        부정 키워드를 문제점 카테고리별로 분류
        
        Args:
            keywords (Dict[str, int]): {keyword: count}
            
        Returns:
            Dict[str, List[Tuple[str, int]]]: {category: [(keyword, count), ...]}
        """
        categorized = defaultdict(list)
        uncategorized = []
        
        for keyword, count in keywords.items():
            found = False
            for category, category_keywords in self.problem_categories.items():
                # 카테고리 키워드에 부분 매칭
                if any(cat_keyword in keyword for cat_keyword in category_keywords):
                    categorized[category].append((keyword, count))
                    found = True
                    break
            
            if not found:
                uncategorized.append((keyword, count))
        
        # 미분류 항목도 추가
        if uncategorized:
            categorized['기타'] = uncategorized
        
        # 각 카테고리 내에서 빈도순 정렬
        for category in categorized:
            categorized[category].sort(key=lambda x: x[1], reverse=True)
        
        return dict(categorized)
    
    def get_improvement_priority_products(self, top_n: int = 5) -> List[Dict]:
        """
        개선 우선순위 상품 Top N 리스트업
        
        Args:
            top_n (int): 상위 몇 개 제품을 반환할지
            
        Returns:
            List[Dict]: 개선 우선순위 상품 리스트
        """
        print("\n" + "=" * 80)
        print(f"개선 우선순위 상품 Top {top_n} 분석")
        print("=" * 80)
        
        # 제품별 부정 키워드 집계
        product_keywords = self.analyze_negative_keywords_by_product()
        
        # 제품 정보 가져오기
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        priority_list = []
        
        for product_id, keywords in product_keywords.items():
            # 총 부정 키워드 빈도
            total_negative_count = sum(keywords.values())
            
            # 제품 정보 조회
            cursor.execute("""
                SELECT product_name, category
                FROM products
                WHERE product_id = ?
            """, (product_id,))
            
            product_info = cursor.fetchone()
            if not product_info:
                continue
            
            product_name, category = product_info
            
            # 평균 별점 및 리뷰 수 조회
            cursor.execute("""
                SELECT AVG(rating), COUNT(*), 
                       SUM(CASE WHEN sentiment = 'Negative' THEN 1 ELSE 0 END)
                FROM reviews
                WHERE product_id = ?
            """, (product_id,))
            
            avg_rating, review_count, negative_count = cursor.fetchone()
            
            # 문제점 카테고리화
            categorized_problems = self.categorize_problems(keywords)
            
            # 주요 문제점 (빈도 Top 5)
            top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:5]
            
            priority_list.append({
                'product_id': product_id,
                'product_name': product_name,
                'category': category,
                'total_negative_keyword_count': total_negative_count,
                'negative_review_count': negative_count,
                'total_review_count': review_count,
                'average_rating': round(avg_rating, 2),
                'negative_ratio': round(negative_count / review_count * 100, 1),
                'top_negative_keywords': [
                    {'keyword': k, 'count': c} for k, c in top_keywords
                ],
                'problem_categories': {
                    cat: [{'keyword': k, 'count': c} for k, c in items[:3]]
                    for cat, items in categorized_problems.items()
                }
            })
        
        conn.close()
        
        # 총 부정 키워드 빈도로 정렬
        priority_list.sort(key=lambda x: x['total_negative_keyword_count'], reverse=True)
        
        return priority_list[:top_n]
    
    def generate_improvement_report(self, top_n: int = 5, 
                                   output_json: str = 'reports/improvement_priority_top5.json',
                                   output_csv: str = 'reports/improvement_priority_top5.csv'):
        """
        개선 리포트 생성
        
        Args:
            top_n (int): 상위 몇 개 제품을 포함할지
            output_json (str): JSON 출력 파일 경로
            output_csv (str): CSV 출력 파일 경로
        """
        import os
        
        # reports 디렉토리 생성
        os.makedirs('reports', exist_ok=True)
        
        # 개선 우선순위 상품 분석
        priority_products = self.get_improvement_priority_products(top_n)
        
        # JSON 저장
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': '2025-11-05',
                'total_products_analyzed': len(priority_products),
                'improvement_priority_list': priority_products
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ JSON 리포트 저장: {output_json}")
        
        # CSV 저장 (간소화 버전)
        with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                '순위', '제품ID', '제품명', '카테고리', 
                '부정키워드수', '부정리뷰수', '전체리뷰수', 
                '평균별점', '부정비율(%)', '주요문제키워드'
            ])
            
            for rank, product in enumerate(priority_products, 1):
                top_keywords_str = ', '.join([
                    f"{k['keyword']}({k['count']})" 
                    for k in product['top_negative_keywords']
                ])
                
                writer.writerow([
                    rank,
                    product['product_id'],
                    product['product_name'],
                    product['category'],
                    product['total_negative_keyword_count'],
                    product['negative_review_count'],
                    product['total_review_count'],
                    product['average_rating'],
                    product['negative_ratio'],
                    top_keywords_str
                ])
        
        print(f"✓ CSV 리포트 저장: {output_csv}")
        
        # 콘솔 출력
        self._print_priority_summary(priority_products)
    
    def _print_priority_summary(self, priority_products: List[Dict]):
        """개선 우선순위 요약 출력"""
        print("\n" + "=" * 80)
        print("🚨 개선 우선순위 상품 Top 5")
        print("=" * 80)
        
        for rank, product in enumerate(priority_products, 1):
            print(f"\n[{rank}위] {product['product_name']} (ID: {product['product_id']})")
            print(f"  📁 카테고리: {product['category']}")
            print(f"  ⭐ 평균 별점: {product['average_rating']}점")
            print(f"  📊 부정 리뷰: {product['negative_review_count']}개 / "
                  f"{product['total_review_count']}개 ({product['negative_ratio']}%)")
            print(f"  🔑 부정 키워드: {product['total_negative_keyword_count']}개")
            
            print(f"\n  주요 문제점:")
            for idx, kw in enumerate(product['top_negative_keywords'], 1):
                print(f"    {idx}. {kw['keyword']} ({kw['count']}회)")
            
            print(f"\n  문제 카테고리:")
            for category, keywords in product['problem_categories'].items():
                if keywords:
                    kw_str = ', '.join([f"{k['keyword']}({k['count']})" for k in keywords[:2]])
                    print(f"    - {category}: {kw_str}")
        
        print("\n" + "=" * 80)


def main():
    """메인 실행 함수"""
    print("=" * 80)
    print("부정 리뷰 분석 시스템 (Phase 2)")
    print("=" * 80)
    
    # 분석기 초기화
    analyzer = NegativeReviewAnalyzer()
    
    # 개선 리포트 생성
    analyzer.generate_improvement_report(top_n=5)
    
    print("\n" + "=" * 80)
    print("✅ Phase 2 완료: 개선 우선순위 분석 리포트 생성 완료!")
    print("=" * 80)
    print("\n생성된 파일:")
    print("  - reports/improvement_priority_top5.json")
    print("  - reports/improvement_priority_top5.csv")


if __name__ == '__main__':
    main()
