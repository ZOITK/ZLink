# ZLink SDKs (Core Engines)

이 폴더는 각 플랫폼별 통신 핵심 모듈을 포함하고 있습니다. ZLink의 목표는 **"복사해서 바로 쓰는 원자성(Atomic Portability)"**입니다.

## 📦 구조

각 언어별 폴더 하위의 `zlink/` 폴더가 **배포용 완전체 모듈**입니다.

- **`server/zlink`**: Go 소켓 서버 엔진 (TCP/UDP, 세션 관리)
- **`client/py/zlink`**: Python 비동기 클라이언트 라이브러리
- **`client/unity/zlink`**: Unity C# 네트워크 모듈 및 플러그인 (examples 포함)

## 🚀 사용 방법

1. 귀하의 프로젝트에서 통신이 필요한 위치에 원하는 플랫폼의 `zlink` 폴더를 통째로 복사합니다.
2. 제너레이터를 통해 생성된 프로토콜이 이미 `zlink/protocol`에 내장되어 있으므로 별도의 경로 설정 없이 바로 인스턴스를 생성하여 사용하면 됩니다.

각 모듈은 외부 의존성을 최소화하여 설계되었으며, `zlink` 폴더 자체가 하나의 독립적인 패키지로 기능합니다.
