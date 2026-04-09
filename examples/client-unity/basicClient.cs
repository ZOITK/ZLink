using System;
using System.Threading.Tasks;
using UnityEngine;
using Zlink;
using Zlink.Network;

/// <summary>
/// ZLink 통합 예제 클라이언트 (상태 관리 및 MonoBehaviour 합본)
/// </summary>
public class BasicClient : MonoBehaviour
{
    private TcpClient tcpClient;
    private UdpClient udpClient;
    private uint playerID;
    private int udpEchoCount;
    private TaskCompletionSource<bool> scenarioDone = new TaskCompletionSource<bool>();

    private async void Start()
    {
        Debug.Log("[zLink] 🚀 ZLink Unity 예제 시작");

        tcpClient = new TcpClient();
        udpClient = new UdpClient();

        await RunScenario();

        Debug.Log("[zLink] ✅ ZLink Unity 예제 완료");
    }

    public async Task RunScenario()
    {
        // 1. 프로토콜 초기화 (TCP/UDP 모두 동일한 방식으로 등록)
        Protocol.Register(tcpClient, OnTcpRecv);
        Protocol.Register(udpClient, OnUdpRecv);

        // 2. 서버 접속
        Zlink.Logger.Info("[Network] 서버 접속 중 (127.0.0.1:8080)");
        if (!await tcpClient.ConnectAsync("127.0.0.1", 8080))
        {
            Zlink.Logger.Error("[Network] TCP 접속 실패");
            return;
        }

        // UDP 서버 주소 및 포트 설정 (8090)
        if (!await udpClient.StartAsync("127.0.0.1", 8090))
        {
            Zlink.Logger.Error("[Network] UDP 시작 실패");
            return;
        }
        Zlink.Logger.Info("[Network] UDP 클라이언트 준비 완료 (127.0.0.1:8090)");

        // 3. 로그인 시도
        Zlink.Logger.Info("[TCP] 로그인 요청 전송: UnityUser");
        var loginReq = new Msg_AuthLoginReq { Nickname = "UnityUser" };
        tcpClient.Send(loginReq.BuildTCP());

        // 4. 시나리오 완료 대기 (최대 15초)
        var timeoutTask = Task.Delay(15000);
        var completedTask = await Task.WhenAny(scenarioDone.Task, timeoutTask);

        if (completedTask == timeoutTask)
        {
            Zlink.Logger.Warn("[Timeout] 시나리오가 15초 내에 완료되지 않았습니다.");
        }

        // 5. 종료
        Zlink.Logger.Info("[Network] 예제 프로그램 정지 중...");
        tcpClient.Disconnect();
        udpClient.Dispose();
    }

    private void OnTcpRecv(object client, object msg)
    {
        switch (msg)
        {
            case Msg_AuthLoginRes loginRes:
                if (loginRes.Result == Protocol.Err_None)
                {
                    playerID = loginRes.PlayerID;
                    Zlink.Logger.Info($"[TCP] 로그인 성공! PlayerID: {playerID}");

                    // 시나리오 2: "안녕하세요" 메시지 전송
                    Zlink.Logger.Info("[TCP] '안녕하세요' 메시지 전송...");
                    var sendReq = new Msg_MessageSendReq { Message = "안녕하세요" };
                    tcpClient.Send(sendReq.BuildTCP());
                }
                else
                {
                    Zlink.Logger.Error($"[TCP] 로그인 실패 결과: {loginRes.Result}");
                    scenarioDone.TrySetResult(false);
                }
                break;

            case Msg_MessageSendRes sendRes:
                Zlink.Logger.Info("[TCP] 메시지 전송 성공 확인 수신");
                // 시나리오 3: UDP 하트비트 10회 전송 시작
                _ = RunUdpScenario();
                break;

            case Msg_MessageReceiveNotify notify:
                Zlink.Logger.Info($"[Notify] {notify.Nickname}: {notify.Message}");
                break;
        }
    }

    private void OnUdpRecv(object client, object msg)
    {
        if (msg is Msg_SystemUDPHeartBitRes res)
        {
            udpEchoCount++;
            Zlink.Logger.Info($"[UDP] 에코 응답 수신 ({udpEchoCount}/10), TS: {res.Timestamp}");

            if (udpEchoCount >= 10)
            {
                // 시나리오 4: 1초 대기 후 종료
                Zlink.Logger.Info("[Scenario] UDP 에코 테스트 완료. 1초 대기...");
                _ = FinishScenario();
            }
        }
    }

    private async Task RunUdpScenario()
    {
        Zlink.Logger.Info("[UDP] 하트비트 10회 전송 시작 (0.1초 간격)");
        for (int i = 1; i <= 10; i++)
        {
            long ts = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            var req = new Msg_SystemUDPHeartBitReq { Timestamp = ts };

            // UDP 헤더에 PlayerID를 Sender로 포함시켜 전송
            udpClient.Send(req.BuildUDP(playerID));
            Zlink.Logger.Info($"[UDP] 하트비트 전송 ({i}/10), TS: {ts}");
            await Task.Delay(100);
        }
    }

    private async Task FinishScenario()
    {
        await Task.Delay(1000);
        scenarioDone.TrySetResult(true);
    }
}
