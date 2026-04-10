using System;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;

namespace Zlink.Network
{
    /// <summary>
    /// 엔진 내부에서 사용되는 TCP 전송 핸들러입니다.
    /// </summary>
    public class TcpClient
    {
        private System.Net.Sockets.TcpClient _client;
        private NetworkStream _stream;
        private CancellationTokenSource _cts;
        private bool _isConnected;

        public bool IsConnected => _isConnected;
        public const int HeaderSize = 24;
        public const ushort MagicZO = 0x4F5A;
        public uint SessionId { get; private set; } // 서버로부터 할당받은 SessionID

        // 엔진 디스패처로 데이터를 넘겨주기 위한 내부 대리자
        public Action<uint, byte[]> InternalOnReceive;

        /// <summary>
        /// ZLink 24바이트 표준 패킷을 조립합니다. (Python Pack과 동일 규격)
        /// Python SDK의 struct.pack("<HIIIIIH", Magic, Version, Cmd, Len, Sess, Err, Seq)과 동일
        /// </summary>
        /// <param name="cmdId">명령 ID</param>
        /// <param name="body">바디 데이터 (null 가능)</param>
        /// <param name="sessionId">세션 ID 또는 Sender ID</param>
        /// <param name="errorCode">에러 코드</param>
        /// <param name="version">프로토콜 버전 (기본값: 1)</param>
        /// <returns>완성된 ZLink 패킷 (헤더 + 바디)</returns>
        public static byte[] Pack(uint cmdId, byte[] body, uint sessionId, uint errorCode, uint version = 1)
        {
            byte[] bodyData = body ?? new byte[0];
            byte[] packet = new byte[HeaderSize + bodyData.Length];

            // 헤더 조립 (24바이트):
            // Offset 0-1: Magic (0x4F5A)
            BitConverter.GetBytes(MagicZO).CopyTo(packet, 0);
            // Offset 2-5: Version
            BitConverter.GetBytes(version).CopyTo(packet, 2);
            // Offset 6-9: Command ID
            BitConverter.GetBytes(cmdId).CopyTo(packet, 6);
            // Offset 10-13: Body Length
            BitConverter.GetBytes((uint)bodyData.Length).CopyTo(packet, 10);
            // Offset 14-17: Session ID / Sender ID
            BitConverter.GetBytes(sessionId).CopyTo(packet, 14);
            // Offset 18-21: Error Code
            BitConverter.GetBytes(errorCode).CopyTo(packet, 18);
            // Offset 22-23: Sequence (Reserved, 기본값 0으로 초기화됨)

            // 바디 추가
            if (bodyData.Length > 0)
                bodyData.CopyTo(packet, HeaderSize);

            return packet;
        }

        public async Task<bool> ConnectAsync(string host, int port)
        {
            try
            {
                _client = new System.Net.Sockets.TcpClient();
                await _client.ConnectAsync(host, port);
                _stream = _client.GetStream();
                _isConnected = true;
                _cts = new CancellationTokenSource();
                _ = ReceiveLoop(_cts.Token);
                return true;
            }
            catch { return false; }
        }

        public void Disconnect()
        {
            _isConnected = false;
            _cts?.Cancel();
            _stream?.Close();
            _client?.Close();
        }

        public void Send(byte[] data)
        {
            if (!_isConnected || _stream == null) return;
            try { _stream.Write(data, 0, data.Length); }
            catch { Disconnect(); }
        }

        private async Task ReceiveLoop(CancellationToken token)
        {
            byte[] headerBuf = new byte[HeaderSize];
            try
            {
                while (!token.IsCancellationRequested && _isConnected)
                {
                    int read = 0;
                    while (read < HeaderSize)
                    {
                        int n = await _stream.ReadAsync(headerBuf, read, HeaderSize - read, token);
                        if (n <= 0) throw new Exception();
                        read += n;
                    }

                    // Offset: 6(Cmd), 10(Len), 14(SessionId) - ZLink Standard
                    uint cmd = BitConverter.ToUInt32(headerBuf, 6);
                    uint bodyLen = BitConverter.ToUInt32(headerBuf, 10);
                    uint sessionId = BitConverter.ToUInt32(headerBuf, 14);

                    // 서버로부터 할당받은 SessionID 저장 (UDP 전송시 사용)
                    SessionId = sessionId;

                    byte[] body = null;
                    if (bodyLen > 0)
                    {
                        body = new byte[bodyLen];
                        int bodyRead = 0;
                        while (bodyRead < (int)bodyLen)
                        {
                            int n = await _stream.ReadAsync(body, bodyRead, (int)bodyLen - bodyRead, token);
                            if (n <= 0) throw new Exception();
                            bodyRead += n;
                        }
                    }
                    InternalOnReceive?.Invoke(cmd, body);
                }
            }
            catch { Disconnect(); }
        }
    }
}
