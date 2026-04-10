// 자동 생성된 프로토콜
// 버전: 1
// [ 2026-04-10 : 11:34:35 ] 자동 생성됨 (zlink-protocol-gen)
using System;
using System.Collections.Generic;
using MessagePack;
using Zlink.Network; // SDK 엔진 참조

namespace Zlink
{
    public static class Protocol
    {
        public const uint CurrentVersion = 1;

        // --- 에러 코드 (Err_) ---

        public const uint Err_None = 0;
        public const uint Err_InvalidValue = 1;
        public const uint Err_Unauthorized = 2;
        public const uint Err_Server = 3;

        // --- 커맨드 ID (Cmd_) ---
        public const uint Cmd_SystemTCPHeartBitReq = 11110001;
        public const uint Cmd_SystemUDPHeartBitReq = 11110002;
        public const uint Cmd_SystemTCPHeartBitRes = 11120001;
        public const uint Cmd_SystemUDPHeartBitRes = 11120002;
        public const uint Cmd_AuthLoginReq = 12110001;
        public const uint Cmd_AuthLoginRes = 12120001;
        public const uint Cmd_MessageSendReq = 13110001;
        public const uint Cmd_MessageSendRes = 13120001;
        public const uint Cmd_MessageReceiveNotify = 13130002;

        /// <summary>엔진 서버에 프로토콜 파서를와 비즈니스 콜백을 등록합니다.</summary>
        public static void Register(object engine, Action<object, object> callback)
        {
            var type = engine.GetType();
            var setProtocol = type.GetMethod("SetProtocol");
            var addRecvCallback = type.GetMethod("AddRecvCallback");

            if (setProtocol != null)
            {
                setProtocol.Invoke(engine, new object[] {
                    new Func<uint, byte[], object>((cmd, body) => _Unmarshal(cmd, body)),
                    new Func<object, bool, uint, byte[]>((msg, isUdp, sessionId) => Pack(msg, isUdp, sessionId))
                });
            }
            addRecvCallback?.Invoke(engine, new object[] { callback });
        }

        public static byte[] Pack(object msg, bool isUdp, uint sessionId = 0)
        {
            var type = msg.GetType();
            var method = isUdp ? type.GetMethod("BuildUDP") : type.GetMethod("BuildTCP");
            if (method == null) return null;

            // UDP 전송시 sessionId를 함께 전달하여 서버가 세션을 매칭할 수 있도록 함
            var args = isUdp ? new object[] { sessionId } : new object[] { (uint)0 };
            return (byte[])method.Invoke(msg, args);
        }

        private static object _Unmarshal(uint command, byte[] body)
        {
            switch (command)
            {

                case Cmd_SystemTCPHeartBitReq: return Msg_SystemTCPHeartBitReq.Decode(body);
                case Cmd_SystemUDPHeartBitReq: return Msg_SystemUDPHeartBitReq.Decode(body);
                case Cmd_SystemTCPHeartBitRes: return Msg_SystemTCPHeartBitRes.Decode(body);
                case Cmd_SystemUDPHeartBitRes: return Msg_SystemUDPHeartBitRes.Decode(body);
                case Cmd_AuthLoginReq: return Msg_AuthLoginReq.Decode(body);
                case Cmd_AuthLoginRes: return Msg_AuthLoginRes.Decode(body);
                case Cmd_MessageSendReq: return Msg_MessageSendReq.Decode(body);
                case Cmd_MessageSendRes: return Msg_MessageSendRes.Decode(body);
                case Cmd_MessageReceiveNotify: return Msg_MessageReceiveNotify.Decode(body);
                default: return null;
            }
        }
    }

    // [ZLink 24B 표준 규격 데이터 레이어]


