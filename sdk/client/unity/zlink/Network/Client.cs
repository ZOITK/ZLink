using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Zlink.Network
{
    /// <summary>
    /// ZLink 통합 클라이언트 엔진입니다. (Orchestrator)
    /// 수신되는 모든 패킷(TCP/UDP)에서 SessionID를 학습하여 유기적으로 통합 관리합니다.
    /// </summary>
    public class Client : IDisposable
    {
        internal _TcpClient TCP { get; private set; }
        internal _UdpClient UDP { get; private set; }

        // 엔진 통합 세션 ID (0이면 서버에 신규/매칭 요청)
        public uint SessionId { get; private set; }

        // 엔진 통합 인터페이스 (Symmetry with Server)
        public Func<uint, byte[], object> Unmarshaler { get; private set; }
        public Func<object, bool, uint, byte[]> Packer { get; private set; }

        private List<Action<object, object>> _onRecvCallbacks = new List<Action<object, object>>();

        public bool IsConnected => (TCP != null && TCP.IsConnected) || (UDP != null && UDP.IsStarted);

        /// <summary>엔진에 프로토콜 주입</summary>
        public void SetProtocol(Func<uint, byte[], object> unmarshaler, Func<object, bool, uint, byte[]> packer)
        {
            Unmarshaler = unmarshaler;
            Packer = packer;
        }

        /// <summary>비즈니스 콜백 등록</summary>
        public void AddRecvCallback(Action<object, object> callback)
        {
            if (!_onRecvCallbacks.Contains(callback))
                _onRecvCallbacks.Add(callback);
        }

        public async Task<bool> StartAsync(string host, int tcpPort = 0, int udpPort = 0)
        {
            SessionId = 0;
            bool success = false;

            if (tcpPort > 0)
            {
                TCP = new _TcpClient();
                TCP.InternalOnReceive = HandleReceive;
                if (await TCP.ConnectAsync(host, tcpPort)) success = true;
            }

            if (udpPort > 0)
            {
                UDP = new _UdpClient();
                UDP.InternalOnReceive = HandleReceive;
                if (await UDP.StartAsync(host, udpPort)) success = true;
            }

            return success;
        }

        /// <summary>메시지 객체를 전송</summary>
        public void Send(object msg, bool useUDP = false)
        {
            if (Packer == null) return;

            // TCP는 항상 0으로 보내어 서버가 IP 매칭 또는 신규 생성을 결정하게 함
            // UDP는 할당받은 SessionId를 사용하여 서버가 기존 세션을 즉시 식별하게 함
            uint sidToSend = useUDP ? SessionId : 0u;

            byte[] data = Packer(msg, useUDP, sidToSend);

            if (useUDP && UDP != null) UDP.Send(data);
            else TCP?.Send(data);
        }

        private void HandleReceive(uint command, byte[] body, uint headerSid)
        {
            // [유기적 학습] 수신 헤더에 유효한 SessionID가 있다면 내 ID로 저장
            if (headerSid > 0 && SessionId != headerSid)
            {
                SessionId = headerSid;
                Logger.Debug($"[Engine] 세션 ID 학습 완료: {SessionId}");
            }

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
            SessionId = 0;
        }

        public void Dispose() => Stop();
    }
}
