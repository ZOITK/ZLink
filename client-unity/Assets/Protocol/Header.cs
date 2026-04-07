using System;
using System.Buffers.Binary;

namespace Zoit.Protocol
{
    /// <summary>
    /// ZPP TCP 헤더 규격 (16 bytes)
    /// [Version(4)][Command(4)][Length(4)][Error(4)]
    /// </summary>
    public struct HeaderTCP
    {
        public uint Version;
        public uint Command;
        public uint Length;
        public uint Error;

        public byte[] Encode()
        {
            var buf = new byte[16];
            BinaryPrimitives.WriteUInt32BigEndian(buf.AsSpan(0), Version);
            BinaryPrimitives.WriteUInt32BigEndian(buf.AsSpan(4), Command);
            BinaryPrimitives.WriteUInt32BigEndian(buf.AsSpan(8), Length);
            BinaryPrimitives.WriteUInt32BigEndian(buf.AsSpan(12), Error);
            return buf;
        }

        public static HeaderTCP Decode(byte[] data)
        {
            return new HeaderTCP
            {
                Version = BinaryPrimitives.ReadUInt32BigEndian(data.AsSpan(0)),
                Command = BinaryPrimitives.ReadUInt32BigEndian(data.AsSpan(4)),
                Length = BinaryPrimitives.ReadUInt32BigEndian(data.AsSpan(8)),
                Error = BinaryPrimitives.ReadUInt32BigEndian(data.AsSpan(12))
            };
        }
    }

    /// <summary>
    /// ZPP UDP 헤더 규격 (20 bytes)
    /// [Version(4)][Command(4)][Length(4)][Sender(4)][Error(4)]
    /// </summary>
    public struct HeaderUDP
    {
        public uint Version;
        public uint Command;
        public uint Length;
        public uint Sender;
        public uint Error;

        public byte[] Encode()
        {
            var buf = new byte[20];
            BinaryPrimitives.WriteUInt32BigEndian(buf.AsSpan(0), Version);
            BinaryPrimitives.WriteUInt32BigEndian(buf.AsSpan(4), Command);
            BinaryPrimitives.WriteUInt32BigEndian(buf.AsSpan(8), Length);
            BinaryPrimitives.WriteUInt32BigEndian(buf.AsSpan(12), Sender);
            BinaryPrimitives.WriteUInt32BigEndian(buf.AsSpan(16), Error);
            return buf;
        }

        public static HeaderUDP Decode(byte[] data)
        {
            return new HeaderUDP
            {
                Version = BinaryPrimitives.ReadUInt32BigEndian(data.AsSpan(0)),
                Command = BinaryPrimitives.ReadUInt32BigEndian(data.AsSpan(4)),
                Length = BinaryPrimitives.ReadUInt32BigEndian(data.AsSpan(8)),
                Sender = BinaryPrimitives.ReadUInt32BigEndian(data.AsSpan(12)),
                Error = BinaryPrimitives.ReadUInt32BigEndian(data.AsSpan(16))
            };
        }
    }
}
