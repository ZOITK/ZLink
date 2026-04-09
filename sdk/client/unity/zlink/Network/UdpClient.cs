using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;
using Zlink;
using Logger = Zlink.Logger;

namespace Zlink.Network
{
    /// <summary>
    /// ZLink 프레임워크 전용 고성능 UDP 클라이언트
    /// </summary>
    public class UdpClient : IDisposable
    {
        private System.Net.Sockets.UdpClient _client;
        private IPEndPoint _remoteEndPoint;
        private CancellationTokenSource _cts;
        private bool _isStarted;

        // --- 핵심 개선: 엔진이 직접 프로토콜과 로직을 관리함 (Go/Python 동일) ---
        public Func<uint, byte[], object> Unmarshaler { get; private set; }
        private Action<object, object> _onRecvCallback;
        
        // 헤더 정보 (제네레이터에 의해 설정됨)
        public int HeaderSize { get; private set; } = 20;
        public Func<byte[], object> HeaderDecoder { get; private set; }


        public void SetUnmarshaler(Func<uint, byte[], object> unmarshaler) => Unmarshaler = unmarshaler;
        public void AddRecvCallback(Action<object, object> callback) => _onRecvCallback = callback;
        
        public void SetHeaderInfo(int headerSize, Func<byte[], object> decoder)
        {
            HeaderSize = headerSize;
            HeaderDecoder = decoder;
        }

        public async Task<bool> StartAsync(string host, int port)
        {
            try
            {
                IPAddress[] addresses = await Dns.GetHostAddressesAsync(host);
                if (addresses.Length == 0) return false;

                _remoteEndPoint = new IPEndPoint(addresses[0], port);
                _client = new System.Net.Sockets.UdpClient();
                // UDP Connect는 필터링 역할을 함
                _client.Connect(_remoteEndPoint);
                _isStarted = true;
                _cts = new CancellationTokenSource();

                Logger.Info($"[UDP] 클라이언트 시작: {host}:{port}");
                _ = ReceiveLoop(_cts.Token);
                return true;
            }
            catch (Exception ex)
            {
                Logger.Error($"[UDP] 시작 실패: {ex.Message}");
                return false;
            }
        }

        public void Stop()
        {
            _isStarted = false;
            _cts?.Cancel();
            _client?.Close();
        }

        public void Send(byte[] data)
        {
            if (!_isStarted || _client == null) return;
            try
            {
                _client.Send(data, data.Length);
            }
            catch (Exception ex)
            {
                Logger.Error($"[UDP] 패킷 전송 오류: {ex.Message}");
            }
        }

        // 하위 호환용 Send (직접 헤더 구성)
        public void Send(uint command, byte[] body, uint senderIdx, uint version = 1)
        {
            if (!_isStarted) return;
            
            // 실제로는 이제 Packet.BuildUDP() 결과를 Send(byte[])로 보내는 것을 권장함
            Logger.Warn("[UDP] Direct Send is deprecated. Use Packet.BuildUDP() and Send(byte[]) instead.");
        }

        private async Task ReceiveLoop(CancellationToken token)
        {
            try
            {
                while (!token.IsCancellationRequested && _isStarted)
                {
                    UdpReceiveResult result = await _client.ReceiveAsync();
                    byte[] data = result.Buffer;

                    if (data.Length < HeaderSize) continue;

                    uint command = 0;
                    uint bodyLen = 0;
                    uint error = 0;
                    uint sender = 0;

                    if (HeaderDecoder != null)
                    {
                        var hdrObj = HeaderDecoder(data);
                        if (hdrObj == null) continue;

                        var type = hdrObj.GetType();
                        command = (uint)type.GetField("Command").GetValue(hdrObj);
                        bodyLen = (uint)type.GetField("Length").GetValue(hdrObj);
                        
                        var errorField = type.GetField("Error");
                        if (errorField != null) error = (uint)errorField.GetValue(hdrObj);
                        
                        var senderField = type.GetField("Sender");
                        if (senderField != null) sender = (uint)senderField.GetValue(hdrObj);
                    }
                    else
                    {
                        // 기본 처리 (Little Endian)
                        command = BitConverter.ToUInt32(data, 4);
                        bodyLen = BitConverter.ToUInt32(data, 8);
                    }

                    byte[] body = null;
                    if (bodyLen > 0 && data.Length >= HeaderSize + bodyLen)
                    {
                        body = new byte[bodyLen];
                        Buffer.BlockCopy(data, HeaderSize, body, 0, (int)bodyLen);
                    }

                    // 통합 디스패처 호출
                    if (Unmarshaler != null && _onRecvCallback != null)
                    {
                        var msg = Unmarshaler(command, body);
                        if (msg != null)
                        {
                            _onRecvCallback.Invoke(this, msg);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                if (!token.IsCancellationRequested)
                {
                    Logger.Warn($"[UDP] 수신 루프 종료: {ex.Message}");
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
