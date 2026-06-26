# zlink로 새 서버 프로젝트 시작하기

**작성일**: 2026-06-25
**대상**: zlink SDK + protocol-gen으로 새 게임/소켓 서버를 시작하는 개발자

이 문서는 빈 폴더에서 시작해 **빌드·실행 가능한 zlink 서버**까지 가는 전체 절차입니다.
모든 명령은 실제 검증된 것입니다.

---

## 0. 사전 준비물

| 도구 | 용도 | 확인 |
|------|------|------|
| Go 1.25.6+ | 서버 빌드 | `go version` |
| uv | 프로토콜 생성기 설치 | `uv --version` |
| git | 의존성(go get) | `git --version` |

---

## 1. 프로토콜 생성기 설치 (최초 1회)

생성기(`protocol-gen`)는 시스템 전역 도구로 한 번만 설치합니다. 이후 모든 프로젝트가 공유합니다.

```bash
uv tool install "git+https://github.com/ZOITK/ZLink#subdirectory=generator"
```

확인:
```bash
protocol-gen --help    # 도움말이 나오면 성공
```

> 설치 위치: 명령어는 `~/.local/bin/protocol-gen`, 실제 코드는 `~/.local/share/uv/tools/protocol-gen/` (격리 환경). 프로젝트 안에 복사되지 않습니다.

---

## 2. 프로젝트 폴더 생성 + 보일러플레이트

```bash
mkdir my-server && cd my-server

# 프로토콜 보일러플레이트 생성 (Makefile + schema.yaml)
protocol-gen init
```

생성 결과:
```
my-server/
└── protocol-gen/
    ├── Makefile       # make protocol
    └── schema.yaml    # 스키마 템플릿 (편집해서 사용)
```

> `init`은 **기존 파일을 덮어쓰지 않습니다**. 이미 있으면 건너뜁니다(안전).

---

## 3. 스키마 정의

`protocol-gen/schema.yaml`을 열어 패킷을 정의합니다. 템플릿에는 system/auth 예제가 들어 있습니다.

```yaml
metadata:
  version: 1
  categories: [system, auth]    # 카테고리 추가 가능
  protocols: [tcp]
  types: [req, res, notify]

definitions:
  auth:
    packets:
      - name: Login
        idx: 1
        proto: tcp
        doc: "로그인"
        pair:
          req: { fields: { Nickname: string } }
          res: { fields: { PlayerID: uint32, Result: uint32 } }
```

- `pair`: req/res 한 쌍을 정의
- `type: notify`: 단방향 통지 패킷
- 지원 타입: `int64`, `uint32`, `string`, 구조체 중첩 등

---

## 4. Go 프로젝트 구조와 출력 경로

Go에서는 생성된 코드를 `protocol/` 패키지로 두는 것이 깔끔합니다. 권장 구조:

```
my-server/
├── go.mod
├── main.go
├── protocol/
│   └── protocol.go        # 생성됨 (package protocol)
└── protocol-gen/
    ├── Makefile
    └── schema.yaml
```

`protocol-gen/Makefile`의 출력 경로를 프로젝트 구조에 맞게 지정합니다:

```bash
cd protocol-gen
make protocol GO_OUT=../protocol/protocol.go CS_OUT=../client/protocol.cs
```

또는 매번 인자를 치기 싫으면 `Makefile`의 `GO_OUT`/`CS_OUT` 기본값을 수정해 git에 커밋합니다.

---

## 5. Go 모듈 초기화 + zlink SDK 의존 추가

```bash
cd my-server         # 프로젝트 루트
go mod init my-server

# zlink SDK 정식 의존 추가 (버전 고정)
go get github.com/ZOITK/ZLink/sdk/server/zlink@v0.1.0
```

생성된 `go.mod` 예시:
```
module my-server

go 1.25.6

require (
    github.com/ZOITK/ZLink/sdk/server/zlink v0.1.0
    github.com/vmihailenco/msgpack/v5 v5.4.1
)
```

> `msgpack`은 생성된 protocol.go가 사용합니다. 다음 단계의 `go mod tidy`가 자동으로 채워줍니다.

---

## 6. 서버 코드 작성 (최소 예제)

프로젝트 루트에 `main.go`:

