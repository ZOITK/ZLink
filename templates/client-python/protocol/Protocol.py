# 자동 생성된 프로토콜
# 버전: 1
# 자동 생성됨 (zoit-protocol-gen)

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
Err_NotFound = 3  # 찾을 수 없음
Err_Server = 4  # 서버 오류

# --- 커맨드 ID (Cmd_) ---
Cmd_SystemTCPHeartBitReq = 11110001  # TCP 하트비트
Cmd_SystemTCPHeartBitRes = 11120001  # TCP 하트비트
Cmd_AuthLoginReq = 12110001  # 로그인
Cmd_AuthLoginRes = 12120001  # 로그인
Cmd_RoomSearchReq = 13110001  # 방 검색
Cmd_RoomCreateReq = 13110002  # 방 생성
Cmd_RoomJoinReq = 13110003  # 방 입장
Cmd_RoomSearchRes = 13120001  # 방 검색
Cmd_RoomCreateRes = 13120002  # 방 생성
Cmd_RoomJoinRes = 13120003  # 방 입장
Cmd_RoomPlayerJoinNotify = 13130004  # 플레이어 입장 알림
Cmd_RoomGameStartNotify = 13130005  # 게임 시작 알림
Cmd_GameGuessReq = 14110001  # 숫자 맞추기
Cmd_GameWinReq = 14110003  # 게임 승리
Cmd_GameChatReq = 14110005  # 채팅 메시지 전송
Cmd_GameGuessRes = 14120001  # 숫자 맞추기
Cmd_GameWinRes = 14120003  # 게임 승리
Cmd_GameChatRes = 14120005  # 채팅 메시지 전송
Cmd_GameGuessNotify = 14130002  # 상대 숫자 맞추기 알림
Cmd_GameWinNotify = 14130004  # 게임 종료 알림
Cmd_GameChatNotify = 14130006  # 채팅 메시지 수신

# =============================================================================
# --- 중앙 집중형 디스패처 (Registration) ---
# =============================================================================

def Register(Engine: Any, Callback: Callable[[Any, Any], Any]):
    """엔진 서버에 프로토콜 파서와 비즈니스 콜백을 등록합니다. (Go와 동일)"""
    # 엔진의 인터페이스 확인 (Duck Typing)
    if hasattr(Engine, 'SetUnmarshaler') and hasattr(Engine, 'AddRecvCallback'):
        Engine.SetUnmarshaler(_Unmarshal)
        Engine.AddRecvCallback(Callback)

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
    _Registry: Dict[int, Type] = {
        Cmd_SystemTCPHeartBitReq: Msg_SystemTCPHeartBitReq,
        Cmd_SystemTCPHeartBitRes: Msg_SystemTCPHeartBitRes,
        Cmd_AuthLoginReq: Msg_AuthLoginReq,
        Cmd_AuthLoginRes: Msg_AuthLoginRes,
        Cmd_RoomSearchReq: Msg_RoomSearchReq,
        Cmd_RoomCreateReq: Msg_RoomCreateReq,
        Cmd_RoomJoinReq: Msg_RoomJoinReq,
        Cmd_RoomSearchRes: Msg_RoomSearchRes,
        Cmd_RoomCreateRes: Msg_RoomCreateRes,
        Cmd_RoomJoinRes: Msg_RoomJoinRes,
        Cmd_RoomPlayerJoinNotify: Msg_RoomPlayerJoinNotify,
        Cmd_RoomGameStartNotify: Msg_RoomGameStartNotify,
        Cmd_GameGuessReq: Msg_GameGuessReq,
        Cmd_GameWinReq: Msg_GameWinReq,
        Cmd_GameChatReq: Msg_GameChatReq,
        Cmd_GameGuessRes: Msg_GameGuessRes,
        Cmd_GameWinRes: Msg_GameWinRes,
        Cmd_GameChatRes: Msg_GameChatRes,
        Cmd_GameGuessNotify: Msg_GameGuessNotify,
        Cmd_GameWinNotify: Msg_GameWinNotify,
        Cmd_GameChatNotify: Msg_GameChatNotify,
    }

    @classmethod
    def GetPacketClass(cls, CmdID: int) -> Optional[Type]:
        return cls._Registry.get(CmdID)

# =============================================================================
# --- 패킷 빌더 및 공통 코덱 ---
# =============================================================================

def Encode(Obj: Any) -> bytes: return msgspec.msgpack.encode(Obj)
def Decode(Cls: Any, Data: bytes) -> Any: return msgspec.msgpack.decode(Data, type=Cls)

# =============================================================================
# --- 패킷 헤더 ---
# =============================================================================

