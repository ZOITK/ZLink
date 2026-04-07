# Go 코드 생성기
from pathlib import Path
from ..models import ProtocolDef, StructDef, FieldDef, PacketDef, ErrorDef

class GoGenerator:
    def __init__(self, protocol: ProtocolDef):
        self.protocol = protocol

    def render(self) -> str:
        """렌더링된 Go 코드를 문자열로 반환"""
        return self._generate_protocol_module()

    def generate(self, output_dir: str) -> None:
        protocol_code = self.render()
        output_path = Path(output_dir) / "go" / "protocol.go"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(protocol_code)
        print(f"✓ Go 프로토콜 생성 (ZPP 규격): {output_path}")

    def _generate_protocol_module(self) -> str:
        # 헤더 사이즈 미리 계산 (상수 정의에서 사용됨)
        tcp_hdr = self.protocol.headers.get("tcp")
        udp_hdr = self.protocol.headers.get("udp")
        tcp_size = sum(self.protocol.get_type(f.type_name).size for f in tcp_hdr.fields) if tcp_hdr else 16
        udp_size = sum(self.protocol.get_type(f.type_name).size for f in udp_hdr.fields) if udp_hdr else 20

        sections = []
        
        # 1. 패키지 및 임포트
        sections.append(f"""// Package protocol - 자동 생성된 프로토콜
// 버전: {self.protocol.version}
// 자동 생성됨 (zlink-protocol-gen)

package protocol

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"github.com/vmihailenco/msgpack/v5"
)""")

        # 2. --- 변수 및 상수 ---
        const_lines = [
            "// =========================================================================",
            "// --- 변수 및 상수 ---",
            "// =========================================================================",
            f"const CurrentVersion = {self.protocol.version}",
            f"const HeaderSize = {tcp_size}",
            f"const HeaderUdpSize = {udp_size}",
            "",
            "type ErrorCode uint32",
            "",
            "// Error Codes",
            "const ("
        ]
        for err in sorted(self.protocol.errors, key=lambda x: x.get_id()):
            const_lines.append(f"\tErr_{err.name} ErrorCode = {err.get_id()} // {err.doc}")
        const_lines.append(")")
        const_lines.append("")
        const_lines.append("// Packet IDs (Cmd_)")
        const_lines.append("const (")
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            const_lines.append(f"\tCmd_{pkt.name} uint32 = {pkt.get_id()} // {pkt.doc}")
        const_lines.append(")")
        sections.append("\n".join(const_lines))

        # 3. --- 구조체 선언 ---
        struct_decl_lines = [
            "// =========================================================================",
            "// --- 구조체 선언 ---",
            "// ========================================================================="
        ]
        for struct in sorted(self.protocol.structs.values(), key=lambda x: x.name):
            struct_decl_lines.append(self._generate_struct_decl(struct))
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            struct_decl_lines.append(self._generate_packet_decl(pkt))
        sections.append("\n".join(struct_decl_lines))

        # 4. --- 공통 인터페이스 ---
        sections.append("""// =========================================================================
// --- 공통 인터페이스 ---
// =========================================================================

// ISession - 엔진 세션 기능을 추상화한 인터페이스 (비즈니스 로직용)
type ISession interface {
	SendRaw(data []byte) error
	Close()
}

// Packet - 모든 패킷 구조체가 구현하는 인터페이스
type Packet interface {
	GetID() uint32
}""")

        # 5. --- 중앙 집중형 디스패처 (Binder) ---

        dispatch_lines = [
            "// =========================================================================",
            "// --- 중앙 집중형 디스패처 (Registration) ---",
            "// =========================================================================",
            "",
            "// Register - 엔진 서버에 프로토콜 파서(최초 1회)와 비즈니스 콜백을 등록합니다.",
            "// 여러 번 호출하여 다중 리스너(Multi-listener)를 구성할 수 있습니다.",
            "func Register(srv any, callback func(ISession, any)) {",
            "\ttype engine interface {",
            "\t\tSetUnmarshaler(func(uint32, []byte) (any, error))",
            "\t\tSetHeaderSize(int, int)",
            "\t\tAddRecvCallback(func(any, any))",
            "\t}",
            "",
            "\tif s, ok := srv.(engine); ok {",
            f"\t\ts.SetHeaderSize(HeaderSize, HeaderUdpSize)",
            "\t\t// 파싱 로직은 최초 1회만 등록됨 (엔진 내부에서 처리)",
            "\t\ts.SetUnmarshaler(_Unmarshal)",
            "\t\t// 콜백 리스트에 추가",
            "\t\ts.AddRecvCallback(func(sess any, msg any) {",
            "\t\t\tcallback(sess.(ISession), msg)",
            "\t\t})",
            "\t}",
            "}",
        ]
        
        dispatch_lines.append("")
        dispatch_lines.append("// _Unmarshal - 커맨드 ID에 따라 바이트 데이터를 해당 구조체로 자동 파싱 (비공개)")
        dispatch_lines.append("func _Unmarshal(cmd uint32, body []byte) (any, error) {")
        dispatch_lines.append("\tswitch cmd {")
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            dispatch_lines.append(f"\tcase Cmd_{pkt.name}:")
            dispatch_lines.append(f"\t\tmsg := &Msg_{pkt.name}{{}}")
            dispatch_lines.append(f"\t\tif err := msg.Decode(body); err != nil {{ return nil, err }}")
            dispatch_lines.append("\t\treturn msg, nil")
        dispatch_lines.append("\t}")
        dispatch_lines.append("\treturn nil, fmt.Errorf(\"unknown command: %d\", cmd)")
        dispatch_lines.append("}")
        sections.append("\n".join(dispatch_lines))

        # 6. --- 시스템 헤더 (정의 기반 동적 생성) ---
        sections.append("// =========================================================================\n"
                        "// --- 시스템 헤더 (정의 기반 동적 생성) ---\n"
                        "// =========================================================================\n")
        
        for h_name, h_def in self.protocol.headers.items():
            struct_name = f"Sys_PackHeader{h_name.upper()}"
            if h_name.lower() == "tcp": struct_name = "Sys_PackHeader" # TCP는 기본 이름 유지
            
            lines = [f"type {struct_name} struct {{"]
            for field in h_def.fields:
                go_type = self._get_go_type(field)
                lines.append(f"\t{field.name} {go_type}")
            lines.append("}")
            
            lines.append(f"func (h *{struct_name}) Encode() []byte {{")
            lines.append("\tbuf := new(bytes.Buffer)")
            lines.append("\tbinary.Write(buf, binary.LittleEndian, h)")
            lines.append("\treturn buf.Bytes()")
            lines.append("}")
            
            lines.append(f"func (h *{struct_name}) Decode(data []byte) error {{")
            lines.append("\treturn binary.Read(bytes.NewReader(data), binary.LittleEndian, h)")
            lines.append("}")
            sections.append("\n".join(lines))

        # 7. --- 구조체 관련 함수 ---
        struct_method_lines = [
            "// =========================================================================",
            "// --- 구조체 관련 함수 (인코딩/디코딩/빌드) ---",
            "// ========================================================================="
        ]
        for struct in sorted(self.protocol.structs.values(), key=lambda x: x.name):
            struct_method_lines.append(self._generate_method_pair(f"Msg_{struct.name}"))
        for pkt in sorted(self.protocol.packets, key=lambda x: x.get_id()):
            struct_method_lines.append(self._generate_method_pair(f"Msg_{pkt.name}"))
            struct_method_lines.append(f"func (p *Msg_{pkt.name}) GetID() uint32 {{ return Cmd_{pkt.name} }}")
            struct_method_lines.append(f"func (p *Msg_{pkt.name}) BuildTCP(errCode ErrorCode) []byte {{")
            struct_method_lines.append("\tbody, _ := p.Encode()")
            struct_method_lines.append("\thdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}")
            struct_method_lines.append("\treturn append(hdr.Encode(), body...)")
            struct_method_lines.append("}")
            struct_method_lines.append(f"func (p *Msg_{pkt.name}) BuildUDP(sender uint32) []byte {{")
            struct_method_lines.append("\tbody, _ := p.Encode()")
            struct_method_lines.append("\thdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}")
            struct_method_lines.append("\treturn append(hdr.Encode(), body...)")
            struct_method_lines.append("}")
        sections.append("\n".join(struct_method_lines))

        return "\n\n".join(sections)

    def _generate_struct_decl(self, struct: StructDef) -> str:
        lines = []
        if struct.doc: lines.append(f"// Msg_{struct.name} - {struct.doc}")
        lines.append(f"type Msg_{struct.name} struct {{")
        lines.append(f'\t_msgpack struct{{}} `msgpack:",as_array"` // 데이터 압축 전송용')
        for field in struct.fields:
            go_type = self._get_go_type(field)
            comment = f" // {field.doc}" if field.doc else ""
            lines.append(f'\t{field.name} {go_type} `msgpack:"{field.name}"`{comment}')
        lines.append("}")
        return "\n".join(lines)

    def _generate_packet_decl(self, pkt: PacketDef) -> str:
        lines = []
        if pkt.doc: lines.append(f"// Msg_{pkt.name} - {pkt.doc}")
        lines.append(f"type Msg_{pkt.name} struct {{")
        lines.append(f'\t_msgpack struct{{}} `msgpack:",as_array"` // 데이터 압축 전송용')
        for field in pkt.fields:
            go_type = self._get_go_type(field)
            comment = f" // {field.doc}" if field.doc else ""
            lines.append(f'\t{field.name} {go_type} `msgpack:"{field.name}"`{comment}')
        lines.append("}")
        return "\n".join(lines)

    def _get_go_type(self, field: FieldDef) -> str:
        base_type = field.element_type
        if base_type in self.protocol.structs: base_type = f"*Msg_{base_type}"
        else:
            type_def = self.protocol.get_type(base_type)
            if type_def: base_type = type_def.go
        return ("[]" * field.array_dimensions) + base_type

    def _generate_method_pair(self, name: str) -> str:
        return f"""func (r *{name}) Encode() ([]byte, error) {{
	return msgpack.Marshal(r)
}}

func (r *{name}) Decode(data []byte) error {{
	return msgpack.Unmarshal(data, r)
}}"""
