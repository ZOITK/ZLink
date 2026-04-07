# Python 코드 생성기
from pathlib import Path
from ..models import ProtocolDef, StructDef, FieldDef, PacketDef, ErrorDef

class PythonGenerator:
    def __init__(self, protocol: ProtocolDef):
        self.protocol = protocol

    def render(self) -> str:
        """렌더링된 Python 코드를 문자열로 반환"""
        return self._generate_protocol_module()

    def generate(self, output_dir: str) -> None:
        """output/python/protocol.py에 생성 (ZPP 규격 준수)"""
        protocol_code = self.render()
        output_path = Path(output_dir) / "python" / "protocol.py"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(protocol_code)
        print(f"✓ Python 프로토콜 생성 (ZPP 규격): {output_path}")

    def _generate_protocol_module(self) -> str:
        header = f"""# 자동 생성된 프로토콜
# 버전: {self.protocol.version}
# 자동 생성됨 (zlink-protocol-gen)

import struct
import msgspec
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Any, Union, Dict, Type, Callable

# =============================================================================
# --- 변수 및 상수 ---
# =============================================================================
CURRENT_VERSION = {self.protocol.version}  # 프로토콜 현재 버전
HEADER_SIZE = 16      # TCP 헤더 크기
HEADER_UDP_SIZE = 20  # UDP 헤더 크기
"""
        # 에러 코드 추가
        header += "\n# --- 에러 코드 (Err_) ---\n"
        for err in sorted(self.protocol.errors, key=lambda x: x.get_id()):
            comment = f"  # {err.doc}" if err.doc else ""
            header += f"Err_{err.name} = {err.get_id()}{comment}\n"
        
        header += "\n# --- 커맨드 ID (Cmd_) ---\n"
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            comment = f"  # {pkt.doc}" if pkt.doc else ""
            header += f"Cmd_{pkt.name} = {pkt.get_id()}{comment}\n"

        header += f"""
# =============================================================================
# --- 중앙 집중형 디스패처 (Registration) ---
# =============================================================================

def Register(Engine: Any, Callback: Callable[[Any, Any], Any]):
    \"\"\"엔진 서버에 프로토콜 파서와 비즈니스 콜백을 등록합니다. (Go와 동일)\"\"\"
    # 엔진의 인터페이스 확인 (Duck Typing)
    if hasattr(Engine, 'SetUnmarshaler') and hasattr(Engine, 'AddRecvCallback'):
        Engine.SetUnmarshaler(_Unmarshal)
        Engine.AddRecvCallback(Callback)

def _Unmarshal(CmdID: int, Body: bytes) -> Optional[Any]:
    \"\"\"커맨드 ID에 따라 데이터를 해당 클래스로 자동 파싱 (비공개)\"\"\"
    Cls = PacketRegistry.GetPacketClass(CmdID)
    if not Cls: return None
    try:
        return Cls.Decode(Body)
    except:
        return None

class PacketRegistry:
    \"\"\"커맨드 ID와 패킷 클래스를 매핑하는 레지스트리\"\"\"
    _Registry: Dict[int, Type] = {{
"""
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            header += f"        Cmd_{pkt.name}: Msg_{pkt.name},\n"

        header += """    }

    @classmethod
    def GetPacketClass(cls, CmdID: int) -> Optional[Type]:
        return cls._Registry.get(CmdID)

# =============================================================================
# --- 패킷 빌더 및 공통 코덱 ---
# =============================================================================

def Encode(Obj: Any) -> bytes: return msgspec.msgpack.encode(Obj)
def Decode(Cls: Any, Data: bytes) -> Any: return msgspec.msgpack.decode(Data, type=Cls)

# =============================================================================
# --- 패킷 헤더 ---
# =============================================================================

@dataclass
class PackHeader:
    \"\"\"TCP 패킷 헤더 (16 bytes)\"\"\"
    Version: int = CURRENT_VERSION
    Command: int = 0
    Length: int = 0
    Error: int = 0
    def Encode(self) -> bytes: return struct.pack("<IIII", self.Version, self.Command, self.Length, self.Error)
    @classmethod
    def Decode(cls, Data: bytes):
        if len(Data) < 16: return None
        v, c, l, e = struct.unpack("<IIII", Data[:16])
        return cls(v, c, l, e)

@dataclass
class PackHeaderUDP:
    \"\"\"UDP 패킷 헤더 (20 bytes)\"\"\"
    Version: int = CURRENT_VERSION
    Command: int = 0
    Length: int = 0
    Sender: int = 0
    Error: int = 0
    def Encode(self) -> bytes: return struct.pack("<IIIII", self.Version, self.Command, self.Length, self.Sender, self.Error)
    @classmethod
    def Decode(cls, Data: bytes):
        if len(Data) < 20: return None
        v, c, l, s, e = struct.unpack("<IIIII", Data[:20])
        return cls(v, c, l, s, e)

# =============================================================================
# --- 데이터 구조체 및 패킷 정의 ---
# =============================================================================
"""
        body_parts = []
        for struct in sorted(self.protocol.structs.values(), key=lambda x: x.name):
            body_parts.append(self._generate_struct_def(struct))
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            body_parts.append(self._generate_packet_def(pkt))

        header += "\n\n".join(body_parts)
        return header

    def _generate_struct_def(self, struct: StructDef) -> str:
        lines = [f"class Msg_{struct.name}(msgspec.Struct, omit_defaults=True, forbid_unknown_fields=False):"]
        if struct.doc: lines.append(f'    """{struct.doc}"""')
        if not struct.fields: lines.append("    pass")
        else:
            for field in struct.fields:
                py_type = self._get_python_type(field)
                comment = f"  # {field.doc}" if field.doc else ""
                lines.append(f"    {field.name}: Optional[{py_type}] = None{comment}")
        lines.append("")
        lines.append("    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)")
        lines.append("    @classmethod\n    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)")
        return "\n".join(lines)

    def _generate_packet_def(self, pkt: PacketDef) -> str:
        lines = [f"class Msg_{pkt.name}(msgspec.Struct, omit_defaults=True, array_like=True):"]
        if pkt.doc: lines.append(f'    """{pkt.doc}"""')
        lines.append(f"    ID = Cmd_{pkt.name}")
        if not pkt.fields: pass
        else:
            for field in pkt.fields:
                py_type = self._get_python_type(field)
                comment = f"  # {field.doc}" if field.doc else ""
                lines.append(f"    {field.name}: Optional[{py_type}] = None{comment}")
        lines.append("")
        lines.append("    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)")
        lines.append("    @classmethod\n    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)")
        lines.append("    def GetID(self) -> int: return self.ID")
        lines.append("    def BuildTCP(self, ErrorCode: int = 0) -> bytes:")
        lines.append("        Body = self.Encode()\n        Hdr = PackHeader(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Error=ErrorCode)")
        lines.append("        return Hdr.Encode() + Body")
        lines.append("    def BuildUDP(self, Sender: int) -> bytes:")
        lines.append("        Body = self.Encode()\n        Hdr = PackHeaderUDP(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Sender=Sender, Error=0)")
        lines.append("        return Hdr.Encode() + Body")
        return "\n".join(lines)

    def _get_python_type(self, field: FieldDef) -> str:
        base_type = field.element_type
        if base_type in self.protocol.structs: base_type = f'"{base_type}"'
        else:
            type_def = self.protocol.get_type(base_type)
            if type_def: base_type = type_def.python
        res = base_type
        for _ in range(field.array_dimensions): res = f"List[{res}]"
        return res
