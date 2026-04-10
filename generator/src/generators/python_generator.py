# Python 코드 생성기 - v13.0 단일 protocol.py 출력
import datetime
from pathlib import Path
from ..models import ProtocolDef, StructDef, FieldDef, PacketDef

class PythonGenerator:
    def __init__(self, protocol: ProtocolDef):
        self.protocol = protocol

    def render(self) -> str:
        """렌더링된 Python 코드를 문자열로 반환"""
        return self._generate_protocol_file()

    def generate(self, output_dir: str) -> None:
        """단일 protocol.py 파일로 생성"""
        # 출력 경로 강제: sdk/client/python/zlink/protocol
        base_path = Path(output_dir) / "python/zlink/protocol"
        base_path.mkdir(parents=True, exist_ok=True)

        code = self.render()
        with open(base_path / "protocol.py", "w", encoding="utf-8") as f:
            f.write(code)

        print(f"✓ Python 프로토콜 생성 완료 (protocol.py)")

    def _generate_protocol_file(self) -> str:
        """protocol.py 전체 내용 생성 (ZLink 24B 표준 규격)"""
        now_str = datetime.datetime.now().strftime("%Y-%m-%d : %H:%M:%S")
        
        lines = []
        lines.append(f'''# 자동 생성된 프로토콜
# 버전: {self.protocol.version}
# [ {now_str} ] 자동 생성됨 (zlink-protocol-gen)
import msgspec
import sys
import os
from typing import Optional, List, Dict, Any

# SDK 또는 Example 환경에서 모두 작동하도록 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from zlink.network.tcp_client import Pack  # SDK 엔진 조립 함수 참조

class PacketRegistry:
    _Registry = {{}}
    @classmethod
    def Unmarshal(cls, cmd: int, data: bytes) -> Any:
        msg_cls = cls._Registry.get(cmd)
        if not msg_cls: return None
        return msg_cls.Decode(data)

def Register(client, callback):
    """엔진 서버 또는 클라이언트에 프로토콜 지식과 비즈니스 콜백을 등록합니다."""
    # 엔진에 마샬러/언마샬러 주입 (Symmetry)
    def packer(msg, use_udp, session_id=0):
        if use_udp:
            return msg.BuildUDP(session_id)
        else:
            return msg.BuildTCP(0)

    client.set_protocol(PacketRegistry.Unmarshal, packer)
    client.add_recv_callback(callback)

# --- 커맨드 ID (Cmd_) ---
''')
        # Cmd_ 상단 정의
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            lines.append(f"Cmd_{pkt.name} = {pkt.get_id()}")

        lines.append("\n# --- 에러 코드 (Err_) ---")
        for e in sorted(self.protocol.errors, key=lambda x: x.index):
            lines.append(f"Err_{e.name} = {e.index}")

        lines.append("")

        # Msg_ 공통 구조체
        for s in sorted(self.protocol.structs.values(), key=lambda x: x.name):
            lines.append(self._generate_struct_def(s))
            lines.append("")

        # Msg_ 패킷 구조체
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            lines.append(self._generate_packet_def(pkt))
            lines.append("")

        # 패킷 레지스트리 등록부
        lines.append("# --- 패킷 레지스트리 등록 ---")
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            lines.append(f"PacketRegistry._Registry[Cmd_{pkt.name}] = Msg_{pkt.name}")

        return "\n".join(lines)

    def _generate_struct_def(self, struct: StructDef) -> str:
        doc = struct.doc if struct.doc else struct.name
        lines = [
            f"class Msg_{struct.name}(msgspec.Struct, omit_defaults=True, array_like=True):",
            f"    \"\"\"{doc}\"\"\"",
        ]
        if not struct.fields:
            lines.append("    pass")
        else:
            for field in struct.fields:
                py_type = self._get_py_type(field)
                doc_str = f" # {field.doc}" if field.doc else ""
                lines.append(f"    {field.name}: Optional[{py_type}] = None{doc_str}")
        
        lines.append("")
        lines.append("    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)")
        lines.append("    @classmethod")
        lines.append(f"    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)")
        return "\n".join(lines)

    def _generate_packet_def(self, pkt: PacketDef) -> str:
        doc = pkt.doc if pkt.doc else pkt.name
        lines = [
            f"class Msg_{pkt.name}(msgspec.Struct, omit_defaults=True, array_like=True):",
            f"    \"\"\"{doc}\"\"\"",
            f"    ID = Cmd_{pkt.name}",
        ]
        for field in pkt.fields:
            py_type = self._get_py_type(field)
            doc_str = f" # {field.doc}" if field.doc else ""
            lines.append(f"    {field.name}: Optional[{py_type}] = None{doc_str}")

        lines.append("")
        lines.append("    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)")
        lines.append("    @classmethod")
        lines.append(f"    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)")
        lines.append("    def GetID(self) -> int: return self.ID")
        
        # --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        lines.append("    def BuildTCP(self, ErrorCode: int = 0) -> bytes:")
        lines.append(f"        return Pack(self.ID, self.Encode(), error_code=ErrorCode, version={self.protocol.version})")
        lines.append("    def BuildUDP(self, Sender: int) -> bytes:")
        lines.append(f"        return Pack(self.ID, self.Encode(), session_id=Sender, version={self.protocol.version})")
        
        return "\n".join(lines)

    def _get_py_type(self, field: FieldDef) -> str:
        base_type = field.element_type
        if base_type in self.protocol.structs:
            base_type = f"Msg_{base_type}"
        else:
            type_def = self.protocol.get_type(base_type)
            if type_def:
                base_type = type_def.python
        for _ in range(field.array_dimensions):
            base_type = f"List[{base_type}]"
        return base_type
