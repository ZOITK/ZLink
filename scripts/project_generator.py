#!/usr/bin/env python3
"""
프로젝트 생성 스크립트 (재설계 버전)
engine은 외부 의존성으로 참조 (복사하지 않음)
"""

import sys
import shutil
import argparse
from pathlib import Path
from typing import Optional


def get_script_dir() -> Path:
	"""스크립트가 위치한 디렉토리"""
	return Path(__file__).parent


def get_project_root() -> Path:
	"""프로젝트 루트"""
	return get_script_dir().parent


def get_templates_dir() -> Path:
	"""템플릿 디렉토리"""
	return get_project_root() / "templates"


def normalize_path(path_str: str) -> Path:
	"""경로 정규화 (절대/상대 모두 지원)"""
	output_path = Path(path_str)
	if not output_path.is_absolute():
		output_path = Path.cwd() / output_path
	return output_path.resolve()


def render_template(template_content: str, variables: dict) -> str:
	"""
	템플릿 내용에서 {{VARIABLE}} 치환
	"""
	result = template_content
	for key, value in variables.items():
		if value:
			result = result.replace(f"{{{{{key}}}}}", str(value))
		else:
			# 값이 없으면 {{VARIABLE}}를 제거하되, 관련 섹션도 제거
			result = result.replace(f"{{{{{key}}}}}", "")
	return result


def copy_template_files(template_dir: Path, dest_dir: Path, variables: dict):
	"""
	.tmpl 파일: 렌더링 후 .tmpl 제거하고 저장
	일반 파일: 그대로 복사
	"""
	for item in template_dir.rglob("*"):
		if item.is_dir():
			continue

		rel_path = item.relative_to(template_dir)

		# .tmpl 파일 처리
		if item.suffix == ".tmpl":
			content = item.read_text(encoding="utf-8")
			rendered = render_template(content, variables)

			# .tmpl 제거한 파일명
			dest_file = dest_dir / rel_path.with_suffix("")
			dest_file.parent.mkdir(parents=True, exist_ok=True)
			dest_file.write_text(rendered, encoding="utf-8")
			print(f"  ✓ {rel_path.with_suffix('')} 생성")

		# 일반 파일 복사 (go.sum, .python-version, uv.lock 등)
		elif item.name not in [".gitkeep"]:
			dest_file = dest_dir / rel_path
			dest_file.parent.mkdir(parents=True, exist_ok=True)
			shutil.copy2(item, dest_file)
			print(f"  ✓ {rel_path} 복사")


def create_protocol_directory(dest_dir: Path, lang: str):
	"""
	protocol 디렉토리 생성 및 기본 파일 작성
	"""
	protocol_dir = dest_dir / "protocol"
	protocol_dir.mkdir(exist_ok=True)

	if lang == "go":
		content = """package protocol

// ISession - 세션 인터페이스
type ISession interface {
	SendRaw(data []byte) error
	RemoteAddr() string
	Close() error
}

// Register - 프로토콜 핸들러 등록
func Register(srv interface{}, handler func(ISession, any)) {
	// make gen 명령어로 실제 프로토콜 코드가 생성됨
}

// OnRecvPacket - 패킷 수신 핸들러
func OnRecvPacket(s ISession, msg any) {
	// TODO: 비즈니스 로직 구현
}
"""
		(protocol_dir / "protocol.go").write_text(content)
		print(f"  ✓ protocol/protocol.go 생성")

	elif lang == "python":
		(protocol_dir / "__init__.py").write_text("")
		content = """# 프로토콜 정의
# make gen 명령어로 실제 프로토콜 코드가 생성됨

class IClient:
	pass

def Register(client: IClient, handler):
	pass

async def OnRecvPacket(client: IClient, msg):
	pass
"""
		(protocol_dir / "protocol.py").write_text(content)
		print(f"  ✓ protocol/protocol.py 생성")

	elif lang == "csharp":
		content = """using System;

namespace Zoit.Protocol
{
	/// <summary>
	/// 프로토콜 정의
	/// make gen 명령어로 실제 프로토콜 코드가 생성됨
	/// </summary>
	public static class Protocol
	{
		public static void Register(object client, Action<object, object> handler)
		{
			// TODO: 프로토콜 핸들러 등록 로직
		}

		public static void OnRecvPacket(object client, object msg)
		{
			// TODO: 비즈니스 로직 구현
		}
	}
}
"""
		(protocol_dir / "protocol.cs").write_text(content)
		print(f"  ✓ protocol/protocol.cs 생성")


