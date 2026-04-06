#!/usr/bin/env python3
"""
프로젝트 생성 스크립트
서버(Go), 클라이언트(Python, Unity3D C#) 프로젝트 자동 생성
"""

import sys
import shutil
import argparse
from pathlib import Path
from typing import Optional


def get_script_dir() -> Path:
    """스크립트가 위치한 디렉토리 반환"""
    return Path(__file__).parent


def get_project_root() -> Path:
    """프로젝트 루트 디렉토리 반환"""
    return get_script_dir().parent


def get_engine_dir() -> Path:
    """engine 디렉토리 반환"""
    return get_project_root() / "engine"


def normalize_path(path_str: str) -> Path:
    """
    경로 정규화 (절대경로 또는 상대경로 모두 지원)
    현재 작업 디렉토리를 기준으로 경로 계산
    """
    output_path = Path(path_str)

    # 상대경로인 경우 현재 작업 디렉토리 기준으로 변환
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path

    return output_path.resolve()


def copy_engine(src_engine: Path, dest_project: Path, engine_subdir: str, dest_subdir: Optional[str] = None):
    """
    engine 특정 언어 폴더의 내용 복사

    Args:
        src_engine: 원본 engine 디렉토리 경로
        dest_project: 대상 프로젝트 디렉토리 경로
        engine_subdir: engine 내의 특정 서브디렉토리 (예: "server-go", "client-python")
        dest_subdir: 대상의 서브디렉토리 (기본값: "engine")
    """
    if dest_subdir is None:
        dest_subdir = "engine"

    src_path = src_engine / engine_subdir
    dest_path = dest_project / dest_subdir

    # 대상 폴더가 이미 존재하면 제거 (새로 생성하기 위해)
    if dest_path.exists():
        shutil.rmtree(dest_path)

    # 해당 언어의 engine 폴더 내용만 복사
    print(f"  engine/{engine_subdir} 복사: {src_path} -> {dest_path}")
    shutil.copytree(src_path, dest_path, ignore=shutil.ignore_patterns('.git', '__pycache__', '.venv', '.pytest_cache', 'node_modules', 'obj', 'bin', '.DS_Store'))


