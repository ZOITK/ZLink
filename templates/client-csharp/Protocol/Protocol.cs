// 자동 생성된 프로토콜
// 버전: 1000009
// 자동 생성됨 (zoit-protocol-gen)
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using MessagePack;

namespace Zoit
{
    /// <summary>
    /// 프로토콜 통합 관리 및 중앙 집중형 디스패처
    /// </summary>
    public static class Protocol
    {
        /// <summary>프로토콜 현재 버전</summary>
        public const uint CurrentVersion = 1000009;

        // =====================================================================
        // --- 에러 코드 (Err_) ---
        // =====================================================================

        /// <summary>정상</summary>
        public const uint Err_None = 0;
        /// <summary>패킷 파싱 실패 / 값 오류</summary>
        public const uint Err_InvalidValue = 1;
        /// <summary>인증 안 된 요청</summary>
        public const uint Err_Unauthorized = 2;
        /// <summary>서버 내부 오류</summary>
        public const uint Err_Server = 3;

        // =====================================================================
        // --- 커맨드 ID (Cmd_) ---
        // =====================================================================

        /// <summary>TCP 하트비트</summary>
        public const uint Cmd_SystemTCPHeartBitReq = 11110001;
        /// <summary>TCP 하트비트</summary>
        public const uint Cmd_SystemTCPHeartBitRes = 11120001;
        /// <summary>UDP 하트비트</summary>
        public const uint Cmd_SystemUDPHeartBitReq = 11210002;
        /// <summary>UDP 하트비트</summary>
        public const uint Cmd_SystemUDPHeartBitRes = 11220002;
        /// <summary>로그인</summary>
        public const uint Cmd_AuthLoginReq = 12110001;
        /// <summary>맵 동접자 수</summary>
        public const uint Cmd_AuthMapTotalUserCountReq = 12110002;
        /// <summary>로그인</summary>
        public const uint Cmd_AuthLoginRes = 12120001;
        /// <summary>맵 동접자 수</summary>
        public const uint Cmd_AuthMapTotalUserCountRes = 12120002;
        /// <summary>방 목록 조회</summary>
        public const uint Cmd_RoomListReq = 13110001;
        /// <summary>방 생성</summary>
        public const uint Cmd_RoomCreateReq = 13110002;
        /// <summary>방 입장</summary>
        public const uint Cmd_RoomJoinReq = 13110003;
        /// <summary>완주자 기록 목록</summary>
        public const uint Cmd_RoomFinishInfoListReq = 13110007;
        /// <summary>방 목록 조회</summary>
        public const uint Cmd_RoomListRes = 13120001;
        /// <summary>방 생성</summary>
        public const uint Cmd_RoomCreateRes = 13120002;
        /// <summary>방 입장</summary>
        public const uint Cmd_RoomJoinRes = 13120003;
        /// <summary>완주자 기록 목록</summary>
        public const uint Cmd_RoomFinishInfoListRes = 13120007;
        /// <summary>라이더 갱신 알림</summary>
        public const uint Cmd_RoomRiderUpdateNotify = 13130004;
        /// <summary>퇴장 알림</summary>
        public const uint Cmd_RoomClientLeaveNotify = 13130005;
        /// <summary>채팅</summary>
        public const uint Cmd_GameChatReq = 14110001;
        /// <summary>채팅</summary>
        public const uint Cmd_GameChatRes = 14120001;
        /// <summary>채팅 알림</summary>
        public const uint Cmd_GameChatNotify = 14130002;
        /// <summary>위치 동기화</summary>
        public const uint Cmd_GameRiderPosSyncNotify = 14230003;
        /// <summary>관리자 설정</summary>
        public const uint Cmd_AdminAdminSetReq = 15110001;

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

