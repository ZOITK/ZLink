# ZLink Protocol Generator
# ZLink 프로토콜 생성기

The ZLink Protocol Generator is the core tool of the ZLink socket framework.
ZLink 프로토콜 생성기는 ZLink 소켓 프레임워크의 핵심인 자동 코드 생성 도구입니다.

It simultaneously generates Go, Python, and C# packet code based on YAML definitions and automatically deploys them to each framework.
YAML 설정을 기반으로 Go, Python, C# 패킷 코드를 동시 생성하고 각 프레임워크에 자동 배포합니다.

---

## 🛠 Usage
## 🛠 사용 방법

1. **Define Schema**: Modify YAML files in the `schemas/` folder to define the packet structure.
1. **스키마 정의**: `schemas/` 폴더 내의 YAML 파일을 수정하여 패킷 구조를 정의합니다.

2. **Generate Code**: Run the following command in the root or this folder.
2. **코드 생성**: 루트 또는 본 폴더에서 다음 명령을 실행합니다.
   ```bash
   make gen
   ```

---

## 🚚 Deployment & Sync Mechanism
## 🚚 배포 및 동기화 메커니즘

When `make gen` is executed, the following tasks are performed automatically:
`make gen` 실행 시 다음 작업이 자동으로 수행됩니다.

1. **Update SDK**: The generated protocol (`Protocol.*`) is deployed to the `sdk/.../zlink/protocol/` folder of each platform.
1. **SDK 업데이트**: 생성된 프로토콜(`Protocol.*`)이 각 플랫폼별 `sdk/.../zlink/protocol/` 폴더로 배포됩니다.

2. **Sync Examples**: The latest SDK state is immediately synchronized to the `zlink` folder under each `examples/` project.
2. **예제 동기화**: 최신 SDK 상태가 각 `examples/` 프로젝트 하위의 `zlink` 폴더로 즉시 동기화됩니다.

This mechanism ensures that the engine and protocol are always synchronized to a single version.
이 메커니즘 덕분에 엔진과 프로토콜은 언제나 하나의 버전으로 동기화된 상태를 유지하게 됩니다.
