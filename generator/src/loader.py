import yaml
from pathlib import Path
from .models import (
    ProtocolDef, TypeDef, StructDef, FieldDef, PacketDef, ErrorDef, HeaderDef, DEFAULT_TYPES
)

def clean_name(prefix: str, cat_title: str, base_name: str, suffix: str = "") -> str:
    """
    네이밍 중복을 방지하여 순수한 프로토콜 이름을 생성합니다.
    v12.2에서는 cmd, err, proto 네임스페이스를 사용하므로 Cmd/Error 접두어를 제거합니다.
    
    Args:
        prefix (str): 기존의 "Error" 또는 "Cmd" (v12.2에서는 식별용으로만 사용)
        cat_title (str): "Auth", "Room" 등의 카테고리 명칭
        base_name (str): YAML에 정의된 기본 이름
        suffix (str): "Req", "Res", "Notify"와 같은 하위 타입 접미사
        
    Returns:
        str: 정규화된 형태의 순수 명칭 (예: AuthOldVersion, AuthLoginReq)
    """
    # base_name의 앞에 이미 prefix가 있다면 제거 (예: ErrorOldVersion -> OldVersion)
    if base_name.startswith(prefix):
        base_name = base_name[len(prefix):]
    
    # base_name의 뒤에 이미 suffix가 있다면 제거 (예: LoginReq -> Login)
    if suffix and base_name.endswith(suffix):
        base_name = base_name[:-len(suffix)]
        
    # v12.2 설계: 접두어(Cmd/Error)를 제외한 순수 이름 반환
    return f"{cat_title}{base_name}{suffix}"

def parse_field(f_name, f_data):
    """
    YAML 필드 정의를 파싱하여 FieldDef 객체로 변환합니다.
    """
    if isinstance(f_data, str):
        return FieldDef(name=f_name, type_name=f_data)
    return FieldDef(
        name=f_name, 
        type_name=f_data["type"], 
        doc=f_data.get("doc", ""),
        desc=f_data.get("desc", "")
    )

def load_protocol(schema_path: str) -> ProtocolDef:
    """
    YAML 스키마 파일을 로드하여 프로토콜 정의 객체(ProtocolDef)를 생성합니다.
    """
    with open(schema_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    metadata = data.get("metadata", {})
    categories = {name: i+1 for i, name in enumerate(metadata.get("categories", []))}
    protocols  = {name: i+1 for i, name in enumerate(metadata.get("protocols", []))}
    msg_types  = {name: i+1 for i, name in enumerate(metadata.get("types", []))}
    
    KIND_CMD = 1
    KIND_ERR = 2

    version = metadata.get("version", 1000000)
    type_defs = DEFAULT_TYPES.copy()
    
    # 구조체 로드
    structs = {}
    def load_structs(source):
        for name, s in source.items():
            fields = [parse_field(fn, fd) for fn, fd in s.get("fields", {}).items()]
            structs[name] = StructDef(name=name, fields=fields, doc=s.get("doc", ""), desc=s.get("desc", ""))

    load_structs(data.get("common_structs", data.get("structs", {})))

    definitions = data.get("definitions", {})
    for cat_name, cat_def in definitions.items():
        load_structs(cat_def.get("structs", {}))

    # 전역 에러 코드 로드 (global_errors 블록, 제네레이터에서 Err_ 접두사 붙임)
    errors = []
    for err_data in data.get("global_errors", []):
        errors.append(ErrorDef(
            name=err_data["name"],
            kind_id=0, category_id=0, index=err_data["idx"],
            doc=err_data.get("doc", "")
        ))
    packets = []
    for cat_name, cat_def in definitions.items():
        cat_id = categories.get(cat_name)
        if cat_id is None: continue
        cat_title = cat_name.capitalize()

        # 패킷 처리 (카테고리별 errors 블록은 v13.0에서 제거됨)
        for pkt_data in cat_def.get("packets", []):
            name = pkt_data["name"]
            idx = pkt_data["idx"]
            proto_id = protocols.get(pkt_data.get("proto", "tcp"), 1)
            doc = pkt_data.get("doc", "")
            desc = pkt_data.get("desc", "")
            
            if "pair" in pkt_data or "req" in pkt_data or "res" in pkt_data:
                source = pkt_data.get("pair", pkt_data)
                if "req" in source:
                    fields = [parse_field(fn, fd) for fn, fd in source["req"].get("fields", {}).items()]
                    # Request 패킷 이름 생성 (Cmd + Category + Name + Req)
                    pkt_name = clean_name("Cmd", cat_title, name, "Req")
                    packets.append(PacketDef(
                        name=pkt_name, 
                        kind_id=KIND_CMD, category_id=cat_id, proto_id=proto_id, 
                        type_id=msg_types.get("req", 1), index=idx, fields=fields, doc=doc, desc=desc
                    ))
                if "res" in source:
                    fields = [parse_field(fn, fd) for fn, fd in source["res"].get("fields", {}).items()]
                    # Response 패킷 이름 생성 (Cmd + Category + Name + Res)
                    pkt_name = clean_name("Cmd", cat_title, name, "Res")
                    packets.append(PacketDef(
                        name=pkt_name, 
                        kind_id=KIND_CMD, category_id=cat_id, proto_id=proto_id, 
                        type_id=msg_types.get("res", 2), index=idx, fields=fields, doc=doc, desc=desc
                    ))
            else:
                # 단방향 패킷(Notify 등) 필드 파싱
                t_id = msg_types.get(pkt_data.get("type", "notify"), 3)
                t_suffix = "Notify" if t_id == 3 else ""
                
                # Notify 등 단방향 패킷 이름 생성
                pkt_name = clean_name("Cmd", cat_title, name, t_suffix)
                
                fields = [parse_field(fn, fd) for fn, fd in pkt_data.get("fields", {}).items()]
                packets.append(PacketDef(
                    name=pkt_name, 
                    kind_id=KIND_CMD, category_id=cat_id, proto_id=proto_id, 
                    type_id=t_id, index=idx, fields=fields, doc=doc, desc=desc
                ))


    # 헤더 정의 로드
    headers = {}
    header_data = data.get("header", {})
    for h_name, h_def in header_data.items():
        h_fields = [parse_field(fn, fd) for fn, fd in h_def.get("fields", {}).items()]
        headers[h_name] = HeaderDef(name=h_name, fields=h_fields)

    return ProtocolDef(
        version=version, 
        types=type_defs, 
        structs=structs, 
        packets=packets, 
        errors=errors, 
        headers=headers,
        constants=data.get("constants", {})
    )
