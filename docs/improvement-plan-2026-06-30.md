# zlink 개선 계획서

**작성일**: 2026-06-30
**대상**: zlink SDK(Go) + 생성기 + 클라이언트(Unity/Python)
**배경**: 외부 냉정 평가(종합 4.7/10, "유망하나 미성숙")에 대한 코드 검증 + 개선 로드맵
**소비자 프로젝트**: moduta (zoit-moduta-socket)

> 이 문서는 **계획** 단계 산출물입니다. 실제 코드 수정은 항목별 승인 후 진행합니다.

---

## 0. 진단 요약 (코드 직접 검증됨)

외부 평가를 코드로 재검증한 결과, **대체로 정확하나 일부 과장·일부 누락**이 있었습니다.

| 평가 항목 | 검증 결과 |
|---|---|
| 테스트 0개 | ✅ 사실 — `*_test.go`/`test_*.py`/`*Test.cs` 전부 0개 |
| NAT 휴리스틱 위험 | ✅ 사실 — `candidates==1`일 때만 자동 바인딩([server.go:128](../sdk/server/zlink/network/server.go#L128)) |
| 위치 중계 O(N²) | ✅ 사실 — `BroadcastUDP`가 수신자마다 재직렬화([server.go:188](../sdk/server/zlink/network/server.go#L188)) |
| "버전 협상 없음" | ⚠️ **절반 틀림** — 헤더에 4B Version 필드 **이미 존재**([interface.go:23](../sdk/server/zlink/network/base/interface.go#L23)). 문제는 "안 읽는 것" |
| (평가 누락) UDP 세션 누수 | 🔴 **추가 발견** — `LastActivity` 추적만, 만료 리퍼 없음 |
| (평가 누락) UDP 단일 스레드 | 🔴 **추가 발견** — 수신 콜백이 읽기 루프에서 동기 실행([udp.go:64-78](../sdk/server/zlink/network/udp.go#L64-L78)) |
| (평가 누락) 세션 하이재킹 | 🔴 **추가 발견** — 순차 SessionID([server.go:42](../sdk/server/zlink/network/server.go#L42)) + 매 패킷 무조건 재바인딩([server.go:117](../sdk/server/zlink/network/server.go#L117)) → 남의 ID로 UDP 트래픽 탈취 가능 |

**결론**: 평가의 4.7점은 다소 가혹(버전 필드 존재 누락으로 프로토콜 취약성 과장). 다만 견고성 결함(세션 누수·NAT 레이스)이 성능보다 먼저 위험.

---

## 1. 테스트 도입 (최우선)

### 문제
842줄 네트워크 코드 + 생성기에 회귀 안전망 0. 모든 후속 개선이 "고친 뒤 안 깨졌는지 확인 불가" 상태.

### 테스트 전략 — 3층 구조
실제 소켓을 여기저기 여는 게 아님. `HandlePacket`이 `[]byte`를 받도록 이미 분리되어 있어 대부분 **소켓 없이** 검증 가능.

| 층 | 소켓 | 검증 대상 | 비중 |
|---|---|---|---|
| 1층 함수 | 없음 | `Pack` 라운드트립, `getNextSessionID` 오버플로우, msgpack 직렬화 | 다수 |
| 2층 로직(가짜 소켓) | mock | **NAT 바인딩·세션 누수·멀티 트랜스포트** ← 핵심 결함 | 핵심 |
| 3층 통합 | 진짜(localhost) | 전체 연결 한 바퀴 | 소수(1~2) |

### 검증 기준
- `cd sdk/server/zlink && go test ./...` 통과
- 최소: Pack 라운드트립, NAT 다중단말 시나리오, UDP 세션 만료, 멀티 트랜스포트 1세션 통합

### moduta 영향
**없음** (내부 추가).

---

## 2. 세션 생명주기 — UDP 세션 누수 차단

### 문제
`getOrCreateUDPSession`이 `udpSessions`+`sessions` 양쪽에 등록([server.go:66-75](../sdk/server/zlink/network/server.go#L66-L75))하지만, UDP 클라가 조용히 사라져도 만료시키는 리퍼가 없음. → 세션 영구 누수 + `activeCount==0` 기반 ID 리셋([server.go:247](../sdk/server/zlink/network/server.go#L247))이 영영 발동 안 됨.

### 해결 방향
- `LastActivity` 기반 만료 리퍼 고루틴 추가 (예: 60초 무활동 시 정리)
- 만료 시 `udpSessions`+`sessions` 동시 제거, `OnSessionClose` 호출
- 타임아웃 값만 설정으로 노출

### 검증 기준
- 2층 테스트: 가짜 시계로 만료 후 세션 수 0 확인

### moduta 영향
**거의 없음** — `OnSessionClose`가 유휴 세션에도 호출됨(동작 추가, API 무변경).

---

## 3. 서버 권위 UDP 바인딩 (NAT 정합성 + 하이재킹 차단)

> **설계 원칙**: 정합성 판단은 100% 서버에 둔다. 클라에 "송신을 참아라" 같은 책임/권한을 주지 않는다. (이 원칙에 따라 "핸드셰이크 전 클라 UDP 송신 금지" 안은 **폐기**)

이 항목은 별개의 두 문제를 다룬다. **(a)는 확정 진행, (b)는 위협 모델 보고 단계적으로.**

### (a) NAT 정합성 — 확정
**문제**: 정규 경로(`sessionID>0`)는 클라가 첫 UDP에 올바른 ID를 실을 때만 동작. ID가 0으로 새면 IP 추측 휴리스틱(`candidates==1`)으로 폴백 → 같은 공인 IP(교실 NAT)에서 세션 난립.

**해결**: 위험한 *추측 폴백*만 제거한다. SessionID 바인딩 골격은 유지.
- `findSessionsByIP` IP 휴리스틱([server.go:122-136](../sdk/server/zlink/network/server.go#L122-L136)) **제거**
- 서버 발급 ID가 유효한 UDP만 처리, **ID=0 또는 미지 ID는 드롭**
- 단 하나의 예외: UDP 단독 모드용 명시적 `Hello`(고정 cmd) — 서버가 ID 발급·회신, 이후 클라가 그 ID를 헤더에 실음

### (b) 하이재킹 차단 — 단계적
**문제**: 순차 SessionID(추측 가능) + 매 패킷 무조건 재바인딩([server.go:117](../sdk/server/zlink/network/server.go#L117)) → 남의 ID로 세션 UDP 트래픽 탈취 가능.

**해결 (1단계, 채택)**: **최초 1회만 바인딩하고 잠금.** 재바인딩은 재핸드셰이크/유휴 만료(개선 2번) 이후에만. → 이미 바인딩된 세션은 ID를 알아도 주소 탈취 불가. 우리가 합의한 구조를 거의 안 건드림.

**해결 (2단계, 보류)**: 최초 바인딩 순간의 짧은 창까지 막으려면 **추측 불가능한 난수 토큰** 발급·검증. **결정 보류** — 클라가 폐쇄망/신뢰 단말이면 불필요, 열린 인터넷/비신뢰면 도입. 위협 모델 확정 후 재논의.

### 검증 기준
- 2층 테스트: 같은 IP·다른 포트 단말 2개가 정상 ID로 보내면 세션 2개로 정확히 분리, ID 누수 경로 미발생
- 2층 테스트: 바인딩된 세션에 타 주소가 같은 ID로 패킷을 보내도 주소가 안 바뀜(잠금 확인)

### moduta 영향 — 사실상 서버 작업 (앱 사용법 무변경)
**클라 SDK가 이미 (a)를 충족함**을 코드로 확인:
- Unity: `sidToSend = useUDP ? SessionId : 0u`([Client.cs:70](../sdk/client/unity/zlink/Network/Client.cs#L70)) + 수신 헤더에서 SessionId 자동 학습([Client.cs:80-84](../sdk/client/unity/zlink/Network/Client.cs#L80-L84))
- Python: 동일([client.py:68](../sdk/client/python/zlink/network/client.py#L68))

→ 앱 코드 `client.Send(msg, useUDP:true)`는 **전후 동일**. 양쪽 클라 SDK가 이미 학습한 ID를 UDP에 실어 보내므로, 서버는 그걸 신뢰하고 추측 폴백만 버리면 됨.

실제 클라 영향은 3가지뿐:
- **(b) 바인딩 잠금**: 0 (순수 서버)
- **ID 학습 전 UDP 드롭**: 거의 0 — 클라는 이미 ID 수신 후 UDP를 쏨(두 예제 모두 수신 핸들러 안에서 UDP 시작). 새던 패킷이 유령 세션 대신 안전 드롭될 뿐
- **NAT 포트 재매핑 시 재연결**: 신규 고려 1개 — SDK 자동 재연결로 흡수 가능

UDP 단독 모드의 `Hello`는 혼합 모드(moduta)엔 해당 없음. → **혼합 모드 한정, 조율 배포 불필요. 스테이지 1로 이동**(로드맵 참조).

> 참고: 검토했던 "접속 시 welcome 패킷으로 ID 학습 한정(#5)"은 **폐기**. #4를 헤더 sessionID=0으로 패킹하면 클라가 헤더를 무시하므로 welcome 없이도 안전 → 불필요한 결합이라 도입 안 함.

---

## 4. 브로드캐스트 O(N²) — ✅ 완료 (BroadcastTo 원시)

### 문제 (근본 원인 = 프레임워크 빈틈)
zlink는 `Send`(1:1)만 제공 → 모든 소비자가 fan-out을 `Send` 루프로 직접 구현 → 수신자마다 `Packer` 재직렬화(O(N²) 인코딩). moduta의 `Room.BroadcastStruct`가 그 사례. **moduta 버그가 아니라 zlink에 브로드캐스트 원시가 없던 빈틈.**

### 해결 (구현됨)
- zlink SDK에 **`BroadcastTo(sessions, msg, exceptID)`** 추가([server.go](../sdk/server/zlink/network/server.go)): 메시지를 **1회만 패킹**(헤더 sessionID=0) 후 세션 목록에 raw 전송. UDP/TCP 자동 분기, exceptID 제외.
- 헤더 ID=0 → **클라이언트는 무시**(발신자는 바디 식별, moduta는 `UserIdx`) → **클라 무변경**.
- moduta는 `Room.BroadcastStruct` 본문을 `BroadcastTo` 호출로 **위임**(호출부·시그니처 무변경).
- 테스트 `TestBroadcastToPacksOnce`(패킹 1회 + exceptID 제외) 통과.

### 남은 한계 (냉정)
**중복 인코딩만** 제거. N번 전송 syscall·**단일 스레드 UDP 수신 루프는 그대로** → 부하 측정으로 실제 천장 확인 필요(미완).

### moduta 영향
서버 1곳(`Room.BroadcastStruct`) 위임 + zlink **v0.1.1** 의존. **클라이언트 무변경.**

---

## 5. 버전 협상 — ⏸️ 보류 (미구현, 필요 시 착수)

### 문제
헤더에 Version 4B가 있지만 읽고 분기하는 로직이 없음. msgpack `as_array`는 순서 의존이라 필드 추가 시 무중단 업데이트 불가.

### 현황
- 이번 작업에서 welcome 기반 ID 학습(method A)을 시도했으나, #4를 헤더=0으로 해결하면서 **불필요해져 폐기**(되돌림).
- 버전 협상 자체는 **미구현**. 지금은 필요 없음 — 프로토콜 무중단 진화가 실제 과제가 될 때 착수.

### 해결 방향 (착수 시)
- 핸드셰이크 시 클라-서버 와이어 버전 교환, 불일치 시 명시적 거부/경고
- (생성기) 하위호환 규칙: 필드는 **끝에만 추가**, 순서 변경 금지 가이드

### moduta 영향
현재 없음(미착수).

---

## 6. 클라이언트 DX 개선 (옵트인)

### 문제
`On<T>` 없음, req/res correlation 없음 → 클라가 디스패치 딕셔너리·캐스팅·콜백 체인 직접 구축.

### 해결 방향
- 타입별 핸들러 `On<T>(handler)` 디스패처 (생성기가 생성)
- req/res correlation: 헤더 `Sequence` 예약 필드([interface.go:48](../sdk/server/zlink/network/base/interface.go#L48)) 활용해 요청-응답 매칭

### 검증 기준
- 예제 클라 보일러플레이트 라인 수 감소

### moduta 영향
**선택적** — 기존 디스패치 방식 그대로 동작. 원할 때만 교체.

---

## 7. 문서 일관성 (부수 작업)

- **DEVELOPMENT_GUIDE.md 1절** 스키마 예시가 구포맷(`packets:` 최상위 + `id:`). 현재 `metadata/definitions/idx` 포맷으로 수정
- 4번 확정 시 ARCHITECTURE.md 헤더 의미 주석 정합화

---

## 8. 실행 현황 (최종)

| 항목 | 상태 | 비고 |
|---|---|---|
| 1. 테스트 도입 | ✅ 완료 | Pack/ID/NAT/하이재킹/리퍼/브로드캐스트 등 10개 (`go test -race`) |
| 2. 세션 누수 리퍼 | ✅ 완료 | `UDPIdleTimeout`(기본 60초) 기반 유휴 UDP 세션 정리 |
| 3. 서버 권위 바인딩 | ✅ 완료 | IP 휴리스틱 제거 + ID=0/미지 드롭 + 바인딩 잠금(하이재킹 차단) |
| 4. 브로드캐스트 O(N²) | ✅ 완료 | zlink `BroadcastTo` 원시 + moduta 위임 (인코딩 1회) |
| 5. 버전 협상 | ⏸️ 보류 | welcome 폐기. 무중단 진화가 과제될 때 착수 |
| 6. 클라 DX(On\<T\>) | ⏸️ 미착수 | 선택·옵트인 |
| 7. 문서 일관성 | ⏳ 일부 | 본 계획서 정정 완료. DEVELOPMENT_GUIDE 구포맷 잔존 |

**릴리스**: zlink **v0.1.1** 태그·푸시 완료(1~4 포함). moduta는 v0.1.1로 업그레이드 + `Room.BroadcastStruct` 위임 적용.

**moduta 영향 결산**: 앱/클라이언트 코드 무변경. 변경된 것은 **서버 1곳(`Room.BroadcastStruct`) + 의존 버전업**뿐.

---

## 9. 다음 후보 (선택)

1. **부하 측정** — 봇 N명 30fps로 CPU/지연 실측 → 단일 스레드 UDP 수신 루프가 실제 천장인지 확인
2. 단일 스레드 UDP 수신 해소(워커 분리) — 측정으로 필요 확인 시
3. 클라/생성기 테스트 추가 (현재 서버 Go에 편중)
4. #5 버전 협상 / #6 DX — 필요 시
5. #7 DEVELOPMENT_GUIDE 구포맷 스키마 예시 수정
