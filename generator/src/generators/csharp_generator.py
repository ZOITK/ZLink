# C# 코드 생성기 - v13.0 단일 Protocol.cs 출력
import datetime
from pathlib import Path
from ..models import ProtocolDef, StructDef, FieldDef, PacketDef

class CSharpGenerator:
    def __init__(self, protocol: ProtocolDef):
        self.protocol = protocol

    def render(self) -> str:
        """렌더링된 C# 코드를 문자열로 반환"""
        return self._generate_protocol_file()

    def generate(self, output_dir: str) -> None:
        """단일 Protocol.cs 파일로 생성"""
        # 출력 경로 강제: sdk/client/unity/zlink/protocol
        base_path = Path(output_dir) / "unity/zlink/protocol"
        base_path.mkdir(parents=True, exist_ok=True)

        code = self.render()
        with open(base_path / "Protocol.cs", "w", encoding="utf-8") as f:
            f.write(code)

        print(f"✓ C# 프로토콜 생성 완료 (Protocol.cs)")

    def _generate_protocol_file(self) -> str:
        """Protocol.cs 전체 내용 생성 (ZLink 24B 표준 규격)"""
        lines = []
        now_str = datetime.datetime.now().strftime("%Y-%m-%d : %H:%M:%S")
        
        lines.append(f"""// 자동 생성된 프로토콜
// 버전: {self.protocol.version}
// [ {now_str} ] 자동 생성됨 (zlink-protocol-gen)
using System;
using System.Collections.Generic;
using MessagePack;
using Zlink.Network; // SDK 엔진 참조

namespace Zlink
{{
    public static class Protocol
    {{
        public const uint CurrentVersion = {self.protocol.version};

        // --- 에러 코드 (Err_) ---
""")
        for e in sorted(self.protocol.errors, key=lambda x: x.index):
            lines.append(f"        public const uint Err_{e.name} = {e.index};")

        lines.append("\n        // --- 커맨드 ID (Cmd_) ---")
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            lines.append(f"        public const uint Cmd_{pkt.name} = {pkt.get_id()};")

        lines.append(f"""
        /// <summary>엔진 서버에 프로토콜 파서를와 비즈니스 콜백을 등록합니다.</summary>
        public static void Register(object engine, Action<object, object> callback)
        {{
            var type = engine.GetType();
            var setProtocol = type.GetMethod("SetProtocol");
            var addRecvCallback = type.GetMethod("AddRecvCallback");

            if (setProtocol != null)
            {{
                setProtocol.Invoke(engine, new object[] {{
                    new Func<uint, byte[], object>((cmd, body) => _Unmarshal(cmd, body)),
                    new Func<object, bool, uint, byte[]>((msg, isUdp, sessionId) => Pack(msg, isUdp, sessionId))
                }});
            }}
            addRecvCallback?.Invoke(engine, new object[] {{ callback }});
        }}

        public static byte[] Pack(object msg, bool isUdp, uint sessionId = 0)
        {{
            var type = msg.GetType();
            var method = isUdp ? type.GetMethod("BuildUDP") : type.GetMethod("BuildTCP");
            if (method == null) return null;

            // UDP 전송시 sessionId를 함께 전달하여 서버가 세션을 매칭할 수 있도록 함
            var args = isUdp ? new object[] {{ sessionId }} : new object[] {{ (uint)0 }};
            return (byte[])method.Invoke(msg, args);
        }}

        private static object _Unmarshal(uint command, byte[] body)
        {{
            switch (command)
            {{
""")
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            lines.append(f"                case Cmd_{pkt.name}: return Msg_{pkt.name}.Decode(body);")

        lines.append("""                default: return null;
            }
        }
    }

    // [ZLink 24B 표준 규격 데이터 레이어]

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
        lines.append("        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---")
        lines.append("        public byte[] BuildTCP(uint errorCode = 0)")
        lines.append("        {")
        lines.append("            return _TcpClient.Pack(GetID(), Encode(), 0, errorCode);")
        lines.append("        }")
        lines.append("")
        lines.append("        public byte[] BuildUDP(uint sender)")
        lines.append("        {")
        lines.append("            return _TcpClient.Pack(GetID(), Encode(), sender, 0);")
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
