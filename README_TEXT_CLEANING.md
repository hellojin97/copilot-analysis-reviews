# 한글 리뷰 텍스트 정제 기능 구현 완료

## 📋 개요

한글 리뷰 텍스트를 분석하고 정제하는 시스템을 구축했습니다. 
kiwipiepy 형태소 분석기를 사용하여 리뷰에서 의미 있는 키워드를 추출하고 감성 분석의 기반을 마련했습니다.

## 🎯 구현 완료 기능

### 1. `text_cleaner.py` - 텍스트 정제 모듈

#### `KoreanTextCleaner` 클래스
한글 텍스트를 전처리하고 정제하는 핵심 클래스입니다.

#### 주요 메서드

1. **`remove_special_characters(text)`**
   - 특수문자 제거
   - 한글, 영문, 숫자, 공백만 유지
   - 여러 공백을 하나로 정리

2. **`remove_repeated_chars(text, max_repeat=2)`**
   - 반복되는 문자 정제
   - 예: "너무무무무" → "너무무"

3. **`extract_nouns(text, min_length=2)`**
   - 명사 추출 (일반명사, 고유명사)
   - 최소 길이 필터링 가능

4. **`extract_keywords(text, pos_tags=None)`**
   - 키워드 추출 (명사, 동사, 형용사)
   - 불용어 자동 제거
   - 품사 태그 커스터마이징 가능

5. **`clean_text(text, remove_stopwords=True)`**
   - 전체 정제 프로세스 실행
   - 특수문자 제거 → 반복 문자 정제 → 불용어 제거

6. **`extract_morphemes(text, target_tags=None)`**
   - 형태소 분석 및 추출
   - (형태소, 품사) 튜플 리스트 반환

7. **`get_sentiment_keywords(text)`**
   - 감성 키워드 자동 추출
   - 긍정/부정 키워드 분류
   - 반환: `{'positive': [...], 'negative': [...]}`

### 2. `test_text_cleaner_with_db.py` - 실전 테스트 모듈

#### `test_with_real_reviews(limit=10)`
- 데이터베이스에서 실제 리뷰 데이터 로드
- 감성별(긍정/부정/중립) 샘플 분석
- 명사, 키워드, 감성 키워드 추출 결과 출력

#### `analyze_keyword_statistics(top_n=20)`
- 전체 4000개 리뷰의 키워드 통계 분석
- 감성별 상위 키워드 빈도 집계
- 시각화 바 차트로 결과 표시

## 📊 분석 결과 (4000개 리뷰)

### Positive 리뷰 상위 키워드
1. 만족 (989회)
2. 추천 (598회)
3. 우수 (350회)
4. 빠르 (250회)
5. 내구 (229회)
6. 실용 (228회)

### Negative 리뷰 상위 키워드
1. 실망 (568회)
2. 불편 (172회)
3. 망가지 (147회)
4. 아쉬움 (139회)
5. 비싸 (132회)

### Neutral 리뷰 상위 키워드
1. 보통 (324회)
2. 정도 (323회)
3. 평범하 (163회)
4. 수준 (160회)

## 🛠️ 기술 스택

- **Python**: 3.12.11
- **형태소 분석**: kiwipiepy 0.21.0 (C++ 기반, 빠른 속도)
- **데이터베이스**: SQLite (reviews.db)
- **데이터 규모**: 4000개 리뷰

## 📁 파일 구조

```
.
├── text_cleaner.py                # 텍스트 정제 모듈
├── test_text_cleaner_with_db.py   # 실전 테스트 스크립트
├── data/
│   └── reviews.db                 # 리뷰 데이터베이스
└── csv/
    ├── customers.csv
    ├── products.csv
    └── reviews.csv
```

## 🚀 사용 방법

### 기본 사용 예제

```python
from text_cleaner import KoreanTextCleaner

# 텍스트 정제기 초기화
cleaner = KoreanTextCleaner()

# 리뷰 텍스트
review = "와! 브랜드 신뢰하고 추천함해서 너무 좋아요."

# 명사 추출
nouns = cleaner.extract_nouns(review)
print(nouns)  # ['브랜드', '신뢰', '추천']

# 키워드 추출
keywords = cleaner.extract_keywords(review)
print(keywords)  # ['브랜드', '신뢰', '추천', '좋']

# 감성 키워드
sentiment = cleaner.get_sentiment_keywords(review)
print(sentiment)  # {'positive': ['신뢰', '추천'], 'negative': []}

# 전체 정제
cleaned = cleaner.clean_text(review)
print(cleaned)
```

