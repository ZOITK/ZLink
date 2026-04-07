# ZLink / ZLink 소켓 프레임워크

> Lightweight multi-platform socket framework for game development
> 게임 개발을 위한 경량 멀티플랫폼 소켓 프레임워크

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📦 Overview / 개요

ZLink is a modular socket communication framework consisting of three independent projects. 
Choose what you need and clone/use that specific folder.

ZLink는 3개의 독립적인 프로젝트로 구성된 모듈식 소켓 통신 프레임워크입니다.
필요한 것만 선택해서 사용하세요.

### Three Independent Projects / 3가지 독립 프로젝트

- **[server-go](./server-go/)** - Go server with protocol generator
  - 프로토콜 제너레이터가 포함된 Go 서버
  - Clone and run `cd server-go && go run examples/basic/main.go`

- **[client-py](./client-py/)** - Python async client library
  - Python 비동기 클라이언트 라이브러리
  - Run with `cd client-py && uv sync && uv run examples/basic/main.py`

- **[client-unity](./client-unity/)** - Unity3D C# client
  - Unity3D C# 클라이언트
  - Copy Assets folder to your Unity project

---

## 🚀 Quick Start / 빠른 시작

### Option 1: Go Server / Go 서버 개발

```bash
# Clone the entire repo or just server-go
git clone https://github.com/ZOITK/ZLink
cd ZLink/server-go

# Test basic server (includes pre-built Protocol.go)
cd examples/basic
go run main.go

# Server starts on TCP port 8080, UDP port 8081
# Press Ctrl+C to stop
```

### Option 2: Python Client / Python 클라이언트 개발

```bash
# Clone and setup
git clone https://github.com/ZOITK/ZLink
cd ZLink/client-py
uv sync

# Run basic client example
uv run examples/basic/main.py
```

### Option 3: Unity Client / Unity 클라이언트 개발

```bash
# Copy client code to your Unity project
# 1. Open your Unity project Assets folder
# 2. Copy ZLink/client-unity/Assets contents to your Assets/
# 3. Use in scripts: using ZoSocket; or using ZoSocket.Protocol;
```

---

## 📁 Repository Structure / 저장소 구조

```
ZLink/
├── server-go/                # Go 서버 프레임워크
│   ├── pkg/                  # 핵심 라이브러리 (config, logger, network)
│   ├── generator/            # 프로토콜 코드 생성기
│   ├── schemas/              # YAML 프로토콜 정의 (basic, game)
│   ├── examples/
│   │   ├── basic/            # 기본 예제 (로그인, 메시지 송수신)
│   │   │   ├── main.go       # 서버 코드
│   │   │   └── protocol/     # Protocol.go (자동 생성됨)
│   │   └── game/             # 게임 예제 (방, 게임, 채팅)
│   │       ├── main.go
│   │       └── protocol/     # Protocol.go (자동 생성됨)
│   ├── Makefile              # 프로토콜 생성 및 빌드
│   └── README.md
│
├── client-py/                # Python 클라이언트
│   ├── src/zlink/            # zlink 패키지 (network, protocol)
│   ├── examples/
│   │   ├── basic/
│   │   │   ├── main.py       # 기본 클라이언트
│   │   │   └── pyproject.toml
│   │   └── game/
│   │       ├── main.py       # 게임 클라이언트
│   │       └── pyproject.toml
│   ├── pyproject.toml        # 패키지 설정
│   └── README.md
│
├── client-unity/             # Unity C# 클라이언트
│   ├── Assets/
│   │   └── ZoSocket/         # 메인 네임스페이스
│   │       ├── Engine/       # 네트워크 라이브러리
│   │       ├── Protocol/     # Protocol.cs 파일
│   │       └── Examples/     # 예제 씬
│   ├── examples/
│   └── README.md
│
├── go.work                   # Go workspace (pkg, examples 포함)
├── Makefile                  # 프로토콜 생성
└── README.md                 # 이 파일
```

---

## 📖 How It Works / 작동 원리

### Server-Client Communication Flow / 서버-클라이언트 통신 흐름