def create_gitignore(dest_dir: Path, lang: str):
	"""각 언어별 .gitignore 생성"""
	if lang == "go":
		content = """# Go
*.o
*.a
*.so
.DS_Store
out/
bin/
*.exe
*.exe~
*.dll
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
	elif lang == "python":
		content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual environments
.venv
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store

# uv
uv.lock
"""
	elif lang == "csharp":
		content = """# Unity
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

# OS
.DS_Store

# Build
bin/
obj/
"""
	else:
		return

	(dest_dir / ".gitignore").write_text(content)
	print(f"  ✓ .gitignore 생성")


def create_readme(dest_dir: Path, lang: str, project_name: str):
	"""README.md 생성"""
	if lang == "go":
		content = f"""# {project_name}

Zo Socket Framework 기반 Go 서버 프로젝트

## 시작하기

### 프로토콜 생성
```bash
make gen
```

### 서버 실행
```bash
go run main.go
```

## 구조
- `protocol/`: 프로토콜 정의
- `main.go`: 서버 진입점
"""
	elif lang == "python":
		content = f"""# {project_name}

Zo Socket Framework 기반 Python 클라이언트 프로젝트

## 시작하기

### 환경 설정
```bash
uv sync
```

### 프로토콜 생성
```bash
make gen
```

### 클라이언트 실행
```bash
uv run main.py
```

## 구조
- `protocol/`: 프로토콜 정의
- `main.py`: 클라이언트 진입점
"""
	elif lang == "csharp":
		content = f"""# {project_name}

Zo Socket Framework 기반 Unity3D C# 클라이언트 프로젝트

## 시작하기

### 프로토콜 생성
```bash
make gen
```

### Unity 사용
1. Assets/ZoSocket 폴더 포함됨
2. Assets/Plugins에 MessagePack DLL 포함됨
3. protocol/protocol.cs는 make gen으로 생성됨

## 구조
- `Assets/ZoSocket/`: 클라이언트 코드
- `Assets/Plugins/`: 외부 라이브러리
"""
	else:
		return

	(dest_dir / "README.md").write_text(content)
	print(f"  ✓ README.md 생성")


def create_server_go(output_path: Path, engine_version: str, engine_local: str):
	"""Go 서버 프로젝트 생성"""
	print(f"\n🚀 Go 서버 프로젝트 생성: {output_path}")

	output_path = normalize_path(str(output_path))

	if output_path.exists():
		print(f"❌ 오류: {output_path} 이미 존재합니다")
		sys.exit(1)

	output_path.mkdir(parents=True, exist_ok=True)
	print(f"✓ 디렉토리 생성: {output_path}")

	# 템플릿 변수
	project_name = output_path.name
	variables = {
		"PROJECT_NAME": project_name,
		"ENGINE_VERSION": engine_version or "latest",
		"ENGINE_LOCAL_REPLACE": "\nreplace dev.azure.com/zoit/zoit-socket-framework/_git/zoit-socket-framework/engine/server-go => ./engine/server-go" if engine_local else "",
	}

	# templates/server-go 복사
	template_dir = get_templates_dir() / "server-go"
	copy_template_files(template_dir, output_path, variables)

	# engine 복사 (로컬 개발용)
	if engine_local:
		src_engine = Path(engine_local).resolve()
		dst_engine = output_path / "engine" / "server-go"
		if src_engine.exists():
			shutil.copytree(src_engine, dst_engine, dirs_exist_ok=True)
			print(f"  ✓ engine 폴더 복사")

	# go.work 파일 생성 (로컬 개발용)
	if engine_local:
		go_work_content = """go 1.25.6

use (
	.
)
"""
		(output_path / "go.work").write_text(go_work_content)
		print(f"  ✓ go.work 생성 (로컬 개발 모드)")

	# .gitignore, README.md
	create_gitignore(output_path, "go")
	create_readme(output_path, "go", project_name)

	print(f"\n✅ Go 서버 프로젝트 생성 완료!")
	print(f"📁 경로: {output_path}")


