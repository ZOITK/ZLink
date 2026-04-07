from typing import List, Tuple
from .models import ProtocolDef

def validate_protocol(protocol: ProtocolDef) -> Tuple[bool, List[str]]:
    errors = []
    for struct_name, struct in protocol.structs.items():
        for field in struct.fields:
            if not field.type_name:
                errors.append(f"{struct_name}.{field.name}: 타입 미정의")
            elif field.is_array:
                element_type = field.element_type
                if not (protocol.is_basic_type(element_type) or protocol.is_struct_type(element_type)):
                    errors.append(f"{struct_name}.{field.name}: 배열 요소 타입 '{element_type}' 미정의")
            else:
                if not (protocol.is_basic_type(field.type_name) or protocol.is_struct_type(field.type_name)):
                    errors.append(f"{struct_name}.{field.name}: 타입 '{field.type_name}' 미정의")

    return len(errors) == 0, errors
