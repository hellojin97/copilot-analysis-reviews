"""
FastAPI 서버 테스트 스크립트

API 엔드포인트를 테스트하고 결과를 출력합니다.
"""
import requests
import json
import time


def test_health():
    """헬스 체크 테스트"""
    print("\n" + "=" * 80)
    print("1. 헬스 체크 테스트")
    print("=" * 80)
    
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error: {e}")


def test_stats_overview():
    """전체 통계 조회 테스트"""
    print("\n" + "=" * 80)
    print("2. 전체 통계 조회 테스트")
    print("=" * 80)
    
    try:
        response = requests.get("http://localhost:8000/api/v1/stats/overview")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error: {e}")


def test_recommend():
    """고객 추천 테스트"""
    print("\n" + "=" * 80)
    print("3. 고객 추천 테스트 (고객 ID: 100)")
    print("=" * 80)
    
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/recommend/100",
            params={"top_n": 3, "exclude_purchased": True}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n고객 ID: {data['customer_id']}")
            print(f"추천 상품 수: {data['total_count']}\n")
            
            for idx, rec in enumerate(data['recommendations'], 1):
                print(f"{idx}. {rec['product_name']} ({rec['category']})")
                print(f"   유사도: {rec['similarity_score']:.4f}")
                print(f"   평균 별점: {rec['average_rating']}★")
                print(f"   리뷰 수: {rec['review_count']}개")
                keywords = ', '.join([k['keyword'] for k in rec['top_keywords'][:3]])
                print(f"   주요 키워드: {keywords}\n")
        else:
            print("Response:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error: {e}")


def test_negative_analysis():
    """부정 리뷰 분석 테스트"""
    print("\n" + "=" * 80)
    print("4. 부정 리뷰 분석 테스트 (Top 3)")
    print("=" * 80)
    
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/negative-analysis",
            params={"top_n": 3}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n분석된 상품 수: {data['total_products_analyzed']}\n")
            
            for idx, product in enumerate(data['improvement_priority_list'], 1):
                print(f"{idx}. {product['product_name']} (ID: {product['product_id']})")
                print(f"   카테고리: {product['category']}")
                print(f"   평균 별점: {product['average_rating']}★")
                print(f"   부정 키워드: {product['total_negative_keyword_count']}개")
                print(f"   부정 비율: {product['negative_ratio']}%")
                
                print(f"   주요 문제점:")
                for kw in product['top_negative_keywords'][:3]:
                    print(f"     - {kw['keyword']} ({kw['count']}회)")
                print()
        else:
            print("Response:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error: {e}")


def test_product_profile():
    """상품 프로필 조회 테스트"""
    print("\n" + "=" * 80)
    print("5. 상품 프로필 조회 테스트 (상품 ID: 39 - 전기히터)")
    print("=" * 80)
    
    try:
        response = requests.get("http://localhost:8000/api/v1/product/39/profile")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n상품 ID: {data['product_id']}")
            print(f"총 키워드 수: {data['total_keywords']}\n")
            print("주요 키워드:")
            for kw in data['top_keywords'][:10]:
                print(f"  - {kw['keyword']}: {kw['weight']:.4f}")
        else:
            print("Response:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error: {e}")


def test_customer_profile():
    """고객 프로필 조회 테스트"""
    print("\n" + "=" * 80)
    print("6. 고객 프로필 조회 테스트 (고객 ID: 100)")
    print("=" * 80)
    
    try:
        response = requests.get("http://localhost:8000/api/v1/customer/100/profile")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n고객 ID: {data['customer_id']}")
            print(f"총 키워드 수: {data['total_keywords']}\n")
            print("주요 키워드 (선호도):")
            for kw in data['top_keywords'][:10]:
                print(f"  - {kw['keyword']}: {kw['weight']:.4f}")
        else:
            print("Response:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """메인 테스트 실행"""
    print("=" * 80)
    print("FastAPI 서버 테스트")
    print("=" * 80)
    print("서버 주소: http://localhost:8000")
    print("API 문서: http://localhost:8000/docs")
    print("=" * 80)
    
    # 서버가 준비될 때까지 대기
    print("\n서버 연결 대기 중...")
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✓ 서버 연결 성공!\n")
                break
        except:
            if i < max_retries - 1:
                time.sleep(1)
            else:
                print("❌ 서버 연결 실패. api_server.py를 먼저 실행해주세요.")
                return
    
    # 테스트 실행
    test_health()
    test_stats_overview()
    test_recommend()
    test_negative_analysis()
    test_product_profile()
    test_customer_profile()
    
    print("\n" + "=" * 80)
    print("✅ 모든 테스트 완료!")
    print("=" * 80)


if __name__ == "__main__":
    main()