    /// <summary>TCP Heartbeat / TCP 하트비트</summary>
    [MessagePackObject]
    public class Msg_SystemTCPHeartBitReq
    {
        [Key(0)] public long ServerTime { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_SystemTCPHeartBitReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_SystemTCPHeartBitReq>(data);
        public uint GetID() => Protocol.Cmd_SystemTCPHeartBitReq;

        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        public byte[] BuildTCP(uint errorCode = 0)
        {
            return TcpClient.Pack(GetID(), Encode(), 0, errorCode);
        }

        public byte[] BuildUDP(uint sender)
        {
            return TcpClient.Pack(GetID(), Encode(), sender, 0);
        }
    }

    /// <summary>UDP Heartbeat / UDP 하트비트</summary>
    [MessagePackObject]
    public class Msg_SystemUDPHeartBitReq
    {
        [Key(0)] public long Timestamp { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_SystemUDPHeartBitReq Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_SystemUDPHeartBitReq>(data);
        public uint GetID() => Protocol.Cmd_SystemUDPHeartBitReq;

        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        public byte[] BuildTCP(uint errorCode = 0)
        {
            return TcpClient.Pack(GetID(), Encode(), 0, errorCode);
        }

        public byte[] BuildUDP(uint sender)
        {
            return TcpClient.Pack(GetID(), Encode(), sender, 0);
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

        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        public byte[] BuildTCP(uint errorCode = 0)
        {
            return TcpClient.Pack(GetID(), Encode(), 0, errorCode);
        }

        public byte[] BuildUDP(uint sender)
        {
            return TcpClient.Pack(GetID(), Encode(), sender, 0);
        }
    }

    /// <summary>UDP Heartbeat / UDP 하트비트</summary>
    [MessagePackObject]
    public class Msg_SystemUDPHeartBitRes
    {
        [Key(0)] public long Timestamp { get; set; }

        public byte[] Encode() => MessagePackSerializer.Serialize(this);
        public static Msg_SystemUDPHeartBitRes Decode(byte[] data) => MessagePackSerializer.Deserialize<Msg_SystemUDPHeartBitRes>(data);
        public uint GetID() => Protocol.Cmd_SystemUDPHeartBitRes;

        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        public byte[] BuildTCP(uint errorCode = 0)
        {
            return TcpClient.Pack(GetID(), Encode(), 0, errorCode);
        }

        public byte[] BuildUDP(uint sender)
        {
            return TcpClient.Pack(GetID(), Encode(), sender, 0);
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

        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        public byte[] BuildTCP(uint errorCode = 0)
        {
            return TcpClient.Pack(GetID(), Encode(), 0, errorCode);
        }

        public byte[] BuildUDP(uint sender)
        {
            return TcpClient.Pack(GetID(), Encode(), sender, 0);
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

        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        public byte[] BuildTCP(uint errorCode = 0)
        {
            return TcpClient.Pack(GetID(), Encode(), 0, errorCode);
        }

        public byte[] BuildUDP(uint sender)
        {
            return TcpClient.Pack(GetID(), Encode(), sender, 0);
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

        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        public byte[] BuildTCP(uint errorCode = 0)
        {
            return TcpClient.Pack(GetID(), Encode(), 0, errorCode);
        }

        public byte[] BuildUDP(uint sender)
        {
            return TcpClient.Pack(GetID(), Encode(), sender, 0);
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

        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        public byte[] BuildTCP(uint errorCode = 0)
        {
            return TcpClient.Pack(GetID(), Encode(), 0, errorCode);
        }

        public byte[] BuildUDP(uint sender)
        {
            return TcpClient.Pack(GetID(), Encode(), sender, 0);
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

        // --- 핵심 개선: 엔진 SDK의 Pack 함수를 사용하여 조립 (SSOT) ---
        public byte[] BuildTCP(uint errorCode = 0)
        {
            return TcpClient.Pack(GetID(), Encode(), 0, errorCode);
        }

        public byte[] BuildUDP(uint sender)
        {
            return TcpClient.Pack(GetID(), Encode(), sender, 0);
        }
    }

} // namespace Zlink