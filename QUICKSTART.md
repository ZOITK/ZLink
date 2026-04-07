# ZLink Quick Start (5분)

이 가이드는 ZLink를 사용하여 Go 서버와 Python 클라이언트를 5분 안에 실행하는 방법을 설명합니다.

## 전제 조건

- Git 설치됨
- Go 1.25.6+ 설치됨
- Python 3.13+ 설치됨
- uv 설치됨

## Step 1: ZLink 저장소 클론 (1분)

```bash
git clone https://github.com/ZOITK/ZLink.git
cd ZLink
```

## Step 2: Go 서버 생성 및 실행 (2분)

### 서버 프로젝트 생성
```bash
make server OUTPUT=../my-server --engine-local ./engine/server-go
```

### 서버 빌드 및 실행
```bash
cd ../my-server
go mod tidy
go build -o server_bin main.go
./server_bin
```

출력:
```
2026-04-07T10:00:00Z	INFO	ZLink Framework Unified Example Server 시작
```

**서버가 포트 8080에서 실행 중입니다!**

## Step 3: Python 클라이언트 생성 및 실행 (2분)

**새 터미널에서:**

```bash
# ZLink 디렉토리로 이동
cd ZLink

# Python 클라이언트 생성
make client LANG=python OUTPUT=../my-client --engine-local ./engine/client-python
cd ../my-client

# 클라이언트 실행
uv run main.py
```

클라이언트가 서버에 연결되었습니다!

---

## 🎉 축하합니다!

이제 ZLink로 멀티플랫폼 게임 서버 아키텍처가 준비되었습니다.

### 다음 단계

1. **프로토콜 정의하기**
   - `ZLink/schemas/` 폴더에 `.yaml` 파일 생성
   - `make gen`으로 프로토콜 코드 자동 생성

2. **비즈니스 로직 구현**
   - `my-server/main.go` - `OnRecvPacket()` 함수 수정
   - `my-client/main.py` - `OnRecvPacket()` 함수 수정

3. **C# 클라이언트 추가**
   ```bash
   make client LANG=csharp OUTPUT=../my-unity
   ```

## 📚 상세 문서

- [README.md](README.md) - 프로젝트 개요
- [CONTRIBUTING.md](CONTRIBUTING.md) - 기여 가이드

## 🆘 문제 해결

### Go 빌드 오류: `unrecognized import path`
```bash
# engine/server-go에서 go.mod 확인
cat ../ZLink/engine/server-go/go.mod
```

### Python 실행 오류: `ModuleNotFoundError`
```bash
# uv로 패키지 재설치
uv sync
uv run main.py
```

---

**Happy coding! 🚀**