### 실전 테스트 실행

```bash
# 샘플 리뷰 분석
python text_cleaner.py

# 데이터베이스 리뷰 분석 + 통계
python test_text_cleaner_with_db.py
```

## 🎯 주요 특징

### 1. 한글 특화
- kiwipiepy를 사용한 정확한 한글 형태소 분석
- JDK 불필요 (C++ 기반으로 빠른 성능)
- 한글 불용어 자동 제거

### 2. 리뷰 특화 기능
- 감성 키워드 자동 분류
- 긍정/부정 단어 사전 내장
- 리뷰에 자주 나오는 특수문자 패턴 처리

### 3. 유연한 커스터마이징
- 품사 태그 선택 가능
- 불용어 추가/제거 가능
- 최소 길이 필터링 옵션

### 4. 대용량 데이터 처리
- 4000개 리뷰 분석 완료
- 효율적인 메모리 사용
- 빠른 처리 속도

## 📈 감성 키워드 사전

### 긍정 키워드 (26개)
```
좋다, 만족, 훌륭, 최고, 추천, 편리, 깔끔, 우수, 신뢰, 예쁘다, 
완벽, 감사, 사랑, 행복, 즐겁, 빠르다, 정확, 안정, 부드럽, 
맛있, 저렴, 가성비, 등
```

### 부정 키워드 (28개)
```
나쁘다, 불만, 실망, 최악, 별로, 불편, 엉성, 의심, 더럽, 
거칠, 비싸다, 느리다, 부족, 시끄럽, 소음, 불안정, 고장, 
망가지, 아쉽, 후회, 짜증, 등
```

## 🔍 분석 인사이트

### 1. 긍정 리뷰 특징
- "만족", "추천", "우수" 등 직접적인 긍정 표현 많음
- "빠르다", "내구성", "실용적" 등 제품 성능 강조
- 브랜드 신뢰도 언급 빈번

### 2. 부정 리뷰 특징
- "실망", "불편", "망가지" 등 문제점 직접 표현
- "비싸다", "가격" 언급 → 가격 대비 만족도 낮음
- "소음", "품질" 등 구체적 불만 사항

### 3. 중립 리뷰 특징
- "보통", "정도", "평범하" 등 애매한 표현
- 긍정과 부정이 혼재
- 별점 3점 중심

## 🔄 다음 단계

### 1. 감성 분석 모델 구축
- [ ] 기존 sentiment 레이블 활용
- [ ] 키워드 기반 감성 점수 계산
- [ ] 워드클라우드 생성

### 2. 시각화 대시보드
- [ ] Streamlit 대시보드 구축
- [ ] 감성 분포 차트
- [ ] 제품별 키워드 분석
- [ ] 시간대별 트렌드 분석

### 3. 고급 분석
- [ ] TF-IDF 키워드 가중치
- [ ] N-gram 분석 (단어 조합)
- [ ] 감성 강도 점수화
- [ ] 토픽 모델링 (LDA)

## 📝 참고사항

### 불용어 관리
현재 기본 불용어 리스트가 포함되어 있으며, 필요시 추가 가능:

```python
cleaner = KoreanTextCleaner()
cleaner.stopwords.add('특정단어')  # 불용어 추가
cleaner.stopwords.remove('이')     # 불용어 제거
```

### 품사 태그 참고
- `NNG`: 일반 명사
- `NNP`: 고유 명사
- `VV`: 동사
- `VA`: 형용사
- `MAG`: 부사

자세한 품사 태그는 [kiwipiepy 문서](https://github.com/bab2min/kiwipiepy) 참고

## ✅ 테스트 완료

- ✅ 텍스트 정제 기능 구현
- ✅ 한글 형태소 분석 (kiwipiepy)
- ✅ 명사/키워드 추출
- ✅ 감성 키워드 분류
- ✅ 4000개 리뷰 통계 분석
- ✅ 실전 데이터 테스트 완료

## 🎉 결론

한글 리뷰 텍스트를 효과적으로 정제하고 분석할 수 있는 시스템이 완성되었습니다.
이제 이 데이터를 기반으로 감성 분석 시각화와 대시보드 구축을 진행할 수 있습니다.
