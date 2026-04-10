using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Zlink.Network
{
    /// <summary>
    /// ZLink 통합 클라이언트 엔진입니다. (Orchestrator)
    /// 서버 엔진과 대칭되는 인터페이스를 제공하며 TCP/UDP를 한곳에서 관리합니다.
    /// </summary>
    public class Client : IDisposable
    {
        public TcpClient TCP { get; private set; }
        public UdpClient UDP { get; private set; }

        // 엔진 통합 인터페이스 (Symmetry with Server)
        public Func<uint, byte[], object> Unmarshaler { get; private set; }
        public Func<object, bool, uint, byte[]> Packer { get; private set; }

        private List<Action<object, object>> _onRecvCallbacks = new List<Action<object, object>>();

        public bool IsConnected => (TCP != null && TCP.IsConnected) || (UDP != null && UDP.IsStarted);

        /// <summary>엔진에 프로토콜 주입 (서버의 SetProtocol과 대칭)</summary>
        public void SetProtocol(Func<uint, byte[], object> unmarshaler, Func<object, bool, uint, byte[]> packer)
        {
            Unmarshaler = unmarshaler;
            Packer = packer;
        }

        /// <summary>비즈니스 콜백 등록 (서버의 AddRecvCallback과 대칭)</summary>
        public void AddRecvCallback(Action<object, object> callback)
        {
            if (!_onRecvCallbacks.Contains(callback))
                _onRecvCallbacks.Add(callback);
        }

        public async Task<bool> StartAsync(string host, int tcpPort = 0, int udpPort = 0)
        {
            bool success = false;

            if (tcpPort > 0)
            {
                TCP = new TcpClient();
                TCP.InternalOnReceive = HandleReceive;
                if (await TCP.ConnectAsync(host, tcpPort)) success = true;
            }

            if (udpPort > 0)
            {
                UDP = new UdpClient();
                UDP.InternalOnReceive = HandleReceive;
                if (await UDP.StartAsync(host, udpPort)) success = true;
            }

            return success;
        }

        /// <summary>메시지 객체를 전송 (TCP/UDP 자동 선택 가능)</summary>
        public void Send(object msg, bool useUDP = false)
        {
            if (Packer == null) return;

            // 서버로부터 할당받은 SessionID (TCP 응답 헤더에서 추출)
            uint sessionId = TCP != null ? TCP.SessionId : 0u;

            // UDP 전송시 SessionID를 함께 전달하여 서버가 세션을 매칭할 수 있도록 함
            byte[] data = Packer(msg, useUDP, sessionId);

            if (useUDP && UDP != null) UDP.Send(data);
            else TCP?.Send(data);
        }

        private void HandleReceive(uint command, byte[] body)
        {
            if (Unmarshaler == null) return;
            var msg = Unmarshaler(command, body);
            if (msg != null)
            {
                var list = new List<Action<object, object>>(_onRecvCallbacks);
                foreach (var cb in list)
                {
                    try { cb.Invoke(this, msg); }
                    catch (Exception ex) { Logger.Error($"[Client] Callback Error: {ex.Message}"); }
                }
            }
        }

        public void Stop()
        {
            TCP?.Disconnect();
            UDP?.Stop();
        }

        public void Dispose() => Stop();
    }
}
