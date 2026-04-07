# C# 코드 생성기 - v13.0 단일 Protocol.cs 출력
from pathlib import Path
from ..models import ProtocolDef, StructDef, FieldDef, PacketDef, ErrorDef

class CSharpGenerator:
    def __init__(self, protocol: ProtocolDef):
        self.protocol = protocol

    def render(self) -> str:
        """렌더링된 C# 코드를 문자열로 반환"""
        return self._generate_protocol_file()

    def generate(self, output_dir: str) -> None:
        """단일 Protocol.cs 파일로 생성"""
        base_path = Path(output_dir) / "csharp"
        base_path.mkdir(parents=True, exist_ok=True)

        code = self.render()
        with open(base_path / "Protocol.cs", "w", encoding="utf-8") as f:
            f.write(code)

        print(f"✓ C# 프로토콜 생성 완료 (Protocol.cs)")

    def _generate_protocol_file(self) -> str:
        """Protocol.cs 전체 내용 생성"""
        # 헤더 사이즈 미리 계산
        tcp_hdr = self.protocol.headers.get("tcp")
        udp_hdr = self.protocol.headers.get("udp")
        tcp_size = sum(self.protocol.get_type(f.type_name).size for f in tcp_hdr.fields) if tcp_hdr else 16
        udp_size = sum(self.protocol.get_type(f.type_name).size for f in udp_hdr.fields) if udp_hdr else 20

        lines = []

        # 파일 헤더
        lines.append(f"""// 자동 생성된 프로토콜
// 버전: {self.protocol.version}
// 자동 생성됨 (zlink-protocol-gen)
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using MessagePack;

namespace Zlink
{{
    /// <summary>
    /// 프로토콜 통합 관리 및 중앙 집중형 디스패처
    /// </summary>
    public static class Protocol
    {{
        /// <summary>프로토콜 현재 버전</summary>
        public const uint CurrentVersion = {self.protocol.version};

        /// <summary>TCP 헤더 크기</summary>
        public const int HeaderSize = {tcp_size};
        /// <summary>UDP 헤더 크기</summary>
        public const int HeaderUdpSize = {udp_size};

        // =====================================================================
        // --- 에러 코드 (Err_) ---
        // =====================================================================
""")

        for e in sorted(self.protocol.errors, key=lambda x: x.index):
            doc = e.doc if e.doc else "에러 코드"
            lines.append(f"        /// <summary>{doc}</summary>")
            lines.append(f"        public const uint Err_{e.name} = {e.index};")

        lines.append("""
        // =====================================================================
        // --- 커맨드 ID (Cmd_) ---
        // =====================================================================
""")

        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            doc = pkt.doc if pkt.doc else "패킷 커맨드"
            lines.append(f"        /// <summary>{doc}</summary>")
            lines.append(f"        public const uint Cmd_{pkt.name} = {pkt.get_id()};")

        lines.append("""
        // =====================================================================
        // --- 중앙 집중형 디스패처 (Registration) ---
        // =====================================================================
        """)

        lines.append(f"""
        /// <summary>엔진 서버에 프로토콜 파서와 비즈니스 콜백을 등록합니다. (Go/Python 동일)</summary>
        public static void Register(object engine, Action<object, object> callback)
        {{
            // 리플렉션을 사용하여 엔진의 메서드 호출 (Duck Typing 방식)
            var type = engine.GetType();
            var setUnmarshaler = type.GetMethod("SetUnmarshaler");
            var addRecvCallback = type.GetMethod("AddRecvCallback");
            var setHeaderInfo = type.GetMethod("SetHeaderInfo");

            if (setUnmarshaler != null && addRecvCallback != null)
            {{
                // 람다식을 사용하여 명시적 델리게이트 생성 (델리게이트 타입 불일치 방지)
                setUnmarshaler.Invoke(engine, new object[] {{ new Func<uint, byte[], object>((cmd, body) => _Unmarshal(cmd, body)) }});
                addRecvCallback.Invoke(engine, new object[] {{ callback }});
            }}

            if (setHeaderInfo != null)
            {{
                // 헤더 정보 설정 (TCP 헤더 크기 및 디코더 호출)
                // 람다식을 사용하여 Sys_PackHeader(Struct)를 object로 박싱하여 전달
                setHeaderInfo.Invoke(engine, new object[] {{ HeaderSize, new Func<byte[], object>(data => Sys_PackHeader.Decode(data)) }});
            }}
        }}""")

        lines.append("""
        private static object _Unmarshal(uint command, byte[] body)
        {
            switch (command)
            {
""")
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            lines.append(f"                case Cmd_{pkt.name}: return Msg_{pkt.name}.Decode(body);")

        lines.append("""                default: return null;
            }
        }
    }

    // =========================================================================
    // --- 시스템 헤더 (정의 기반 동적 생성) ---
    // =========================================================================
""")

        for h_name, h_def in self.protocol.headers.items():
            struct_name = f"Sys_PackHeader{h_name.upper()}"
            if h_name.lower() == "tcp": struct_name = "Sys_PackHeader"

            size_const = "Protocol.HeaderUdpSize" if h_name.lower() == "udp" else "Protocol.HeaderSize"

            lines.append(f"    [StructLayout(LayoutKind.Sequential, Pack = 1)]")
            lines.append(f"    public struct {struct_name}")
            lines.append(f"    {{")
            
            for f in h_def.fields:
                lines.append(f"        public {self._get_cs_type(f)} {f.name};")
            
            lines.append("")
            lines.append(f"        public byte[] Encode()")
            lines.append(f"        {{")
            lines.append(f"            var buf = new byte[{size_const}];")
            offset = 0
            for f in h_def.fields:
                t_def = self.protocol.get_type(f.type_name)
                if t_def:
                    lines.append(f"            BitConverter.TryWriteBytes(buf.AsSpan({offset}), {f.name});")
                    offset += t_def.size
            lines.append(f"            return buf;")
            lines.append(f"        }}")
            
            lines.append("")
            lines.append(f"        public static {struct_name} Decode(byte[] data)")
            lines.append(f"        {{")
            lines.append(f"            if (data == null || data.Length < {size_const}) return default;")
            lines.append(f"            return new {struct_name}")
            lines.append(f"            {{")
            offset = 0
            for f in h_def.fields:
                t_def = self.protocol.get_type(f.type_name)
                if t_def:
                    if t_def.name == "uint8":
                        lines.append(f"                {f.name} = data[{offset}],")
                    else:
                        suffix = t_def.csharp.capitalize()
                        if suffix == "Uint": suffix = "UInt32"
                        if suffix == "Ushort": suffix = "UInt16"
                        if suffix == "Int": suffix = "Int32"
                        lines.append(f"                {f.name} = BitConverter.To{suffix}(data, {offset}),")
                    offset += t_def.size
            lines.append(f"            }};")
            lines.append(f"        }}")
            lines.append(f"    }}")
            lines.append("")

        lines.append("""
    // =========================================================================
    // --- 데이터 구조체 및 패킷 정의 ---
    // =========================================================================
""")

        # Msg_ 공통 구조체
        for s in sorted(self.protocol.structs.values(), key=lambda x: x.name):
            lines.append(self._generate_struct_def(s))
            lines.append("")

        # Msg_ 패킷 구조체
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            lines.append(self._generate_packet_def(pkt))
            lines.append("")

        lines.append("} // namespace Zlink")

        return "\n".join(lines)

    def _generate_struct_def(self, struct: StructDef) -> str:
        doc = struct.doc if struct.doc else struct.name
        lines = [
            f"    /// <summary>{doc}</summary>",
            "    [MessagePackObject]",
            f"    public class Msg_{struct.name}",
            "    {",
            ]
        for i, field in enumerate(struct.fields):
            cs_type = self._get_cs_type(field)
            if field.doc:
                lines.append(f"        /// <summary>{field.doc}</summary>")
            lines.append(f"        [Key({i})] public {cs_type} {field.name} {{ get; set; }}")
        
        lines.append("")
        lines.append("        public byte[] Encode() => MessagePackSerializer.Serialize(this);")
        lines.append(f"        public static Msg_{struct.name} Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_{struct.name}>(data);")
        lines.append("    }")
        return "\n".join(lines)

    def _generate_packet_def(self, pkt: PacketDef) -> str:
        doc = pkt.doc if pkt.doc else pkt.name
        lines = [
            f"    /// <summary>{doc}</summary>",
            "    [MessagePackObject]",
            f"    public class Msg_{pkt.name}",
            "    {",
            ]
        for i, field in enumerate(pkt.fields):
            cs_type = self._get_cs_type(field)
            if field.doc:
                lines.append(f"        /// <summary>{field.doc}</summary>")
            lines.append(f"        [Key({i})] public {cs_type} {field.name} {{ get; set; }}")
        
        lines.append("")
        lines.append("        public byte[] Encode() => MessagePackSerializer.Serialize(this);")
        lines.append(f"        public static Msg_{pkt.name} Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_{pkt.name}>(data);")
        lines.append(f"        public uint GetID() => Protocol.Cmd_{pkt.name};")
        lines.append("")
        lines.append("        public byte[] BuildTCP(uint errorCode = 0)")
        lines.append("        {")
        lines.append("            var body = Encode();")
        # 동적 헤더 생성에 맞춰 필드 할당 (표준 필드가 존재한다고 가정)
        lines.append(f"            var hdr = new Sys_PackHeader {{ Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode }};")
        lines.append(f"            var result = new byte[Protocol.HeaderSize + body.Length];")
        lines.append(f"            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderSize);")
        lines.append(f"            Buffer.BlockCopy(body, 0, result, Protocol.HeaderSize, body.Length);")
        lines.append("            return result;")
        lines.append("        }")
        lines.append("")
        lines.append("        public byte[] BuildUDP(uint sender)")
        lines.append("        {")
        lines.append("            var body = Encode();")
        lines.append(f"            var hdr = new Sys_PackHeaderUDP {{ Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 }};")
        lines.append(f"            var result = new byte[Protocol.HeaderUdpSize + body.Length];")
        lines.append(f"            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderUdpSize);")
        lines.append(f"            Buffer.BlockCopy(body, 0, result, Protocol.HeaderUdpSize, body.Length);")
        lines.append("            return result;")
        lines.append("        }")
        lines.append("    }")
        return "\n".join(lines)

    def _get_cs_type(self, field: FieldDef) -> str:
        base_type = field.element_type
        if base_type in self.protocol.structs:
            base_type = f"Msg_{base_type}"
        else:
            type_def = self.protocol.get_type(base_type)
            if type_def:
                base_type = type_def.csharp
        for _ in range(field.array_dimensions):
            base_type = f"List<{base_type}>"
        return base_type
