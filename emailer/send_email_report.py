"""
원클릭 대시보드 이메일 전송 스크립트

API 서버 없이 직접 데이터를 수집하여 이메일로 전송합니다.
"""
import sqlite3
from datetime import datetime
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from emailer.email_reporter import EmailReporter
from src.recommendation_system import RecommendationSystem
from src.analyze_negative_reviews import NegativeReviewAnalyzer


def collect_data_directly():
    """
    API 서버 없이 직접 데이터 수집
    
    Returns:
        Dict: 수집된 데이터
    """
    print("=" * 80)
    print("데이터 직접 수집 중...")
    print("=" * 80)
    
    data = {}
    
    try:
        # 1. 전체 통계
        print("1. 전체 통계 조회...")
        conn = sqlite3.connect('data/reviews.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT customer_id) as total_customers,
                COUNT(DISTINCT product_id) as total_products,
                COUNT(*) as total_reviews,
                AVG(rating) as avg_rating,
                SUM(CASE WHEN sentiment = 'Positive' THEN 1 ELSE 0 END) as positive_count,
                SUM(CASE WHEN sentiment = 'Negative' THEN 1 ELSE 0 END) as negative_count,
                SUM(CASE WHEN sentiment = 'Neutral' THEN 1 ELSE 0 END) as neutral_count
            FROM reviews
        """)
        
        stats = cursor.fetchone()
        conn.close()
        
        total_customers, total_products, total_reviews, avg_rating, positive, negative, neutral = stats
        
        data['stats'] = {
            "overview": {
                "total_customers": total_customers,
                "total_products": total_products,
                "total_reviews": total_reviews,
                "average_rating": round(avg_rating, 2)
            },
            "sentiment_distribution": {
                "positive": {
                    "count": positive,
                    "percentage": round(positive / total_reviews * 100, 1)
                },
                "negative": {
                    "count": negative,
                    "percentage": round(negative / total_reviews * 100, 1)
                },
                "neutral": {
                    "count": neutral,
                    "percentage": round(neutral / total_reviews * 100, 1)
                }
            }
        }
        print("   ✓ 전체 통계 수집 완료")
        
        # 2. 부정 리뷰 분석
        print("2. 부정 리뷰 분석 수행...")
        analyzer = NegativeReviewAnalyzer()
        priority_products = analyzer.get_improvement_priority_products(top_n=5)
        
        data['negative_analysis'] = {
            "generated_at": datetime.now().isoformat(),
            "total_products_analyzed": len(priority_products),
            "improvement_priority_list": priority_products
        }
        print("   ✓ 부정 리뷰 분석 완료")
        
        # 3. 추천 시스템 (샘플)
        print("3. 추천 시스템 샘플 생성...")
        recommender = RecommendationSystem()
        recommender.load_profiles()
        
        # 고객 ID 100 또는 50으로 시도
        for customer_id in [100, 50, 200, 300]:
            try:
                recommendations = recommender.recommend_products(customer_id, top_n=5)
                if recommendations:
                    data['recommendation_sample'] = {
                        "customer_id": customer_id,
                        "recommendations": recommendations,
                        "total_count": len(recommendations),
                        "generated_at": datetime.now().isoformat()
                    }
                    print(f"   ✓ 추천 샘플 생성 완료 (고객 ID: {customer_id})")
                    break
            except:
                continue
        
        if 'recommendation_sample' not in data:
            print("   ⚠️  추천 샘플을 생성할 수 없습니다.")
        
        print("\n✓ 모든 데이터 수집 완료")
        return data
    
    except Exception as e:
        print(f"❌ 데이터 수집 중 오류: {e}")
        raise


def main():
    """메인 실행 함수"""
    import os
    
    print("=" * 80)
    print("📧 원클릭 대시보드 이메일 전송")
    print("=" * 80)
    
    # 이메일 설정 (환경변수 우선, 없으면 기본값)
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "ilhj1228@gmail.com")
    APP_PASSWORD = os.getenv("APP_PASSWORD", "phoc nhry asbr svnn")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "ilhj1228@gmail.com")
    
    try:
        # 1. 데이터 수집
        data = collect_data_directly()
        
        # 2. EmailReporter 초기화
        reporter = EmailReporter(
            sender_email=SENDER_EMAIL,
            app_password=APP_PASSWORD
        )
        
        # 3. 차트 생성
        from src.chart_generator import ChartGenerator
        print("\n차트 생성 중...")
        generator = ChartGenerator()
        chart_images = generator.create_all_charts(data)
        
        # 4. HTML 리포트 생성
        html_content = reporter.generate_html_report(data, include_charts=True)
        
        # 5. 이메일 전송
        today = datetime.now().strftime("%Y년 %m월 %d일")
        subject = f"[리뷰 분석] 대시보드 리포트 - {today}"
        
        reporter.send_email(
            recipient_email=RECIPIENT_EMAIL,
            subject=subject,
            html_content=html_content,
            attach_json=data,  # JSON 원본 데이터도 첨부
            chart_images=chart_images  # 차트 이미지 첨부
        )
        
        print("\n" + "=" * 80)
        print("🎉 이메일 전송 완료!")
        print("=" * 80)
        print(f"수신자: {RECIPIENT_EMAIL}")
        print(f"제목: {subject}")
        print("=" * 80)
        print("\n이메일함을 확인해주세요!")
        
    except Exception as e:
        print(f"\n❌ 프로그램 종료: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