def create_client_python(output_path: Path, engine_version: str, engine_local: str):
	"""Python 클라이언트 프로젝트 생성"""
	print(f"\n🚀 Python 클라이언트 프로젝트 생성: {output_path}")

	output_path = normalize_path(str(output_path))

	if output_path.exists():
		print(f"❌ 오류: {output_path} 이미 존재합니다")
		sys.exit(1)

	output_path.mkdir(parents=True, exist_ok=True)
	print(f"✓ 디렉토리 생성: {output_path}")

	# 템플릿 변수
	project_name = output_path.name
	engine_local_sources = ""
	if engine_local:
		engine_local_sources = f"""
[tool.uv.sources]
zoit-socket-client = {{ path = "{engine_local}", editable = true }}"""

	variables = {
		"PROJECT_NAME": project_name,
		"ENGINE_VERSION": engine_version or "latest",
		"ENGINE_LOCAL_SOURCES": engine_local_sources,
	}

	# templates/client-python 복사
	template_dir = get_templates_dir() / "client-python"
	copy_template_files(template_dir, output_path, variables)

	# .gitignore, README.md
	create_gitignore(output_path, "python")
	create_readme(output_path, "python", project_name)

	print(f"\n✅ Python 클라이언트 프로젝트 생성 완료!")
	print(f"📁 경로: {output_path}")


def create_client_csharp(output_path: Path, engine_version: str, engine_local: str):
	"""Unity3D C# 클라이언트 프로젝트 생성"""
	print(f"\n🚀 C# (Unity3D) 클라이언트 프로젝트 생성: {output_path}")

	output_path = normalize_path(str(output_path))

	if output_path.exists():
		print(f"❌ 오류: {output_path} 이미 존재합니다")
		sys.exit(1)

	output_path.mkdir(parents=True, exist_ok=True)
	print(f"✓ 디렉토리 생성: {output_path}")

	# Assets 디렉토리 생성
	assets_dir = output_path / "Assets"
	assets_dir.mkdir(exist_ok=True)

	# ZoSocket 디렉토리
	zo_socket_dir = assets_dir / "ZoSocket"
	zo_socket_dir.mkdir(exist_ok=True)

	# engine/client-csharp의 .cs 파일 복사
	engine_csharp_dir = get_project_root() / "engine" / "client-csharp"
	for item in ["logger", "network", "protocol"]:
		src = engine_csharp_dir / item
		dst = zo_socket_dir / "Engine" / item
		if src.exists():
			shutil.copytree(src, dst, dirs_exist_ok=True)
			print(f"  ✓ {item} 복사")

	# Plugins 복사
	plugins_src = engine_csharp_dir / "plugins"
	plugins_dst = assets_dir / "Plugins"
	if plugins_src.exists():
		shutil.copytree(plugins_src, plugins_dst, dirs_exist_ok=True)
		print(f"  ✓ plugins 복사")

	# .gitignore, README.md
	create_gitignore(output_path, "csharp")
	create_readme(output_path, "csharp", output_path.name)

	print(f"\n✅ C# (Unity3D) 클라이언트 프로젝트 생성 완료!")
	print(f"📁 경로: {output_path}")


def main():
	"""메인 함수"""
	parser = argparse.ArgumentParser(description="Zo Socket Framework 프로젝트 생성")

	subparsers = parser.add_subparsers(dest="command", help="명령어")

	# server 명령어
	server_parser = subparsers.add_parser("server", help="Go 서버 프로젝트 생성")
	server_parser.add_argument("output_path", help="생성 경로")
	server_parser.add_argument("--engine-version", default="latest", help="engine 버전 (기본값: latest)")
	server_parser.add_argument("--engine-local", default="", help="로컬 engine 경로 (없으면 외부 참조)")

	# client 명령어
	client_parser = subparsers.add_parser("client", help="클라이언트 프로젝트 생성")
	client_parser.add_argument("language", choices=["python", "csharp"], help="프로그래밍 언어")
	client_parser.add_argument("output_path", help="생성 경로")
	client_parser.add_argument("--engine-version", default="latest", help="engine 버전 (기본값: latest)")
	client_parser.add_argument("--engine-local", default="", help="로컬 engine 경로 (없으면 외부 참조)")

	args = parser.parse_args()

	if not args.command:
		parser.print_help()
		sys.exit(1)

	try:
		if args.command == "server":
			create_server_go(args.output_path, args.engine_version, args.engine_local)
		elif args.command == "client":
			if args.language == "python":
				create_client_python(args.output_path, args.engine_version, args.engine_local)
			elif args.language == "csharp":
				create_client_csharp(args.output_path, args.engine_version, args.engine_local)
	except Exception as e:
		print(f"\n❌ 오류: {e}", file=sys.stderr)
		sys.exit(1)


if __name__ == "__main__":
	main()
