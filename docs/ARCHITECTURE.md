# ZLink Technical Architecture

[English](#english) | [한국어](#korean)

<a name="english"></a>
# English

ZLink follows a unified architecture designed for high performance and high productivity in cross-platform real-time communication.

---

## 1. Unified Packet Structure

ZLink uses a **unified 24-byte binary header** for both TCP and UDP to ensure consistency.

### ZLink Standard Header (24 Bytes)
| Offset | Size | Field | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| 0-1 | 2 | Magic | uint16 | Magic Number (0x4F5A = "ZO") |
| 2-5 | 4 | Version | uint32 | Protocol Version |
| 6-9 | 4 | Command | uint32 | Command ID |
| 10-13 | 4 | Length | uint32 | Body Length |
| 14-17 | 4 | SessionID / SenderIdx | uint32 | Session ID (TCP) or Sender ID (UDP) |
| 18-21 | 4 | Error | uint32 | Error Code |
| 22-23 | 2 | Sequence | uint16 | Reserved (Default: 0) |

**Total**: 24 bytes (little-endian format)

### Format String
- Python: `HEADER_FMT = "<HIIIIIH"`
- C#: `BitConverter` with offsets at 0, 2, 6, 10, 14, 18, 22

---

## 2. Session Lifecycle

ZLink server manages the connection lifecycle through specialized Session objects.

1. **Accept**: The `TCPServer` accepts a connection and creates a `Session`.
2. **Orchestration**: `Session` handles packet unmarshaling and dispatches it to registered callbacks.
3. **Closing**: When the connection is lost or `Close()` is called, resources are cleaned up immediately.

---

## 3. Protocol-SDK Integration

ZLink emphasizes the "Source of Truth" derived from YAML definitions. The generator not only creates packet data structures but also generates **Dispatcher** logic that maps Command IDs to specific structures. This generated logic is deployed directly into the SDK, so developers never have to write manual parsing code.

---

## 4. Architecture Symmetry

The API design of the Go server is reflected in the Python and Unity clients as much as possible. This allows developers to work seamlessly across different platforms without needing to relearn the communication model.

[Back to Top](#)

---

<a name="korean"></a>
# 🇰🇷 한글 가이드 (Korean Version)

ZLink는 교차 플랫폼 실시간 통신에서 고성능과 고생산성을 목표로 설계된 통합 아키텍처를 따릅니다.

---

## 1. 통합 패킷 구조

ZLink는 일관성을 보장하기 위해 TCP와 UDP 모두에 **통합된 24바이트 바이너리 헤더**를 사용합니다.

### ZLink 표준 헤더 (24 바이트)
| 오프셋 | 크기 | 필드 | 타입 | 설명 |
| :--- | :--- | :--- | :--- | :--- |
| 0-1 | 2 | Magic | uint16 | 매직 넘버 (0x4F5A = "ZO") |
| 2-5 | 4 | Version | uint32 | 프로토콜 버전 |
| 6-9 | 4 | Command | uint32 | 커맨드 ID |
| 10-13 | 4 | Length | uint32 | 바디 길이 |
| 14-17 | 4 | SessionID / SenderIdx | uint32 | 세션 ID (TCP) 또는 송신자 ID (UDP) |
| 18-21 | 4 | Error | uint32 | 에러 코드 |
| 22-23 | 2 | Sequence | uint16 | 예약됨 (기본값: 0) |

**전체**: 24 바이트 (Little-endian 형식)

### 형식 문자열
- Python: `HEADER_FMT = "<HIIIIIH"`
- C#: `BitConverter` (오프셋: 0, 2, 6, 10, 14, 18, 22)

---

## 2. 세션 라이프사이클

ZLink 서버는 특화된 Session 객체를 통해 연결 라이프사이클을 관리합니다.

1. **수락(Accept)**: `TCPServer`가 연결을 수신하고 `Session`을 생성합니다.
2. **조율(Orchestration)**: `Session`이 패킷 언마샬링을 처리하고 등록된 콜백으로 분기합니다.
3. **종료(Closing)**: 연결이 끊기거나 `Close()`가 호출되면 즉시 자원이 정리됩니다.

---

## 3. 프로토콜-SDK 일체화

ZLink는 YAML 정의로부터 파생되는 "단일 진실 공급원(Source of Truth)"을 강조합니다. 제네레이터는 패킷 데이터 구조뿐만 아니라, 커맨드 ID를 특정 구조체로 매핑해 주는 **디스패처(Dispatcher)** 로직도 함께 생성합니다. 이 로직이 SDK 내부에 직접 배포되므로 개발자는 수동 파싱 코드를 작성할 필요가 없습니다.

---

## 4. 아키텍처 대칭성

Go 서버의 API 설계 철학을 Python과 Unity 클라이언트에도 최대한 투영했습니다. 덕분에 개발자는 플랫폼을 넘나들며 개발할 때 통신 모델을 다시 배울 필요 없이 일관된 개발 경험을 가질 수 있습니다.

[위로 이동 (Back to Top)](#)
