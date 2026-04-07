# 자동 생성된 프로토콜
# 버전: 1
# 자동 생성됨 (zlink-protocol-gen)

import struct
import msgspec
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Any, Union, Dict, Type, Callable

# =============================================================================
# --- 변수 및 상수 ---
# =============================================================================
CURRENT_VERSION = 1  # 프로토콜 현재 버전
HEADER_SIZE = 16      # TCP 헤더 크기
HEADER_UDP_SIZE = 20  # UDP 헤더 크기

# --- 에러 코드 (Err_) ---
Err_None = 0  # 정상
Err_InvalidValue = 1  # 잘못된 값
Err_Unauthorized = 2  # 인증 필요
Err_Server = 3  # 서버 오류

# --- 커맨드 ID (Cmd_) ---
Cmd_SystemTCPHeartBitReq = 11110001  # TCP Heartbeat / TCP 하트비트
Cmd_SystemTCPHeartBitRes = 11120001  # TCP Heartbeat / TCP 하트비트
Cmd_AuthLoginReq = 12110001  # Login / 로그인
Cmd_AuthLoginRes = 12120001  # Login / 로그인
Cmd_MessageSendReq = 13110001  # Send Message / 메시지 전송
Cmd_MessageSendRes = 13120001  # Send Message / 메시지 전송
Cmd_MessageReceiveNotify = 13130002  # Receive Message / 메시지 수신

# =============================================================================
# --- 중앙 집중형 디스패처 (Registration) ---
# =============================================================================

def Register(Engine: Any, Callback: Callable[[Any, Any], Any]):
    """엔진 서버에 프로토콜 파서와 비즈니스 콜백을 등록합니다. (Go와 동일)"""
    if hasattr(Engine, 'SetUnmarshaler') and hasattr(Engine, 'AddRecvCallback'):
        Engine.SetUnmarshaler(_Unmarshal)
        Engine.AddRecvCallback(Callback)
    
    if hasattr(Engine, 'SetHeaderInfo'):
        Engine.SetHeaderInfo(HEADER_SIZE, PackHeader.Decode)

def _Unmarshal(CmdID: int, Body: bytes) -> Optional[Any]:
    """커맨드 ID에 따라 데이터를 해당 클래스로 자동 파싱 (비공개)"""
    Cls = PacketRegistry.GetPacketClass(CmdID)
    if not Cls: return None
    try:
        return Cls.Decode(Body)
    except:
        return None

class PacketRegistry:
    """커맨드 ID와 패킷 클래스를 매핑하는 레지스트리"""
    _Registry: Dict[int, Type] = {}

    @classmethod
    def GetPacketClass(cls, CmdID: int) -> Optional[Type]:
        return cls._Registry.get(CmdID)

# =============================================================================
# --- 패킷 빌더 및 공통 코덱 ---
# =============================================================================

def Encode(Obj: Any) -> bytes: return msgspec.msgpack.encode(Obj)
def Decode(Cls: Any, Data: bytes) -> Any: return msgspec.msgpack.decode(Data, type=Cls)

# =============================================================================
# --- 패킷 헤더 (정의 기반 동적 생성) ---
# =============================================================================
@dataclass
class PackHeader:
    """TCP 패킷 헤더"""
    Version: int = 0
    Command: int = 0
    Length: int = 0
    Error: int = 0
    def Encode(self) -> bytes: return struct.pack("<IIII", self.Version, self.Command, self.Length, self.Error)
    @classmethod
    def Decode(cls, Data: bytes):
        if len(Data) < struct.calcsize("<IIII"): return None
        vals = struct.unpack("<IIII", Data[:struct.calcsize("<IIII")])
        return cls(*vals)

@dataclass
class PackHeaderUDP:
    """UDP 패킷 헤더"""
    Version: int = 0
    Command: int = 0
    Length: int = 0
    Sender: int = 0
    Error: int = 0
    def Encode(self) -> bytes: return struct.pack("<IIIII", self.Version, self.Command, self.Length, self.Sender, self.Error)
    @classmethod
    def Decode(cls, Data: bytes):
        if len(Data) < struct.calcsize("<IIIII"): return None
        vals = struct.unpack("<IIIII", Data[:struct.calcsize("<IIIII")])
        return cls(*vals)


