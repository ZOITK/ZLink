using System;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;
using Zlink.Logger;

namespace Zlink.Network
{
    /// <summary>
    /// ZLink 프레임워크 전용 고성능 TCP 클라이언트 (Async 기반)
    /// </summary>
    public class TcpClient : IDisposable
    {
        private System.Net.Sockets.TcpClient _client;
        private NetworkStream _stream;
        private CancellationTokenSource _cts;
        private bool _isConnected;

        // --- 핵심 개선: 엔진이 직접 프로토콜과 로직을 관리함 (Go/Python 동일) ---
        public Func<uint, byte[], object> Unmarshaler { get; private set; }
        private readonly List<Action<object, object>> _onRecvCallbacks = new List<Action<object, object>>();
        
        // 헤더 정보 (제네레이터에 의해 설정됨)
        public int HeaderSize { get; private set; } = 16;
        public Func<byte[], object> HeaderDecoder { get; private set; }

        public bool IsConnected => _isConnected && _client != null && _client.Connected;

        public void AddRecvCallback(Action<object, object> callback) => _onRecvCallbacks.Add(callback);
        public void SetUnmarshaler(Func<uint, byte[], object> unmarshaler) => Unmarshaler = unmarshaler;
        
        public void SetHeaderInfo(int headerSize, Func<byte[], object> decoder)
        {
            HeaderSize = headerSize;
            HeaderDecoder = decoder;
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

                Logger.Logger.Info($"[TCP] 서버 연결 성공: {host}:{port}");
                _ = ReceiveLoop(_cts.Token);
                return true;
            }
            catch (Exception ex)
            {
                Logger.Logger.Error($"[TCP] 연결 실패: {ex.Message}");
                return false;
            }
        }

        public void Send(byte[] data)
        {
            if (!IsConnected) return;
            try
            {
                _stream.Write(data, 0, data.Length);
            }
            catch (Exception ex)
            {
                Logger.Logger.Error($"[TCP] 전송 오류: {ex.Message}");
                Disconnect();
            }
        }

        public void Disconnect()
        {
            if (!_isConnected) return;
            _isConnected = false;
            _cts?.Cancel();
            _stream?.Close();
            _client?.Close();
            Logger.Logger.Info("[TCP] 연결 종료");
        }

        private async Task ReceiveLoop(CancellationToken token)
        {
            byte[] headerBuf = new byte[64]; // 충분한 크기 할당
            try
            {
                while (!token.IsCancellationRequested && IsConnected)
                {
                    // 1. 헤더 읽기
                    int read = 0;
                    int targetSize = HeaderSize;
                    while (read < targetSize)
                    {
                        int n = await _stream.ReadAsync(headerBuf, read, targetSize - read, token);
                        if (n <= 0) throw new Exception("연결 종료");
                        read += n;
                    }

                    uint command = 0;
                    uint bodyLen = 0;

                    if (HeaderDecoder != null)
                    {
                        var hdrObj = HeaderDecoder(headerBuf);
                        if (hdrObj == null) continue;

                        // 리플렉션을 통해 Command와 Length 필드 추출 (엔진 범용성 확보)
                        var type = hdrObj.GetType();
                        command = (uint)type.GetField("Command").GetValue(hdrObj);
                        bodyLen = (uint)type.GetField("Length").GetValue(hdrObj);
                    }
                    else
                    {
                        // 기본 처리 (하위 호환성용 - Little Endian)
                        command = BitConverter.ToUInt32(headerBuf, 4);
                        bodyLen = BitConverter.ToUInt32(headerBuf, 8);
                    }
                    
                    // 2. 바디 읽기
                    byte[] body = null;
                    if (bodyLen > 0)
                    {
                        body = new byte[bodyLen];
                        int bodyRead = 0;
                        while (bodyRead < bodyLen)
                        {
                            int n = await _stream.ReadAsync(body, bodyRead, (int)bodyLen - bodyRead, token);
                            if (n <= 0) throw new Exception("바디 수신 중 연결 종료");
                            bodyRead += n;
                        }
                    }

                    // 3. 자동 객체 변환 및 모든 콜백 호출
                    if (Unmarshaler != null)
                    {
                        var msg = Unmarshaler(command, body);
                        if (msg != null)
                        {
                            foreach (var cb in _onRecvCallbacks)
                            {
                                cb.Invoke(this, msg);
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                if (!token.IsCancellationRequested)
                {
                    Logger.Logger.Warn($"[TCP] 수신 루프 비정상 종료: {ex.Message}");
                    Disconnect();
                }
            }
        }

        public void Dispose()
        {
            Disconnect();
            _cts?.Dispose();
        }
    }
}