                case Cmd_SystemTCPHeartBitReq: return Msg_SystemTCPHeartBitReq.Decode(body);
                case Cmd_SystemTCPHeartBitRes: return Msg_SystemTCPHeartBitRes.Decode(body);
                case Cmd_SystemUDPHeartBitReq: return Msg_SystemUDPHeartBitReq.Decode(body);
                case Cmd_SystemUDPHeartBitRes: return Msg_SystemUDPHeartBitRes.Decode(body);
                case Cmd_AuthLoginReq: return Msg_AuthLoginReq.Decode(body);
                case Cmd_AuthMapTotalUserCountReq: return Msg_AuthMapTotalUserCountReq.Decode(body);
                case Cmd_AuthLoginRes: return Msg_AuthLoginRes.Decode(body);
                case Cmd_AuthMapTotalUserCountRes: return Msg_AuthMapTotalUserCountRes.Decode(body);
                case Cmd_RoomListReq: return Msg_RoomListReq.Decode(body);
                case Cmd_RoomCreateReq: return Msg_RoomCreateReq.Decode(body);
                case Cmd_RoomJoinReq: return Msg_RoomJoinReq.Decode(body);
                case Cmd_RoomFinishInfoListReq: return Msg_RoomFinishInfoListReq.Decode(body);
                case Cmd_RoomListRes: return Msg_RoomListRes.Decode(body);
                case Cmd_RoomCreateRes: return Msg_RoomCreateRes.Decode(body);
                case Cmd_RoomJoinRes: return Msg_RoomJoinRes.Decode(body);
                case Cmd_RoomFinishInfoListRes: return Msg_RoomFinishInfoListRes.Decode(body);
                case Cmd_RoomRiderUpdateNotify: return Msg_RoomRiderUpdateNotify.Decode(body);
                case Cmd_RoomClientLeaveNotify: return Msg_RoomClientLeaveNotify.Decode(body);
                case Cmd_GameChatReq: return Msg_GameChatReq.Decode(body);
                case Cmd_GameChatRes: return Msg_GameChatRes.Decode(body);
                case Cmd_GameChatNotify: return Msg_GameChatNotify.Decode(body);
                case Cmd_GameRiderPosSyncNotify: return Msg_GameRiderPosSyncNotify.Decode(body);
                case Cmd_AdminAdminSetReq: return Msg_AdminAdminSetReq.Decode(body);
                default: return null;
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

    /// <summary>룸 상세 정보</summary>
    [MessagePackObject]
    public class Msg_RecvRoomInfo
    {
        [Key(0)] public uint RoomIdx { get; set; }
        [Key(1)] public string Title { get; set; }
        [Key(2)] public string MapUid { get; set; }
        [Key(3)] public uint HostUserIdx { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RecvRoomInfo Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RecvRoomInfo>(data);
    }

    /// <summary>방 생성 정보</summary>
    [MessagePackObject]
    public class Msg_RoomCreateInfo
    {
        [Key(0)] public uint RoomMaxUser { get; set; }
        [Key(1)] public uint Lap { get; set; }
        [Key(2)] public string Title { get; set; }
        [Key(3)] public string MapUid { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomCreateInfo Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomCreateInfo>(data);
    }

    /// <summary>완주 기록</summary>
    [MessagePackObject]
    public class Msg_RoomFinishInfo
    {
        [Key(0)] public string LoginID { get; set; }
        [Key(1)] public string Nick { get; set; }
        [Key(2)] public uint RiderIndex { get; set; }
        [Key(3)] public long FinishTime { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomFinishInfo Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomFinishInfo>(data);
    }

    /// <summary>라이더 참여 정보</summary>
    [MessagePackObject]
    public class Msg_RoomJoinInfo
    {
        [Key(0)] public string LoginID { get; set; }
        [Key(1)] public uint UserIdx { get; set; }
        [Key(2)] public string Nick { get; set; }
        [Key(3)] public float Distance { get; set; }
        [Key(4)] public uint RiderIndex { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomJoinInfo Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomJoinInfo>(data);
    }

    /// <summary>방 정보 요약</summary>
    [MessagePackObject]
    public class Msg_RoomListInfo
    {
        [Key(0)] public uint RoomIdx { get; set; }
        [Key(1)] public string Title { get; set; }
        [Key(2)] public uint RoomMaxUser { get; set; }
        [Key(3)] public uint RoomUserCount { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomListInfo Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomListInfo>(data);
    }