# =============================================================================
# --- 데이터 구조체 및 패킷 정의 ---
# =============================================================================
class Msg_SystemTCPHeartBitReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """TCP Heartbeat / TCP 하트비트"""
    ID = Cmd_SystemTCPHeartBitReq
    ServerTime: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        Body = self.Encode()
        Hdr = PackHeader(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Error=ErrorCode)
        return Hdr.Encode() + Body
    def BuildUDP(self, Sender: int) -> bytes:
        Body = self.Encode()
        Hdr = PackHeaderUDP(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Sender=Sender, Error=0)
        return Hdr.Encode() + Body

class Msg_SystemTCPHeartBitRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """TCP Heartbeat / TCP 하트비트"""
    ID = Cmd_SystemTCPHeartBitRes
    ServerTime: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        Body = self.Encode()
        Hdr = PackHeader(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Error=ErrorCode)
        return Hdr.Encode() + Body
    def BuildUDP(self, Sender: int) -> bytes:
        Body = self.Encode()
        Hdr = PackHeaderUDP(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Sender=Sender, Error=0)
        return Hdr.Encode() + Body

class Msg_AuthLoginReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """Login / 로그인"""
    ID = Cmd_AuthLoginReq
    Nickname: Optional[str] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        Body = self.Encode()
        Hdr = PackHeader(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Error=ErrorCode)
        return Hdr.Encode() + Body
    def BuildUDP(self, Sender: int) -> bytes:
        Body = self.Encode()
        Hdr = PackHeaderUDP(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Sender=Sender, Error=0)
        return Hdr.Encode() + Body

class Msg_AuthLoginRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """Login / 로그인"""
    ID = Cmd_AuthLoginRes
    PlayerID: Optional[int] = None
    Result: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        Body = self.Encode()
        Hdr = PackHeader(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Error=ErrorCode)
        return Hdr.Encode() + Body
    def BuildUDP(self, Sender: int) -> bytes:
        Body = self.Encode()
        Hdr = PackHeaderUDP(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Sender=Sender, Error=0)
        return Hdr.Encode() + Body

class Msg_MessageSendReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """Send Message / 메시지 전송"""
    ID = Cmd_MessageSendReq
    Message: Optional[str] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        Body = self.Encode()
        Hdr = PackHeader(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Error=ErrorCode)
        return Hdr.Encode() + Body
    def BuildUDP(self, Sender: int) -> bytes:
        Body = self.Encode()
        Hdr = PackHeaderUDP(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Sender=Sender, Error=0)
        return Hdr.Encode() + Body

class Msg_MessageSendRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """Send Message / 메시지 전송"""
    ID = Cmd_MessageSendRes
    Result: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        Body = self.Encode()
        Hdr = PackHeader(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Error=ErrorCode)
        return Hdr.Encode() + Body
    def BuildUDP(self, Sender: int) -> bytes:
        Body = self.Encode()
        Hdr = PackHeaderUDP(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Sender=Sender, Error=0)
        return Hdr.Encode() + Body

class Msg_MessageReceiveNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """Receive Message / 메시지 수신"""
    ID = Cmd_MessageReceiveNotify
    PlayerID: Optional[int] = None
    Nickname: Optional[str] = None
    Message: Optional[str] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        Body = self.Encode()
        Hdr = PackHeader(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Error=ErrorCode)
        return Hdr.Encode() + Body
    def BuildUDP(self, Sender: int) -> bytes:
        Body = self.Encode()
        Hdr = PackHeaderUDP(Version=CURRENT_VERSION, Command=self.ID, Length=len(Body), Sender=Sender, Error=0)
        return Hdr.Encode() + Body

# --- 패킷 레지스트리 등록 ---
PacketRegistry._Registry[Cmd_SystemTCPHeartBitReq] = Msg_SystemTCPHeartBitReq
PacketRegistry._Registry[Cmd_SystemTCPHeartBitRes] = Msg_SystemTCPHeartBitRes
PacketRegistry._Registry[Cmd_AuthLoginReq] = Msg_AuthLoginReq
PacketRegistry._Registry[Cmd_AuthLoginRes] = Msg_AuthLoginRes
PacketRegistry._Registry[Cmd_MessageSendReq] = Msg_MessageSendReq
PacketRegistry._Registry[Cmd_MessageSendRes] = Msg_MessageSendRes
PacketRegistry._Registry[Cmd_MessageReceiveNotify] = Msg_MessageReceiveNotify
