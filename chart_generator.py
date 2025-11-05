"""
차트 생성 모듈

경영진용 대시보드 시각화 차트를 생성합니다.
"""
import matplotlib
matplotlib.use('Agg')  # GUI 없이 실행 (서버/GitHub Actions)
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
from io import BytesIO
from typing import Dict, List, Tuple
import platform


class ChartGenerator:
    """차트 생성 클래스"""
    
    def __init__(self):
        """ChartGenerator 초기화"""
        self._setup_korean_font()
        self._setup_style()
    
    def _setup_korean_font(self):
        """
        한글 폰트 설정
        """
        system = platform.system()
        
        if system == 'Windows':
            # Windows: 맑은 고딕
            plt.rcParams['font.family'] = 'Malgun Gothic'
        elif system == 'Darwin':  # macOS
            # macOS: AppleGothic
            plt.rcParams['font.family'] = 'AppleGothic'
        else:  # Linux
            # Linux: Noto Sans CJK KR 또는 DejaVu Sans
            try:
                # GitHub Actions Ubuntu에서 사용 가능한 폰트
                plt.rcParams['font.family'] = 'DejaVu Sans'
            except:
                pass
        
        # 마이너스 기호 깨짐 방지
        plt.rcParams['axes.unicode_minus'] = False
    
    def _setup_style(self):
        """
        차트 스타일 설정
        """
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        plt.rcParams['figure.dpi'] = 100
        plt.rcParams['savefig.dpi'] = 150
        plt.rcParams['figure.facecolor'] = 'white'
    
    def create_sentiment_pie_chart(self, sentiment_data: Dict) -> BytesIO:
        """
        감성 분포 파이 차트 생성
        
        Args:
            sentiment_data (Dict): 감성 분포 데이터
            
        Returns:
            BytesIO: 이미지 바이트 스트림
        """
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # 데이터 준비
        labels = []
        sizes = []
        colors = []
        explode = []
        
        if 'positive' in sentiment_data:
            labels.append(f"긍정 😊\n{sentiment_data['positive']['percentage']:.1f}%")
            sizes.append(sentiment_data['positive']['count'])
            colors.append('#38ef7d')
            explode.append(0.05)
        
        if 'negative' in sentiment_data:
            labels.append(f"부정 😞\n{sentiment_data['negative']['percentage']:.1f}%")
            sizes.append(sentiment_data['negative']['count'])
            colors.append('#f45c43')
            explode.append(0.1)  # 부정 강조
        
        if 'neutral' in sentiment_data:
            labels.append(f"중립 😐\n{sentiment_data['neutral']['percentage']:.1f}%")
            sizes.append(sentiment_data['neutral']['count'])
            colors.append('#95a5a6')
            explode.append(0.05)
        
        # 파이 차트 그리기
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct='%d개',
            explode=explode,
            shadow=True,
            startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'}
        )
        
        # 자동 텍스트 스타일링
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
        
        ax.set_title('리뷰 감성 분포', fontsize=16, weight='bold', pad=20)
        
        # 이미지를 BytesIO로 저장
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return buf
    
    def create_priority_bar_chart(self, priority_list: List[Dict]) -> BytesIO:
        """
        개선 우선순위 상품 Top 5 막대 차트
        
        Args:
            priority_list (List[Dict]): 우선순위 상품 목록
            
        Returns:
            BytesIO: 이미지 바이트 스트림
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 데이터 준비 (상위 5개)
        products = [p['product_name'][:15] + '...' if len(p['product_name']) > 15 
                   else p['product_name'] for p in priority_list[:5]]
        negative_ratios = [p['negative_ratio'] for p in priority_list[:5]]
        
        # 색상 그라데이션 (빨강 -> 주황)
        colors = plt.cm.Reds(np.linspace(0.7, 0.4, len(products)))
        
        # 막대 차트
        bars = ax.barh(products, negative_ratios, color=colors, edgecolor='black', linewidth=1.5)
        
        # 값 표시
        for i, (bar, value) in enumerate(zip(bars, negative_ratios)):
            ax.text(value + 1, bar.get_y() + bar.get_height()/2, 
                   f'{value:.1f}%', 
                   va='center', fontsize=11, weight='bold')
        
        ax.set_xlabel('부정 리뷰 비율 (%)', fontsize=12, weight='bold')
        ax.set_title('개선 우선순위 상품 Top 5 (부정 비율)', fontsize=16, weight='bold', pad=20)
        ax.set_xlim(0, max(negative_ratios) * 1.15)
        
        # 그리드 설정
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # 이미지를 BytesIO로 저장
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return buf
    
    def create_rating_comparison_chart(self, priority_list: List[Dict]) -> BytesIO:
        """
        평균 별점 vs 부정 비율 비교 차트
        
        Args:
            priority_list (List[Dict]): 우선순위 상품 목록
            
        Returns:
            BytesIO: 이미지 바이트 스트림
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # 데이터 준비 (상위 5개)
        products = [p['product_name'][:12] + '...' if len(p['product_name']) > 12 
                   else p['product_name'] for p in priority_list[:5]]
        ratings = [p['average_rating'] for p in priority_list[:5]]
        negative_ratios = [p['negative_ratio'] for p in priority_list[:5]]
        
        # 차트 1: 평균 별점
        colors1 = plt.cm.RdYlGn(np.array(ratings) / 5.0)  # 별점 기반 색상
        bars1 = ax1.bar(range(len(products)), ratings, color=colors1, edgecolor='black', linewidth=1.5)
        ax1.set_xticks(range(len(products)))
        ax1.set_xticklabels(products, rotation=45, ha='right', fontsize=10)
        ax1.set_ylabel('평균 별점', fontsize=11, weight='bold')
        ax1.set_title('평균 별점', fontsize=14, weight='bold')
        ax1.set_ylim(0, 5)
        ax1.axhline(y=3.0, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='기준선 (3.0)')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        # 값 표시
        for bar, value in zip(bars1, ratings):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{value:.1f}★',
                    ha='center', va='bottom', fontsize=10, weight='bold')
        
        # 차트 2: 부정 비율
        colors2 = plt.cm.Reds(np.array(negative_ratios) / max(negative_ratios))
        bars2 = ax2.bar(range(len(products)), negative_ratios, color=colors2, edgecolor='black', linewidth=1.5)
        ax2.set_xticks(range(len(products)))
        ax2.set_xticklabels(products, rotation=45, ha='right', fontsize=10)
        ax2.set_ylabel('부정 비율 (%)', fontsize=11, weight='bold')
        ax2.set_title('부정 리뷰 비율', fontsize=14, weight='bold')
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        # 값 표시
        for bar, value in zip(bars2, negative_ratios):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{value:.1f}%',
                    ha='center', va='bottom', fontsize=10, weight='bold')
        
        fig.suptitle('별점 vs 부정 비율 비교', fontsize=16, weight='bold', y=1.02)
        
        # 이미지를 BytesIO로 저장
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return buf
    
    def create_keyword_wordcloud(self, priority_list: List[Dict], max_words: int = 50) -> BytesIO:
        """
        부정 키워드 워드클라우드 생성
        
        Args:
            priority_list (List[Dict]): 우선순위 상품 목록
            max_words (int): 최대 단어 수
            
        Returns:
            BytesIO: 이미지 바이트 스트림
        """
        # 모든 부정 키워드 수집
        keyword_freq = {}
        for product in priority_list[:5]:
            for kw in product.get('top_negative_keywords', []):
                keyword = kw['keyword']
                count = kw['count']
                keyword_freq[keyword] = keyword_freq.get(keyword, 0) + count
        
        if not keyword_freq:
            # 키워드가 없으면 빈 이미지 반환
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, '키워드 데이터 없음', ha='center', va='center', fontsize=20)
            ax.axis('off')
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            plt.close()
            return buf
        
        # 워드클라우드 생성
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='Reds',
            max_words=max_words,
            relative_scaling=0.5,
            min_font_size=10,
            font_path=self._get_korean_font_path()
        ).generate_from_frequencies(keyword_freq)
        
        # 플롯
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('부정 리뷰 주요 키워드 (Top 5 상품)', fontsize=16, weight='bold', pad=20)
        
        # 이미지를 BytesIO로 저장
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()
        
        return buf
    
    def _get_korean_font_path(self) -> str:
        """
        한글 워드클라우드용 폰트 경로 반환
        
        Returns:
            str: 폰트 파일 경로
        """
        system = platform.system()
        
        if system == 'Windows':
            return 'C:/Windows/Fonts/malgun.ttf'
        elif system == 'Darwin':  # macOS
            return '/System/Library/Fonts/AppleGothic.ttf'
        else:  # Linux
            # Ubuntu/GitHub Actions용 - DejaVu Sans 사용
            return '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    
    def create_recommendation_scatter_chart(self, recommendations: List[Dict]) -> BytesIO:
        """
        추천 상품 유사도 산점도 차트
        
        Args:
            recommendations (List[Dict]): 추천 상품 목록
            
        Returns:
            BytesIO: 이미지 바이트 스트림
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 데이터 준비
        products = [r['product_name'][:20] + '...' if len(r['product_name']) > 20 
                   else r['product_name'] for r in recommendations[:5]]
        similarities = [r['similarity_score'] for r in recommendations[:5]]
        ratings = [r['average_rating'] for r in recommendations[:5]]
        review_counts = [r['review_count'] for r in recommendations[:5]]
        
        # 버블 크기 (리뷰 수에 비례)
        sizes = [min(rc * 5, 1000) for rc in review_counts]
        
        # 색상 (유사도에 따라)
        colors = plt.cm.viridis(np.array(similarities))
        
        # 산점도
        scatter = ax.scatter(similarities, ratings, s=sizes, c=similarities, 
                            cmap='viridis', alpha=0.6, edgecolors='black', linewidth=2)
        
        # 제품명 레이블
        for i, txt in enumerate(products):
            ax.annotate(txt, (similarities[i], ratings[i]), 
                       fontsize=9, ha='center', va='bottom',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))
        
        ax.set_xlabel('유사도 점수', fontsize=12, weight='bold')
        ax.set_ylabel('평균 별점', fontsize=12, weight='bold')
        ax.set_title('추천 상품 유사도 vs 별점 (버블 크기 = 리뷰 수)', fontsize=14, weight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 컬러바
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('유사도', fontsize=11, weight='bold')
        
        # 이미지를 BytesIO로 저장
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return buf
    
    def create_all_charts(self, data: Dict) -> Dict[str, BytesIO]:
        """
        모든 차트 생성 (올인원)
        
        Args:
            data (Dict): 분석 데이터
            
        Returns:
            Dict[str, BytesIO]: 차트 이름과 이미지 바이트 스트림 딕셔너리
        """
        print("\n" + "=" * 80)
        print("📊 차트 생성 중...")
        print("=" * 80)
        
        charts = {}
        
        try:
            # 1. 감성 분포 파이 차트
            print("1. 감성 분포 파이 차트 생성 중...")
            sentiment_data = data.get('stats', {}).get('sentiment_distribution', {})
            if sentiment_data:
                charts['sentiment_pie'] = self.create_sentiment_pie_chart(sentiment_data)
                print("   ✓ 감성 분포 파이 차트 완료")
            
            # 2. 개선 우선순위 막대 차트
            print("2. 개선 우선순위 막대 차트 생성 중...")
            priority_list = data.get('negative_analysis', {}).get('improvement_priority_list', [])
            if priority_list:
                charts['priority_bar'] = self.create_priority_bar_chart(priority_list)
                print("   ✓ 개선 우선순위 막대 차트 완료")
            
            # 3. 별점 vs 부정 비율 비교 차트
            print("3. 별점 vs 부정 비율 비교 차트 생성 중...")
            if priority_list:
                charts['rating_comparison'] = self.create_rating_comparison_chart(priority_list)
                print("   ✓ 별점 vs 부정 비율 비교 차트 완료")
            
            # 4. 부정 키워드 워드클라우드
            print("4. 부정 키워드 워드클라우드 생성 중...")
            if priority_list:
                charts['keyword_wordcloud'] = self.create_keyword_wordcloud(priority_list)
                print("   ✓ 부정 키워드 워드클라우드 완료")
            
            # 5. 추천 상품 산점도
            print("5. 추천 상품 산점도 생성 중...")
            recommendations = data.get('recommendation_sample', {}).get('recommendations', [])
            if recommendations:
                charts['recommendation_scatter'] = self.create_recommendation_scatter_chart(recommendations)
                print("   ✓ 추천 상품 산점도 완료")
            
            print("\n✓ 모든 차트 생성 완료!")
            print(f"총 {len(charts)}개 차트 생성됨")
            return charts
        
        except Exception as e:
            print(f"❌ 차트 생성 중 오류: {e}")
            raise


def main():
    """테스트용 메인 함수"""
    import json
    
    # 샘플 데이터
    sample_data = {
        'stats': {
            'sentiment_distribution': {
                'positive': {'count': 2000, 'percentage': 50.0},
                'negative': {'count': 1200, 'percentage': 30.0},
                'neutral': {'count': 800, 'percentage': 20.0}
            }
        },
        'negative_analysis': {
            'improvement_priority_list': [
                {
                    'product_name': '전기히터',
                    'average_rating': 2.5,
                    'negative_ratio': 47.1,
                    'top_negative_keywords': [
                        {'keyword': '불량', 'count': 15},
                        {'keyword': '고장', 'count': 12}
                    ]
                },
                {
                    'product_name': '노트북',
                    'average_rating': 3.2,
                    'negative_ratio': 35.5,
                    'top_negative_keywords': [
                        {'keyword': '느림', 'count': 10},
                        {'keyword': '발열', 'count': 8}
                    ]
                }
            ]
        }
    }
    
    # 차트 생성기 초기화
    generator = ChartGenerator()
    
    # 모든 차트 생성
    charts = generator.create_all_charts(sample_data)
    
    print(f"\n생성된 차트: {list(charts.keys())}")


if __name__ == "__main__":
    main()
