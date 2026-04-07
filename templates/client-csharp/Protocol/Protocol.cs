// 자동 생성된 프로토콜
// 버전: 1
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
        public const uint CurrentVersion = 1;

        // =====================================================================
        // --- 에러 코드 (Err_) ---
        // =====================================================================

        /// <summary>정상</summary>
        public const uint Err_None = 0;
        /// <summary>잘못된 값</summary>
        public const uint Err_InvalidValue = 1;
        /// <summary>인증 필요</summary>
        public const uint Err_Unauthorized = 2;
        /// <summary>찾을 수 없음</summary>
        public const uint Err_NotFound = 3;
        /// <summary>서버 오류</summary>
        public const uint Err_Server = 4;

        // =====================================================================
        // --- 커맨드 ID (Cmd_) ---
        // =====================================================================

        /// <summary>TCP 하트비트</summary>
        public const uint Cmd_SystemTCPHeartBitReq = 11110001;
        /// <summary>TCP 하트비트</summary>
        public const uint Cmd_SystemTCPHeartBitRes = 11120001;
        /// <summary>로그인</summary>
        public const uint Cmd_AuthLoginReq = 12110001;
        /// <summary>로그인</summary>
        public const uint Cmd_AuthLoginRes = 12120001;
        /// <summary>방 검색</summary>
        public const uint Cmd_RoomSearchReq = 13110001;
        /// <summary>방 생성</summary>
        public const uint Cmd_RoomCreateReq = 13110002;
        /// <summary>방 입장</summary>
        public const uint Cmd_RoomJoinReq = 13110003;
        /// <summary>방 검색</summary>
        public const uint Cmd_RoomSearchRes = 13120001;
        /// <summary>방 생성</summary>
        public const uint Cmd_RoomCreateRes = 13120002;
        /// <summary>방 입장</summary>
        public const uint Cmd_RoomJoinRes = 13120003;
        /// <summary>플레이어 입장 알림</summary>
        public const uint Cmd_RoomPlayerJoinNotify = 13130004;
        /// <summary>게임 시작 알림</summary>
        public const uint Cmd_RoomGameStartNotify = 13130005;
        /// <summary>숫자 맞추기</summary>
        public const uint Cmd_GameGuessReq = 14110001;
        /// <summary>게임 승리</summary>
        public const uint Cmd_GameWinReq = 14110003;
        /// <summary>채팅 메시지 전송</summary>
        public const uint Cmd_GameChatReq = 14110005;
        /// <summary>숫자 맞추기</summary>
        public const uint Cmd_GameGuessRes = 14120001;
        /// <summary>게임 승리</summary>
        public const uint Cmd_GameWinRes = 14120003;
        /// <summary>채팅 메시지 전송</summary>
        public const uint Cmd_GameChatRes = 14120005;
        /// <summary>상대 숫자 맞추기 알림</summary>
        public const uint Cmd_GameGuessNotify = 14130002;
        /// <summary>게임 종료 알림</summary>
        public const uint Cmd_GameWinNotify = 14130004;
        /// <summary>채팅 메시지 수신</summary>
        public const uint Cmd_GameChatNotify = 14130006;

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
                case Cmd_AuthLoginReq: return Msg_AuthLoginReq.Decode(body);
                case Cmd_AuthLoginRes: return Msg_AuthLoginRes.Decode(body);
                case Cmd_RoomSearchReq: return Msg_RoomSearchReq.Decode(body);
                case Cmd_RoomCreateReq: return Msg_RoomCreateReq.Decode(body);
                case Cmd_RoomJoinReq: return Msg_RoomJoinReq.Decode(body);
                case Cmd_RoomSearchRes: return Msg_RoomSearchRes.Decode(body);
                case Cmd_RoomCreateRes: return Msg_RoomCreateRes.Decode(body);
                case Cmd_RoomJoinRes: return Msg_RoomJoinRes.Decode(body);
                case Cmd_RoomPlayerJoinNotify: return Msg_RoomPlayerJoinNotify.Decode(body);
                case Cmd_RoomGameStartNotify: return Msg_RoomGameStartNotify.Decode(body);
                case Cmd_GameGuessReq: return Msg_GameGuessReq.Decode(body);
                case Cmd_GameWinReq: return Msg_GameWinReq.Decode(body);
                case Cmd_GameChatReq: return Msg_GameChatReq.Decode(body);
                case Cmd_GameGuessRes: return Msg_GameGuessRes.Decode(body);
                case Cmd_GameWinRes: return Msg_GameWinRes.Decode(body);
                case Cmd_GameChatRes: return Msg_GameChatRes.Decode(body);
                case Cmd_GameGuessNotify: return Msg_GameGuessNotify.Decode(body);
                case Cmd_GameWinNotify: return Msg_GameWinNotify.Decode(body);
                case Cmd_GameChatNotify: return Msg_GameChatNotify.Decode(body);
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

    /// <summary>방 정보</summary>
    [MessagePackObject]
    public class Msg_RoomInfo
    {
        [Key(0)] public uint RoomID { get; set; }
        [Key(1)] public string RoomName { get; set; }
        [Key(2)] public uint HostPlayerID { get; set; }
        [Key(3)] public string HostNickname { get; set; }
        [Key(4)] public uint PlayerCount { get; set; }
        [Key(5)] public uint Status { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomInfo Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomInfo>(data);
    }

    /// <summary>TCP 하트비트</summary>
    [MessagePackObject]
    public class Msg_SystemTCPHeartBitReq
    {
        [Key(0)] public long ServerTime { get; set; }

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
        [Key(0)] public long ServerTime { get; set; }

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

    /// <summary>로그인</summary>
    [MessagePackObject]
    public class Msg_AuthLoginReq
    {
        [Key(0)] public string Nickname { get; set; }

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

    /// <summary>로그인</summary>
    [MessagePackObject]
    public class Msg_AuthLoginRes
    {
        [Key(0)] public uint PlayerID { get; set; }
        [Key(1)] public uint Result { get; set; }

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

    /// <summary>방 검색</summary>
    [MessagePackObject]
    public class Msg_RoomSearchReq
    {

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomSearchReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomSearchReq>(data);
        public uint GetID() => Protocol.Cmd_RoomSearchReq;

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
        [Key(0)] public string RoomName { get; set; }

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
        [Key(0)] public uint RoomID { get; set; }

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

    /// <summary>방 검색</summary>
    [MessagePackObject]
    public class Msg_RoomSearchRes
    {
        [Key(0)] public List<Msg_RoomInfo> Rooms { get; set; }
        [Key(1)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomSearchRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomSearchRes>(data);
        public uint GetID() => Protocol.Cmd_RoomSearchRes;

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
        [Key(0)] public uint RoomID { get; set; }
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
        [Key(0)] public uint RoomID { get; set; }
        [Key(1)] public uint OpponentPlayerID { get; set; }
        [Key(2)] public string OpponentNickname { get; set; }
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

    /// <summary>플레이어 입장 알림</summary>
    [MessagePackObject]
    public class Msg_RoomPlayerJoinNotify
    {
        [Key(0)] public uint PlayerID { get; set; }
        [Key(1)] public string Nickname { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomPlayerJoinNotify Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomPlayerJoinNotify>(data);
        public uint GetID() => Protocol.Cmd_RoomPlayerJoinNotify;

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

    /// <summary>게임 시작 알림</summary>
    [MessagePackObject]
    public class Msg_RoomGameStartNotify
    {
        [Key(0)] public uint TargetNumber { get; set; }
        [Key(1)] public uint MaxNumber { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_RoomGameStartNotify Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_RoomGameStartNotify>(data);
        public uint GetID() => Protocol.Cmd_RoomGameStartNotify;

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

    /// <summary>숫자 맞추기</summary>
    [MessagePackObject]
    public class Msg_GameGuessReq
    {
        [Key(0)] public uint GuessNumber { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameGuessReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameGuessReq>(data);
        public uint GetID() => Protocol.Cmd_GameGuessReq;

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

    /// <summary>게임 승리</summary>
    [MessagePackObject]
    public class Msg_GameWinReq
    {
        [Key(0)] public uint GuessNumber { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameWinReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameWinReq>(data);
        public uint GetID() => Protocol.Cmd_GameWinReq;

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

    /// <summary>채팅 메시지 전송</summary>
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

    /// <summary>숫자 맞추기</summary>
    [MessagePackObject]
    public class Msg_GameGuessRes
    {
        [Key(0)] public uint Result { get; set; }
        [Key(1)] public uint Hint { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameGuessRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameGuessRes>(data);
        public uint GetID() => Protocol.Cmd_GameGuessRes;

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

    /// <summary>게임 승리</summary>
    [MessagePackObject]
    public class Msg_GameWinRes
    {
        [Key(0)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameWinRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameWinRes>(data);
        public uint GetID() => Protocol.Cmd_GameWinRes;

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

    /// <summary>채팅 메시지 전송</summary>
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

    /// <summary>상대 숫자 맞추기 알림</summary>
    [MessagePackObject]
    public class Msg_GameGuessNotify
    {
        [Key(0)] public uint PlayerID { get; set; }
        [Key(1)] public string Nickname { get; set; }
        [Key(2)] public uint GuessNumber { get; set; }
        [Key(3)] public uint Hint { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameGuessNotify Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameGuessNotify>(data);
        public uint GetID() => Protocol.Cmd_GameGuessNotify;

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

    /// <summary>게임 종료 알림</summary>
    [MessagePackObject]
    public class Msg_GameWinNotify
    {
        [Key(0)] public uint WinnerPlayerID { get; set; }
        [Key(1)] public string WinnerNickname { get; set; }
        [Key(2)] public uint CorrectNumber { get; set; }
        [Key(3)] public uint TryCount { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_GameWinNotify Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_GameWinNotify>(data);
        public uint GetID() => Protocol.Cmd_GameWinNotify;

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

    /// <summary>채팅 메시지 수신</summary>
    [MessagePackObject]
    public class Msg_GameChatNotify
    {
        [Key(0)] public uint PlayerID { get; set; }
        [Key(1)] public string Nickname { get; set; }
        [Key(2)] public string Message { get; set; }

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

} // namespace Zoit