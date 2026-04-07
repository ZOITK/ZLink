/*
기본 에코 클라이언트 - 간단한 메시지 송수신
*/
using System;
using System.Threading.Tasks;
using Zlink;
using Zlink.Network;
using Zlink.Logger;


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
		Logger.Logger.Info($"[Client] 로그인 시도: {this.nickname}");
		var req = new Msg_AuthLoginReq { Nickname = this.nickname };
		client.Send(req.BuildTCP());
		await Task.Delay(100);
	}

	/// <summary>
	/// 메시지 전송
	/// </summary>
	public async Task SendMessageAsync(TcpClient client, string message)
	{
		Logger.Logger.Info($"[Client] 메시지 전송: {message}");
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
			Logger.Logger.Info($"[Client] ✓ 로그인 성공 (ID: {msg.PlayerID})");

			// 메시지 전송
			await Task.Delay(500);
			await this.SendMessageAsync(client, "안녕하세요!");
		}
		else
		{
			Logger.Logger.Error($"[Client] ✗ 로그인 실패: {msg.Result}");
		}
	}

	/// <summary>
	/// 메시지 전송 응답 처리
	/// </summary>
	public void HandleSendResponse(Msg_MessageSendRes msg)
	{
		if (msg.Result == 0)
		{
			Logger.Logger.Info("[Client] ✓ 메시지 전송 성공");
		}
	}

	/// <summary>
	/// 메시지 수신 알림 처리
	/// </summary>
	public void HandleReceiveNotify(Msg_MessageReceiveNotify msg)
	{
		Logger.Logger.Info($"[Chat] {msg.Nickname}: {msg.Message}");
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


/// <summary>
/// 프로그램 메인 클래스
/// </summary>
public class Program
{
	private static BasicClient basicClient;

	public static async Task Main(string[] args)
	{
		Logger.Logger.Info("🚀 기본 에코 클라이언트 시작");

		// 클라이언트 초기화
		var client = new TcpClient();
		Protocol.Register(client, OnRecvPacket);

		// 닉네임 설정 (커맨드라인 인자 또는 기본값)
		string nickname = args.Length > 0 ? args[0] : "Player1";
		basicClient = new BasicClient(nickname);

		// 서버 연결
		Logger.Logger.Info("[Network] 서버 연결 중... (127.0.0.1:8080)");
		if (!await client.ConnectAsync("127.0.0.1", 8080))
		{
			Logger.Logger.Error("[Network] 서버 연결 실패");
			return;
		}

		Logger.Logger.Info("[Network] ✓ 서버 연결 성공");

		// 로그인
		await basicClient.LoginAsync(client);

		// 하트비트 루프
		_ = Task.Run(async () =>
		{
			while (basicClient.IsRunning && client.IsConnected)
			{
				await Task.Delay(5000);
				var heartbeat = new Msg_SystemTCPHeartBitReq { ServerTime = DateTimeOffset.UtcNow.ToUnixTimeSeconds() };
				client.Send(heartbeat.BuildTCP());
			}
		});

		// 10초 유지
		await Task.Delay(10000);

		Logger.Logger.Info("[Network] 연결 종료");
		basicClient.Stop();
		// TcpClient.CloseAsync() -> Disconnect()로 매핑 확인 필요. TcpClient에는 Disconnect()가 있음.
        client.Disconnect();
	}

	/// <summary>
	/// 패킷 수신 핸들러
	/// </summary>
	private static void OnRecvPacket(object client, object msg)
	{
		var tcpClient = (TcpClient)client;

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
				Logger.Logger.Debug($"[System] 하트비트 응답: {hbRes.ServerTime}");
				break;
		}
	}
}
