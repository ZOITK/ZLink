# CLI 인터페이스
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .loader import load_protocol
from .validator import validate_protocol
import yaml

from .generators.python_generator import PythonGenerator
from .generators.go_generator import GoGenerator
from .generators.csharp_generator import CSharpGenerator
from .generators.markdown_generator import MarkdownGenerator


def main():
    """
    CLI 진입점 함수입니다.
    """
    # 'init' 서브커맨드: 새 프로젝트 보일러플레이트(Makefile + schema.yaml) 생성
    # 기존 사용법(protocol-gen --schema ...)과 충돌하지 않도록 argparse 이전에 분기합니다.
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        from .scaffold import run_init
        # init 다음 인자가 있으면 생성 위치로 사용 (없으면 ./protocol-gen)
        target = sys.argv[2] if len(sys.argv) > 2 else None
        run_init(target)
        return

    parser = argparse.ArgumentParser(description="zlink-protocol-gen - 프로토콜 코드 생성기")
    
    # 위치 인자
    parser.add_argument("schema_pos", nargs="?", help="YAML 스키마 파일 경로")
    
    # 옵션 인자
    parser.add_argument("--schema", help="YAML 스키마 파일 경로")
    parser.add_argument("--output-dir", default="output", help="출력 디렉토리 (기본값: output)")
    parser.add_argument("--languages", default="python,go,csharp", help="생성 언어 (기본값: python,go,csharp)")

    # 언어별 출력 파일 경로 직접 지정 옵션 (Makefile 등에서 활용)
    parser.add_argument("--go-out", help="Go 프로토콜 출력 파일 경로")
    parser.add_argument("--cs-out", help="C# 프로토콜 출력 파일 경로")
    parser.add_argument("--py-out", help="Python 프로토콜 출력 파일 경로")
    parser.add_argument("--md-out", help="마크다운 명세서 출력 경로 (미지정 시 자동 위치, 항상 생성됨)")

    args = parser.parse_args()

    # 스키마 경로 결정
    schema_path = args.schema or args.schema_pos

    if not schema_path:
        parser.print_help()
        sys.exit(1)

    try:
        generate_protocol(
            schema_path=schema_path,
            output_dir=args.output_dir,
            languages=[l.strip() for l in args.languages.split(",")],
            go_out=args.go_out,
            cs_out=args.cs_out,
            py_out=args.py_out,
            md_out=args.md_out
        )
        print("\n✓ 코드 생성 완료!")
    except Exception as e:
        print(f"\n✗ 오류: {e}", file=sys.stderr)
        sys.exit(1)


def generate_protocol(
    schema_path: str,
    output_dir: str,
    languages: List[str],
    go_out: Optional[str] = None,
    cs_out: Optional[str] = None,
    py_out: Optional[str] = None,
    md_out: Optional[str] = None
) -> None:
    print(f"📝 프로토콜 로드: {schema_path}")
    protocol = load_protocol(schema_path)
    print(f"   ✓ 버전: {protocol.version}, 구조체: {len(protocol.structs)}개")

    print(f"\n🔍 프로토콜 검증")
    success, errors = validate_protocol(protocol)
    if not success:
        raise RuntimeError("\n".join(errors))
    print(f"   ✓ 검증 성공")

    print(f"\n⚙️  코드 생성")
    
    # 출력 경로 설정 (언어별 지정이 없으면 output_dir 하위에 생성)
    # 개별 출력 경로가 모두 지정된 경우 기본 폴더를 생성하지 않음
    if not (go_out and cs_out and py_out):
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = None

    for lang in languages:
        lang = lang.strip().lower()
        if lang == "python":
            gen = PythonGenerator(protocol)
            out = py_out if py_out else str(Path(output_dir) / "Protocol.py")
            save_generated_code(gen, out)
        elif lang == "go":
            gen = GoGenerator(protocol)
            out = go_out if go_out else str(Path(output_dir) / "Protocol.go")
            save_generated_code(gen, out)
        elif lang == "csharp":
            gen = CSharpGenerator(protocol)
            out = cs_out if cs_out else str(Path(output_dir) / "Protocol.cs")
            save_generated_code(gen, out)
        else:
            print(f"   ⚠️  알 수 없는 언어: {lang}")

    # 마크다운 명세서는 언어 선택과 무관하게 항상 생성합니다 (클라이언트 개발용 문서).
    # 원본 구조(카테고리/req-res 짝/필드 설명)를 보존하기 위해 raw YAML을 직접 사용합니다.
    with open(schema_path, "r", encoding="utf-8") as f:
        raw_spec = yaml.safe_load(f)
    md_gen = MarkdownGenerator(raw_spec)
    md_path = md_out if md_out else str(Path(output_dir) / "Protocol.md")
    save_generated_code(md_gen, md_path)

def save_generated_code(generator, output_file: str) -> None:
    path = Path(output_file).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    
    code = generator.render()
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"   ✓ 생성됨: {path}")


if __name__ == "__main__":
    main()
