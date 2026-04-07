using System;
using System.Threading.Tasks;
using Zoit;
using Zoit.Network;
using Zoit.Logger;

public class SampleClient
{
    public static async Task Main(string[] args)
    {
        ClientLogger.Info("ZPP Framework Unified C# Client 시작");

        // 1. TCP 클라이언트 초기화
        var client = new TcpClient();

        // 2. [통일된 사용법] Register 한 줄로 프로토콜과 핸들러 바인딩
        Protocol.Register(client, OnRecvPacket);

        // 3. 서버 연결
        if (!await client.ConnectAsync("127.0.0.1", 8080))
        {
            return;
        }

        // 4. 로그인 요청 전송 (BuildTCP 사용으로 통일성 확보)
        ClientLogger.Info("[Main] 로그인 요청 전송 시도...");
        var loginReq = new Msg_AuthLoginReq { LoginID = "unified_cs_bot_01" };
        client.Send(loginReq.BuildTCP());

        // 5. 하트비트 루프 (파이썬/Go와 동일하게 5초 간격)
        _ = Task.Run(async () =>
        {
            while (client.IsConnected)
            {
                await Task.Delay(5000);
                var heartbeat = new Msg_SystemTCPHeartBitReq { ServerTime = DateTimeOffset.UtcNow.ToUnixTimeSeconds() };
                client.Send(heartbeat.BuildTCP());
            }
        });

        // 대기 (Ctrl+C 등으로 종료 전까지 유지)
        while (client.IsConnected)
        {
            await Task.Delay(1000);
        }
    }

    // OnRecvPacket - 파이썬/Go 예제와 100% 동일한 비즈니스 로직
    private static void OnRecvPacket(object client, object msg)
    {
        switch (msg)
        {
            case Msg_AuthLoginRes loginRes:
                ClientLogger.Info($"[Handler] 로그인 응답 수신: UserIdx={loginRes.UserIdx}, Result={loginRes.Result}");
                break;

            case Msg_SystemTCPHeartBitRes hbRes:
                ClientLogger.Debug($"[Handler] 하트비트 응답 수신: {hbRes.ServerTime}");
                break;
        }
    }
}
