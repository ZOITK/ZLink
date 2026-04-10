using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;

namespace Zlink.Network
{
    /// <summary>
    /// 엔진 내부에서 사용되는 UDP 전송 핸들러입니다.
    /// </summary>
    public class UdpClient
    {
        private System.Net.Sockets.UdpClient _client;
        private CancellationTokenSource _cts;
        private bool _isStarted;
        public bool IsStarted => _isStarted;

        public Action<uint, byte[]> InternalOnReceive;

        public async Task<bool> StartAsync(string host, int port)
        {
            try
            {
                IPAddress[] addr = await Dns.GetHostAddressesAsync(host);
                if (addr.Length == 0) return false;
                _client = new System.Net.Sockets.UdpClient();
                _client.Connect(new IPEndPoint(addr[0], port));
                _isStarted = true;
                _cts = new CancellationTokenSource();
                _ = ReceiveLoop(_cts.Token);
                return true;
            }
            catch { return false; }
        }

        public void Stop()
        {
            _isStarted = false;
            _cts?.Cancel();
            _client?.Close();
        }

        /// <summary>
        /// UDP 클라이언트를 정리합니다. (IDisposable 구현)
        /// </summary>
        public void Dispose() => Stop();

        public void Send(byte[] data)
        {
            if (!_isStarted) return;
            try { _client.Send(data, data.Length); }
            catch { }
        }

        private async Task ReceiveLoop(CancellationToken token)
        {
            try
            {
                while (!token.IsCancellationRequested && _isStarted)
                {
                    var result = await _client.ReceiveAsync();
                    byte[] data = result.Buffer;
                    if (data.Length < 24) continue;

                    // Offset: 6(Cmd), 10(Len) - Standard
                    uint cmd = BitConverter.ToUInt32(data, 6);
                    uint bodyLen = BitConverter.ToUInt32(data, 10);

                    byte[] body = null;
                    if (bodyLen > 0 && data.Length >= 24 + bodyLen)
                    {
                        body = new byte[bodyLen];
                        Buffer.BlockCopy(data, 24, body, 0, (int)bodyLen);
                    }
                    InternalOnReceive?.Invoke(cmd, body);
                }
            }
            catch { }
        }
    }
}
