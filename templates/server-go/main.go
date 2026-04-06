package main

import (
	"fmt"
	"log/slog"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"

	"__PROJECT_NAME__/protocol"

	"github.com/zoit/zo-socket-framework/engine/server-go/pkg/config"
	"github.com/zoit/zo-socket-framework/engine/server-go/pkg/logger"
	"github.com/zoit/zo-socket-framework/engine/server-go/pkg/network"
)

func main() {
	cfg := config.Load()
	logger.Init(cfg.NodeEnv)

	slog.Info("ZPP Framework Unified Example Server 시작")

	srv := network.NewServer(cfg)

	// [통일된 사용법] Register 한 줄로 프로토콜과 핸들러 바인딩
	protocol.Register(srv, OnRecvPacket)

	srv.OnConnect = func(conn net.Conn) {
		sess := network.NewSession(conn)
		sess.SetUDPServer(srv.UDP)

		slog.Info("[Server] 새 클라이언트 접속", "addr", sess.RemoteAddr)
		sess.HandleConnection(srv)
		slog.Info("[Server] 클라이언트 접속 종료", "addr", sess.RemoteAddr)
		sess.Close()
	}

	if err := srv.Start(); err != nil {
		slog.Error("서버 가동 실패", "err", err)
		os.Exit(1)
	}

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	<-sigCh
	srv.Stop()
}

// OnRecvPacket - 파이썬 예제와 100% 동일한 비즈니스 로직
func OnRecvPacket(s protocol.ISession, msg any) {
	switch m := msg.(type) {
	case *protocol.Msg_AuthLoginReq:
		slog.Info("[Handler] 로그인 요청 수신", "id", m.LoginID)

		// 응답 패킷 전송 (BuildTCP 사용)
		res := &protocol.Msg_AuthLoginRes{
			UserIdx:   12345,
			StartTime: time.Now().UnixMilli(),
			Result:    uint32(protocol.Err_None),
		}
		_ = s.SendRaw(res.BuildTCP(protocol.Err_None))

	case *protocol.Msg_SystemTCPHeartBitReq:
		slog.Debug("[Handler] 하트비트 수신", "clientTime", m.ServerTime)

		// 하트비트 응답 전송
		res := &protocol.Msg_SystemTCPHeartBitRes{
			ServerTime: m.ServerTime,
		}
		_ = s.SendRaw(res.BuildTCP(protocol.Err_None))

	default:
		slog.Warn("[Handler] 미처리 패킷 수신", "type", fmt.Sprintf("%T", msg))
	}
}
