// 자동 생성된 프로토콜
// 버전: 1
// 자동 생성됨 (zlink-protocol-gen)
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using MessagePack;

namespace Zlink
{
    /// <summary>
    /// 프로토콜 통합 관리 및 중앙 집중형 디스패처
    /// </summary>
    public static class Protocol
    {
        /// <summary>프로토콜 현재 버전</summary>
        public const uint CurrentVersion = 1;

        /// <summary>TCP 헤더 크기</summary>
        public const int HeaderSize = 16;
        /// <summary>UDP 헤더 크기</summary>
        public const int HeaderUdpSize = 20;

        // =====================================================================
        // --- 에러 코드 (Err_) ---
        // =====================================================================

        /// <summary>정상</summary>
        public const uint Err_None = 0;
        /// <summary>잘못된 값</summary>
        public const uint Err_InvalidValue = 1;
        /// <summary>인증 필요</summary>
        public const uint Err_Unauthorized = 2;
        /// <summary>서버 오류</summary>
        public const uint Err_Server = 3;

        // =====================================================================
        // --- 커맨드 ID (Cmd_) ---
        // =====================================================================

        /// <summary>TCP Heartbeat / TCP 하트비트</summary>
        public const uint Cmd_SystemTCPHeartBitReq = 11110001;
        /// <summary>TCP Heartbeat / TCP 하트비트</summary>
        public const uint Cmd_SystemTCPHeartBitRes = 11120001;
        /// <summary>Login / 로그인</summary>
        public const uint Cmd_AuthLoginReq = 12110001;
        /// <summary>Login / 로그인</summary>
        public const uint Cmd_AuthLoginRes = 12120001;
        /// <summary>Send Message / 메시지 전송</summary>
        public const uint Cmd_MessageSendReq = 13110001;
        /// <summary>Send Message / 메시지 전송</summary>
        public const uint Cmd_MessageSendRes = 13120001;
        /// <summary>Receive Message / 메시지 수신</summary>
        public const uint Cmd_MessageReceiveNotify = 13130002;

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
            var setHeaderInfo = type.GetMethod("SetHeaderInfo");

            if (setUnmarshaler != null && addRecvCallback != null)
            {
                setUnmarshaler.Invoke(engine, new object[] { new Func<uint, byte[], object>(_Unmarshal) });
                addRecvCallback.Invoke(engine, new object[] { callback });
            }

