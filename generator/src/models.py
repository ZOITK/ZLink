from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

@dataclass
class TypeDef:
    name: str
    go: str
    python: str
    csharp: str
    size: Any

# 글로벌 표준 타입 정의
DEFAULT_TYPES = {
    "int32":   TypeDef("int32",   "int32",   "int",   "int",    4),
    "uint8":   TypeDef("uint8",   "uint8",   "int",   "byte",   1),
    "uint16":  TypeDef("uint16",  "uint16",  "int",   "ushort", 2),
    "uint32":  TypeDef("uint32",  "uint32",  "int",   "uint",   4),
    "int64":   TypeDef("int64",   "int64",   "int",   "long",   8),
    "float32": TypeDef("float32", "float32", "float", "float",  4),
    "float64": TypeDef("float64", "float64", "float", "double", 8),
    "string":  TypeDef("string",  "string",  "str",   "string", "variable"),
    "bool":    TypeDef("bool",    "bool",    "bool",  "bool",   1),
}

@dataclass
class FieldDef:
    name: str
    type_name: str
    doc: str = ""
    desc: str = ""
    is_array: bool = field(init=False)
    array_dimensions: int = field(init=False, default=0)
    element_type: str = field(init=False)

    def __post_init__(self):
        self.is_array = False
        self.array_dimensions = 0
        current_type = self.type_name
        while current_type.startswith("array(") and current_type.endswith(")"):
            self.is_array = True
            self.array_dimensions += 1
            current_type = current_type[6:-1]
        self.element_type = current_type

@dataclass
class StructDef:
    name: str
    fields: List[FieldDef]
    doc: str = ""
    desc: str = ""

@dataclass
class PacketDef:
    name: str
    kind_id: int
    category_id: int
    proto_id: int
    type_id: int
    index: int
    fields: List[FieldDef] = field(default_factory=list)
    doc: str = ""
    desc: str = ""

    def get_id(self) -> int:
        return (self.kind_id * 10**7) + (self.category_id * 10**6) + \
               (self.proto_id * 10**5) + (self.type_id * 10**4) + self.index

@dataclass
class ErrorDef:
    name: str
    kind_id: int
    category_id: int
    index: int
    doc: str = ""
    desc: str = ""

    def get_id(self) -> int:
        return (self.kind_id * 10**7) + (self.category_id * 10**6) + self.index

@dataclass
class ProtocolDef:
    version: int
    types: Dict[str, TypeDef]
    structs: Dict[str, StructDef]
    packets: List[PacketDef]
    errors: List[ErrorDef]
    constants: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def get_type(self, type_name: str) -> Optional[TypeDef]:
        return self.types.get(type_name)

    def get_struct(self, struct_name: str) -> Optional[StructDef]:
        return self.structs.get(struct_name)

    def is_basic_type(self, type_name: str) -> bool:
        return type_name in self.types

    def is_struct_type(self, type_name: str) -> bool:
        return type_name in self.structs
