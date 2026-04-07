# ZLink에 기여하기

ZLink에 기여해주셔서 감사합니다! 이 문서는 프로젝트에 기여하는 방법을 설명합니다.

## 🤝 기여 방법

### 1. 버그 리포트

버그를 발견하셨나요? [GitHub Issues](https://github.com/ZOITK/ZLink/issues)에 보고해주세요.

**버그 리포트 포함 사항:**
- 버그에 대한 명확한 설명
- 재현 단계
- 예상 동작 vs 실제 동작
- 환경 정보 (OS, Go/Python 버전)

### 2. 기능 요청

새로운 기능이 필요하신가요? [GitHub Discussions](https://github.com/ZOITK/ZLink/discussions)에서 아이디어를 제안해주세요.

**기능 요청 포함 사항:**
- 기능 설명
- 사용 사례
- 예상 동작

### 3. 코드 기여

#### 준비 사항

1. **저장소 Fork**
   ```bash
   # GitHub에서 ZOITK/ZLink를 fork합니다
   ```

2. **로컬에 클론**
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/ZLink.git
   cd ZLink
   git remote add upstream https://github.com/ZOITK/ZLink.git
   ```

3. **브랜치 생성**
   ```bash
   git checkout -b feature/your-feature-name
   # 또는 버그 수정
   git checkout -b fix/bug-name
   ```

#### 코드 작성 규칙

**Go:**
- Go 공식 스타일 가이드 준수
- `go fmt`, `go vet` 통과
- 함수에 한글 주석 작성

**Python:**
- PEP 8 준수
- 타입 힌트 사용
- 함수에 한글 docstring 작성

**C#:**
- C# 공식 코딩 규칙 준수
- 클래스/메서드 XML 문서 작성 (한글)

#### 커밋 메시지 규칙

```
[타입] 제목

- 한글로 작성
- 제목은 명령형 (예: "Add", "Fix", "Update")
- 본문은 왜 이 변경이 필요한지 설명

예:
[Feat] Go 서버에 WebSocket 지원 추가

- TCP 기반 통신에서 WebSocket 지원으로 확장
- 웹 브라우저 클라이언트 연결 가능
- 기존 TCP 프로토콜은 하위 호환성 유지
```

**커밋 타입:**
- `[Feat]` - 새로운 기능
- `[Fix]` - 버그 수정
- `[Docs]` - 문서 변경
- `[Refactor]` - 코드 리팩토링
- `[Test]` - 테스트 추가/수정
- `[Chore]` - 빌드, 의존성 등

#### Pull Request 프로세스

1. **upstream main과 동기화**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Pull Request 생성**
   - GitHub에서 PR을 생성합니다
   - 설명: 변경 사항과 이유를 명확하게 작성
   - 관련 Issue가 있으면 `Closes #이슈번호` 포함

4. **리뷰 대응**
   - 코드 리뷰 피드백에 응답
   - 필요한 변경사항 수정
   - 새 커밋으로 추가 (재작성 금지)

#### 테스트

PR을 제출하기 전에 로컬에서 테스트하세요:

**Go 서버:**
```bash
cd engine/server-go
go test ./...
go build .
```

**Python 클라이언트:**
```bash
cd engine/client-python
uv run pytest
```

## 📋 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/YOUR_GITHUB_USERNAME/ZLink.git
cd ZLink

# Go 환경 설정
go mod download

# Python 환경 설정
cd engine/client-python
uv sync
```

## 🗂️ 프로젝트 구조

- `engine/` - 언어별 엔진 구현
- `generator/` - 프로토콜 코드 생성기
- `templates/` - 프로젝트 템플릿
- `schemas/` - 프로토콜 YAML 정의
- `scripts/` - 헬퍼 스크립트
- `tests/` - 테스트 코드

## 💬 질문 및 지원

- **일반 질문**: [GitHub Discussions](https://github.com/ZOITK/ZLink/discussions)
- **버그 리포트**: [GitHub Issues](https://github.com/ZOITK/ZLink/issues)

## 📄 라이선스

기여하신 코드는 MIT 라이선스 하에 배포됩니다.

---

감사합니다! 🙏
