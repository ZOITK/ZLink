# ZLink Examples (Blueprints)

ZLink SDK를 실제 프로젝트에 어떻게 통합하고 활용하는지 보여주는 청사진 예제들입니다. 모든 예제는 내부에 `zlink` SDK를 포함하고 있거나 참조하고 있어 즉시 실행 가능합니다.

## 🚀 실행 가이드

### 1. Go 서버 예제 (server-go)
가장 표준적인 서버 구현체입니다. `sdk/server/zlink` 모듈을 로컬에서 참조합니다.
```bash
cd server-go
go run cmd/main.go
```

### 2. Python 클라이언트 예제 (client-py)
비동기 통신을 지원하는 Python 클라이언트입니다.
```bash
cd client-py
uv run main.py
```

### 3. Unity 클라이언트 예제 (client-unity)
모든 소스코드가 `Assets/zlink` 하위에 정규화되어 있습니다.
- 유니티 에디터에서 `examples/` 내의 `Main` 씬 또는 스크립트를 참조하여 테스트하세요.

---

모든 예제의 프로토콜은 `generator`를 통해 한꺼번에 업데이트할 수 있습니다.
