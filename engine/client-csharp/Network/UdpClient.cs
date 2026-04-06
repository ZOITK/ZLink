using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;
using Zoit.Logger;
using Zoit.Protocol;

namespace Zoit.Network
{
    /// <summary>
    /// ZPP 프레임워크 전용 고성능 UDP 클라이언트
    /// </summary>
    public class UdpClient : IDisposable
    {
        private System.Net.Sockets.UdpClient _client;
        private IPEndPoint _remoteEndPoint;
        private CancellationTokenSource _cts;
        private bool _isStarted;

        public event Action<NetworkPacket> OnReceivePacket;

        public async Task<bool> StartAsync(string host, int port)
        {
            try
            {
                IPAddress[] addresses = await Dns.GetHostAddressesAsync(host);
                if (addresses.Length == 0) return false;

                _remoteEndPoint = new IPEndPoint(addresses[0], port);
                _client = new System.Net.Sockets.UdpClient();
                _client.Connect(_remoteEndPoint);
                _isStarted = true;
                _cts = new CancellationTokenSource();

                ClientLogger.Info($"[UDP] 클라이언트 시작: {host}:{port}");
                _ = ReceiveLoop(_cts.Token);
                return true;
            }
            catch (Exception ex)
            {
                ClientLogger.Error($"[UDP] 시작 실패: {ex.Message}");
                return false;
            }
        }

        public void Stop()
        {
            _isStarted = false;
            _cts?.Cancel();
            _client?.Close();
        }

        public void Send(uint command, byte[] body, uint senderIdx, uint version = 1)
        {
            if (!_isStarted) return;

            try
            {
                var header = new HeaderUDP
                {
                    Version = version,
                    Command = command,
                    Length = (uint)(body?.Length ?? 0),
                    Sender = senderIdx,
                    Error = 0
                };
                byte[] headerBytes = header.Encode();
                byte[] fullPacket = new byte[headerBytes.Length + (body?.Length ?? 0)];
                
                Buffer.BlockCopy(headerBytes, 0, fullPacket, 0, headerBytes.Length);
                if (body != null) Buffer.BlockCopy(body, 0, fullPacket, headerBytes.Length, body.Length);

                _client.Send(fullPacket, fullPacket.Length);
            }
            catch (Exception ex)
            {
                ClientLogger.Error($"[UDP] 패킷 전송 오류: {ex.Message}");
            }
        }

        private async Task ReceiveLoop(CancellationToken token)
        {
            try
            {
                while (!token.IsCancellationRequested && _isStarted)
                {
                    UdpReceiveResult result = await _client.ReceiveAsync();
                    byte[] data = result.Buffer;

                    if (data.Length < 20) continue;

                    var header = HeaderUDP.Decode(data);
                    byte[] body = null;
                    if (header.Length > 0 && data.Length >= 20 + header.Length)
                    {
                        body = new byte[header.Length];
                        Buffer.BlockCopy(data, 20, body, 0, (int)header.Length);
                    }

                    OnReceivePacket?.Invoke(new NetworkPacket(header.Command, body, header.Error, header.Sender));
                }
            }
            catch (Exception ex)
            {
                if (!token.IsCancellationRequested)
                {
                    ClientLogger.Warn($"[UDP] 수신 루프 종료: {ex.Message}");
                }
            }
        }

        public void Dispose()
        {
            Stop();
            _cts?.Dispose();
        }
    }
}
