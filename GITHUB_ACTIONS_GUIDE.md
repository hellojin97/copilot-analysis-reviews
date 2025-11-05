# 🚀 GitHub Actions 이메일 리포트 자동화 가이드

## 📋 개요

GitHub Workflow를 통해 수동으로 실행하면 대시보드 리포트를 이메일로 자동 전송합니다.

---

## 🔐 1단계: GitHub Secrets 등록

GitHub 저장소에 민감한 정보(이메일 비밀번호)를 안전하게 저장합니다.

### 설정 방법:

1. **GitHub 저장소로 이동**
   - 브라우저에서 GitHub 저장소 열기

2. **Settings 클릭**
   - 상단 메뉴에서 `Settings` 선택

3. **Secrets and variables 선택**
   - 왼쪽 사이드바에서 `Secrets and variables` → `Actions` 클릭

4. **New repository secret 클릭**

5. **다음 Secrets 추가**:

#### Secret 1: SENDER_EMAIL
```
Name: SENDER_EMAIL
Secret: ilhj1228@gmail.com
```

#### Secret 2: APP_PASSWORD
```
Name: APP_PASSWORD
Secret: phoc nhry asbr svnn
```

6. **Add secret 클릭하여 저장**

### ✅ 확인 체크리스트

- [ ] `SENDER_EMAIL` Secret 등록 완료
- [ ] `APP_PASSWORD` Secret 등록 완료
- [ ] Secret 이름 정확히 입력 (대소문자 구분)

---

## 📤 2단계: GitHub에 코드 푸시

### 필수 파일 확인:

```bash
# Git 상태 확인
git status

# 필요한 파일들이 있는지 확인
# ✓ .github/workflows/send-email-report.yml
# ✓ send_email_report.py (환경변수 지원 버전)
# ✓ email_reporter.py
# ✓ recommendation_system.py
# ✓ analyze_negative_reviews.py
# ✓ text_cleaner.py
# ✓ csv/ 디렉토리 (customers.csv, products.csv, reviews.csv)
# ✓ data/reviews.db (선택사항 - 없으면 자동 생성)
```

### Git 커밋 및 푸시:

```bash
# 변경사항 추가
git add .

# 커밋
git commit -m "Add GitHub Actions workflow for email reporting"

# GitHub에 푸시
git push origin main
```

**주의**: `main` 브랜치 이름을 확인하세요 (일부는 `master`일 수 있음)

---

## ▶️ 3단계: Workflow 수동 실행

### GitHub UI에서 실행:

1. **GitHub 저장소 → Actions 탭**
   - 상단 메뉴에서 `Actions` 클릭

2. **Workflow 선택**
   - 왼쪽 사이드바에서 `Send Dashboard Email Report` 클릭

3. **Run workflow 버튼 클릭**
   - 오른쪽 상단의 `Run workflow` 버튼 클릭

4. **수신자 이메일 입력** (선택사항)
   - `recipient_email`: 기본값은 `ilhj1228@gmail.com`
   - 다른 이메일로 보내려면 여기서 변경

5. **Run workflow 실행**
   - 녹색 `Run workflow` 버튼 클릭

6. **실행 확인**
   - Workflow가 시작되면 실시간으로 진행 상황 확인 가능
   - 각 단계별 로그 확인 가능

---

## 📊 Workflow 단계 설명

### 실행 순서:

1. **Checkout 코드** ✅
   - GitHub 저장소에서 최신 코드 가져오기

2. **Python 설정** 🐍
   - Python 3.12 설치
   - pip 캐시 활성화

3. **의존성 설치** 📦
   - kiwipiepy, scikit-learn, requests 설치

4. **데이터베이스 확인** 🗄️
   - `data/reviews.db` 존재 확인
   - 없으면 CSV 파일에서 자동 생성

5. **상품 프로필 캐시 생성** 💾
   - `cache/product_profiles.pkl` 생성
   - 추천 시스템 초기화

6. **이메일 리포트 전송** 📧
   - HTML 대시보드 생성
   - 이메일 전송

7. **전송 완료 알림** ✅
   - 성공/실패 메시지 출력

---

## 🔍 실행 로그 확인

### Workflow 실행 중:

1. **Actions 탭**에서 실행 중인 workflow 클릭
2. **Jobs** 섹션에서 `send-email-report` 클릭
3. **각 단계별 로그** 확인:
   - ✅ 녹색 체크: 성공
   - 🔄 노란색: 진행 중
   - ❌ 빨간색: 실패

### 성공 시 로그 예시:
```
✓ 데이터베이스 파일 존재
✓ 캐시 파일 존재
✓ 모든 데이터 수집 완료
✓ HTML 리포트 생성 완료
✓ 이메일 전송 완료
✅ 이메일 리포트가 성공적으로 전송되었습니다!
```

---

## 🎯 수신자 이메일 변경

### 방법 1: Workflow 실행 시 입력

```
Run workflow 클릭 → recipient_email 입력 → Run workflow
```

### 방법 2: Workflow 파일 수정

`.github/workflows/send-email-report.yml` 파일에서:

```yaml
inputs:
  recipient_email:
    description: '수신자 이메일 주소'
    required: false
    default: 'your-new-email@example.com'  # 여기 수정
    type: string
```