def create_server_go(output_path: Path):
    """
    Go 서버 프로젝트 생성
    """
    print(f"\n🚀 Go 서버 프로젝트 생성: {output_path}")

    # 경로 확인 및 생성
    output_path = normalize_path(str(output_path))

    if output_path.exists():
        print(f"❌ 오류: {output_path} 폴더가 이미 존재합니다.")
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=False)
    print(f"✓ 프로젝트 디렉토리 생성: {output_path}")

    # engine 복사
    copy_engine(get_engine_dir(), output_path, "server-go")

    # go.mod 생성
    project_name = output_path.name
    go_mod_content = f"""module {project_name}

go 1.25.6

replace github.com/zoit/zo-socket-framework/engine/server-go => ./engine

require (
	github.com/vmihailenco/msgpack/v5 v5.4.1
	github.com/zoit/zo-socket-framework/engine/server-go v0.0.0-00010101000000-000000000000
)

require github.com/vmihailenco/tagparser/v2 v2.0.0 // indirect
"""

    go_mod_path = output_path / "go.mod"
    go_mod_path.write_text(go_mod_content)
    print(f"✓ go.mod 생성")

    # protocol 디렉토리 생성
    protocol_dir = output_path / "protocol"
    protocol_dir.mkdir(exist_ok=True)

    # 기본 Protocol.go 생성
    protocol_go_content = """package protocol

// ISession - 세션 인터페이스
type ISession interface {
	SendRaw(data []byte) error
	RemoteAddr() string
	Close() error
}

// Register - 프로토콜 핸들러 등록
func Register(srv interface{}, handler func(ISession, any)) {
	// TODO: 프로토콜 핸들러 등록 로직
	// make gen 명령어로 실제 프로토콜 코드가 생성될 때까지 빈 구현
}

// OnRecvPacket - 패킷 수신 핸들러
func OnRecvPacket(s ISession, msg any) {
	// TODO: 비즈니스 로직 구현
}
"""

    protocol_go_path = protocol_dir / "Protocol.go"
    protocol_go_path.write_text(protocol_go_content)
    print(f"✓ 기본 Protocol.go 생성")

    # main.go 생성
    main_go_content = """package main

import (
	"log/slog"
	"net"
	"os"
	"os/signal"
	"syscall"

	"__PROJECT_NAME__/protocol"

	"github.com/zoit/zo-socket-framework/engine/server-go/pkg/config"
	"github.com/zoit/zo-socket-framework/engine/server-go/pkg/logger"
	"github.com/zoit/zo-socket-framework/engine/server-go/pkg/network"
)

func main() {
	cfg := config.Load()
	logger.Init(cfg.NodeEnv)

	slog.Info("서버 시작")

	srv := network.NewServer(cfg)

	// 프로토콜과 핸들러 바인딩
	protocol.Register(srv, protocol.OnRecvPacket)

	srv.OnConnect = func(conn net.Conn) {
		sess := network.NewSession(conn)
		sess.SetUDPServer(srv.UDP)

		slog.Info("[Server] 새 클라이언트 접속", "addr", sess.RemoteAddr)
		sess.HandleConnection(srv)
		slog.Info("[Server] 클라이언트 접속 종료", "addr", sess.RemoteAddr)
		sess.Close()
	}

	if err := srv.Start(); err != nil {
		slog.Error("서버 가동 실패", "err", err)
		os.Exit(1)
	}

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	<-sigCh
	srv.Stop()
}
""".replace("__PROJECT_NAME__", project_name)

    main_go_path = output_path / "main.go"
    main_go_path.write_text(main_go_content)
    print(f"✓ main.go 생성")

    # .gitignore 생성
    gitignore_content = """# Go
*.o
*.a
*.so
.DS_Store
out/
bin/
*.exe
*.exe~
*.dll
*.so
*.dylib

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Binary
/server_bin

# Dependencies
go.sum
"""

    gitignore_path = output_path / ".gitignore"
    gitignore_path.write_text(gitignore_content)
    print(f"✓ .gitignore 생성")

    # README.md 생성
    readme_content = f"""# {project_name}

Zo Socket Framework 기반 Go 서버 프로젝트

## 시작하기

### 프로토콜 생성
```bash
cd {output_path.parent}
make gen
```

### 서버 실행
```bash
go run main.go
```

## 구조
- `engine/`: 프레임워크 엔진
- `protocol/`: 프로토콜 정의
- `main.go`: 서버 메인 파일
"""

    readme_path = output_path / "README.md"
    readme_path.write_text(readme_content)
    print(f"✓ README.md 생성")

    print(f"\n✅ Go 서버 프로젝트 생성 완료!")
    print(f"📁 경로: {output_path}")
    print(f"\n📋 다음 단계:")
    print(f"  1. cd {output_path}")
    print(f"  2. make gen (프로토콜 파일 생성)")
    print(f"  3. go run main.go (서버 실행)")


def create_client_python(output_path: Path):
    """
    Python 클라이언트 프로젝트 생성
    """
    print(f"\n🚀 Python 클라이언트 프로젝트 생성: {output_path}")

    # 경로 확인 및 생성
    output_path = normalize_path(str(output_path))

    if output_path.exists():
        print(f"❌ 오류: {output_path} 폴더가 이미 존재합니다.")
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=False)
    print(f"✓ 프로젝트 디렉토리 생성: {output_path}")

    # engine 복사
    copy_engine(get_engine_dir(), output_path, "client-python")

    # pyproject.toml 생성
    project_name = output_path.name.replace("-", "_")

    pyproject_content = f"""[project]
name = "{project_name}"
version = "0.1.0"
description = "Zo Socket Framework 기반 Python 클라이언트"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "asyncio>=4.0.0",
    "msgspec>=0.20.0",
    "zoit-client-python",
]

[tool.uv.sources]
zoit-client-python = {{ path = "./engine/client-python", editable = true }}
"""

    pyproject_path = output_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)
    print(f"✓ pyproject.toml 생성")

    # protocol 디렉토리 생성
    protocol_dir = output_path / "protocol"
    protocol_dir.mkdir(exist_ok=True)

    # __init__.py 생성
    init_path = protocol_dir / "__init__.py"
    init_path.write_text("")
    print(f"✓ protocol/__init__.py 생성")

    # 기본 Protocol.py 생성
    protocol_py_content = """# 프로토콜 정의
# make gen 명령어로 실제 프로토콜 코드가 생성될 때까지 빈 구현

class IClient:
    \"\"\"클라이언트 인터페이스\"\"\"
    pass


def Register(client: IClient, handler):
    \"\"\"
    프로토콜 핸들러 등록

    Args:
        client: 클라이언트 인스턴스
        handler: 메시지 수신 핸들러
    \"\"\"
    # TODO: 프로토콜 핸들러 등록 로직
    pass


async def OnRecvPacket(client: IClient, msg):
    \"\"\"
    패킷 수신 핸들러

    Args:
        client: 클라이언트 인스턴스
        msg: 수신한 메시지 객체
    \"\"\"
    # TODO: 비즈니스 로직 구현
    pass
"""

    protocol_py_path = protocol_dir / "Protocol.py"
    protocol_py_path.write_text(protocol_py_content)
    print(f"✓ 기본 Protocol.py 생성")

    # main.py 생성
    main_py_content = """import asyncio
from engine.network.tcp_client import AsyncTcpClient
from engine.logger.logger import logger
import protocol.Protocol as protocol


async def main():
    logger.info("Python 클라이언트 시작")

    # TCP 클라이언트 초기화
    client = AsyncTcpClient(Host="127.0.0.1", Port=8080)

    # 프로토콜과 핸들러 바인딩
    protocol.Register(client, protocol.OnRecvPacket)

    # 서버 연결
    if not await client.Connect():
        return

    logger.info("서버에 연결되었습니다.")

    # TODO: 패킷 송수신 로직 구현

    await client.Close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
"""

    main_py_path = output_path / "main.py"
    main_py_path.write_text(main_py_content)
    print(f"✓ main.py 생성")

    # .gitignore 생성
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store

