"""
이메일 리포트 전송 모듈

API 분석 결과를 HTML 대시보드로 변환하여 이메일로 전송합니다.
"""
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from typing import Dict, List, Optional
import json
from chart_generator import ChartGenerator


class EmailReporter:
    """이메일 리포트 전송 클래스"""
    
    def __init__(self, sender_email: str, app_password: str):
        """
        EmailReporter 초기화
        
        Args:
            sender_email (str): 송신 이메일
            app_password (str): Gmail 앱 비밀번호
        """
        self.sender_email = sender_email
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def fetch_api_data(self, base_url: str = "http://localhost:8000") -> Dict:
        """
        API에서 데이터 수집
        
        Args:
            base_url (str): API 서버 주소
            
        Returns:
            Dict: 수집된 데이터
        """
        print("=" * 80)
        print("API 데이터 수집 중...")
        print("=" * 80)
        
        data = {}
        
        try:
            # 1. 전체 통계
            print("1. 전체 통계 조회...")
            response = requests.get(f"{base_url}/api/v1/stats/overview", timeout=10)
            if response.status_code == 200:
                data['stats'] = response.json()
                print("   ✓ 전체 통계 수집 완료")
            
            # 2. 부정 리뷰 분석 (Top 5)
            print("2. 부정 리뷰 분석 조회...")
            response = requests.get(f"{base_url}/api/v1/negative-analysis?top_n=5", timeout=30)
            if response.status_code == 200:
                data['negative_analysis'] = response.json()
                print("   ✓ 부정 리뷰 분석 수집 완료")
            
            # 3. 샘플 고객 추천 (고객 ID 100)
            print("3. 샘플 고객 추천 조회...")
            response = requests.get(f"{base_url}/api/v1/recommend/100?top_n=5", timeout=10)
            if response.status_code == 200:
                data['recommendation_sample'] = response.json()
                print("   ✓ 샘플 추천 수집 완료")
            elif response.status_code == 404:
                print("   ⚠️  고객 ID 100의 추천 데이터 없음")
                # 다른 고객 시도 (ID 50)
                response = requests.get(f"{base_url}/api/v1/recommend/50?top_n=5", timeout=10)
                if response.status_code == 200:
                    data['recommendation_sample'] = response.json()
                    print("   ✓ 샘플 추천 수집 완료 (고객 ID 50)")
            
            print("\n✓ 모든 데이터 수집 완료")
            return data
        
        except requests.exceptions.ConnectionError:
            print("❌ API 서버에 연결할 수 없습니다. api_server.py가 실행 중인지 확인하세요.")
            raise
        except Exception as e:
            print(f"❌ 데이터 수집 중 오류: {e}")
            raise
    
    def generate_html_report(self, data: Dict, include_charts: bool = True) -> str:
        """
        HTML 리포트 생성
        
        Args:
            data (Dict): API 데이터
            include_charts (bool): 차트 이미지 포함 여부
            
        Returns:
            str: HTML 콘텐츠
        """
        print("\n" + "=" * 80)
        print("HTML 리포트 생성 중...")
        print("=" * 80)
        
        # 현재 날짜
        today = datetime.now().strftime("%Y년 %m월 %d일")
        
        # 통계 데이터
        stats = data.get('stats', {})
        overview = stats.get('overview', {})
        sentiment = stats.get('sentiment_distribution', {})
        
        # 부정 리뷰 분석
        negative = data.get('negative_analysis', {})
        priority_list = negative.get('improvement_priority_list', [])
        
        # 추천 샘플
        recommendation = data.get('recommendation_sample', {})
        
        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>리뷰 분석 대시보드 리포트</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f7fa;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .stat-card h3 {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        
        .stat-card .value {{
            font-size: 36px;
            font-weight: bold;
        }}
        
        .sentiment-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .sentiment-card {{
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .sentiment-card.positive {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }}
        
        .sentiment-card.negative {{
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            color: white;
        }}
        
        .sentiment-card.neutral {{
            background: linear-gradient(135deg, #bdc3c7 0%, #95a5a6 100%);
            color: white;
        }}
        
        .sentiment-card h3 {{
            font-size: 16px;
            margin-bottom: 10px;
        }}
        
        .sentiment-card .count {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .sentiment-card .percentage {{
            font-size: 18px;
            opacity: 0.9;
        }}
        
        .priority-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .priority-table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .priority-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .priority-table td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
        }}
        
        .priority-table tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        .rank-badge {{
            display: inline-block;
            width: 30px;
            height: 30px;
            line-height: 30px;
            text-align: center;
            border-radius: 50%;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            font-weight: bold;
        }}
        
        .rating {{
            color: #ffa500;
            font-weight: bold;
        }}
        
        .negative-ratio {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .keyword-badge {{
            display: inline-block;
            background: #f0f0f0;
            padding: 5px 10px;
            border-radius: 15px;
            margin: 2px;
            font-size: 12px;
            color: #555;
        }}
        
        .recommendation-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }}
        
        .recommendation-card h4 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 18px;
        }}
        
        .recommendation-card .meta {{
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        
        .recommendation-card .similarity {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .footer p {{
            margin-bottom: 10px;
        }}
        
        .alert-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        
        .alert-box strong {{
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 헤더 -->
        <div class="header">
            <h1>📊 리뷰 분석 대시보드 리포트</h1>
            <p>생성일: {today}</p>
        </div>
        
        <!-- 콘텐츠 -->
        <div class="content">
            <!-- 전체 통계 섹션 -->
            <div class="section">
                <h2 class="section-title">📈 전체 통계</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>총 고객 수</h3>
                        <div class="value">{overview.get('total_customers', 0):,}명</div>
                    </div>
                    <div class="stat-card">
                        <h3>총 상품 수</h3>
                        <div class="value">{overview.get('total_products', 0):,}개</div>
                    </div>
                    <div class="stat-card">
                        <h3>총 리뷰 수</h3>
                        <div class="value">{overview.get('total_reviews', 0):,}개</div>
                    </div>
                    <div class="stat-card">
                        <h3>평균 별점</h3>
                        <div class="value">{overview.get('average_rating', 0):.1f}★</div>
                    </div>
                </div>
                
                <!-- 감성 분포 -->
                <h3 style="margin-bottom: 15px; color: #555;">감성 분포</h3>
                <div class="sentiment-grid">
                    <div class="sentiment-card positive">
                        <h3>😊 긍정</h3>
                        <div class="count">{sentiment.get('positive', {}).get('count', 0):,}</div>
                        <div class="percentage">{sentiment.get('positive', {}).get('percentage', 0):.1f}%</div>
                    </div>
                    <div class="sentiment-card negative">
                        <h3>😞 부정</h3>
                        <div class="count">{sentiment.get('negative', {}).get('count', 0):,}</div>
                        <div class="percentage">{sentiment.get('negative', {}).get('percentage', 0):.1f}%</div>
                    </div>
                    <div class="sentiment-card neutral">
                        <h3>😐 중립</h3>
                        <div class="count">{sentiment.get('neutral', {}).get('count', 0):,}</div>
                        <div class="percentage">{sentiment.get('neutral', {}).get('percentage', 0):.1f}%</div>
                    </div>
                </div>
            </div>
            
            <!-- 개선 우선순위 섹션 -->
            <div class="section">
                <h2 class="section-title">🚨 개선 우선순위 상품 Top 5</h2>
                <div class="alert-box">
                    <strong>⚠️ 주의:</strong> 아래 상품들은 부정 리뷰 비율이 높아 즉각적인 개선이 필요합니다.
                </div>
                
                <table class="priority-table">
                    <thead>
                        <tr>
                            <th>순위</th>
                            <th>상품명</th>
                            <th>카테고리</th>
                            <th>평균 별점</th>
                            <th>부정 비율</th>
                            <th>주요 문제점</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        
        # 개선 우선순위 테이블 데이터
        for idx, product in enumerate(priority_list[:5], 1):
            keywords = ', '.join([
                f"{kw['keyword']}({kw['count']})"
                for kw in product.get('top_negative_keywords', [])[:3]
            ])
            
            html_content += f"""
                        <tr>
                            <td><span class="rank-badge">{idx}</span></td>
                            <td><strong>{product.get('product_name', 'N/A')}</strong></td>
                            <td>{product.get('category', 'N/A')}</td>
                            <td class="rating">{product.get('average_rating', 0):.1f}★</td>
                            <td class="negative-ratio">{product.get('negative_ratio', 0):.1f}%</td>
                            <td>
"""
            
            # 키워드 뱃지
            for kw in product.get('top_negative_keywords', [])[:3]:
                html_content += f'<span class="keyword-badge">{kw["keyword"]} ({kw["count"]}회)</span>'
            
            html_content += """
                            </td>
                        </tr>
"""
        
        html_content += """
                    </tbody>
                </table>
                
                <!-- 차트 이미지 섹션 -->
                {'<div style="margin-top: 40px;"><h3 style="margin-bottom: 20px; color: #555;">📊 시각화 분석</h3><div style="text-align: center; margin-bottom: 30px;"><img src="cid:priority_bar" alt="Priority Bar Chart" style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></div><div style="text-align: center; margin-bottom: 30px;"><img src="cid:rating_comparison" alt="Rating Comparison" style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></div><div style="text-align: center; margin-bottom: 30px;"><img src="cid:keyword_wordcloud" alt="Keyword Wordcloud" style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></div></div>' if include_charts else ''}
            </div>
"""
        
        # 추천 샘플이 있으면 추가
        if recommendation:
            customer_id = recommendation.get('customer_id', 'N/A')
            recommendations = recommendation.get('recommendations', [])
            
            html_content += f"""
            <!-- 추천 시스템 샘플 섹션 -->
            <div class="section">
                <h2 class="section-title">🎁 추천 시스템 샘플 (고객 ID: {customer_id})</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    고객의 긍정 리뷰 키워드 기반 맞춤 추천 상품입니다.
                </p>
"""
            
            for idx, rec in enumerate(recommendations[:5], 1):
                keywords = ', '.join([k['keyword'] for k in rec.get('top_keywords', [])[:3]])
                
                html_content += f"""
                <div class="recommendation-card">
                    <h4>{idx}. {rec.get('product_name', 'N/A')} ({rec.get('category', 'N/A')})</h4>
                    <div class="meta">
                        ⭐ 평균 별점: <strong>{rec.get('average_rating', 0):.2f}</strong> | 
                        💬 리뷰: <strong>{rec.get('review_count', 0)}개</strong>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="similarity">유사도: {rec.get('similarity_score', 0):.4f}</span>
                    </div>
                    <div style="color: #666; font-size: 14px;">
                        주요 키워드: {keywords}
                    </div>
                </div>
"""
            
            html_content += """
            </div>
"""
        
        # Footer
        html_content += f"""
        </div>
        
        <!-- 푸터 -->
        <div class="footer">
            <p><strong>리뷰 분석 및 추천 시스템</strong></p>
            <p>이 리포트는 자동으로 생성되었습니다.</p>
            <p>생성 시각: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
</body>
</html>
"""
        
        print("✓ HTML 리포트 생성 완료")
        return html_content
    
    def send_email(self, 
                   recipient_email: str, 
                   subject: str, 
                   html_content: str,
                   attach_json: Optional[Dict] = None,
                   chart_images: Optional[Dict] = None):
        """
        이메일 전송
        
        Args:
            recipient_email (str): 수신자 이메일
            subject (str): 이메일 제목
            html_content (str): HTML 콘텐츠
            attach_json (Dict, optional): 첨부할 JSON 데이터
            chart_images (Dict, optional): 차트 이미지 딕셔너리 (name -> BytesIO)
        """
        print("\n" + "=" * 80)
        print("이메일 전송 중...")
        print("=" * 80)
        
        # 이메일 메시지 생성 (related로 변경 - 이미지 임베드 지원)
        msg = MIMEMultipart('related')
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Alternative 파트 (HTML과 텍스트)
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        
        # HTML 파트 추가
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg_alternative.attach(html_part)
        
        # 차트 이미지 첨부 (인라인)
        if chart_images:
            print(f"차트 이미지 첨부 중... ({len(chart_images)}개)")
            for chart_name, img_buffer in chart_images.items():
                img_buffer.seek(0)  # 버퍼 위치 리셋
                img_part = MIMEImage(img_buffer.read())
                img_part.add_header('Content-ID', f'<{chart_name}>')
                img_part.add_header('Content-Disposition', 'inline', filename=f'{chart_name}.png')
                msg.attach(img_part)
                print(f"   ✓ {chart_name}.png 첨부 완료")
        
        # JSON 첨부 (선택사항)
        if attach_json:
            json_str = json.dumps(attach_json, ensure_ascii=False, indent=2)
            json_part = MIMEText(json_str, 'plain', 'utf-8')
            json_part.add_header('Content-Disposition', 'attachment', 
                               filename='dashboard_data.json')
            msg.attach(json_part)
        
        try:
            # SMTP 서버 연결
            print(f"SMTP 서버 연결 중... ({self.smtp_server}:{self.smtp_port})")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            
            # 로그인
            print("로그인 중...")
            server.login(self.sender_email, self.app_password)
            
            # 이메일 전송
            print(f"이메일 전송 중... ({recipient_email})")
            server.send_message(msg)
            
            # 연결 종료
            server.quit()
            
            print("=" * 80)
            print("✅ 이메일 전송 완료!")
            print("=" * 80)
            print(f"수신자: {recipient_email}")
            print(f"제목: {subject}")
            print("=" * 80)
        
        except smtplib.SMTPAuthenticationError:
            print("❌ 인증 실패: 이메일 또는 앱 비밀번호를 확인하세요.")
            raise
        except Exception as e:
            print(f"❌ 이메일 전송 실패: {e}")
            raise
    
    def send_dashboard_report(self, 
                             recipient_email: str, 
                             api_base_url: str = "http://localhost:8000",
                             attach_raw_data: bool = False,
                             include_charts: bool = True):
        """
        대시보드 리포트 수집 및 전송 (올인원)
        
        Args:
            recipient_email (str): 수신자 이메일
            api_base_url (str): API 서버 주소
            attach_raw_data (bool): 원본 JSON 데이터 첨부 여부
            include_charts (bool): 차트 이미지 포함 여부
        """
        print("\n" + "=" * 80)
        print("📊 대시보드 리포트 생성 및 전송 프로세스 시작")
        print("=" * 80)
        
        try:
            # 1. API 데이터 수집
            data = self.fetch_api_data(api_base_url)
            
            # 2. 차트 생성 (옵션)
            chart_images = None
            if include_charts:
                print("\n차트 생성 중...")
                generator = ChartGenerator()
                chart_images = generator.create_all_charts(data)
            
            # 3. HTML 리포트 생성
            html_content = self.generate_html_report(data, include_charts=include_charts)
            
            # 4. 이메일 전송
            today = datetime.now().strftime("%Y년 %m월 %d일")
            subject = f"[리뷰 분석] 대시보드 리포트 - {today}"
            
            self.send_email(
                recipient_email=recipient_email,
                subject=subject,
                html_content=html_content,
                attach_json=data if attach_raw_data else None,
                chart_images=chart_images
            )
            
            print("\n" + "=" * 80)
            print("🎉 모든 작업이 성공적으로 완료되었습니다!")
            print("=" * 80)
        
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            raise


def main():
    """메인 실행 함수"""
    print("=" * 80)
    print("📧 이메일 리포트 전송 시스템")
    print("=" * 80)
    
    # 이메일 설정
    SENDER_EMAIL = "ilhj1228@gmail.com"
    APP_PASSWORD = "phoc nhry asbr svnn"
    RECIPIENT_EMAIL = "ilhj1228@gmail.com"
    
    # EmailReporter 초기화
    reporter = EmailReporter(
        sender_email=SENDER_EMAIL,
        app_password=APP_PASSWORD
    )
    
    # 대시보드 리포트 전송
    try:
        reporter.send_dashboard_report(
            recipient_email=RECIPIENT_EMAIL,
            api_base_url="http://localhost:8000",
            attach_raw_data=True  # JSON 원본 데이터도 첨부
        )
    except Exception as e:
        print(f"\n프로그램 종료: {e}")


if __name__ == "__main__":
    main()