    /// <summary>TCP 하트비트</summary>
    [MessagePackObject]
    public class Msg_SystemTCPHeartBitReq
    {
        [Key(0)] public double ServerTime { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_SystemTCPHeartBitReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_SystemTCPHeartBitReq>(data);
        public uint GetID() => Protocol.Cmd_SystemTCPHeartBitReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>TCP 하트비트</summary>
    [MessagePackObject]
    public class Msg_SystemTCPHeartBitRes
    {
        [Key(0)] public double ServerTime { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_SystemTCPHeartBitRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_SystemTCPHeartBitRes>(data);
        public uint GetID() => Protocol.Cmd_SystemTCPHeartBitRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>UDP 하트비트</summary>
    [MessagePackObject]
    public class Msg_SystemUDPHeartBitReq
    {
        [Key(0)] public long Timestamp { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_SystemUDPHeartBitReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_SystemUDPHeartBitReq>(data);
        public uint GetID() => Protocol.Cmd_SystemUDPHeartBitReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>UDP 하트비트</summary>
    [MessagePackObject]
    public class Msg_SystemUDPHeartBitRes
    {
        [Key(0)] public long Timestamp { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_SystemUDPHeartBitRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_SystemUDPHeartBitRes>(data);
        public uint GetID() => Protocol.Cmd_SystemUDPHeartBitRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>로그인</summary>
    [MessagePackObject]
    public class Msg_AuthLoginReq
    {
        [Key(0)] public string LoginID { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_AuthLoginReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_AuthLoginReq>(data);
        public uint GetID() => Protocol.Cmd_AuthLoginReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>맵 동접자 수</summary>
    [MessagePackObject]
    public class Msg_AuthMapTotalUserCountReq
    {
        [Key(0)] public List<string> MapUids { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_AuthMapTotalUserCountReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_AuthMapTotalUserCountReq>(data);
        public uint GetID() => Protocol.Cmd_AuthMapTotalUserCountReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>로그인</summary>
    [MessagePackObject]
    public class Msg_AuthLoginRes
    {
        [Key(0)] public uint UserIdx { get; set; }
        [Key(1)] public long StartTime { get; set; }
        [Key(2)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_AuthLoginRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_AuthLoginRes>(data);
        public uint GetID() => Protocol.Cmd_AuthLoginRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>맵 동접자 수</summary>
    [MessagePackObject]
    public class Msg_AuthMapTotalUserCountRes
    {
        [Key(0)] public List<uint> Counts { get; set; }
        [Key(1)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_AuthMapTotalUserCountRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_AuthMapTotalUserCountRes>(data);
        public uint GetID() => Protocol.Cmd_AuthMapTotalUserCountRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>방 목록 조회</summary>
    [MessagePackObject]
    public class Msg_RoomListReq
    {
        [Key(0)] public string MapUid { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomListReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomListReq>(data);
        public uint GetID() => Protocol.Cmd_RoomListReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>방 생성</summary>
    [MessagePackObject]
    public class Msg_RoomCreateReq
    {
        [Key(0)] public Msg_RoomCreateInfo CreateInfo { get; set; }
        [Key(1)] public List<Msg_RoomJoinInfo> Riders { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomCreateReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomCreateReq>(data);
        public uint GetID() => Protocol.Cmd_RoomCreateReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>방 입장</summary>
    [MessagePackObject]
    public class Msg_RoomJoinReq
    {
        [Key(0)] public uint RoomIdx { get; set; }
        [Key(1)] public List<Msg_RoomJoinInfo> Riders { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomJoinReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomJoinReq>(data);
        public uint GetID() => Protocol.Cmd_RoomJoinReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>완주자 기록 목록</summary>
    [MessagePackObject]
    public class Msg_RoomFinishInfoListReq
    {
        [Key(0)] public uint RoomIdx { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomFinishInfoListReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomFinishInfoListReq>(data);
        public uint GetID() => Protocol.Cmd_RoomFinishInfoListReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>방 목록 조회</summary>
    [MessagePackObject]
    public class Msg_RoomListRes
    {
        [Key(0)] public List<Msg_RoomListInfo> Rooms { get; set; }
        [Key(1)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomListRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomListRes>(data);
        public uint GetID() => Protocol.Cmd_RoomListRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>방 생성</summary>
    [MessagePackObject]
    public class Msg_RoomCreateRes
    {
        [Key(0)] public uint RoomIdx { get; set; }
        [Key(1)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomCreateRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomCreateRes>(data);
        public uint GetID() => Protocol.Cmd_RoomCreateRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>방 입장</summary>
    [MessagePackObject]
    public class Msg_RoomJoinRes
    {
        [Key(0)] public Msg_RecvRoomInfo RoomInfo { get; set; }
        [Key(1)] public uint UserIdx { get; set; }
        [Key(2)] public List<Msg_RoomJoinInfo> OtherRiders { get; set; }
        [Key(3)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomJoinRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomJoinRes>(data);
        public uint GetID() => Protocol.Cmd_RoomJoinRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>완주자 기록 목록</summary>
    [MessagePackObject]
    public class Msg_RoomFinishInfoListRes
    {
        [Key(0)] public List<Msg_RoomFinishInfo> Finishes { get; set; }
        [Key(1)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomFinishInfoListRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomFinishInfoListRes>(data);
        public uint GetID() => Protocol.Cmd_RoomFinishInfoListRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>라이더 갱신 알림</summary>
    [MessagePackObject]
    public class Msg_RoomRiderUpdateNotify
    {
        [Key(0)] public List<Msg_RoomJoinInfo> Users { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomRiderUpdateNotify Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomRiderUpdateNotify>(data);
        public uint GetID() => Protocol.Cmd_RoomRiderUpdateNotify;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>퇴장 알림</summary>
    [MessagePackObject]
    public class Msg_RoomClientLeaveNotify
    {
        [Key(0)] public uint LeaverUserIdx { get; set; }
        [Key(1)] public uint HostUserIdx { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomClientLeaveNotify Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomClientLeaveNotify>(data);
        public uint GetID() => Protocol.Cmd_RoomClientLeaveNotify;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>채팅</summary>
    [MessagePackObject]
    public class Msg_GameChatReq
    {
        [Key(0)] public string Message { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameChatReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameChatReq>(data);
        public uint GetID() => Protocol.Cmd_GameChatReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>채팅</summary>
    [MessagePackObject]
    public class Msg_GameChatRes
    {
        [Key(0)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameChatRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameChatRes>(data);
        public uint GetID() => Protocol.Cmd_GameChatRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>채팅 알림</summary>
    [MessagePackObject]
    public class Msg_GameChatNotify
    {
        [Key(0)] public uint UserIdx { get; set; }
        [Key(1)] public string Message { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameChatNotify Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameChatNotify>(data);
        public uint GetID() => Protocol.Cmd_GameChatNotify;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>위치 동기화</summary>
    [MessagePackObject]
    public class Msg_GameRiderPosSyncNotify
    {
        [Key(0)] public long Timestamp { get; set; }
        [Key(1)] public List<List<float>> Riders { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameRiderPosSyncNotify Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameRiderPosSyncNotify>(data);
        public uint GetID() => Protocol.Cmd_GameRiderPosSyncNotify;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

    /// <summary>관리자 설정</summary>
    [MessagePackObject]
    public class Msg_AdminAdminSetReq
    {
        [Key(0)] public uint Enabled { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_AdminAdminSetReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_AdminAdminSetReq>(data);
        public uint GetID() => Protocol.Cmd_AdminAdminSetReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[16 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 16);
            Buffer.BlockCopy(body, 0, result, 16, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[20 + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, 20);
            Buffer.BlockCopy(body, 0, result, 20, body.Length);
            return result;
        }
    }

} // namespace Zoit