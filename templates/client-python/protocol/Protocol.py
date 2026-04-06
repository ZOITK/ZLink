# 자동 생성된 프로토콜
# 버전: 1000009
# 자동 생성됨 (zoit-protocol-gen)

import struct
import msgspec
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Any, Union, Dict, Type, Callable

# =============================================================================
# --- 변수 및 상수 ---
# =============================================================================
CURRENT_VERSION = 1000009  # 프로토콜 현재 버전
HEADER_SIZE = 16      # TCP 헤더 크기
HEADER_UDP_SIZE = 20  # UDP 헤더 크기

# --- 에러 코드 (Err_) ---
Err_None = 0  # 정상
Err_InvalidValue = 1  # 패킷 파싱 실패 / 값 오류
Err_Unauthorized = 2  # 인증 안 된 요청
Err_Server = 3  # 서버 내부 오류

# --- 커맨드 ID (Cmd_) ---
Cmd_SystemTCPHeartBitReq = 11110001  # TCP 하트비트
Cmd_SystemTCPHeartBitRes = 11120001  # TCP 하트비트
Cmd_SystemUDPHeartBitReq = 11210002  # UDP 하트비트
Cmd_SystemUDPHeartBitRes = 11220002  # UDP 하트비트
Cmd_AuthLoginReq = 12110001  # 로그인
Cmd_AuthMapTotalUserCountReq = 12110002  # 맵 동접자 수
Cmd_AuthLoginRes = 12120001  # 로그인
Cmd_AuthMapTotalUserCountRes = 12120002  # 맵 동접자 수
Cmd_RoomListReq = 13110001  # 방 목록 조회
Cmd_RoomCreateReq = 13110002  # 방 생성
Cmd_RoomJoinReq = 13110003  # 방 입장
Cmd_RoomFinishInfoListReq = 13110007  # 완주자 기록 목록
Cmd_RoomListRes = 13120001  # 방 목록 조회
Cmd_RoomCreateRes = 13120002  # 방 생성
Cmd_RoomJoinRes = 13120003  # 방 입장
Cmd_RoomFinishInfoListRes = 13120007  # 완주자 기록 목록
Cmd_RoomRiderUpdateNotify = 13130004  # 라이더 갱신 알림
Cmd_RoomClientLeaveNotify = 13130005  # 퇴장 알림
Cmd_GameChatReq = 14110001  # 채팅
Cmd_GameChatRes = 14120001  # 채팅
Cmd_GameChatNotify = 14130002  # 채팅 알림
Cmd_GameRiderPosSyncNotify = 14230003  # 위치 동기화
Cmd_AdminAdminSetReq = 15110001  # 관리자 설정

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
        Cmd_SystemUDPHeartBitReq: Msg_SystemUDPHeartBitReq,
        Cmd_SystemUDPHeartBitRes: Msg_SystemUDPHeartBitRes,
        Cmd_AuthLoginReq: Msg_AuthLoginReq,
        Cmd_AuthMapTotalUserCountReq: Msg_AuthMapTotalUserCountReq,
        Cmd_AuthLoginRes: Msg_AuthLoginRes,
        Cmd_AuthMapTotalUserCountRes: Msg_AuthMapTotalUserCountRes,
        Cmd_RoomListReq: Msg_RoomListReq,
        Cmd_RoomCreateReq: Msg_RoomCreateReq,
        Cmd_RoomJoinReq: Msg_RoomJoinReq,
        Cmd_RoomFinishInfoListReq: Msg_RoomFinishInfoListReq,
        Cmd_RoomListRes: Msg_RoomListRes,
        Cmd_RoomCreateRes: Msg_RoomCreateRes,
        Cmd_RoomJoinRes: Msg_RoomJoinRes,
        Cmd_RoomFinishInfoListRes: Msg_RoomFinishInfoListRes,
        Cmd_RoomRiderUpdateNotify: Msg_RoomRiderUpdateNotify,
        Cmd_RoomClientLeaveNotify: Msg_RoomClientLeaveNotify,
        Cmd_GameChatReq: Msg_GameChatReq,
        Cmd_GameChatRes: Msg_GameChatRes,
        Cmd_GameChatNotify: Msg_GameChatNotify,
        Cmd_GameRiderPosSyncNotify: Msg_GameRiderPosSyncNotify,
        Cmd_AdminAdminSetReq: Msg_AdminAdminSetReq,
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
class Msg_RecvRoomInfo(msgspec.Struct, omit_defaults=True, forbid_unknown_fields=False):
    """룸 상세 정보"""
    RoomIdx: Optional[int] = None
    Title: Optional[str] = None
    MapUid: Optional[str] = None
    HostUserIdx: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)

