package main

import (
	"log"
	"log/slog"
	"net"
	"os"
	"os/signal"
	"syscall"

	"zlink/base"
	"zlink/network"
	"zlink/protocol"
)

func main() {
	// 1. ZLink 서버 엔진 생성 (TCP: 8080, UDP: 8090)
	server := network.NewServer(8080, 8090)

	// 2. 프로토콜 핸들러 등록
	protocol.Register(server, func(sess protocol.ISession, msg any) {
		switch m := msg.(type) {
		case *protocol.Msg_AuthLoginReq:
			slog.Info("[TCP] 로그인 요청 수신", "nickname", m.Nickname)
			res := &protocol.Msg_AuthLoginRes{
				PlayerID: 1001, // 예제용 고정 ID
				Result:   uint32(protocol.Err_None),
			}
			sess.SendRaw(res.BuildTCP(protocol.Err_None))

		case *protocol.Msg_MessageSendReq:
			slog.Info("[TCP] 메시지 수신", "msg", m.Message)
			// 수신 확인 응답
			res := &protocol.Msg_MessageSendRes{
				Result: uint32(protocol.Err_None),
			}
			sess.SendRaw(res.BuildTCP(protocol.Err_None))

			// 에코 알림 (선택사항이지만 시나리오 확인용으로 좋음)
			notify := &protocol.Msg_MessageReceiveNotify{
				PlayerID: 1001,
				Nickname: "Server",
				Message:  "확인했습니다: " + m.Message,
			}
			sess.SendRaw(notify.BuildTCP(protocol.Err_None))

		case *protocol.Msg_SystemTCPHeartBitReq:
			// TCP 하트비트 응답
			res := &protocol.Msg_SystemTCPHeartBitRes{
				ServerTime: m.ServerTime,
			}
			sess.SendRaw(res.BuildTCP(protocol.Err_None))
		}
	})

	// 3. UDP 에코 핸들러 (저수준 OnPacket 후킹)
	// 클라이언트가 UDP로 보낸 하트비트를 그대로 에코해줍니다.
	server.OnPacket = func(hdr *base.HeaderUDP, body []byte, addr *net.UDPAddr) {
		// 언마샬러를 통해 어떤 패킷인지 확인
		msg, err := server.Unmarshaler(hdr.Command, body)
		if err != nil {
			return
		}

		if req, ok := msg.(*protocol.Msg_SystemUDPHeartBitReq); ok {
			slog.Info("[UDP] 하트비트 수신", "addr", addr.String(), "ts", req.Timestamp)

			// 응답 생성 (Res)
			res := &protocol.Msg_SystemUDPHeartBitRes{
				Timestamp: req.Timestamp,
			}

			// UDP로 다시 전송
			// sender ID는 클라이언트가 보낸 것을 그대로 사용하거나 0(서버)으로 설정
			respData := res.BuildUDP(0)
			server.UDP.SendTo(respData, addr.IP.String(), addr.Port)
		}
	}

	// 4. 서버 시작
	if err := server.Start(); err != nil {
		log.Fatalf("서버 시작 실패: %v", err)
	}

	slog.Info("🚀 ZLink 예제 서버 가동 중 (8080)")

	// 5. 종료 시그널 대기
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	<-sigCh

	server.Stop()
	slog.Info("서버 종료 완료")
}
