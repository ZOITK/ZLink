package main

import (
	"log/slog"
	"net"
	"os"
	"os/signal"
	"sync"
	"syscall"

	"{{PROJECT_NAME}}/protocol"

	"github.com/ZOITK/ZLink/engine/server-go/pkg/config"
	"github.com/ZOITK/ZLink/engine/server-go/pkg/logger"
	"github.com/ZOITK/ZLink/engine/server-go/pkg/network"
)

// Player - 플레이어 정보
type Player struct {
	PlayerID uint32
	Nickname string
	Session  protocol.ISession
}

// BasicServer - 기본 서버 상태 관리
type BasicServer struct {
	mu      sync.RWMutex
	Players map[uint32]*Player // PlayerID -> Player
	nextID  uint32
}

var basicServer *BasicServer

func init() {
	basicServer = &BasicServer{
		Players: make(map[uint32]*Player),
		nextID:  1000,
	}
}

func main() {
	cfg := config.Load()
	logger.Init(cfg.NodeEnv)

	slog.Info("🚀 Basic Server Started / 기본 서버 시작됨")

	srv := network.NewServer(cfg)
	protocol.Register(srv, OnRecvPacket)

	srv.OnConnect = func(conn net.Conn) {
		sess := network.NewSession(conn)
		sess.SetUDPServer(srv.UDP)

		slog.Info("[Server] New client connected / 새 클라이언트 접속", "addr", sess.RemoteAddr)
		sess.HandleConnection(srv)
		slog.Info("[Server] Client disconnected / 클라이언트 접속 종료", "addr", sess.RemoteAddr)
		sess.Close()
	}

	if err := srv.Start(); err != nil {
		slog.Error("Server start failed / 서버 가동 실패", "err", err)
		os.Exit(1)
	}

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	<-sigCh

	slog.Info("Server shutting down / 서버 종료 중...")
	srv.Stop()
}

// OnRecvPacket - 패킷 수신 핸들러 (모든 메시지의 진입점)
func OnRecvPacket(s protocol.ISession, msg any) {
	switch m := msg.(type) {
	case *protocol.Msg_AuthLoginReq:
		handleLogin(s, m)

	case *protocol.Msg_MessageSendReq:
		handleMessage(s, m)

	case *protocol.Msg_SystemTCPHeartBitReq:
		handleHeartBeat(s, m)

	default:
		slog.Warn("[Handler] Unknown packet type / 미처리 패킷", "type", msg)
	}
}

// handleLogin - 로그인 처리
func handleLogin(s protocol.ISession, req *protocol.Msg_AuthLoginReq) {
	basicServer.mu.Lock()
	defer basicServer.mu.Unlock()

	playerID := basicServer.nextID
	basicServer.nextID++

	player := &Player{
		PlayerID: playerID,
		Nickname: req.Nickname,
		Session:  s,
	}

	basicServer.Players[playerID] = player

	slog.Info("[Login] Player logged in / 플레이어 로그인", "playerID", playerID, "nickname", req.Nickname)

	res := &protocol.Msg_AuthLoginRes{
		PlayerID: playerID,
		Result:   0, // Success
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))
}

// handleMessage - 메시지 처리 (에코 기능)
func handleMessage(s protocol.ISession, req *protocol.Msg_MessageSendReq) {
	basicServer.mu.Lock()
	defer basicServer.mu.Unlock()

	// 현재 세션의 플레이어 찾기
	var player *Player
	for _, p := range basicServer.Players {
		if p.Session == s {
			player = p
			break
		}
	}
	if player == nil {
		return
	}

	slog.Info("[Message] Received / 메시지 수신", "from", player.Nickname, "msg", req.Message)

	// 응답
	res := &protocol.Msg_MessageSendRes{
		Result: 0, // Success
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))

	// 모든 플레이어에게 메시지 브로드캐스트
	for _, p := range basicServer.Players {
		notifyMsg := &protocol.Msg_MessageReceiveNotify{
			PlayerID: player.PlayerID,
			Nickname: player.Nickname,
			Message:  req.Message,
		}
		_ = p.Session.SendRaw(notifyMsg.BuildTCP(protocol.Err_None))
	}
}

// handleHeartBeat - 하트비트 처리
func handleHeartBeat(s protocol.ISession, req *protocol.Msg_SystemTCPHeartBitReq) {
	res := &protocol.Msg_SystemTCPHeartBitRes{
		ServerTime: req.ServerTime,
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))
}
