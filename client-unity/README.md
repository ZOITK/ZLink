# ZLink Client (Unity) / ZLink 클라이언트 (Unity)

> C# client library for Unity3D
> Unity3D용 C# 클라이언트 라이브러리

## 🚀 Getting Started / 시작하기

### 1. Copy Assets / Assets 복사
```bash
# Copy Assets/ folder to your Unity project
cp -r Assets /path/to/your/unity/project/
```

### 2. Setup Connection / 연결 설정
```csharp
using Zoit.Network;
using Zoit.Logger;

public class GameClient : MonoBehaviour
{
    private TcpClient client;

    async void Start()
    {
        client = new TcpClient();
        Protocol.Register(client, OnRecvPacket);
        
        if (await client.ConnectAsync("127.0.0.1", 8080))
        {
            Debug.Log("Connected to server");
        }
    }

    void OnRecvPacket(object client, object msg)
    {
        switch (msg)
        {
            case Msg_AuthLoginRes loginRes:
                HandleLogin(loginRes);
                break;
        }
    }
}
```

---

## 📁 Directory Structure / 디렉토리 구조

```
client-unity/
├── Assets/
│   ├── ZoSocket/
│   │   ├── Engine/          # Client library
│   │   │   ├── Network/
│   │   │   ├── Logger/
│   │   │   └── Protocol/
│   │   └── Protocol.cs      # Generated protocol
│   ├── Plugins/             # Dependencies
│   └── Examples/
│       ├── Basic/
│       └── Game/
│
└── README.md
```

---

## 🔧 Features / 특징

- **Unity-Compatible** / Unity 호환
  - Works with Unity 2020+
  - 2020+ 버전 지원

- **Async Support** / 비동기 지원
  - async/await patterns
  - async/await 패턴 지원

- **MessagePack** / MessagePack
  - Fast serialization
  - 빠른 직렬화

---

## 📚 Examples / 예제

See `Assets/Examples/` for:
- `Basic/` - Echo client example
- `Game/` - Full game client example

---

## 📄 License / 라이선스

[MIT License](../LICENSE)
