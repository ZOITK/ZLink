import struct
from dataclasses import dataclass

@dataclass
class HeaderTCP:
    version: int = 1
    command: int = 0
    length: int = 0
    error: int = 0

    @staticmethod
    def decode(data: bytes):
        # Big-endian, 4 uint32 (16 bytes)
        v, c, l, e = struct.unpack(">IIII", data)
        return HeaderTCP(v, c, l, e)

    def encode(self) -> bytes:
        return struct.pack(">IIII", self.version, self.command, self.length, self.error)

@dataclass
class HeaderUDP:
    version: int = 1
    command: int = 0
    length: int = 0
    sender: int = 0
    error: int = 0

    @staticmethod
    def decode(data: bytes):
        # Big-endian, 5 uint32 (20 bytes)
        v, c, l, s, e = struct.unpack(">IIIII", data)
        return HeaderUDP(v, c, l, s, e)

    def encode(self) -> bytes:
        return struct.pack(">IIIII", self.version, self.command, self.length, self.sender, self.error)
