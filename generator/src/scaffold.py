# 프로젝트 스캐폴딩 (protocol-gen init)
#
# 새 프로젝트에서 `protocol-gen init` 실행 시, 현재 위치에 protocol-gen/ 폴더를
# 만들고 그 안에 Makefile과 schema.yaml 템플릿을 생성합니다.
# 이미 존재하는 파일은 덮어쓰지 않습니다(skip).
from pathlib import Path
from typing import Optional

# ----------------------------------------------------------------------------
# 템플릿: Makefile
#   - 레시피 라인은 반드시 탭(\t) 들여쓰기여야 make가 정상 동작합니다.
#   - 출력 경로(GO_OUT/CS_OUT)는 변수라 `make protocol GO_OUT=경로`로 오버라이드 가능합니다.
# ----------------------------------------------------------------------------
MAKEFILE_TEMPLATE = """\
# zlink 프로토콜 생성 (protocol-gen init 으로 생성됨)
#
# schema.yaml(단일 진실 원천) → protocol.go + protocol.cs 를 생성합니다.
#
# [생성기 설치 - 1회]
#   uv tool install "git+https://github.com/ZOITK/ZLink#subdirectory=generator"
#
# [사용]
#   make protocol                          # 기본 경로(./protocol.go, ./protocol.cs)
#   make protocol GO_OUT=../server/p.go    # 출력 경로 오버라이드

SCHEMA := schema.yaml
GO_OUT := protocol.go
CS_OUT := protocol.cs

.PHONY: protocol
protocol:
\tprotocol-gen --schema $(SCHEMA) --languages go,csharp --go-out $(GO_OUT) --cs-out $(CS_OUT)
\t@echo "✅ 프로토콜 생성 완료: $(GO_OUT), $(CS_OUT)"
"""

# ----------------------------------------------------------------------------
# 템플릿: schema.yaml
#   - 바로 `make protocol`이 동작하도록 검증된 최소 예제(system/auth)를 담습니다.
#   - 실제 프로젝트에서는 이 파일을 편집해 패킷을 정의합니다.
# ----------------------------------------------------------------------------
SCHEMA_TEMPLATE = """\
metadata:
  version: 1
  categories: [system, auth]
  protocols: [tcp]
  types: [req, res, notify]

# 전역 에러 코드
global_errors:
  - { name: None,         idx: 0, doc: "정상" }
  - { name: InvalidValue, idx: 1, doc: "잘못된 값" }
  - { name: Unauthorized, idx: 2, doc: "인증 필요" }
  - { name: Server,       idx: 3, doc: "서버 오류" }

definitions:
  system:
    packets:
      - name: TCPHeartBit
        idx: 1
        proto: tcp
        doc: "TCP Heartbeat / TCP 하트비트"
        desc: "Keep-alive check / 연결 생존 확인"
        req: { fields: { ServerTime: int64 } }
        res: { fields: { ServerTime: int64 } }

  auth:
    packets:
      - name: Login
        idx: 1
        proto: tcp
        doc: "Login / 로그인"
        desc: "Login with nickname / 닉네임으로 로그인"
        pair:
          req: { fields: { Nickname: string } }
          res: { fields: { PlayerID: uint32, Result: uint32 } }
"""

# init이 생성하는 파일 목록 (파일명, 내용)
_SCAFFOLD_FILES = [
    ("Makefile", MAKEFILE_TEMPLATE),
    ("schema.yaml", SCHEMA_TEMPLATE),
]


def run_init(target_dir: Optional[str] = None) -> None:
    """
    현재 위치(또는 지정 경로)에 protocol-gen/ 폴더와 보일러플레이트를 생성합니다.

    Args:
        target_dir: 생성 위치. 미지정 시 ./protocol-gen 을 사용합니다.

    동작:
        - 폴더가 없으면 만들고, 파일은 없을 때만 생성합니다(기존 파일 보존).
    """
    base = Path(target_dir).resolve() if target_dir else (Path.cwd() / "protocol-gen").resolve()
    base.mkdir(parents=True, exist_ok=True)

    created = []
    skipped = []
    for name, content in _SCAFFOLD_FILES:
        path = base / name
        if path.exists():
            skipped.append(name)
            continue
        path.write_text(content, encoding="utf-8")
        created.append(name)

    print(f"📁 스캐폴딩 위치: {base}")
    for name in created:
        print(f"   ✓ 생성됨: {name}")
    for name in skipped:
        print(f"   • 건너뜀(이미 존재): {name}")

    print("\n다음 단계:")
    print(f"   1) cd {base.name}")
    print("   2) schema.yaml 편집")
    print("   3) make protocol")
