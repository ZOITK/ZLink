# 자동 생성된 프로토콜
# 버전: 1
# [ 2026-04-10 : 16:57:23 ] 자동 생성됨 (zlink-protocol-gen)
import msgspec
import sys
import os
from typing import Optional, List, Dict, Any

# SDK 또는 Example 환경에서 모두 작동하도록 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from zlink.network.tcp_client import Pack  # SDK 엔진 조립 함수 참조

class PacketRegistry:
    _Registry = {}
    @classmethod
    def Unmarshal(cls, cmd: int, data: bytes) -> Any:
        msg_cls = cls._Registry.get(cmd)
        if not msg_cls: return None
        return msg_cls.Decode(data)

def Register(client, callback):
    """엔진 서버 또는 클라이언트에 프로토콜 지식과 비즈니스 콜백을 등록합니다."""
    # 엔진에 마샬러/언마샬러 주입 (Symmetry)
    def packer(msg, use_udp, session_id=0):
        if use_udp:
            return msg.BuildUDP(session_id)
        else:
            return msg.BuildTCP(0)

    client.set_protocol(PacketRegistry.Unmarshal, packer)
    client.add_recv_callback(callback)

# --- 커맨드 ID (Cmd_) ---

Cmd_SystemTCPHeartBitReq = 11110001
Cmd_SystemUDPHeartBitReq = 11110002
Cmd_SystemTCPHeartBitRes = 11120001
Cmd_SystemUDPHeartBitRes = 11120002
Cmd_AuthLoginReq = 12110001
Cmd_AuthLoginRes = 12120001
Cmd_MessageSendReq = 13110001
Cmd_MessageSendRes = 13120001
Cmd_MessageReceiveNotify = 13130002

# --- 에러 코드 (Err_) ---
Err_None = 0
Err_InvalidValue = 1
Err_Unauthorized = 2
Err_Server = 3

class Msg_SystemTCPHeartBitReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """TCP Heartbeat / TCP 하트비트"""
    ID = Cmd_SystemTCPHeartBitReq
    ServerTime: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=0, error_code=ErrorCode, version=1)
    def BuildUDP(self, SessionID: int) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=SessionID, version=1)

class Msg_SystemUDPHeartBitReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """UDP Heartbeat / UDP 하트비트"""
    ID = Cmd_SystemUDPHeartBitReq
    Timestamp: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=0, error_code=ErrorCode, version=1)
    def BuildUDP(self, SessionID: int) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=SessionID, version=1)

class Msg_SystemTCPHeartBitRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """TCP Heartbeat / TCP 하트비트"""
    ID = Cmd_SystemTCPHeartBitRes
    ServerTime: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=0, error_code=ErrorCode, version=1)
    def BuildUDP(self, SessionID: int) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=SessionID, version=1)

class Msg_SystemUDPHeartBitRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """UDP Heartbeat / UDP 하트비트"""
    ID = Cmd_SystemUDPHeartBitRes
    Timestamp: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=0, error_code=ErrorCode, version=1)
    def BuildUDP(self, SessionID: int) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=SessionID, version=1)

class Msg_AuthLoginReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """Login / 로그인"""
    ID = Cmd_AuthLoginReq
    Nickname: Optional[str] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=0, error_code=ErrorCode, version=1)
    def BuildUDP(self, SessionID: int) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=SessionID, version=1)

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
        return Pack(self.ID, self.Encode(), session_id=0, error_code=ErrorCode, version=1)
    def BuildUDP(self, SessionID: int) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=SessionID, version=1)

class Msg_MessageSendReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """Send Message / 메시지 전송"""
    ID = Cmd_MessageSendReq
    Message: Optional[str] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=0, error_code=ErrorCode, version=1)
    def BuildUDP(self, SessionID: int) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=SessionID, version=1)

class Msg_MessageSendRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """Send Message / 메시지 전송"""
    ID = Cmd_MessageSendRes
    Result: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)
    def GetID(self) -> int: return self.ID
    def BuildTCP(self, ErrorCode: int = 0) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=0, error_code=ErrorCode, version=1)
    def BuildUDP(self, SessionID: int) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=SessionID, version=1)

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
        return Pack(self.ID, self.Encode(), session_id=0, error_code=ErrorCode, version=1)
    def BuildUDP(self, SessionID: int) -> bytes:
        return Pack(self.ID, self.Encode(), session_id=SessionID, version=1)

# --- 패킷 레지스트리 등록 ---
PacketRegistry._Registry[Cmd_SystemTCPHeartBitReq] = Msg_SystemTCPHeartBitReq
PacketRegistry._Registry[Cmd_SystemUDPHeartBitReq] = Msg_SystemUDPHeartBitReq
PacketRegistry._Registry[Cmd_SystemTCPHeartBitRes] = Msg_SystemTCPHeartBitRes
PacketRegistry._Registry[Cmd_SystemUDPHeartBitRes] = Msg_SystemUDPHeartBitRes
PacketRegistry._Registry[Cmd_AuthLoginReq] = Msg_AuthLoginReq
PacketRegistry._Registry[Cmd_AuthLoginRes] = Msg_AuthLoginRes
PacketRegistry._Registry[Cmd_MessageSendReq] = Msg_MessageSendReq
PacketRegistry._Registry[Cmd_MessageSendRes] = Msg_MessageSendRes
PacketRegistry._Registry[Cmd_MessageReceiveNotify] = Msg_MessageReceiveNotify