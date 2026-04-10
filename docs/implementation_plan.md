# 멀티 트랜스포트 통합 세션(Multi-Transport Session) 개편 계획

하나의 `Session` 객체가 TCP 연결과 UDP 주소를 동시에 관리하는 '멀티 트랜스포트' 구조로 개편하여, 통신 수단에 구애받지 않는 단일화된 세션 관리 체계를 구축합니다.

## 핵심 아키텍처 (Mechanism)
1. **통합 세션 객체**: `Session` 구조체가 `tcpConn`과 `udpAddr`를 필드로 가집니다.
2. **유기적 바인딩**: UDP 패킷 수신 시, 엔진은 헤더의 `SessionID`를 분석하여 기존 TCP 세션에 주소를 자율 업데이트합니다.
3. **상태 기록**: 세션은 `LastActivity` 필드를 유지하며, 비즈니스 로직은 이를 통해 타임아웃 여부를 결정할 수 있습니다.

## 작업 범위
- `udp_session.go` 제거 및 `session.go` 통합 리팩토링.
- `server.go`에 세션 레지스트리 및 자동 바인딩 로직 구현.
- 브로드캐스트 전용 메서드(`BroadcastUDP`) 추가.
