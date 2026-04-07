# ZLink

> 멀티플랫폼 게임 서버 프레임워크 - Go 서버, Python/C# 클라이언트를 한 번에 구축하세요.

[![GitHub](https://img.shields.io/badge/GitHub-ZOITK%2FZLink-blue)](https://github.com/ZOITK/ZLink)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 특징

- **멀티플랫폼 지원**: Go 서버, Python 클라이언트, Unity3D C# 클라이언트
- **자동 프로젝트 생성**: `make server`/`make client` 명령어로 프로젝트 자동 생성
- **MessagePack 기반**: 고속 직렬화/역직렬화
- **프로토콜 정의 기반**: YAML 스키마로 프로토콜 정의 후 자동 코드 생성
- **개발 친화적**: 로컬 개발 모드 지원, 템플릿 기반 프로젝트 생성

## 🚀 빠른 시작

### 1단계: 저장소 클론
```bash
git clone https://github.com/ZOITK/ZLink.git
cd ZLink
```

### 2단계: Go 서버 생성
```bash
make server OUTPUT=../my-server --engine-local ./engine/server-go
cd ../my-server
go mod tidy && go build -o server_bin main.go
./server_bin
```

### 3단계: Python 클라이언트 생성
```bash
make client LANG=python OUTPUT=../my-client --engine-local ./engine/client-python
cd ../my-client
uv run main.py
```

### 4단계: Unity C# 클라이언트 생성
```bash
make client LANG=csharp OUTPUT=../my-unity
```

## 📦 설치 및 요구사항

### 시스템 요구사항
- **Go 1.25.6+** (서버 개발)
- **Python 3.13+** (Python 클라이언트)
- **uv** (Python 패키지 관리)
- **Make** (프로젝트 생성 자동화)

### 의존성 설치

**macOS:**
```bash
brew install go
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Linux:**
```bash
# Go 설치: https://golang.org/dl/
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
# Go 설치: https://golang.org/dl/
irm https://astral.sh/uv/install.ps1 | iex
```

## 📁 프로젝트 구조

```
ZLink/
├── engine/
│   ├── server-go/
│   │   ├── pkg/
│   │   │   ├── network/     # TCP/UDP 네트워크
│   │   │   ├── logger/      # 로깅
│   │   │   └── config/      # 설정
│   │   └── go.mod
│   ├── client-python/       # Python 클라이언트
│   │   ├── src/zoit_socket_client/
│   │   └── pyproject.toml
│   └── client-csharp/       # C# 클라이언트
│       ├── logger/
│       ├── network/
│       └── protocol/
├── generator/               # 프로토콜 생성기
├── templates/               # 프로젝트 템플릿
├── schemas/                 # 프로토콜 YAML 정의
├── scripts/
│   └── project_generator.py
├── Makefile
├── go.work
└── README.md
```

## 🔧 명령어

```bash
# 프로토콜 생성
make gen

# 서버 생성 (로컬 개발)
make server OUTPUT=../my-server --engine-local ./engine/server-go

# 클라이언트 생성 (Python)
make client LANG=python OUTPUT=../my-client --engine-local ./engine/client-python

# 클라이언트 생성 (C#)
make client LANG=csharp OUTPUT=../my-unity

# 도움말
make help
```

## 📖 문서

- [QUICKSTART.md](QUICKSTART.md) - 5분 안에 시작하기
- [CONTRIBUTING.md](CONTRIBUTING.md) - 기여 가이드

## 📄 라이선스

[MIT License](LICENSE)