# uv
.uv/
uv.lock
"""

    gitignore_path = output_path / ".gitignore"
    gitignore_path.write_text(gitignore_content)
    print(f"✓ .gitignore 생성")

    # README.md 생성
    readme_content = f"""# {project_name}

Zo Socket Framework 기반 Python 클라이언트 프로젝트

## 시작하기

### 환경 설정
```bash
# uv를 이용한 가상환경 생성
uv sync
```

### 프로토콜 생성
```bash
cd ..
make gen
```

### 클라이언트 실행
```bash
uv run main.py
```

## 구조
- `engine/`: 프레임워크 엔진
- `protocol/`: 프로토콜 정의
- `main.py`: 클라이언트 메인 파일
"""

    readme_path = output_path / "README.md"
    readme_path.write_text(readme_content)
    print(f"✓ README.md 생성")

    print(f"\n✅ Python 클라이언트 프로젝트 생성 완료!")
    print(f"📁 경로: {output_path}")
    print(f"\n📋 다음 단계:")
    print(f"  1. cd {output_path}")
    print(f"  2. uv sync (의존성 설치)")
    print(f"  3. make gen (프로토콜 파일 생성)")
    print(f"  4. uv run main.py (클라이언트 실행)")


def create_client_csharp(output_path: Path):
    """
    Unity3D C# 클라이언트 프로젝트 생성 (Assets 폴더 지원)
    """
    print(f"\n🚀 C# (Unity3D) 클라이언트 프로젝트 생성: {output_path}")

    # 경로 확인 및 생성
    output_path = normalize_path(str(output_path))

    if output_path.exists():
        print(f"❌ 오류: {output_path} 폴더가 이미 존재합니다.")
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=False)
    print(f"✓ 프로젝트 디렉토리 생성: {output_path}")

    # Assets 디렉토리 생성
    assets_dir = output_path / "Assets"
    assets_dir.mkdir(exist_ok=True)

    # ZoSocket 디렉토리 생성
    zo_socket_dir = assets_dir / "ZoSocket"
    zo_socket_dir.mkdir(exist_ok=True)

    # Protocol 디렉토리 생성
    protocol_dir = zo_socket_dir / "Protocol"
    protocol_dir.mkdir(exist_ok=True)

    # engine 복사 (Assets 내부)
    copy_engine(get_engine_dir(), output_path, "client-csharp", "Assets/engine")
    print(f"✓ engine 폴더를 Assets에 복사")

    # 기본 Protocol.cs 생성
    protocol_cs_content = """using System;

namespace Zoit.Protocol
{
    /// <summary>
    /// 프로토콜 정의
    /// make gen 명령어로 실제 프로토콜 코드가 생성될 때까지 빈 구현
    /// </summary>
    public static class Protocol
    {
        /// <summary>
        /// 프로토콜 핸들러 등록
        /// </summary>
        public static void Register(object client, Action<object, object> handler)
        {
            // TODO: 프로토콜 핸들러 등록 로직
        }

