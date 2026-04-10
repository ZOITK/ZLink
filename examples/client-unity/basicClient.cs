using System;
using System.Threading.Tasks;
using UnityEngine;
using Zlink;
using Zlink.Network;

/// <summary>
/// ZLink 통합 예제 클라이언트 (Client 엔진 기반)
/// Python SDK와 동일한 구조로 구현
/// </summary>
public class BasicClient : MonoBehaviour
{
    private Client client;
    private uint playerID;
    private int udpEchoCount;
    private TaskCompletionSource<bool> scenarioDone = new TaskCompletionSource<bool>();

    private async void Start()
    {
        Debug.Log("[zLink] 🚀 ZLink Unity 예제 시작");

        await RunScenario();

        Debug.Log("[zLink] ✅ ZLink Unity 예제 완료");
    }

    /// <summary>
    /// 메인 시나리오: 로그인 → 메시지 전송 → UDP 하트비트 10회 → 종료
    /// </summary>
    private async Task RunScenario()
    {
        // 1. 통합 클라이언트 엔진 생성 및 프로토콜 등록
        client = new Client();
        Protocol.Register(client, OnRecv);

        // 2. 서버 접속 (TCP + UDP 동시 활성화)
        Zlink.Logger.Info("[Network] 서버 접속 중 (TCP:8080 / UDP:8090)");
        if (!await client.StartAsync("127.0.0.1", tcpPort: 8080, udpPort: 8090))
        {
            Zlink.Logger.Error("[Network] 서버 접속 실패");
            return;
        }

        // 3. 로그인 시도
        Zlink.Logger.Info("[TCP] 로그인 요청 전송: UnityUser");
        var loginReq = new Msg_AuthLoginReq { Nickname = "UnityUser" };
        client.Send(loginReq);

        // 4. 시나리오 완료 대기 (최대 15초)
        try
        {
            await Task.WhenAny(scenarioDone.Task, Task.Delay(15000));
            if (!scenarioDone.Task.IsCompleted)
            {
                Zlink.Logger.Warn("[Timeout] 시나리오가 15초 내에 완료되지 않았습니다.");
            }
        }
        catch (Exception ex)
        {
            Zlink.Logger.Error($"[Error] {ex.Message}");
        }

        // 5. 종료
        Zlink.Logger.Info("[Network] 연결 종료");
        client.Stop();
        client.Dispose();
    }

    /// <summary>
    /// 모든 패킷 수신 처리 (TCP/UDP 통합 콜백)
    /// </summary>
    private async void OnRecv(object engine, object msg)
    {
        if (msg is Msg_AuthLoginRes loginRes)
        {
            // 시나리오 1: 로그인 응답
            if (loginRes.Result == Protocol.Err_None)
            {
                playerID = loginRes.PlayerID;
                Zlink.Logger.Info($"[TCP] 로그인 성공! PlayerID: {playerID}");

                // 시나리오 2: 메시지 전송
                Zlink.Logger.Info("[TCP] '안녕하세요' 메시지 전송...");
                var sendReq = new Msg_MessageSendReq { Message = "안녕하세요" };
                client.Send(sendReq);
            }
            else
            {
                Zlink.Logger.Error($"[TCP] 로그인 실패: {loginRes.Result}");
                scenarioDone.TrySetResult(false);
            }
        }
        else if (msg is Msg_MessageSendRes sendRes)
        {
            // 메시지 전송 성공 확인
            Zlink.Logger.Info("[TCP] 메시지 전송 성공 확인");
            // 시나리오 3: UDP 하트비트 10회 전송 시작
            await RunUdpScenario();
        }
        else if (msg is Msg_SystemUDPHeartBitRes heartBitRes)
        {
            // 시나리오 3: UDP 하트비트 응답 수신
            udpEchoCount++;
            Zlink.Logger.Info($"[UDP] 에코 응답 수신 ({udpEchoCount}/10), TS: {heartBitRes.Timestamp}");

            if (udpEchoCount >= 10)
            {
                // 시나리오 4: 1초 대기 후 종료
                Zlink.Logger.Info("[Scenario] UDP 에코 테스트 완료. 1초 대기...");
                await Task.Delay(1000);
                scenarioDone.TrySetResult(true);
            }
        }
        else if (msg is Msg_MessageReceiveNotify notify)
        {
            // 다른 플레이어의 메시지 수신
            Zlink.Logger.Info($"[Notify] {notify.Nickname}: {notify.Message}");
        }
    }

    /// <summary>
    /// UDP 하트비트 10회 전송 시나리오
    /// </summary>
    private async Task RunUdpScenario()
    {
        Zlink.Logger.Info("[UDP] 하트비트 10회 전송 시작 (0.1초 간격)");
        for (int i = 1; i <= 10; i++)
        {
            long ts = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            var req = new Msg_SystemUDPHeartBitReq { Timestamp = ts };

            // UDP로 전송 (playerID를 sessionId로 함께 전달)
            client.Send(req, useUDP: true);
            Zlink.Logger.Info($"[UDP] 하트비트 전송 ({i}/10), TS: {ts}");
            await Task.Delay(100);
        }
    }
}
