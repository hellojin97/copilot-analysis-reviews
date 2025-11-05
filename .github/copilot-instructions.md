Style Guide Instructions for Copilot
1. 언어: Python

- 모든 Python 코드는 PEP 8 스타일 가이드를 엄격하게 준수합니다.

2. 네이밍 컨벤션 (Naming Convention)

- 변수와 함수명은 snake_case를 사용합니다. (예: `user_name`, `calculate_total`)
- 클래스명은 PascalCase (또는 CapWords)를 사용합니다. (예: `UserAccount`, `DatabaseConnection`)
- 상수는 전체 대문자와 스네이크 케이스를 조합하여 사용합니다. (예: `MAX_RETRIES`, `DEFAULT_TIMEOUT`)

3. 주석 및 문서화 (Comments & Docstrings)

- 모든 public 함수와 클래스에는 반드시 Docstring을 한글로 작성합니다.
- Docstring은 함수의 목적, 매개변수(Args), 반환 값(Returns)을 명확하게 설명해야 합니다.
- 복잡한 로직에는 `#`를 사용하여 간결한 인라인 주석을 추가합니다.

4. 코드 형식

- 한 줄의 최대 길이는 88자로 제한합니다.
- import 구문은 표준 라이브러리, 서드 파티 라이브러리, 로컬 애플리케이션 순서로 그룹화합니다.


Framework & Library Usage Guide
1. 웹 프레임워크 (Web Framework)
- 모든 웹 애플리케이션은 FastAPI를 사용하여 개발합니다.
- API 엔드포인트를 생성할 때는 FastAPI의 자동 JSON 직렬화 기능을 활용합니다.
- 라우팅(Routing)은 `@app.get()`, `@app.post()` 등의 데코레이터를 사용합니다.
- 요청 및 응답 데이터는 Pydantic 모델을 사용하여 타입 힌트와 자동 검증을 적용합니다.
2. 데이터베이스 (Database)
- 데이터베이스는 SQLite를 사용합니다.
- 데이터베이스 파일 경로는 환경 변수로 관리하거나, 프로젝트 루트의 `data/` 디렉토리 내에 저장합니다.
- 데이터베이스와의 모든 상호작용은 SQLAlchemy ORM을 통해 이루어져야 합니다.
- SQLAlchemy 연결 URI는 `sqlite:///경로/파일명.db` 형식을 사용합니다. (예: `sqlite:///data/app.db`)
- 절대로 순수 SQL 쿼리(Raw SQL Query)를 문자열로 작성하지 않습니다.
- 데이터베이스 모델은 `db.Model`을 상속받아 클래스로 정의합니다.
3. API 클라이언트 (API Client)
- 외부 HTTP API를 호출할 때는 `requests` 라이브러리를 사용합니다.
- 모든 `requests` 호출에는 5초의 타임아웃(timeout)을 설정해야 합니다.
(예: `requests.get(url, timeout=5)`)


Security Rules for Copilot
1. SQL 인젝션 방지 (Preventing SQL Injection)
- 데이터베이스 쿼리를 생성할 때, f-string이나 '+' 연산자를 사용하여 사용자 입력을 직접 삽입하는 것을 금지합니다.
- 항상 ORM을 사용하거나, 파라미터화된 쿼리(parameterized queries)를 사용하여 SQL 인젝션을 방지합니다.
2. 사용자 입력 처리 (Handling User Input)
- 외부로부터 들어오는 모든 입력(예: HTTP 요청의 body, query parameter)은 사용하기 전에 반드시 유효성을 검사(validate)하고 필요한 경우 정제(sanitize)해야 합니다.
- 파일 업로드 시 파일명을 처리할 때는 `werkzeug.utils.secure_filename`과 같은 라이브러리를 사용하여 경로 조작(Path Traversal) 공격을 방지합니다.
3. 비밀 정보 관리 (Secrets Management)
- API 키, 데이터베이스 비밀번호, 토큰 등의 민감한 정보는 소스 코드에 절대 하드코딩하지 않습니다.
- 모든 비밀 정보는 환경 변수(Environment Variables) 또는 Vault와 같은 보안 관리 도구를 통해 불러와야 합니다.
4. 에러 처리 (Error Handling)
- `try...except` 블록에서 `except Exception:`과 같이 너무 광범위한 예외 처리를 지양하고,
구체적인 예외를 명시합니다.
- 사용자에게 보여주는 에러 메시지에는 시스템 내부 경로, 스택 트레이스 등 민감한 정보가 포함되어서는 안 됩니다.