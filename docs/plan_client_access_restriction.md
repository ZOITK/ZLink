# 클라이언트 액세스 제한 및 명칭 통일 계획 (Client Access Restriction)

## 1. 개요
Python 및 Unity SDK에서 하위 전송 계층인 `TcpClient`와 `UdpClient`를 직접 사용하는 것을 방지하고, 통합 엔지인 `Client`를 통해서만 네트워크 기능을 이용하도록 강제합니다. 이를 위해 명칭을 `_TcpClient`, `_UdpClient`로 통일하고 접근 범위를 제한합니다.

## 2. 수정 대상 및 내역

### 2.1 Python SDK
- **`sdk/client/python/zlink/network/tcp_client.py`**
    - `AsyncTcpClient` 클래스명을 `_TcpClient`로 변경.
- **`sdk/client/python/zlink/network/udp_client.py`**
    - `AsyncUdpClient` 클래스명을 `_UdpClient`로 변경.
- **`sdk/client/python/zlink/network/client.py`**
    - 임포트 구문 수정: `AsyncTcpClient` -> `_TcpClient`, `AsyncUdpClient` -> `_UdpClient`.
    - `start()` 메서드 내 인스턴스 생성 로직 수정.

### 2.2 Unity/C# SDK
- **`sdk/client/unity/zlink/Network/TcpClient.cs`**
    - `public class TcpClient` -> `internal class _TcpClient`.
- **`sdk/client/unity/zlink/Network/UdpClient.cs`**
    - `public class UdpClient` -> `internal class _UdpClient`.
- **`sdk/client/unity/zlink/Network/Client.cs`**
    - `public TcpClient TCP` 프로퍼티 -> `internal _TcpClient TCP`로 변경 및 명칭 수정.
    - `public UdpClient UDP` 프로퍼티 -> `internal _UdpClient UDP`로 변경 및 명칭 수정.
    - `StartAsync()` 메서드 내 인스턴스 생성 로직 수정.

## 3. 검증 계획
1. **코드 정적 분석:** 수정 후 `Client` 클래스 외부에서 `_TcpClient`, `_UdpClient`를 참조하는 곳이 없는지 확인.
2. **Unity 컴파일 확인:** C#의 `internal` 키워드 적용으로 외부 어셈블리(예제 코드)에서 접근 불가함을 보장.
3. **Python 규칙 확인:** 언더바(`_`) 접두사를 통해 내부용임을 명시하고, `__init__.py` 등을 통해 노출되지 않도록 설정.
