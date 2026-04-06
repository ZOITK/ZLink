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
        lines = []

        # 파일 헤더
        lines.append(f"""// 자동 생성된 프로토콜
// 버전: {self.protocol.version}
// 자동 생성됨 (zoit-protocol-gen)
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using MessagePack;

namespace Zoit
{{
    /// <summary>
    /// 프로토콜 통합 관리 및 중앙 집중형 디스패처
    /// </summary>
    public static class Protocol
    {{
        /// <summary>프로토콜 현재 버전</summary>
        public const uint CurrentVersion = {self.protocol.version};

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

        /// <summary>엔진 서버에 프로토콜 파서와 비즈니스 콜백을 등록합니다. (Go/Python 동일)</summary>
        public static void Register(object engine, Action<object, object> callback)
        {
            // 리플렉션을 사용하여 엔진의 메서드 호출 (Duck Typing 방식)
            var type = engine.GetType();
            var setUnmarshaler = type.GetMethod("SetUnmarshaler");
            var addRecvCallback = type.GetMethod("AddRecvCallback");

            if (setUnmarshaler != null && addRecvCallback != null)
            {
                setUnmarshaler.Invoke(engine, new object[] { new Func<uint, byte[], object>(_Unmarshal) });
                addRecvCallback.Invoke(engine, new object[] { callback });
            }
        }

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

        private static byte[] Combine(byte[] a, byte[] b)
        {
            if (b == null || b.Length == 0) return a;
            var result = new byte[a.Length + b.Length];
            Buffer.BlockCopy(a, 0, result, 0, a.Length);
            Buffer.BlockCopy(b, 0, result, a.Length, b.Length);
            return result;
        }
    }

    // =========================================================================
    // --- 시스템 헤더 ---
    // =========================================================================

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct Sys_PackHeader
    {
        public uint Version;
        public uint Command;
        public uint Length;
        public uint Error;

        public byte[] Encode()
        {
            var buf = new byte[16];
            BitConverter.TryWriteBytes(buf.AsSpan(0),  Version);
            BitConverter.TryWriteBytes(buf.AsSpan(4),  Command);
            BitConverter.TryWriteBytes(buf.AsSpan(8),  Length);
            BitConverter.TryWriteBytes(buf.AsSpan(12), Error);
            return buf;
        }

        public static Sys_PackHeader Decode(byte[] data)
        {
            return new Sys_PackHeader
            {
                Version = BitConverter.ToUInt32(data, 0),
                Command = BitConverter.ToUInt32(data, 4),
                Length  = BitConverter.ToUInt32(data, 8),
                Error   = BitConverter.ToUInt32(data, 12)
            };
        }
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct Sys_PackHeaderUDP
    {
        public uint Version;
        public uint Command;
        public uint Length;
        public uint Sender;
        public uint Error;

        public byte[] Encode()
        {
            var buf = new byte[20];
            BitConverter.TryWriteBytes(buf.AsSpan(0),  Version);
            BitConverter.TryWriteBytes(buf.AsSpan(4),  Command);
            BitConverter.TryWriteBytes(buf.AsSpan(8),  Length);
            BitConverter.TryWriteBytes(buf.AsSpan(12), Sender);
            BitConverter.TryWriteBytes(buf.AsSpan(16), Error);
            return buf;
        }

        public static Sys_PackHeaderUDP Decode(byte[] data)
        {
            return new Sys_PackHeaderUDP
            {
                Version = BitConverter.ToUInt32(data, 0),
                Command = BitConverter.ToUInt32(data, 4),
                Length  = BitConverter.ToUInt32(data, 8),
                Sender  = BitConverter.ToUInt32(data, 12),
                Error   = BitConverter.ToUInt32(data, 16)
            };
        }
    }

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

        lines.append("} // namespace Zoit")

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
        lines.append("            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };")
        lines.append("            var result = new byte[16 + body.Length];")
        lines.append("            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);")
        lines.append("            Buffer.BlockCopy(body, 0, result, 16, body.Length);")
        lines.append("            return result;")
        lines.append("        }")
        lines.append("")
        lines.append("        public byte[] BuildUDP(uint sender)")
        lines.append("        {")
        lines.append("            var body = Encode();")
        lines.append("            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };")
        lines.append("            var result = new byte[20 + body.Length];")
        lines.append("            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);")
        lines.append("            Buffer.BlockCopy(body, 0, result, 20, body.Length);")
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
