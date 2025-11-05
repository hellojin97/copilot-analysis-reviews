"""
한글 리뷰 텍스트 정제 함수 모듈

리뷰 텍스트를 전처리하고 정제하는 기능을 제공합니다.
"""
import re
from typing import List, Optional
from kiwipiepy import Kiwi


class KoreanTextCleaner:
    """한글 텍스트 정제 클래스"""
    
    def __init__(self):
        """
        KoreanTextCleaner 초기화
        Kiwi 형태소 분석기를 로드합니다.
        """
        print("Kiwi 형태소 분석기를 초기화합니다...")
        self.kiwi = Kiwi()
        print("✓ Kiwi 초기화 완료")
        
        # 불용어 리스트 (stopwords)
        self.stopwords = {
            '이', '가', '은', '는', '을', '를', '의', '에', '와', '과', '도', '로', '으로',
            '해서', '하고', '한', '그', '저', '이런', '저런', '것', '등', '및',
            '있다', '없다', '이다', '아니다', '되다', '하다', '같다',
            '등', '이', '들', '안', '못', '점', '너무', '정말', '진짜', '아주'
        }
    
    def remove_special_characters(self, text: str) -> str:
        """
        특수문자 제거
        
        Args:
            text (str): 원본 텍스트
            
        Returns:
            str: 특수문자가 제거된 텍스트
        """
        # 한글, 영문, 숫자, 공백만 남기기
        text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def remove_repeated_chars(self, text: str, max_repeat: int = 2) -> str:
        """
        반복되는 문자 제거
        예: '너무무무무' -> '너무무'
        
        Args:
            text (str): 원본 텍스트
            max_repeat (int): 허용할 최대 반복 횟수
            
        Returns:
            str: 반복 문자가 정제된 텍스트
        """
        result = []
        prev_char = ''
        count = 0
        
        for char in text:
            if char == prev_char:
                count += 1
                if count < max_repeat:
                    result.append(char)
            else:
                result.append(char)
                prev_char = char
                count = 0
        
        return ''.join(result)
    
    def extract_nouns(self, text: str, min_length: int = 2) -> List[str]:
        """
        명사 추출
        
        Args:
            text (str): 원본 텍스트
            min_length (int): 추출할 명사의 최소 길이
            
        Returns:
            List[str]: 추출된 명사 리스트
        """
        # Kiwi를 사용한 형태소 분석
        tokens = self.kiwi.tokenize(text)
        
        # 명사(NNG, NNP)만 추출
        nouns = []
        for token in tokens:
            if token.tag in ['NNG', 'NNP']:  # 일반명사, 고유명사
                if len(token.form) >= min_length:
                    nouns.append(token.form)
        
        return nouns
    
    def extract_keywords(self, text: str, pos_tags: Optional[List[str]] = None) -> List[str]:
        """
        키워드 추출 (명사, 동사, 형용사)
        
        Args:
            text (str): 원본 텍스트
            pos_tags (List[str]): 추출할 품사 태그 (기본값: 명사, 동사, 형용사)
            
        Returns:
            List[str]: 추출된 키워드 리스트
        """
        if pos_tags is None:
            # 기본: 명사, 동사, 형용사
            pos_tags = ['NNG', 'NNP', 'VV', 'VA']
        
        tokens = self.kiwi.tokenize(text)
        
        keywords = []
        for token in tokens:
            if token.tag in pos_tags:
                # 불용어 제거
                if token.form not in self.stopwords:
                    keywords.append(token.form)
        
        return keywords
    
    def clean_text(self, text: str, remove_stopwords: bool = True) -> str:
        """
        텍스트 전체 정제 프로세스
        
        Args:
            text (str): 원본 텍스트
            remove_stopwords (bool): 불용어 제거 여부
            
        Returns:
            str: 정제된 텍스트
        """
        # 1. 특수문자 제거
        text = self.remove_special_characters(text)
        
        # 2. 반복 문자 정제
        text = self.remove_repeated_chars(text)
        
        # 3. 불용어 제거 (선택사항)
        if remove_stopwords:
            tokens = self.kiwi.tokenize(text)
            filtered_tokens = [
                token.form for token in tokens 
                if token.form not in self.stopwords
            ]
            text = ' '.join(filtered_tokens)
        
        # 4. 공백 정리
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_morphemes(self, text: str, target_tags: Optional[List[str]] = None) -> List[tuple]:
        """
        형태소 분석 및 추출
        
        Args:
            text (str): 원본 텍스트
            target_tags (List[str]): 추출할 품사 태그 리스트
            
        Returns:
            List[tuple]: (형태소, 품사) 튜플 리스트
        """
        tokens = self.kiwi.tokenize(text)
        
        if target_tags is None:
            # 모든 형태소 반환
            return [(token.form, token.tag) for token in tokens]
        else:
            # 특정 품사만 반환
            return [
                (token.form, token.tag) for token in tokens 
                if token.tag in target_tags
            ]
    
    def get_sentiment_keywords(self, text: str) -> dict:
        """
        감성 키워드 추출 (긍정/부정)
        
        Args:
            text (str): 원본 텍스트
            
        Returns:
            dict: {'positive': [...], 'negative': [...]}
        """
        # 긍정 키워드
        positive_words = {
            '좋다', '좋음', '만족', '훌륭', '최고', '추천', '편리', '깔끔', '우수',
            '신뢰', '예쁘다', '예쁨', '완벽', '감사', '사랑', '행복', '즐겁',
            '빠르다', '빠름', '정확', '안정', '부드럽', '맛있', '저렴', '가성비'
        }
        
        # 부정 키워드
        negative_words = {
            '나쁘다', '나쁨', '불만', '실망', '최악', '별로', '불편', '엉성', '나쁘',
            '의심', '더럽', '거칠', '비싸다', '비싼', '느리다', '느림', '부족',
            '시끄럽', '소음', '불안정', '고장', '망가지', '아쉽', '후회', '짜증'
        }
        
        # 형태소 분석
        tokens = self.kiwi.tokenize(text)
        
        positive_found = []
        negative_found = []
        
        for token in tokens:
            form = token.form
            # 긍정 키워드 체크
            for pos_word in positive_words:
                if pos_word in form:
                    positive_found.append(form)
                    break
            
            # 부정 키워드 체크
            for neg_word in negative_words:
                if neg_word in form:
                    negative_found.append(form)
                    break
        
        return {
            'positive': list(set(positive_found)),
            'negative': list(set(negative_found))
        }


