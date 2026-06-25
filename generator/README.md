# ZLink Protocol Generator

[English](#english) | [한국어](#korean)

<a name="english"></a>
# English

The ZLink Protocol Generator is the core tool of the ZLink socket framework. It simultaneously generates Go, Python, and C# packet code based on YAML definitions and automatically deploys them to each framework.

---

## 🛠 Usage

### Option 1: Using Makefile (Local Development)

1. **Define Schema**: Modify YAML files in the `schemas/` folder to define the packet structure.
2. **Generate Code**: Run the following command in the generator folder.
   ```bash
   make gen schemas=./schemas/your_schema.yaml output=<destination_dir>
   ```

### Option 2: Using `uv tool install` (Standalone CLI)

For external projects (e.g., game servers), install the generator as a system-wide tool:

```bash
# Install from GitHub
uv tool install git+https://github.com/ZOITK/ZLink#subdirectory=generator

# Or install from local checkout
uv tool install <path_to_zlink>/generator
```

Then use it anywhere:
```bash
protocol-gen --schema moduta.yaml --go-out protocol.go --cs-out Protocol.cs
```

---

## 🚚 Deployment & Sync Mechanism

When `make gen` is executed, the following tasks are performed automatically:

1. **Update SDK**: The generated protocol (`Protocol.*`) is deployed to the `sdk/.../zlink/protocol/` folder of each platform.
2. **Sync Examples**: The latest SDK state is immediately synchronized to the `zlink` folder under each `examples/` project.

This mechanism ensures that the engine and protocol are always synchronized to a single version.

[Back to Top](#)

---

<a name="korean"></a>
# 🇰🇷 한글 가이드 (Korean Version)

ZLink 프로토콜 생성기는 ZLink 소켓 프레임워크의 핵심인 자동 코드 생성 도구입니다. YAML 설정을 기반으로 Go, Python, C# 패킷 코드를 동시 생성하고 각 프레임워크에 자동 배포합니다.

---

## 🛠 사용 방법

### 방법 1: Makefile 사용 (로컬 개발)

1. **스키마 정의**: `schemas/` 폴더 내의 YAML 파일을 수정하여 패킷 구조를 정의합니다.
2. **코드 생성**: generator 폴더에서 다음 명령을 실행합니다.
   ```bash
   make gen schemas=./schemas/your_schema.yaml output=<destination_dir>
   ```

### 방법 2: `uv tool install` 사용 (설치형 CLI)

게임 서버 같은 외부 프로젝트에서는 생성기를 시스템 전역 도구로 설치합니다:

```bash
# GitHub에서 설치
uv tool install git+https://github.com/ZOITK/ZLink#subdirectory=generator

# 또는 로컬 체크아웃에서
uv tool install <zlink_경로>/generator
```

그 후 어디서든 사용 가능:
```bash
protocol-gen --schema moduta.yaml --go-out protocol.go --cs-out Protocol.cs
```

---

## 🚚 배포 및 동기화 메커니즘

`make gen` 실행 시 다음 작업이 자동으로 수행됩니다.

1. **SDK 업데이트**: 생성된 프로토콜(`Protocol.*`)이 각 플랫폼별 `sdk/.../zlink/protocol/` 폴더로 배포됩니다.
2. **예제 동기화**: 최신 SDK 상태가 각 `examples/` 프로젝트 하위의 `zlink` 폴더로 즉시 동기화됩니다.

이 메커니즘 덕분에 엔진과 프로토콜은 언제나 하나의 버전으로 동기화된 상태를 유지하게 됩니다.

[위로 이동 (Back to Top)](#)