```
1. Server defines protocol in YAML
   서버가 YAML로 프로토콜 정의
   └─ schemas/basic.yaml (로그인, 메시지 송수신)
   └─ schemas/game.yaml (방, 게임 로직)

2. Generator creates Protocol.go
   제너레이터가 Protocol.go 생성
   └─ examples/basic/protocol/Protocol.go
   └─ examples/game/protocol/Protocol.go

3. Server implements OnRecvPacket handler
   서버가 메시지 핸들러 구현
   └─ examples/basic/main.go
   └─ examples/game/main.go

4. Client receives Protocol.go (manually)
   클라이언트가 Protocol 파일을 받음 (수동)
   └─ server가 protocol 파일 전달
   └─ 클라이언트가 구현

5. Client and Server communicate with MessagePack
   MessagePack으로 통신
```

---

## 🔧 Features / 특징

- **Protocol Auto-generation** / 프로토콜 자동생성
  - Define packets in YAML, generate code automatically
  - YAML로 패킷 정의, 코드 자동생성

- **Multi-language** / 다중 언어 지원
  - Go server, Python client, C#/Unity client
  - Go 서버, Python 클라이언트, C#/Unity 클라이언트

- **TCP & UDP** / TCP 및 UDP 지원
  - Configurable protocol per packet
  - 패킷별로 프로토콜 선택 가능

- **MessagePack Serialization** / MessagePack 직렬화
  - Fast binary format, smaller payload
  - 빠른 바이너리 포맷, 작은 페이로드

- **Session Management** / 세션 관리
  - Automatic session lifecycle
  - Session-based packet routing
  - 자동 세션 관리, 세션 기반 라우팅

---

## 💻 Detailed Usage / 상세 사용법

### Modifying Protocol / 프로토콜 수정하기

Server-side 프로토콜을 수정할 때:

```bash
cd ZLink/server-go

# 1. Edit protocol schema
vi schemas/basic.yaml  # or schemas/game.yaml

# 2. Generate Protocol.go
make gen

# 3. Rebuild server
cd examples/basic
go run main.go
```

### Using with Existing Project / 기존 프로젝트에 적용

#### Go Server
```bash
# Copy entire server-go folder to your project
cp -r ZLink/server-go ../my-game-server
cd ../my-game-server

# Modify examples/basic/main.go with your game logic
go run examples/basic/main.go
```

#### Python Client
```bash
# Add to your project's pyproject.toml
# (if using as external module)
dependencies = [
    "zlink",  # from local ZLink/client-py
]

# Or copy client code to your project
cp -r ZLink/client-py/src/zlink ../my-game-client/src/
```

#### Unity Client
```
1. Open your Unity project
2. Copy ZLink/client-unity/Assets to your Assets folder
3. In your C# script:
   using ZoSocket;
   
   var client = new TCPClient("localhost", 8080);
   await client.Connect();
   await client.SendLogin(nickname);
```

---

## 📚 Documentation / 문서

- [Go Server Guide](./server-go/README.md) - 서버 개발 상세 가이드
- [Python Client Guide](./client-py/README.md) - Python 클라이언트 가이드
- [Unity Client Guide](./client-unity/README.md) - Unity C# 클라이언트 가이드

---

## 🎯 Examples / 예제

### Basic Example / 기본 예제
- **Protocol**: Login, Send/Receive Message, Heartbeat
- **Server**: `server-go/examples/basic/main.go`
- **Python Client**: `client-py/examples/basic/main.py`
- **Use case**: Chat server, simple message broadcasting

### Game Example / 게임 예제
- **Protocol**: Room creation, Room search, Game start, Number guessing
- **Server**: `server-go/examples/game/main.go`
- **Python Client**: `client-py/examples/game/main.py`
- **Use case**: Multiplayer game server with game rooms

---

## 🔧 Configuration / 설정

### Server Configuration / 서버 설정

Environment variables:

```bash
TCP_PORT=8080         # TCP 포트 (기본값: 8080)
UDP_PORT=8081         # UDP 포트 (기본값: 8081)
NODE_ENV=development  # 환경 (development/production)
```

### Client Configuration / 클라이언트 설정

In code / 코드에서:

```python
# Python
client = TCPClient(host="127.0.0.1", port=8080)
await client.connect()
```

```csharp
// C#
var client = new TCPClient("127.0.0.1", 8080);
await client.ConnectAsync();
```

---

## 📄 License / 라이선스

[MIT License](LICENSE)
