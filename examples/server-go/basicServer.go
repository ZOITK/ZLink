package main

import (
	"log/slog"
	"os"
	"zlink/logger"
	"zlink/network"
	"zlink-example-server/protocol"
)

func main() {
	// 로거 초기화 (개발 환경)
	logger.Init("development")

	// 1. 서버 생성 (TCP: 8080, UDP: 8090)
	server := network.NewServer(8080, 8090)

	// 2. 프로토콜 통합 등록 (Organic Integration)
	// 이제 모든 TCP/UDP 메시지는 이 하나의 콜백으로 유기적으로 들어옵니다.
	protocol.Register(server, func(sess protocol.ISession, msg any) {
		switch m := msg.(type) {
		case *protocol.Msg_AuthLoginReq:
			slog.Info("[ZLink] 로그인 요청 수신", "nickname", m.Nickname, "sessionID", sess.ID())
			server.Send(sess, &protocol.Msg_AuthLoginRes{
				PlayerID: 1001,
				Result:   uint32(protocol.Err_None),
			})

		case *protocol.Msg_MessageSendReq:
			slog.Info("[ZLink] 메시지 수신", "msg", m.Message, "sessionID", sess.ID())
			server.Send(sess, &protocol.Msg_MessageSendRes{
				Result: uint32(protocol.Err_None),
			})

			// [유기적 브로드캐스트] UDP 바인딩된 모든 대상에게 통지
			server.BroadcastUDP(&protocol.Msg_MessageReceiveNotify{
				PlayerID: 1001,
				Nickname: "System",
				Message:  "[UDP공지] " + m.Message,
			})

		case *protocol.Msg_SystemUDPHeartBitReq:
			slog.Info("[UDP] 하트비트 수신", "ts", m.Timestamp, "sessionID", sess.ID())
			server.Send(sess, &protocol.Msg_SystemUDPHeartBitRes{
				Timestamp: m.Timestamp,
			})

		case *protocol.Msg_SystemTCPHeartBitReq:
			slog.Info("[TCP] 하트비트 수신", "ts", m.ServerTime, "sessionID", sess.ID())
			server.Send(sess, &protocol.Msg_SystemTCPHeartBitRes{
				ServerTime: m.ServerTime,
			})
		}
	})

	// 3. 엔진 이벤트 핸들러
	server.OnSessionOpen = func(sess *network.Session) {
		slog.Info("[zLink/Engine] 새로운 세션 생성", "id", sess.ID(), "addr", sess.RemoteAddr)
	}

	// 4. 서버 가동
	slog.Info("[zLink/Engine] 서버 가동 시작", "tcp", 8080, "udp", 8090)
	if err := server.Start(); err != nil {
		slog.Error("[zLink/Engine] 서버 시작 실패", "err", err)
		os.Exit(1)
	}
}

/*
=== UDP Standalone 모드 사용 예제 ===

TCP 없이 UDP만으로 서버를 구성할 때:

	func mainStandalone() {
		logger.Init("development")

		// TCP 포트를 0으로 지정하면 UDP 단독 모드로 자동 활성화
		server := network.NewServer(0, 8090)

		protocol.Register(server, func(sess protocol.ISession, msg any) {
			switch m := msg.(type) {
			case *protocol.Msg_SystemUDPHeartBitReq:
				slog.Info("[UDP Standalone] 하트비트", "ts", m.Timestamp)
				server.Send(sess, &protocol.Msg_SystemUDPHeartBitRes{
					Timestamp: m.Timestamp,
				})
			}
		})

		server.OnSessionOpen = func(sess *network.Session) {
			slog.Info("[UDP Standalone] 새 클라이언트", "addr", sess.RemoteAddr)
		}

		// UDP만 블로킹으로 기동 (TCP 없음)
		slog.Info("[UDP Standalone] 시작", "port", 8090)
		if err := server.Start(); err != nil {
			slog.Error("[UDP Standalone] 서버 시작 실패", "err", err)
			os.Exit(1)
		}
	}

=== 포트 0 자동 모드 판단 ===

NewServer(tcpPort, udpPort) 사용시:

- NewServer(8080, 8090)  → TCP:8080 + UDP:8090 혼합 모드 (기존 동작)
- NewServer(0, 8090)     → UDP:8090 단독 모드 (TCP 없음, UDP가 메인 루프)
- NewServer(8080, 0)     → TCP:8080 단독 모드 (UDP 없음)
*/
