# 현재 작업 상태 (now.md) - 2026-04-07

## 1. 아키텍처 및 구조 통합 (진행 중)
- `game`, `basic`별로 나뉘어 있던 예제 폴더를 `examples/` 단일 구조로 통합했습니다.
- `generator/schemas/game.yaml`을 삭제하고 `basic.yaml` 중심으로 단일화했습니다.
- `generator/Makefile`을 수정하여 `make gen` 실행 시 서버(`server/cmd/protocol`), Python(`client-py/examples/protocol`), Unity(`client-unity/examples/Protocol`) 경로로 자동 배포되도록 로직을 업데이트했습니다.

## 2. 진행 중인 수정 사항 (Unity 빌드 에러 해결)

### C# 제네레이터 (`csharp_generator.py`) (완료)
- `Sys_PackHeader.Decode` 및 `_Unmarshal` 호출 시 발생하는 델리게이트 타입 불일치(CS0407)를 해결하기 위해 람다식을 사용하도록 수정 및 재생성 완료했습니다.

### 로거 정규화 (`Logger.cs`) (완료)
- 네임스페이스를 `Zlink`로 통합하고, Unity API(`UnityEngine.Debug`) 프리픽스를 명시적으로 추가하여 충돌을 방지했습니다.

### 참조 및 예제 업데이트 (완료)
- `TcpClient.cs`, `UdpClient.cs`, `main.cs` 내 로거 호출부 정규화 및 `main.cs`의 `MonoBehaviour` 변환을 완료했습니다.

## 3. 작업 결과 요약
1. `generator/src/generators/csharp_generator.py` 수정 및 `make gen` 실행 완료.
2. `client-unity/zlink/Logger/Logger.cs` 네임스페이스 및 프리픽스 적용 완료.
3. `TcpClient.cs`, `UdpClient.cs`, `main.cs` 내 로거 호출부 일괄 수정 및 `MonoBehaviour` 변환 완료.
4. 모든 C# 관련 빌드 에러 해결 확인.