def example_usage():
    """사용 예제"""
    print("=" * 80)
    print("한글 텍스트 정제 함수 사용 예제")
    print("=" * 80)
    
    # KoreanTextCleaner 인스턴스 생성
    cleaner = KoreanTextCleaner()
    
    # 샘플 리뷰 텍스트
    sample_reviews = [
        "와! 브랜드 신뢰하고 추천함해서 너무 좋아요. 다음에도 이 브랜드로 살 예정입니다.",
        "음... 소음 심함하고 밤에 못씀해서 다시 사고 싶지 않아요.",
        "LED 조명 후기 남깁니다!!! 디자인 예쁨해서 기대 이상이었어요~~ 품질 우수하기까지!"
    ]
    
    for idx, review in enumerate(sample_reviews, 1):
        print(f"\n[리뷰 {idx}]")
        print(f"원본: {review}")
        print("-" * 80)
        
        # 1. 특수문자 제거
        cleaned = cleaner.remove_special_characters(review)
        print(f"특수문자 제거: {cleaned}")
        
        # 2. 명사 추출
        nouns = cleaner.extract_nouns(review)
        print(f"명사 추출: {', '.join(nouns)}")
        
        # 3. 키워드 추출
        keywords = cleaner.extract_keywords(review)
        print(f"키워드 추출: {', '.join(keywords)}")
        
        # 4. 전체 정제
        fully_cleaned = cleaner.clean_text(review)
        print(f"전체 정제: {fully_cleaned}")
        
        # 5. 감성 키워드
        sentiment_keywords = cleaner.get_sentiment_keywords(review)
        print(f"긍정 키워드: {', '.join(sentiment_keywords['positive']) if sentiment_keywords['positive'] else '없음'}")
        print(f"부정 키워드: {', '.join(sentiment_keywords['negative']) if sentiment_keywords['negative'] else '없음'}")
    
    print("\n" + "=" * 80)
    print("✓ 예제 실행 완료!")
    print("=" * 80)


if __name__ == '__main__':
    example_usage()
