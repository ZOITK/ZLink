using System;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;
using Zoit.Logger;
using Zoit.Protocol;

namespace Zoit.Network
{
    /// <summary>
    /// ZPP 프레임워크 전용 고성능 TCP 클라이언트 (Async 기반)
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

        public bool IsConnected => _isConnected && _client != null && _client.Connected;

        public void AddRecvCallback(Action<object, object> callback) => _onRecvCallbacks.Add(callback);
        public void SetUnmarshaler(Func<uint, byte[], object> unmarshaler) => Unmarshaler = unmarshaler;

        public async Task<bool> ConnectAsync(string host, int port)
        {
            try
            {
                _client = new System.Net.Sockets.TcpClient();
                await _client.ConnectAsync(host, port);
                _stream = _client.GetStream();
                _isConnected = true;
                _cts = new CancellationTokenSource();

                ClientLogger.Info($"[TCP] 서버 연결 성공: {host}:{port}");
                _ = ReceiveLoop(_cts.Token);
                return true;
            }
            catch (Exception ex)
            {
                ClientLogger.Error($"[TCP] 연결 실패: {ex.Message}");
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
                ClientLogger.Error($"[TCP] 전송 오류: {ex.Message}");
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
            ClientLogger.Info("[TCP] 연결 종료");
        }

        private async Task ReceiveLoop(CancellationToken token)
        {
            byte[] headerBuf = new byte[16];
            try
            {
                while (!token.IsCancellationRequested && IsConnected)
                {
                    // 1. 헤더 읽기 (16 bytes)
                    int read = 0;
                    while (read < 16)
                    {
                        int n = await _stream.ReadAsync(headerBuf, read, 16 - read, token);
                        if (n <= 0) throw new Exception("연결 종료");
                        read += n;
                    }

                    var header = HeaderTCP.Decode(headerBuf);
                    
                    // 2. 바디 읽기
                    byte[] body = null;
                    if (header.Length > 0)
                    {
                        body = new byte[header.Length];
                        int bodyRead = 0;
                        while (bodyRead < header.Length)
                        {
                            int n = await _stream.ReadAsync(body, bodyRead, (int)header.Length - bodyRead, token);
                            if (n <= 0) throw new Exception("바디 수신 중 연결 종료");
                            bodyRead += n;
                        }
                    }

                    // 3. 자동 객체 변환 및 모든 콜백 호출
                    if (Unmarshaler != null)
                    {
                        var msg = Unmarshaler(header.Command, body);
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
                    ClientLogger.Warn($"[TCP] 수신 루프 비정상 종료: {ex.Message}");
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
