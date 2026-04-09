# ZLink Development Guide

This guide explains how to extend and maintain the ZLink framework.

---

## 1. Adding New Packets

To add a new communication packet, follow these steps:

1. **Modify Schema**: Open `generator/schemas/basic.yaml` and add your packet definition.
   ```yaml
   packets:
     - name: Msg_MyNewActionReq
       id: 14110001
       desc: "My new action request"
       fields:
         - name: Data
           type: string
   ```
2. **Run Generator**: Run `make gen` in the `generator/` folder.
3. **Check SDK**: Verify that the new structures are generated in the `protocol/` subfolder of each SDK.
4. **Implement Handler**: Register a handler in your application using `protocol.Register`.

---

## 2. Modifying SDK Engines

When modifying the core engine logic (e.g., in `sdk/server/zlink/network/`):

- **Logging**: Always include the `[zLink]` prefix in all logs.
- **Symmetry**: Ensure that similar behavioral changes are reflected across Go, Python, and Unity SDKs for consistency.
- **Sync**: After modifying core SDK files, run `make gen` to synchronize those changes to the `examples/` folders.

---

## 3. Best Practices

- **Thread Safety**: Ensure that network callbacks in Unity do not touch non-thread-safe Unity APIs unless dispatched to the main thread.
- **Error Handling**: Use the `Error` field in headers to communicate protocol-level errors efficiently.

=============================================================================

# ZLink 개발 가이드

ZLink 프레임워크를 확장하고 유지보수하는 방법을 설명합니다.

---

## 1. 새로운 패킷 추가하기

새로운 통신 패킷을 추가하려면 다음 단계를 따르세요:

1. **스키마 수정**: `generator/schemas/basic.yaml` 파일을 열어 패킷 정의를 추가합니다.
   ```yaml
   packets:
     - name: Msg_MyNewActionReq
       id: 14110001
       desc: "My new action request"
       fields:
         - name: Data
           type: string
   ```
2. **제네레이터 실행**: `generator/` 폴더에서 `make gen`을 실행합니다.
3. **SDK 확인**: 각 SDK의 `protocol/` 폴더에 새로운 구조체가 생성되었는지 확인합니다.
4. **핸들러 구현**: 애플리케이션에서 `protocol.Register`를 사용하여 핸들러를 등록합니다.

---

## 2. SDK 엔진 수정하기

핵심 엔진 로직(예: `sdk/server/zlink/network/`)을 수정할 때:

- **로깅**: 모든 로그에는 반드시 `[zLink]` 접두어를 포함해야 합니다.
- **대칭성**: 일관성을 위해 Go, Python, Unity SDK 전반에 유사한 동작 변경이 반영되도록 하세요.
- **동기화**: 핵심 SDK 파일을 수정한 후에는 `make gen`을 실행하여 해당 변경 사항을 `examples/` 폴더로 동기화하세요.

---

## 3. 권장 사항

- **스레드 안전성**: Unity의 네트워크 콜백이 메인 스레드로 분기되지 않은 상태에서 스레드 안전하지 않은 Unity API를 건드리지 않도록 주의하세요.
- **에러 처리**: 헤더의 `Error` 필드를 사용하여 프로토콜 레벨의 에러를 효율적으로 전달하세요.