```go
package main

import (
	"log/slog"
	"os"

	"github.com/ZOITK/ZLink/sdk/server/zlink/logger"
	"github.com/ZOITK/ZLink/sdk/server/zlink/network"

	"my-server/protocol"
)

func main() {
	// 로거 초기화
	logger.Init("development")

	// 서버 생성 (TCP: 8080, UDP: 8090)
	// 포트 0을 주면 해당 프로토콜은 비활성화됩니다. (예: NewServer(8080, 0) → TCP 전용)
	server := network.NewServer(8080, 8090)

	// 모든 TCP/UDP 메시지가 이 콜백 하나로 들어옵니다.
	protocol.Register(server, func(sess protocol.ISession, msg any) {
		switch m := msg.(type) {
		case *protocol.Msg_AuthLoginReq:
			slog.Info("로그인 요청", "nickname", m.Nickname, "sessionID", sess.ID())
			server.Send(sess, &protocol.Msg_AuthLoginRes{
				PlayerID: 1001,
				Result:   uint32(protocol.Err_None),
			})
		}
	})

	// 세션 이벤트 (연결/해제)
	server.OnSessionOpen = func(sess *network.Session) {
		slog.Info("새 세션", "id", sess.ID(), "addr", sess.RemoteAddr)
	}
	server.OnSessionClose = func(sess *network.Session) {
		slog.Info("세션 종료", "id", sess.ID())
		// 여기서 방 퇴장/정리 로직 호출
	}

	// 서버 가동
	slog.Info("서버 시작", "tcp", 8080, "udp", 8090)
	if err := server.Start(); err != nil {
		slog.Error("서버 시작 실패", "err", err)
		os.Exit(1)
	}
}
```

핵심 API:
| API | 설명 |
|-----|------|
| `network.NewServer(tcp, udp)` | 서버 생성 (포트 0 = 해당 프로토콜 비활성) |
| `protocol.Register(server, cb)` | 모든 패킷 수신 콜백 등록 |
| `server.Send(sess, msg)` | 특정 세션에 전송 |
| `server.BroadcastUDP(msg)` | UDP 바인딩된 전체에 통지 |
| `server.OnSessionOpen / OnSessionClose` | 연결/해제 이벤트 |
| `server.Start()` | 블로킹 가동 |

---

## 7. 빌드 & 실행

```bash
cd my-server
make -C protocol-gen protocol GO_OUT=../protocol/protocol.go  # 프로토콜 생성
go mod tidy                                                    # 의존성 정리
go build -o bin/server ./...                                   # 빌드
./bin/server                                                   # 실행
```

서버가 TCP 8080 / UDP 8090에서 대기하면 성공입니다.

---

## 8. 다음 단계

- **세션 ↔ 게임 컨텍스트 연결**: SDK 세션 ID와 게임 ID(유저/방)를 잇는 메타데이터 패턴이 필요합니다. zoit-moduta-socket의 `SessionMeta` 구조를 참고하세요.
- **방/룸 관리**: `OnSessionClose`에서 방 퇴장·빈 방 삭제를 처리합니다.
- **배포**: systemd 서비스 등록 스크립트는 zoit-moduta-socket의 `run_service.sh`를 참고하세요. (실행 중 바이너리 교체 시 **서비스를 먼저 중지**해야 ETXTBSY를 피합니다.)

---

## 9. 트러블슈팅

| 증상 | 원인 / 해결 |
|------|-------------|
| `protocol-gen: command not found` | 1단계 미설치. `uv tool install …` 실행 |
| `make protocol` 실패 | 생성기 미설치 또는 schema.yaml 문법 오류 |
| `cannot find module … zlink` | `go get …/sdk/server/zlink@v0.1.0` 누락 |
| import 경로 빨간 줄 | `go mod tidy` 실행 |
| 배포 시 `Text file busy` | 실행 중 바이너리 교체. 먼저 서비스 중지 |

---

## 요약 (한눈에)

```bash
# 1회
uv tool install "git+https://github.com/ZOITK/ZLink#subdirectory=generator"

# 새 프로젝트마다
mkdir my-server && cd my-server
protocol-gen init                    # 보일러플레이트
go mod init my-server
go get github.com/ZOITK/ZLink/sdk/server/zlink@v0.1.0
# schema.yaml 편집 → main.go 작성
make -C protocol-gen protocol GO_OUT=../protocol/protocol.go
go mod tidy && go build -o bin/server ./... && ./bin/server
```
