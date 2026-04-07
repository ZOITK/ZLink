# ZLink Server (Go) / ZLink 서버 (Go)

> Production-ready Go server framework with built-in protocol generator
> 프로토콜 제너레이터가 포함된 프로덕션 레벨 Go 서버 프레임워크

## 🚀 Quick Start / 빠른 시작

```bash
# Install dependencies
go mod tidy

# Generate protocol from YAML schema
make gen

# Run example server
cd examples/basic
go run main.go

# Or build
go build -o server_bin main.go
./server_bin
```

---

## 📋 Workflow / 워크플로우

### 1. Define Protocol / 프로토콜 정의
Create YAML schema in `schemas/`:

```yaml
# schemas/game.yaml
metadata:
  version: 1
  categories: [system, auth, game]
  protocols: [tcp, udp]

definitions:
  auth:
    packets:
      - name: Login
        idx: 1
        proto: tcp
        pair:
          req: { fields: { Nickname: string } }
          res: { fields: { PlayerID: uint32, Result: uint32 } }
```

### 2. Generate Protocol Code / 프로토콜 코드 생성
```bash
make gen
# Generates: protocol/Protocol.go
```

### 3. Implement Server Logic / 서버 로직 구현
```go
// main.go
func OnRecvPacket(s protocol.ISession, msg any) {
    switch m := msg.(type) {
    case *protocol.Msg_AuthLoginReq:
        handleLogin(s, m)
    }
}
```

### 4. Build & Run / 빌드 & 실행
```bash
go build -o server_bin main.go
TCP_PORT=8080 UDP_PORT=8081 ./server_bin
```

---

## 📁 Directory Structure / 디렉토리 구조

- `pkg/` - Core server library / 서버 코어 라이브러리
- `generator/` - Protocol code generator / 프로토콜 코드 생성기
- `schemas/` - Protocol YAML definitions / YAML 프로토콜 정의
- `examples/` - Sample implementations / 예제
  - `basic/` - Echo server / 에코 서버
  - `game/` - Number guessing game / 숫자맞추기 게임
- `protocol/` - Generated protocol code / 생성된 프로토콜 코드
