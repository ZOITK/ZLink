using System;
using System.Threading.Tasks;
using UnityEngine;
using Zlink;
using Zlink.Network;
using Logger = Zlink.Logger;

/// <summary>
/// Unity 메인 컴포넌트
/// </summary>
public class Main : MonoBehaviour
{
    private BasicClient basicClient;
    private TcpClient client;

    private async void Start()
    {
        Logger.Info("🚀 Unity 기본 에코 클라이언트 시작");

        // 클라이언트 초기화
        client = new TcpClient();
        Protocol.Register(client, OnRecvPacket);

        // 닉네임 설정
        string nickname = "UnityPlayer_" + UnityEngine.Random.Range(1000, 9999);
        basicClient = new BasicClient(nickname);

        // 서버 연결
        Logger.Info("[Network] 서버 연결 중... (127.0.0.1:8080)");
        if (!await client.ConnectAsync("127.0.0.1", 8080))
        {
            Logger.Error("[Network] 서버 연결 실패");
            return;
        }

        Logger.Info("[Network] ✓ 서버 연결 성공");

        // 로그인
        await basicClient.LoginAsync(client);

        // 하트비트 루프
        _ = Task.Run(async () =>
        {
            while (basicClient != null && basicClient.IsRunning && client != null && client.IsConnected)
            {
                await Task.Delay(5000);
                if (client == null || !client.IsConnected) break;

                var heartbeat = new Msg_SystemTCPHeartBitReq { ServerTime = DateTimeOffset.UtcNow.ToUnixTimeSeconds() };
                client.Send(heartbeat.BuildTCP());
            }
        });

        // 10초 유지 (테스트용)
        await Task.Delay(10000);

        if (client != null && client.IsConnected)
        {
            Logger.Info("[Network] 연결 종료 (테스트 종료)");
            basicClient.Stop();
            client.Disconnect();
        }
    }

    private void OnDestroy()
    {
        if (client != null)
        {
            basicClient?.Stop();
            client.Disconnect();
            client.Dispose();
        }
    }

    /// <summary>
    /// 패킷 수신 핸들러
    /// </summary>
    private void OnRecvPacket(object clientObj, object msg)
    {
        var tcpClient = (TcpClient)clientObj;

        switch (msg)
        {
            case Msg_AuthLoginRes loginRes:
                _ = basicClient.HandleLoginResponse(tcpClient, loginRes);
                break;

            case Msg_MessageSendRes sendRes:
                basicClient.HandleSendResponse(sendRes);
                break;

            case Msg_MessageReceiveNotify notifyMsg:
                basicClient.HandleReceiveNotify(notifyMsg);
                break;

            case Msg_SystemTCPHeartBitRes hbRes:
                Logger.Debug($"[System] 하트비트 응답: {hbRes.ServerTime}");
                break;
        }
    }
}
