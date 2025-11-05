"""
FastAPI 기반 추천 시스템 REST API

Phase 3 추천 시스템을 JSON 형태로 제공하는 RESTful API 서버입니다.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uvicorn
from datetime import datetime
import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.recommendation_system import RecommendationSystem
from src.analyze_negative_reviews import NegativeReviewAnalyzer
from emailer.email_reporter import EmailReporter


# FastAPI 앱 초기화
app = FastAPI(
    title="리뷰 분석 및 추천 시스템 API",
    description="고객 리뷰 분석, 부정 키워드 집계, 상품 추천 기능을 제공하는 REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 전역 인스턴스
recommender = None
analyzer = None


# Pydantic 모델 정의
class RecommendationResponse(BaseModel):
    """추천 응답 모델"""
    customer_id: int
    recommendations: List[Dict]
    total_count: int
    generated_at: str


class NegativeAnalysisResponse(BaseModel):
    """부정 리뷰 분석 응답 모델"""
    generated_at: str
    total_products_analyzed: int
    improvement_priority_list: List[Dict]


class HealthResponse(BaseModel):
    """헬스 체크 응답 모델"""
    status: str
    message: str
    timestamp: str


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    error: str
    detail: str
    timestamp: str


@app.on_event("startup")
async def startup_event():
    """
    서버 시작 시 추천 시스템 및 분석기 초기화
    """
    global recommender, analyzer
    
    print("=" * 80)
    print("추천 시스템 API 서버 초기화 중...")
    print("=" * 80)
    
    # 추천 시스템 초기화
    recommender = RecommendationSystem()
    
    # 캐시된 프로필 로드 (없으면 생성)
    if os.path.exists('cache/product_profiles.pkl'):
        recommender.load_profiles()
        print("✓ 상품 프로필 캐시 로드 완료")
    else:
        print("⚠️  캐시가 없습니다. 상품 프로필을 새로 생성합니다...")
        recommender.build_all_product_profiles()
        recommender.save_profiles()
        print("✓ 상품 프로필 생성 및 저장 완료")
    
    # 부정 리뷰 분석기 초기화
    analyzer = NegativeReviewAnalyzer()
    print("✓ 부정 리뷰 분석기 초기화 완료")
    
    print("=" * 80)
    print("✅ API 서버 준비 완료!")
    print("=" * 80)
    print("📖 API 문서: http://localhost:8000/docs")
    print("📖 ReDoc 문서: http://localhost:8000/redoc")
    print("=" * 80)


@app.get("/", response_model=HealthResponse)
async def root():
    """
    루트 엔드포인트 - API 상태 확인
    """
    return HealthResponse(
        status="running",
        message="리뷰 분석 및 추천 시스템 API가 정상 작동 중입니다.",
        timestamp=datetime.now().isoformat()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    헬스 체크 엔드포인트
    """
    return HealthResponse(
        status="healthy",
        message="모든 시스템이 정상입니다.",
        timestamp=datetime.now().isoformat()
    )


@app.get("/api/v1/recommend/{customer_id}", response_model=RecommendationResponse)
async def get_recommendations(
    customer_id: int,
    top_n: int = Query(default=5, ge=1, le=20, description="추천할 상품 개수 (1-20)"),
    exclude_purchased: bool = Query(default=True, description="이미 리뷰 작성한 상품 제외 여부")
):
    """
    고객 맞춤 상품 추천 API
    
    Args:
        customer_id (int): 고객 ID
        top_n (int): 추천할 상품 개수 (기본값: 5, 최대: 20)
        exclude_purchased (bool): 이미 구매한 상품 제외 여부 (기본값: True)
    
    Returns:
        RecommendationResponse: 추천 상품 목록
    
    Example:
        GET /api/v1/recommend/100?top_n=5&exclude_purchased=true
    """
    try:
        # 추천 실행
        recommendations = recommender.recommend_products(
            customer_id=customer_id,
            top_n=top_n,
            exclude_purchased=exclude_purchased
        )
        
        if not recommendations:
            raise HTTPException(
                status_code=404,
                detail=f"고객 ID {customer_id}에 대한 추천 결과가 없습니다. 긍정 리뷰가 없거나 고객이 존재하지 않을 수 있습니다."
            )
        
        return RecommendationResponse(
            customer_id=customer_id,
            recommendations=recommendations,
            total_count=len(recommendations),
            generated_at=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"추천 처리 중 오류가 발생했습니다: {str(e)}"
        )


@app.get("/api/v1/negative-analysis", response_model=NegativeAnalysisResponse)
async def get_negative_analysis(
    top_n: int = Query(default=5, ge=1, le=50, description="분석할 상품 개수 (1-50)")
):
    """
    부정 리뷰 분석 및 개선 우선순위 상품 API
    
    Args:
        top_n (int): 개선 우선순위 상위 N개 상품 (기본값: 5, 최대: 50)
    
    Returns:
        NegativeAnalysisResponse: 개선 우선순위 상품 목록
    
    Example:
        GET /api/v1/negative-analysis?top_n=10
    """
    try:
        # 부정 리뷰 분석 실행
        priority_products = analyzer.get_improvement_priority_products(top_n=top_n)
        
        if not priority_products:
            raise HTTPException(
                status_code=404,
                detail="부정 리뷰 분석 결과가 없습니다."
            )
        
        return NegativeAnalysisResponse(
            generated_at=datetime.now().isoformat(),
            total_products_analyzed=len(priority_products),
            improvement_priority_list=priority_products
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"부정 리뷰 분석 중 오류가 발생했습니다: {str(e)}"
        )


