# ZLink Reference Examples

[English](#english) | [한국어](#korean)

<a name="english"></a>
# English

The `examples/` folder contains pure blueprints showing how to utilize ZLink's multi-platform SDK. Every example is based on the `basic.yaml` protocol and demonstrates a standard communication scenario.

---

## 🏃 Standard Scenario

1. **Connection & Login**: Connect via TCP and request login.
2. **Message Exchange**: Send a "Hello" message and receive an echo notify from the server.
3. **UDP Heartbeat**: Send 10 consecutive UDP heartbeat bursts (0.1s interval).
4. **Safety Shutdown**: Wait 1 second and disconnect.

---

## 📂 Example Projects

- **`server-go/`**: An echo-server implementation using the Go engine (`basicServer.go`).
- **`client-py/`**: A simulation client using Python's `asyncio` (`basicClient.py`).
- **`client-unity/`**: A MonoBehaviour-based consolidated component for Unity (`BasicClient.cs`).

[Back to Top](#)

---

<a name="korean"></a>
# 🇰🇷 한글 가이드 (Korean Version)

`examples/` 폴더는 ZLink의 멀티플랫폼 SDK를 어떻게 활용하는지 보여주는 순수 청사진(Blueprint)들을 포함하고 있습니다. 모든 예제는 `basic.yaml` 프로토콜을 기반으로 하며, 표준 통신 시나리오를 시연합니다.

---

## 🏃 표준 시나리오

1. **접속 및 로그인**: TCP로 접속하여 로그인을 요청합니다.
2. **메시지 교환**: "안녕하세요" 메시지 전송 후 서버의 에코 알림을 수신합니다.
3. **UDP 하트비트**: UDP 하트비트 10회를 연속으로 전송(0.1초 간격) 합니다.
4. **안전 종료**: 1초 대기 후 접속을 해제합니다.

---

## 📂 예제 프로젝트

- **`server-go/`**: Go 엔진을 사용한 에코 서버 구현체입니다 (`basicServer.go`).
- **`client-py/`**: Python `asyncio`를 사용한 시뮬레이션 클라이언트입니다 (`basicClient.py`).
- **`client-unity/`**: Unity용 MonoBehaviour 기반 통합 컴포넌트 예제입니다 (`BasicClient.cs`).

[위로 이동 (Back to Top)](#)
