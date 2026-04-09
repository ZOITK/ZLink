# ZLink - High-Performance Multi-Platform Socket Framework
# ZLink - 고성능 멀티플랫폼 소켓 프레임워크

> **"Copy the `zlink` folder, Build your Logic."**
> **"`zlink` 폴더를 복사하고, 당신의 로직을 구축하세요."**

ZLink is an ultra-lightweight, high-performance multi-platform socket framework for game and real-time application development.
ZLink는 게임 및 실시간 애플리케이션 개발을 위한 초경량, 고성능 멀티플랫폼 소켓 프레임워크입니다.

It aims for **Atomic Portability**, allowing you to start development immediately by copying a single `zlink` folder to any platform.
모든 플랫폼에서 `zlink` 폴더 하나만 복사하면 즉시 개발을 시작할 수 있는 **원자적 휴대성(Atomic Portability)**을 지향합니다.

---

## 📦 Architecture Overview
## 📦 아키텍처 개요

ZLink completely separates the core engine (SDK) from the implementation examples.
ZLink는 핵심 엔진(SDK)과 이를 활용하는 예제(Examples)가 완벽하게 분리되어 있습니다.

- **`sdk/`**: A complete module containing the core engine and protocol base for each language.
- **`sdk/`**: 각 언어별 핵심 통신 엔진과 프로토콜 기반이 담긴 **완전체 모듈**입니다.
- **`examples/`**: A blueprint showing how to integrate and use the SDK in a project.
- **`examples/`**: SDK를 프로젝트에 어떻게 통합하고 사용하는지 보여주는 **청사진(Blueprint)**입니다.
- **`generator/`**: A powerful tool that automatically generates Go, Python, and C# packet code from YAML definitions.
- **`generator/`**: YAML 정의만으로 Go, Python, C# 패킷 코드를 자동 생성해 주는 강력한 도구입니다.

---

## 🚀 Quick Start
## 🚀 빠른 시작

### 1. Protocol Definition
### 1. 프로토콜 정의
Define the packet structure by modifying the `generator/schemas/basic.yaml` file.
`generator/schemas/basic.yaml` 파일을 수정하여 패킷 구조를 정의합니다.

```bash
cd generator
make gen   # Generate protocol and sync to all SDKs/Examples
           # 프로토콜 생성 및 모든 SDK/예제 자동 배포 및 동기화
```

### 2. Run Go Server
### 2. Go 서버 실행
Integrate the `sdk/server/zlink` folder into your project and run the server.
`sdk/server/zlink` 폴더를 프로젝트에 포함하고 서버를 실행합니다.

```bash
cd examples/server-go
go run basicServer.go
```

### 3. Run Clients (Python & Unity)
### 3. 클라이언트 실행 (Python 및 Unity)

- **Python**: Copy the `sdk/client/python/zlink` folder.
- **Python**: `sdk/client/python/zlink` 폴더를 복사합니다.
  ```bash
  cd examples/client-py
  uv run basicClient.py
  ```

- **Unity**: Copy the entire `sdk/client/unity/zlink` folder under Unity's `Assets`.
- **Unity**: `sdk/client/unity/zlink` 폴더 전체를 Unity의 `Assets` 하위에 복사합니다.
  - Refer to `examples/client-unity/BasicClient.cs` to connect components.
  - `examples/client-unity/BasicClient.cs` 예제를 참고하여 컴포넌트를 연결하세요.

---

## 📁 Project Structure
## 📁 저장소 구조

```text
ZLink Root/
├── sdk/                 # Core libraries for each platform (Source of Truth)
│                        # 플랫폼별 핵심 라이브러리
│   ├── server/zlink/    # Go server engine with built-in protocol
│   │                    # Go 서버 엔진 및 프로토콜 내장
│   ├── client/python/zlink/ # Python asynchronous library
│   │                        # Python 비동기 라이브러리
│   └── client/unity/zlink/  # C# module and plugins for Unity
│                            # Unity용 C# 모듈 및 플러그인
├── examples/            # SDK usage projects (Executable samples)
│                        # SDK 활용 프로젝트 (실행 가능한 샘플)
│   ├── server-go/       # Go server implementation example
│   │                    # Go 서버 구현 예제
│   ├── client-py/       # Python client implementation example
│   │                    # Python 클라이언트 구현 예제
│   └── client-unity/    # Unity client implementation example
│                        # Unity 클라이언트 구현 예제
├── generator/           # Protocol auto-generator
│                        # 프로토콜 자동 생성기
└── docs/                # Architecture and detailed guidelines
                         # 아키텍처 및 상세 가이드라인
```

---

## 🌟 Core Strategy
## 🌟 핵심 가치

1. **Single Folder Packaging**: The `zlink` folder is independent in all languages. This folder alone completes the communication foundation.
1. **원폴더(Single Folder) 패키징**: 모든 언어에서 `zlink` 폴더는 독립적입니다. 이 폴더만 있으면 별도의 설정 없이 통신 기반이 완성됩니다.

2. **Protocol-SDK Integration**: The generator deploys code directly inside the SDK. Engines and packets move together, eliminating version management pain.
2. **프로토콜-SDK 일체화**: 제네레이터는 코드를 SDK 내부에 직접 배포합니다. 엔진과 패킷이 늘 함께 움직여 버전 관리의 고통을 없앴습니다.

3. **Architecture Symmetry**: The session management philosophy of the server (Go) is reflected directly in the clients (Python/C#).
3. **완벽한 대칭성(Architecture Symmetry)**: 서버(Go)의 세션 관리 철학이 클라이언트(Python/C#)에도 그대로 투영되어 익숙한 개발 경험을 제공합니다.

---

## 📄 License
## 📄 라이선스
[MIT License](LICENSE)