@dataclass
class PackHeader:
    """TCP 패킷 헤더 (16 bytes)"""
    Version: int = CURRENT_VERSION
    Command: int = 0
    Length: int = 0
    Error: int = 0
    def Encode(self) -> bytes: return struct.pack("<IIII", self.Version, self.Command, self.Length, self.Error)
    @classmethod
    def Decode(cls, Data: bytes):
        if len(Data) < 16: return None
        v, c, l, e = struct.unpack("<IIII", Data[:16])
        return cls(v, c, l, e)

@dataclass
class PackHeaderUDP:
    """UDP 패킷 헤더 (20 bytes)"""
    Version: int = CURRENT_VERSION
    Command: int = 0
    Length: int = 0
    Sender: int = 0
    Error: int = 0
    def Encode(self) -> bytes: return struct.pack("<IIIII", self.Version, self.Command, self.Length, self.Sender, self.Error)
    @classmethod
    def Decode(cls, Data: bytes):
        if len(Data) < 20: return None
        v, c, l, s, e = struct.unpack("<IIIII", Data[:20])
        return cls(v, c, l, s, e)

# =============================================================================
# --- 데이터 구조체 및 패킷 정의 ---
# =============================================================================
class Msg_RoomInfo(msgspec.Struct, omit_defaults=True, forbid_unknown_fields=False):
    """방 정보"""
    RoomID: Optional[int] = None
    RoomName: Optional[str] = None
    HostPlayerID: Optional[int] = None
    HostNickname: Optional[str] = None
    PlayerCount: Optional[int] = None
    Status: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)

class Msg_SystemTCPHeartBitReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """TCP 하트비트"""
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
    """TCP 하트비트"""
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
    """로그인"""
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
    """로그인"""
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

class Msg_RoomSearchReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """방 검색"""
    ID = Cmd_RoomSearchReq

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

class Msg_RoomCreateReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """방 생성"""
    ID = Cmd_RoomCreateReq
    RoomName: Optional[str] = None

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

class Msg_RoomJoinReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """방 입장"""
    ID = Cmd_RoomJoinReq
    RoomID: Optional[int] = None

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

class Msg_RoomSearchRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """방 검색"""
    ID = Cmd_RoomSearchRes
    Rooms: Optional[List["RoomInfo"]] = None
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

class Msg_RoomCreateRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """방 생성"""
    ID = Cmd_RoomCreateRes
    RoomID: Optional[int] = None
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

class Msg_RoomJoinRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """방 입장"""
    ID = Cmd_RoomJoinRes
    RoomID: Optional[int] = None
    OpponentPlayerID: Optional[int] = None
    OpponentNickname: Optional[str] = None
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

class Msg_RoomPlayerJoinNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """플레이어 입장 알림"""
    ID = Cmd_RoomPlayerJoinNotify
    PlayerID: Optional[int] = None
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

class Msg_RoomGameStartNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """게임 시작 알림"""
    ID = Cmd_RoomGameStartNotify
    TargetNumber: Optional[int] = None
    MaxNumber: Optional[int] = None

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

class Msg_GameGuessReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """숫자 맞추기"""
    ID = Cmd_GameGuessReq
    GuessNumber: Optional[int] = None

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

class Msg_GameWinReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """게임 승리"""
    ID = Cmd_GameWinReq
    GuessNumber: Optional[int] = None

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

class Msg_GameChatReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """채팅 메시지 전송"""
    ID = Cmd_GameChatReq
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

class Msg_GameGuessRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """숫자 맞추기"""
    ID = Cmd_GameGuessRes
    Result: Optional[int] = None
    Hint: Optional[int] = None

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

class Msg_GameWinRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """게임 승리"""
    ID = Cmd_GameWinRes
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

class Msg_GameChatRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """채팅 메시지 전송"""
    ID = Cmd_GameChatRes
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

class Msg_GameGuessNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """상대 숫자 맞추기 알림"""
    ID = Cmd_GameGuessNotify
    PlayerID: Optional[int] = None
    Nickname: Optional[str] = None
    GuessNumber: Optional[int] = None
    Hint: Optional[int] = None

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

class Msg_GameWinNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """게임 종료 알림"""
    ID = Cmd_GameWinNotify
    WinnerPlayerID: Optional[int] = None
    WinnerNickname: Optional[str] = None
    CorrectNumber: Optional[int] = None
    TryCount: Optional[int] = None

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

class Msg_GameChatNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """채팅 메시지 수신"""
    ID = Cmd_GameChatNotify
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