class Msg_RoomCreateInfo(msgspec.Struct, omit_defaults=True, forbid_unknown_fields=False):
    """방 생성 정보"""
    RoomMaxUser: Optional[int] = None
    Lap: Optional[int] = None
    Title: Optional[str] = None
    MapUid: Optional[str] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)

class Msg_RoomFinishInfo(msgspec.Struct, omit_defaults=True, forbid_unknown_fields=False):
    """완주 기록"""
    LoginID: Optional[str] = None
    Nick: Optional[str] = None
    RiderIndex: Optional[int] = None
    FinishTime: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)

class Msg_RoomJoinInfo(msgspec.Struct, omit_defaults=True, forbid_unknown_fields=False):
    """라이더 참여 정보"""
    LoginID: Optional[str] = None
    UserIdx: Optional[int] = None
    Nick: Optional[str] = None
    Distance: Optional[float] = None
    RiderIndex: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)

class Msg_RoomListInfo(msgspec.Struct, omit_defaults=True, forbid_unknown_fields=False):
    """방 정보 요약"""
    RoomIdx: Optional[int] = None
    Title: Optional[str] = None
    RoomMaxUser: Optional[int] = None
    RoomUserCount: Optional[int] = None

    def Encode(self) -> bytes: return msgspec.msgpack.encode(self)
    @classmethod
    def Decode(cls, Data: bytes): return msgspec.msgpack.decode(Data, type=cls)

class Msg_SystemTCPHeartBitReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """TCP 하트비트"""
    ID = Cmd_SystemTCPHeartBitReq
    ServerTime: Optional[float] = None

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
    ServerTime: Optional[float] = None

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

class Msg_SystemUDPHeartBitReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """UDP 하트비트"""
    ID = Cmd_SystemUDPHeartBitReq
    Timestamp: Optional[int] = None

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

class Msg_SystemUDPHeartBitRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """UDP 하트비트"""
    ID = Cmd_SystemUDPHeartBitRes
    Timestamp: Optional[int] = None

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
    LoginID: Optional[str] = None

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

class Msg_AuthMapTotalUserCountReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """맵 동접자 수"""
    ID = Cmd_AuthMapTotalUserCountReq
    MapUids: Optional[List[str]] = None

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
    UserIdx: Optional[int] = None
    StartTime: Optional[int] = None
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

class Msg_AuthMapTotalUserCountRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """맵 동접자 수"""
    ID = Cmd_AuthMapTotalUserCountRes
    Counts: Optional[List[int]] = None
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

class Msg_RoomListReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """방 목록 조회"""
    ID = Cmd_RoomListReq
    MapUid: Optional[str] = None

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
    CreateInfo: Optional["RoomCreateInfo"] = None
    Riders: Optional[List["RoomJoinInfo"]] = None

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
    RoomIdx: Optional[int] = None
    Riders: Optional[List["RoomJoinInfo"]] = None

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

class Msg_RoomFinishInfoListReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """완주자 기록 목록"""
    ID = Cmd_RoomFinishInfoListReq
    RoomIdx: Optional[int] = None

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

class Msg_RoomListRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """방 목록 조회"""
    ID = Cmd_RoomListRes
    Rooms: Optional[List["RoomListInfo"]] = None
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
    RoomIdx: Optional[int] = None
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
    RoomInfo: Optional["RecvRoomInfo"] = None
    UserIdx: Optional[int] = None
    OtherRiders: Optional[List["RoomJoinInfo"]] = None
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

class Msg_RoomFinishInfoListRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """완주자 기록 목록"""
    ID = Cmd_RoomFinishInfoListRes
    Finishes: Optional[List["RoomFinishInfo"]] = None
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

class Msg_RoomRiderUpdateNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """라이더 갱신 알림"""
    ID = Cmd_RoomRiderUpdateNotify
    Users: Optional[List["RoomJoinInfo"]] = None

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

class Msg_RoomClientLeaveNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """퇴장 알림"""
    ID = Cmd_RoomClientLeaveNotify
    LeaverUserIdx: Optional[int] = None
    HostUserIdx: Optional[int] = None

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
    """채팅"""
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

class Msg_GameChatRes(msgspec.Struct, omit_defaults=True, array_like=True):
    """채팅"""
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

class Msg_GameChatNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """채팅 알림"""
    ID = Cmd_GameChatNotify
    UserIdx: Optional[int] = None
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

class Msg_GameRiderPosSyncNotify(msgspec.Struct, omit_defaults=True, array_like=True):
    """위치 동기화"""
    ID = Cmd_GameRiderPosSyncNotify
    Timestamp: Optional[int] = None
    Riders: Optional[List[List[float]]] = None

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

class Msg_AdminAdminSetReq(msgspec.Struct, omit_defaults=True, array_like=True):
    """관리자 설정"""
    ID = Cmd_AdminAdminSetReq
    Enabled: Optional[int] = None

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