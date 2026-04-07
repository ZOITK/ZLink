# ZLink / ZLink 소켓 프레임워크

> Lightweight multi-platform socket framework for game development
> 게임 개발을 위한 경량 멀티플랫폼 소켓 프레임워크

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📦 Overview / 개요

ZLink is a modular socket communication framework consisting of three independent projects:

ZLink는 3개의 독립적인 프로젝트로 구성된 모듈식 소켓 통신 프레임워크입니다:

- **[server-go](./server-go/)** - Go server with protocol generator / 프로토콜 제너레이터가 포함된 Go 서버
- **[client-py](./client-py/)** - Python async client library / Python 비동기 클라이언트 라이브러리
- **[client-unity](./client-unity/)** - Unity3D C# client / Unity3D C# 클라이언트

---

## 🚀 Getting Started / 시작하기

Choose what you need and clone only that folder:

필요한 것만 선택해서 clone하세요:

### For Go Server Developers / Go 서버 개발자
```bash
git clone https://github.com/ZOITK/ZLink
cd ZLink/server-go
make help
```

### For Python Client Developers / Python 클라이언트 개발자
```bash
git clone https://github.com/ZOITK/ZLink
cd ZLink/client-py
uv sync
```

### For Unity Developers / Unity 개발자
```bash
git clone https://github.com/ZOITK/ZLink
# Copy ZLink/client-unity/Assets to your project
```

---

## 📁 Repository Structure / 저장소 구조

```
ZLink/
├── server-go/               # Go 서버 + 프로토콜 제너레이터
│   ├── pkg/                 # 서버 코어 라이브러리
│   ├── generator/           # 프로토콜 코드 생성기
│   ├── schemas/             # YAML 프로토콜 정의
│   ├── examples/
│   │   ├── basic/           # 기본 에코 서버
│   │   └── game/            # 숫자맞추기 게임
│   └── README.md
│
├── client-py/               # Python 클라이언트
│   ├── src/zlink/           # zlink 패키지
│   ├── examples/
│   │   ├── basic/           # 기본 에코 클라이언트
│   │   └── game/            # 게임 클라이언트
│   └── README.md
│
└── client-unity/            # Unity C# 클라이언트
    ├── Assets/              # 클라이언트 코드
    ├── examples/
    │   ├── basic/
    │   └── game/
    └── README.md
```

---

## 🔧 Features / 특징

- **Protocol Auto-generation** / 프로토콜 자동생성
  - Define in YAML, generate code automatically
  - YAML로 정의하면 코드 자동생성

- **Multi-language Support** / 다중 언어 지원
  - Go, Python, C#/Unity

- **TCP/UDP** / TCP/UDP 지원
  - Flexible network protocols
  - 유연한 네트워크 프로토콜

- **MessagePack Serialization** / MessagePack 직렬화
  - Fast binary serialization
  - 빠른 바이너리 직렬화

- **Async/Await Support** / Async/Await 지원
  - Non-blocking network I/O
  - 논블로킹 네트워크 I/O

---

## 📚 Documentation / 문서

- [Go Server Guide](./server-go/README.md) - 서버 개발 가이드
- [Python Client Guide](./client-py/README.md) - Python 클라이언트 가이드
- [Unity Client Guide](./client-unity/README.md) - Unity 클라이언트 가이드

---

## 📄 License / 라이선스

[MIT License](LICENSE)
