# ZLink Client (Python) / ZLink 클라이언트 (Python)

> Lightweight async Python client library for ZLink
> ZLink용 경량 비동기 Python 클라이언트 라이브러리

## 🚀 Quick Start / 빠른 시작

```bash
# Install dependencies
uv sync

# Run example client
uv run examples/basic/main.py

# Or game client
uv run examples/game/main.py
```

---

## 📦 Installation / 설치

### From PyPI / PyPI에서
```bash
pip install zlink
# or with uv
uv add zlink
```

### Local Development / 로컬 개발
```bash
uv sync
uv run main.py
```

---

## 🎯 Usage / 사용법

```python
import asyncio
from zlink import AsyncTcpClient

async def main():
    # Create client
    client = AsyncTcpClient(Host="127.0.0.1", Port=8080)
    
    # Register handlers
    client.SetUnmarshaler(_Unmarshal)
    client.AddRecvCallback(OnRecvPacket)
    
    # Connect to server
    await client.Connect()
    
    # Send message
    req = Msg_AuthLoginReq(Nickname="Player1")
    await client.Send(req.BuildTCP())
    
    # Keep running
    await asyncio.sleep(10)
    await client.Close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📁 Directory Structure / 디렉토리 구조

```
client-py/
├── src/zlink/                   # zlink 패키지
│   ├── network/                 # Network module
│   ├── logger/                  # Logging module
│   └── protocol/                # Protocol base
│
├── examples/
│   ├── basic/                   # Echo client
│   │   └── main.py
│   └── game/                    # Game client
│       └── main.py
│
└── pyproject.toml
```

---

## 🔧 Features / 특징

- **Async/Await Support** / 비동기 지원
  - Non-blocking network I/O
  - 논블로킹 네트워크 I/O

- **MessagePack Serialization** / MessagePack 직렬화
  - Fast binary format
  - 빠른 바이너리 포맷

- **Auto Protocol Handling** / 자동 프로토콜 처리
  - Type-safe message handling
  - 타입 안전 메시지 처리

---

## 📚 Examples / 예제

### Basic Echo Client / 기본 에코 클라이언트
```bash
uv run examples/basic/main.py
```

### Game Client / 게임 클라이언트
```bash
uv run examples/game/main.py
```

---

## 📄 License / 라이선스

[MIT License](../LICENSE)