        /// <summary>
        /// 패킷 수신 핸들러
        /// </summary>
        public static void OnRecvPacket(object client, object msg)
        {
            // TODO: 비즈니스 로직 구현
        }
    }
}
"""

    protocol_cs_path = protocol_dir / "Protocol.cs"
    protocol_cs_path.write_text(protocol_cs_content)
    print(f"✓ 기본 Protocol.cs 생성")

    # Assets/ZoSocket/Scripts 디렉토리
    scripts_dir = zo_socket_dir / "Scripts"
    scripts_dir.mkdir(exist_ok=True)

    # SampleClient.cs 생성
    sample_client_content = """using System;
using System.Threading.Tasks;
using Zoit;
using Zoit.Network;
using Zoit.Logger;
using Zoit.Protocol;

public class SampleClient
{
    public static async Task Main(string[] args)
    {
        ClientLogger.Info("C# 클라이언트 시작");

        // TCP 클라이언트 초기화
        var client = new TcpClient();

        // 프로토콜과 핸들러 바인딩
        Protocol.Register(client, OnRecvPacket);

        // 서버 연결
        if (!await client.ConnectAsync("127.0.0.1", 8080))
        {
            return;
        }

        ClientLogger.Info("서버에 연결되었습니다.");

        // TODO: 패킷 송수신 로직 구현

        await client.Close();
    }

    /// <summary>
    /// 패킷 수신 핸들러
    /// </summary>
    private static void OnRecvPacket(object client, object msg)
    {
        // TODO: 메시지 처리 로직
    }
}
"""

    sample_client_path = scripts_dir / "SampleClient.cs"
    sample_client_path.write_text(sample_client_content)
    print(f"✓ SampleClient.cs 생성")

    # .gitignore 생성
    gitignore_content = """# Unity
Library/
Logs/
Temp/
UserSettings/
*.log
.vs/
*.csproj
*.sln
*.user

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build
bin/
obj/
dist/
"""

    gitignore_path = output_path / ".gitignore"
    gitignore_path.write_text(gitignore_content)
    print(f"✓ .gitignore 생성")

    # README.md 생성
    project_name = output_path.name
    readme_content = f"""# {project_name}

Zo Socket Framework 기반 Unity3D C# 클라이언트 프로젝트

## 시작하기

### 프로토콜 생성
\`\`\`bash
cd ..
make gen
\`\`\`

### Unity에서 사용
1. Assets/ZoSocket 폴더가 프로젝트에 포함됨
2. Assets/engine 폴더에 Zo Socket Framework 엔진 포함
3. Protocol.cs는 make gen으로 생성된 실제 프로토콜로 교체됨

### 클라이언트 사용 예
\`\`\`csharp
var client = new TcpClient();
Protocol.Register(client, OnRecvPacket);
await client.ConnectAsync("127.0.0.1", 8080);
\`\`\`

## 구조
- `Assets/ZoSocket/`: 클라이언트 코드
  - `Protocol/`: 프로토콜 정의
  - `Scripts/`: 클라이언트 구현
- `Assets/engine/`: 프레임워크 엔진
"""

    readme_path = output_path / "README.md"
    readme_path.write_text(readme_content)
    print(f"✓ README.md 생성")

    print(f"\n✅ C# (Unity3D) 클라이언트 프로젝트 생성 완료!")
    print(f"📁 경로: {output_path}")
    print(f"\n📋 다음 단계:")
    print(f"  1. cd {output_path}")
    print(f"  2. make gen (프로토콜 파일 생성)")
    print(f"  3. Unity에서 프로젝트 열기")
    print(f"  4. Assets/ZoSocket 폴더 사용")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="Zo Socket Framework 프로젝트 생성 도구"
    )

    subparsers = parser.add_subparsers(dest="command", help="명령어")

    # server 명령어
    server_parser = subparsers.add_parser("server", help="Go 서버 프로젝트 생성")
    server_parser.add_argument("output_path", help="생성할 프로젝트 경로")

    # client 명령어
    client_parser = subparsers.add_parser("client", help="클라이언트 프로젝트 생성")
    client_parser.add_argument(
        "language",
        choices=["python", "csharp"],
        help="프로그래밍 언어 (python, csharp)"
    )
    client_parser.add_argument("output_path", help="생성할 프로젝트 경로")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "server":
            create_server_go(args.output_path)
        elif args.command == "client":
            if args.language == "python":
                create_client_python(args.output_path)
            elif args.language == "csharp":
                create_client_csharp(args.output_path)
    except Exception as e:
        print(f"\n❌ 오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
