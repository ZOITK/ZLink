using System;
using System.Threading.Tasks;
using Zlink;
using Zlink.Network;
using Logger = Zlink.Logger;

/// <summary>
/// 기본 에코 클라이언트 상태 관리
/// </summary>
public class BasicClient
{
    private string nickname;
    private uint playerID;
    private bool isRunning;

    public BasicClient(string nickname)
    {
        this.nickname = nickname;
        this.playerID = 0;
        this.isRunning = true;
    }

    /// <summary>
    /// 로그인 요청 전송
    /// </summary>
    public async Task LoginAsync(TcpClient client)
    {
        Logger.Info($"[Client] 로그인 시도: {this.nickname}");
        var req = new Msg_AuthLoginReq { Nickname = this.nickname };
        client.Send(req.BuildTCP());
        await Task.Delay(100);
    }

    /// <summary>
    /// 메시지 전송
    /// </summary>
    public async Task SendMessageAsync(TcpClient client, string message)
    {
        Logger.Info($"[Client] 메시지 전송: {message}");
        var req = new Msg_MessageSendReq { Message = message };
        client.Send(req.BuildTCP());
        await Task.Delay(100);
    }

    /// <summary>
    /// 로그인 응답 처리
    /// </summary>
    public async Task HandleLoginResponse(TcpClient client, Msg_AuthLoginRes msg)
    {
        if (msg.Result == 0)
        {
            this.playerID = msg.PlayerID;
            Logger.Info($"[Client] ✓ 로그인 성공 (ID: {msg.PlayerID})");

            // 메시지 전송
            await Task.Delay(500);
            await this.SendMessageAsync(client, "안녕하세요!");
        }
        else
        {
            Logger.Error($"[Client] ✗ 로그인 실패: {msg.Result}");
        }
    }

    /// <summary>
    /// 메시지 전송 응답 처리
    /// </summary>
    public void HandleSendResponse(Msg_MessageSendRes msg)
    {
        if (msg.Result == 0)
        {
            Logger.Info("[Client] ✓ 메시지 전송 성공");
        }
    }

    /// <summary>
    /// 메시지 수신 알림 처리
    /// </summary>
    public void HandleReceiveNotify(Msg_MessageReceiveNotify msg)
    {
        Logger.Info($"[Chat] {msg.Nickname}: {msg.Message}");
    }

    /// <summary>
    /// 실행 종료
    /// </summary>
    public void Stop()
    {
        this.isRunning = false;
    }

    /// <summary>
    /// 실행 상태 확인
    /// </summary>
    public bool IsRunning => this.isRunning;
}