@app.get("/api/v1/product/{product_id}/profile")
async def get_product_profile(product_id: int):
    """
    특정 상품의 키워드 프로필 조회 API
    
    Args:
        product_id (int): 상품 ID
    
    Returns:
        JSON: 상품 키워드 프로필
    
    Example:
        GET /api/v1/product/39/profile
    """
    try:
        if product_id not in recommender.product_profiles:
            raise HTTPException(
                status_code=404,
                detail=f"상품 ID {product_id}의 프로필을 찾을 수 없습니다."
            )
        
        profile = recommender.product_profiles[product_id]
        
        # 상위 키워드만 반환 (빈도순)
        sorted_keywords = sorted(
            profile.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        return {
            "product_id": product_id,
            "total_keywords": len(profile),
            "top_keywords": [
                {"keyword": k, "weight": round(w, 4)}
                for k, w in sorted_keywords
            ],
            "generated_at": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"상품 프로필 조회 중 오류가 발생했습니다: {str(e)}"
        )


@app.get("/api/v1/customer/{customer_id}/profile")
async def get_customer_profile(customer_id: int):
    """
    특정 고객의 키워드 프로필 조회 API
    
    Args:
        customer_id (int): 고객 ID
    
    Returns:
        JSON: 고객 키워드 프로필
    
    Example:
        GET /api/v1/customer/100/profile
    """
    try:
        profile = recommender.build_customer_profile(customer_id)
        
        if not profile:
            raise HTTPException(
                status_code=404,
                detail=f"고객 ID {customer_id}의 프로필을 생성할 수 없습니다. 긍정 리뷰가 없거나 고객이 존재하지 않을 수 있습니다."
            )
        
        # 상위 키워드만 반환
        sorted_keywords = sorted(
            profile.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        return {
            "customer_id": customer_id,
            "total_keywords": len(profile),
            "top_keywords": [
                {"keyword": k, "weight": round(w, 4)}
                for k, w in sorted_keywords
            ],
            "generated_at": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"고객 프로필 조회 중 오류가 발생했습니다: {str(e)}"
        )


@app.get("/api/v1/stats/overview")
async def get_stats_overview():
    """
    전체 통계 개요 API
    
    Returns:
        JSON: 리뷰 데이터 통계
    
    Example:
        GET /api/v1/stats/overview
    """
    try:
        import sqlite3
        
        conn = sqlite3.connect('data/reviews.db')
        cursor = conn.cursor()
        
        # 전체 통계 조회
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
        
        return {
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
            },
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"통계 조회 중 오류가 발생했습니다: {str(e)}"
        )


@app.post("/api/v1/send-report")
async def send_email_report(
    recipient_email: str = Query(..., description="수신자 이메일 주소"),
    attach_raw_data: bool = Query(default=False, description="JSON 원본 데이터 첨부 여부")
):
    """
    대시보드 리포트 이메일 전송 API
    
    Args:
        recipient_email (str): 수신자 이메일 주소
        attach_raw_data (bool): JSON 원본 데이터 첨부 여부 (기본값: False)
    
    Returns:
        JSON: 전송 결과
    
    Example:
        POST /api/v1/send-report?recipient_email=user@example.com&attach_raw_data=true
    """
    try:
        # 이메일 설정 (환경변수로 관리하는 것이 보안상 좋음)
        SENDER_EMAIL = "ilhj1228@gmail.com"
        APP_PASSWORD = "phoc nhry asbr svnn"
        
        # EmailReporter 초기화
        reporter = EmailReporter(
            sender_email=SENDER_EMAIL,
            app_password=APP_PASSWORD
        )
        
        # 리포트 전송
        reporter.send_dashboard_report(
            recipient_email=recipient_email,
            api_base_url="http://localhost:8000",
            attach_raw_data=attach_raw_data
        )
        
        return {
            "status": "success",
            "message": "이메일이 성공적으로 전송되었습니다.",
            "recipient": recipient_email,
            "sent_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"이메일 전송 중 오류가 발생했습니다: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    전역 예외 처리
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


def main():
    """
    FastAPI 서버 실행
    """
    print("\n" + "=" * 80)
    print("FastAPI 서버 시작")
    print("=" * 80)
    print("서버 주소: http://localhost:8000")
    print("API 문서: http://localhost:8000/docs")
    print("ReDoc 문서: http://localhost:8000/redoc")
    print("=" * 80)
    print("\n종료하려면 Ctrl+C를 누르세요.\n")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