---

## 🔧 문제 해결

### 문제 1: Secrets 오류

**증상**:
```
Error: Secret SENDER_EMAIL not found
```

**해결**:
1. GitHub Settings → Secrets 확인
2. Secret 이름 정확히 확인 (대소문자 구분)
3. Secret 재등록

### 문제 2: 이메일 전송 실패

**증상**:
```
SMTPAuthenticationError
```

**해결**:
1. Gmail 앱 비밀번호 재생성
2. `APP_PASSWORD` Secret 업데이트
3. 2단계 인증 활성화 확인

### 문제 3: 데이터베이스 파일 없음

**증상**:
```
❌ 데이터베이스 파일이 없습니다.
```

**해결**:
- CSV 파일(`csv/*.csv`)이 GitHub에 푸시되었는지 확인
- Workflow가 자동으로 DB 생성

### 문제 4: 의존성 설치 실패

**증상**:
```
ERROR: Could not find a version that satisfies the requirement
```

**해결**:
1. `.github/workflows/send-email-report.yml` 확인
2. Python 버전 호환성 확인
3. 패키지 버전 명시:
```yaml
pip install kiwipiepy==0.21.0 scikit-learn==1.5.2
```

---

## 📅 자동 스케줄 실행 (선택사항)

매일 자동으로 실행하려면 Workflow에 추가:

```yaml
on:
  workflow_dispatch:  # 수동 실행
    inputs:
      recipient_email:
        description: '수신자 이메일 주소'
        required: false
        default: 'ilhj1228@gmail.com'
        type: string
  
  schedule:  # 자동 스케줄 추가
    - cron: '0 0 * * *'  # 매일 자정 (UTC)
    # 한국 시간 오전 9시 = UTC 0시
```

### Cron 표현식 예시:
- `0 0 * * *` - 매일 자정 (UTC)
- `0 9 * * 1` - 매주 월요일 오전 9시 (UTC)
- `0 0 1 * *` - 매월 1일 자정 (UTC)

---

## 🎨 커스터마이징

### 1. 리포트 내용 변경

`send_email_report.py` 수정:

```python
# Top 10으로 변경
priority_products = analyzer.get_improvement_priority_products(top_n=10)

# 추천 개수 변경
recommendations = recommender.recommend_products(customer_id, top_n=10)
```

### 2. 이메일 제목 변경

`send_email_report.py` 수정:

```python
subject = f"[주간 리포트] 리뷰 분석 - {today}"
```

### 3. HTML 디자인 변경

`email_reporter.py`의 `generate_html_report()` 함수 수정

---

## 🔒 보안 권장사항

### ✅ 해야 할 것:
- [x] GitHub Secrets 사용
- [x] 환경변수로 민감 정보 관리
- [x] .gitignore에 .env 추가
- [x] 앱 비밀번호 사용 (일반 비밀번호 X)

### ❌ 하지 말아야 할 것:
- [ ] 코드에 이메일 비밀번호 하드코딩
- [ ] .env 파일 Git에 커밋
- [ ] Gmail 일반 비밀번호 사용
- [ ] Public 저장소에 민감 정보 노출

---

## 📊 Workflow 파일 구조

```yaml
.github/workflows/send-email-report.yml
├── on: workflow_dispatch          # 수동 실행 트리거
│   └── inputs                     # 입력 파라미터
│       └── recipient_email        # 수신자 이메일
├── jobs                           # 작업 정의
│   └── send-email-report         # 작업 이름
│       ├── runs-on: ubuntu-latest # 실행 환경
│       └── steps                  # 실행 단계
│           ├── Checkout           # 코드 가져오기
│           ├── Python 설정        # Python 3.12 설치
│           ├── 의존성 설치        # pip install
│           ├── 데이터베이스 확인  # DB 체크
│           ├── 캐시 생성          # 프로필 캐시
│           └── 이메일 전송        # 리포트 전송
```

---

## 🎯 체크리스트

### 설정 완료 확인:

- [ ] GitHub Secrets 등록 (`SENDER_EMAIL`, `APP_PASSWORD`)
- [ ] Workflow 파일 생성 (`.github/workflows/send-email-report.yml`)
- [ ] `send_email_report.py` 환경변수 지원 버전으로 수정
- [ ] CSV 파일 Git에 포함 (`csv/*.csv`)
- [ ] `.gitignore` 설정 완료
- [ ] GitHub에 코드 푸시 완료

### 실행 확인:

- [ ] Actions 탭에서 Workflow 확인
- [ ] 수동 실행 테스트
- [ ] 이메일 수신 확인
- [ ] 로그 확인

---

## 🎉 완료!

이제 GitHub에서 버튼 클릭 한 번으로 대시보드 리포트를 이메일로 받을 수 있습니다!

### 실행 방법:
1. GitHub → Actions → Send Dashboard Email Report
2. Run workflow 클릭
3. (선택) 수신자 이메일 입력
4. Run workflow 실행
5. 이메일 확인! 📬

---

## 📞 문의

문제가 발생하면 GitHub Actions 로그를 확인하세요:
- Actions 탭 → 실행 중인 workflow → 각 단계별 로그 확인

**Happy Reporting!** 🚀