            if (setHeaderInfo != null)
            {
                // 헤더 정보 설정 (TCP 헤더 크기 및 디코더 호출)
                setHeaderInfo.Invoke(engine, new object[] { HeaderSize, new Func<byte[], object>(Sys_PackHeader.Decode) });
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
                case Cmd_MessageSendReq: return Msg_MessageSendReq.Decode(body);
                case Cmd_MessageSendRes: return Msg_MessageSendRes.Decode(body);
                case Cmd_MessageReceiveNotify: return Msg_MessageReceiveNotify.Decode(body);
                default: return null;
            }
        }
    }

    // =========================================================================
    // --- 시스템 헤더 (정의 기반 동적 생성) ---
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
            var buf = new byte[Protocol.HeaderSize];
            BitConverter.TryWriteBytes(buf.AsSpan(0), Version);
            BitConverter.TryWriteBytes(buf.AsSpan(4), Command);
            BitConverter.TryWriteBytes(buf.AsSpan(8), Length);
            BitConverter.TryWriteBytes(buf.AsSpan(12), Error);
            return buf;
        }

        public static Sys_PackHeader Decode(byte[] data)
        {
            if (data == null || data.Length < Protocol.HeaderSize) return default;
            return new Sys_PackHeader
            {
                Version = BitConverter.ToUInt32(data, 0),
                Command = BitConverter.ToUInt32(data, 4),
                Length = BitConverter.ToUInt32(data, 8),
                Error = BitConverter.ToUInt32(data, 12),
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
            var buf = new byte[Protocol.HeaderUdpSize];
            BitConverter.TryWriteBytes(buf.AsSpan(0), Version);
            BitConverter.TryWriteBytes(buf.AsSpan(4), Command);
            BitConverter.TryWriteBytes(buf.AsSpan(8), Length);
            BitConverter.TryWriteBytes(buf.AsSpan(12), Sender);
            BitConverter.TryWriteBytes(buf.AsSpan(16), Error);
            return buf;
        }

        public static Sys_PackHeaderUDP Decode(byte[] data)
        {
            if (data == null || data.Length < Protocol.HeaderUdpSize) return default;
            return new Sys_PackHeaderUDP
            {
                Version = BitConverter.ToUInt32(data, 0),
                Command = BitConverter.ToUInt32(data, 4),
                Length = BitConverter.ToUInt32(data, 8),
                Sender = BitConverter.ToUInt32(data, 12),
                Error = BitConverter.ToUInt32(data, 16),
            };
        }
    }


    // =========================================================================
    // --- 데이터 구조체 및 패킷 정의 ---
    // =========================================================================

    /// <summary>TCP Heartbeat / TCP 하트비트</summary>
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
            var result = new byte[Protocol.HeaderSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderSize, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[Protocol.HeaderUdpSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderUdpSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderUdpSize, body.Length);
            return result;
        }
    }

    /// <summary>TCP Heartbeat / TCP 하트비트</summary>
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
            var result = new byte[Protocol.HeaderSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderSize, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[Protocol.HeaderUdpSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderUdpSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderUdpSize, body.Length);
            return result;
        }
    }

    /// <summary>Login / 로그인</summary>
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
            var result = new byte[Protocol.HeaderSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderSize, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[Protocol.HeaderUdpSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderUdpSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderUdpSize, body.Length);
            return result;
        }
    }

    /// <summary>Login / 로그인</summary>
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
            var result = new byte[Protocol.HeaderSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderSize, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[Protocol.HeaderUdpSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderUdpSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderUdpSize, body.Length);
            return result;
        }
    }

    /// <summary>Send Message / 메시지 전송</summary>
    [MessagePackObject]
    public class Msg_MessageSendReq
    {
        [Key(0)] public string Message { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_MessageSendReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_MessageSendReq>(data);
        public uint GetID() => Protocol.Cmd_MessageSendReq;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[Protocol.HeaderSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderSize, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[Protocol.HeaderUdpSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderUdpSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderUdpSize, body.Length);
            return result;
        }
    }

    /// <summary>Send Message / 메시지 전송</summary>
    [MessagePackObject]
    public class Msg_MessageSendRes
    {
        [Key(0)] public uint Result { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_MessageSendRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_MessageSendRes>(data);
        public uint GetID() => Protocol.Cmd_MessageSendRes;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[Protocol.HeaderSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderSize, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[Protocol.HeaderUdpSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderUdpSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderUdpSize, body.Length);
            return result;
        }
    }

    /// <summary>Receive Message / 메시지 수신</summary>
    [MessagePackObject]
    public class Msg_MessageReceiveNotify
    {
        [Key(0)] public uint PlayerID { get; set; }
        [Key(1)] public string Nickname { get; set; }
        [Key(2)] public string Message { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_MessageReceiveNotify Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_MessageReceiveNotify>(data);
        public uint GetID() => Protocol.Cmd_MessageReceiveNotify;

        public byte[] BuildTCP(uint errorCode = 0)
        {
            var body = Encode();
            var hdr = new Sys_PackHeader { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Error = errorCode };
            var result = new byte[Protocol.HeaderSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderSize, body.Length);
            return result;
        }

        public byte[] BuildUDP(uint sender)
        {
            var body = Encode();
            var hdr = new Sys_PackHeaderUDP { Version = Protocol.CurrentVersion, Command = GetID(), Length = (uint)body.Length, Sender = sender, Error = 0 };
            var result = new byte[Protocol.HeaderUdpSize + body.Length];
            Buffer.BlockCopy(hdr.Encode(), 0, result, 0, Protocol.HeaderUdpSize);
            Buffer.BlockCopy(body, 0, result, Protocol.HeaderUdpSize, body.Length);
            return result;
        }
    }

} // namespace Zlink