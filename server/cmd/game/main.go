package main

import (
	"fmt"
	"log/slog"
	"math/rand"
	"net"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	"github.com/ZOITK/ZLink/examples/game/protocol"
	"github.com/ZOITK/ZLink/engine/server-go/config"
	"github.com/ZOITK/ZLink/engine/server-go/logger"
	"github.com/ZOITK/ZLink/engine/server-go/network"
)

// 플레이어 상태 상수
const (
	PlayerStateLogin = iota
	PlayerStateSearching
	PlayerStateInGame
)

// 게임 상태 상수
const (
	GameStateWaiting = iota
	GameStateInProgress
	GameStateFinished
)

// Player - 플레이어 정보 저장
type Player struct {
	PlayerID  uint32
	Nickname  string
	State     int
	Session   protocol.ISession
	RoomID    uint32
	GuessCount int
}

// Game - 게임 방 정보 저장
type Game struct {
	RoomID        uint32
	RoomName      string
	Status        int
	TargetNumber  uint32
	Players       map[uint32]*Player // PlayerID -> Player
	PlayersSlice  []*Player
	CreatedAt     time.Time
	HostPlayerID  uint32
	IsMultiplayer uint32 // 0: 싱글플레이, 1: 멀티플레이
}

// GameServer - 게임 서버 전체 상태 관리
type GameServer struct {
	mu              sync.RWMutex
	Players         map[uint32]*Player      // PlayerID -> Player
	Rooms           map[uint32]*Game        // RoomID -> Game
	WaitingPlayers  []*Player               // 대기 중인 플레이어
	nextPlayerID    uint32
	nextRoomID      uint32
}

var gameServer *GameServer

func init() {
	gameServer = &GameServer{
		Players:        make(map[uint32]*Player),
		Rooms:          make(map[uint32]*Game),
		WaitingPlayers: make([]*Player, 0),
		nextPlayerID:   1000,
		nextRoomID:     1,
	}
}

func main() {
	cfg := config.Load()
	logger.Init(cfg.NodeEnv)

	slog.Info("🎮 게임 서버 시작")

	srv := network.NewServer(cfg)
	protocol.Register(srv, OnRecvPacket)

	// 새 클라이언트 연결 처리
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

	// Graceful shutdown
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	<-sigCh

	slog.Info("서버 종료 중...")
	srv.Stop()
}

// OnRecvPacket - 메시지 수신 핸들러 (모든 패킷의 진입점)
func OnRecvPacket(s protocol.ISession, msg any) {
	switch m := msg.(type) {
	case *protocol.Msg_AuthLoginReq:
		handleLogin(s, m)

	case *protocol.Msg_RoomSearchReq:
		handleRoomSearch(s)

	case *protocol.Msg_RoomCreateReq:
		handleRoomCreate(s, m)

	case *protocol.Msg_RoomJoinReq:
		handleRoomJoin(s, m)

	case *protocol.Msg_GameGuessReq:
		handleGuess(s, m)

	case *protocol.Msg_GameWinReq:
		handleWin(s, m)

	case *protocol.Msg_GameChatReq:
		handleChat(s, m)

	case *protocol.Msg_SystemTCPHeartBitReq:
		handleHeartBeat(s, m)

	default:
		slog.Warn("[Handler] 미처리 패킷 수신", "type", fmt.Sprintf("%T", msg))
	}
}

// handleLogin - 로그인 처리
// 플레이어를 등록하고 PlayerID를 발급함
func handleLogin(s protocol.ISession, req *protocol.Msg_AuthLoginReq) {
	gameServer.mu.Lock()
	defer gameServer.mu.Unlock()

	playerID := gameServer.nextPlayerID
	gameServer.nextPlayerID++

	player := &Player{
		PlayerID: playerID,
		Nickname: req.Nickname,
		State:    PlayerStateLogin,
		Session:  s,
	}

	gameServer.Players[playerID] = player
	slog.Info("[Login] 플레이어 로그인", "playerID", playerID, "nickname", req.Nickname)

	// 응답
	res := &protocol.Msg_AuthLoginRes{
		PlayerID: playerID,
		Result:   0, // Success
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))
}

// handleRoomSearch - 대기 중인 게임 방 검색
// 현재 대기 중인 플레이어가 있으면 게임을 생성함
func handleRoomSearch(s protocol.ISession) {
	gameServer.mu.Lock()
	defer gameServer.mu.Unlock()

	// 플레이어 찾기
	var player *Player
	for _, p := range gameServer.Players {
		if p.Session == s {
			player = p
			break
		}
	}
	if player == nil {
		return
	}

	// 사용 가능한 방 조회 (멀티플레이만 검색)
	var availableRooms []*protocol.Msg_RoomInfo
	for _, game := range gameServer.Rooms {
		if game.IsMultiplayer == 1 && game.Status == GameStateWaiting && len(game.Players) == 1 {
			availableRooms = append(availableRooms, &protocol.Msg_RoomInfo{
				RoomID:        game.RoomID,
				RoomName:      game.RoomName,
				HostPlayerID:  game.HostPlayerID,
				HostNickname:  gameServer.Players[game.HostPlayerID].Nickname,
				PlayerCount:   uint32(len(game.Players)),
				Status:        uint32(game.Status),
				IsMultiplayer: game.IsMultiplayer,
			})
		}
	}

	slog.Info("[RoomSearch] 검색 완료", "playerID", player.PlayerID, "rooms", len(availableRooms))

	res := &protocol.Msg_RoomSearchRes{
		Rooms:  availableRooms,
		Result: 0, // Success
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))
}

// handleRoomCreate - 새 게임 방 생성
// 플레이어를 방의 host로 설정하고 대기 상태로 전환
func handleRoomCreate(s protocol.ISession, req *protocol.Msg_RoomCreateReq) {
	gameServer.mu.Lock()
	defer gameServer.mu.Unlock()

	// 플레이어 찾기
	var player *Player
	for _, p := range gameServer.Players {
		if p.Session == s {
			player = p
			break
		}
	}
	if player == nil {
		return
	}

	roomID := gameServer.nextRoomID
	gameServer.nextRoomID++

	game := &Game{
		RoomID:        roomID,
		RoomName:      req.RoomName,
		Status:        GameStateWaiting,
		Players:       make(map[uint32]*Player),
		PlayersSlice:  make([]*Player, 0),
		CreatedAt:     time.Now(),
		HostPlayerID:  player.PlayerID,
		IsMultiplayer: req.IsMultiplayer,
	}

	player.RoomID = roomID
	player.State = PlayerStateInGame
	game.Players[player.PlayerID] = player
	game.PlayersSlice = append(game.PlayersSlice, player)

	// 싱글플레이면 바로 게임 시작, 멀티플레이면 대기
	if req.IsMultiplayer == 0 {
		// 싱글플레이: 게임 즉시 시작
		game.Status = GameStateInProgress
		game.TargetNumber = uint32(rand.Intn(100) + 1)
		slog.Info("[RoomCreate] 싱글플레이 방 생성 및 게임 시작", "roomID", roomID, "hostID", player.PlayerID, "targetNumber", game.TargetNumber)

		// 게임 시작 알림 전송
		notifyMsg := &protocol.Msg_RoomGameStartNotify{
			TargetNumber: game.TargetNumber,
			MaxNumber:    100,
		}
		_ = player.Session.SendRaw(notifyMsg.BuildTCP(protocol.Err_None))
	} else {
		// 멀티플레이: 다른 플레이어 대기
		game.Status = GameStateWaiting
		player.State = PlayerStateSearching
		slog.Info("[RoomCreate] 멀티플레이 방 생성 완료", "roomID", roomID, "hostID", player.PlayerID, "roomName", req.RoomName)
	}

	gameServer.Rooms[roomID] = game

	res := &protocol.Msg_RoomCreateRes{
		RoomID: roomID,
		Result: 0, // Success
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))
}

// handleRoomJoin - 기존 게임 방 입장
// 두 번째 플레이어가 입장하면 게임 시작
func handleRoomJoin(s protocol.ISession, req *protocol.Msg_RoomJoinReq) {
	gameServer.mu.Lock()
	defer gameServer.mu.Unlock()

	// 플레이어 찾기
	var player *Player
	for _, p := range gameServer.Players {
		if p.Session == s {
			player = p
			break
		}
	}
	if player == nil {
		return
	}

	// 방 찾기
	game, exists := gameServer.Rooms[req.RoomID]
	if !exists || game.Status != GameStateWaiting || len(game.Players) != 1 || game.IsMultiplayer != 1 {
		res := &protocol.Msg_RoomJoinRes{
			RoomID: req.RoomID,
			Result: 3, // NotFound
		}
		_ = s.SendRaw(res.BuildTCP(protocol.Err_NotFound))
		return
	}

	// 플레이어 추가
	player.RoomID = req.RoomID
	player.State = PlayerStateInGame
	game.Players[player.PlayerID] = player
	game.PlayersSlice = append(game.PlayersSlice, player)

	// 게임 시작
	hostID := game.HostPlayerID
	game.Status = GameStateInProgress
	game.TargetNumber = uint32(rand.Intn(100) + 1) // 1~100

	slog.Info("[RoomJoin] 게임 시작", "roomID", req.RoomID, "players", len(game.PlayersSlice))

	// 입장한 플레이어에게 응답
	hostNickname := gameServer.Players[hostID].Nickname
	res := &protocol.Msg_RoomJoinRes{
		RoomID:               req.RoomID,
		OpponentPlayerID:     hostID,
		OpponentNickname:     hostNickname,
		Result:               0, // Success
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))

	// 모든 플레이어에게 게임 시작 알림
	for _, p := range game.PlayersSlice {
		notifyMsg := &protocol.Msg_RoomGameStartNotify{
			TargetNumber: game.TargetNumber,
			MaxNumber:    100,
		}
		_ = p.Session.SendRaw(notifyMsg.BuildTCP(protocol.Err_None))
	}
}

// handleGuess - 숫자 맞추기
// 정답이 아니면 힌트를 반환 (0: 너무 작음, 1: 너무 큼, 2: 정답)
func handleGuess(s protocol.ISession, req *protocol.Msg_GameGuessReq) {
	gameServer.mu.Lock()
	defer gameServer.mu.Unlock()

	// 플레이어 찾기
	var player *Player
	for _, p := range gameServer.Players {
		if p.Session == s {
			player = p
			break
		}
	}
	if player == nil {
		return
	}

	// 게임 찾기
	game, exists := gameServer.Rooms[player.RoomID]
	if !exists || game.Status != GameStateInProgress {
		return
	}

	player.GuessCount++

	var hint uint32
	if req.GuessNumber < game.TargetNumber {
		hint = 0 // 너무 작음
	} else if req.GuessNumber > game.TargetNumber {
		hint = 1 // 너무 큼
	} else {
		hint = 2 // 정답 (별도로 Win 메시지로 처리)
	}

	slog.Info("[Guess] 숫자 맞추기", "playerID", player.PlayerID, "guess", req.GuessNumber, "hint", hint)

	// 응답
	res := &protocol.Msg_GameGuessRes{
		Result: 0, // Success
		Hint:   hint,
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))

	// 다른 플레이어에게 알림
	for _, p := range game.PlayersSlice {
		if p.PlayerID != player.PlayerID {
			notifyMsg := &protocol.Msg_GameGuessNotify{
				PlayerID:    player.PlayerID,
				Nickname:    player.Nickname,
				GuessNumber: req.GuessNumber,
				Hint:        hint,
			}
			_ = p.Session.SendRaw(notifyMsg.BuildTCP(protocol.Err_None))
		}
	}
}

// handleWin - 게임 승리 (정답을 맞춤)
// 게임을 종료하고 모든 플레이어에게 결과 알림
func handleWin(s protocol.ISession, req *protocol.Msg_GameWinReq) {
	gameServer.mu.Lock()
	defer gameServer.mu.Unlock()

	// 플레이어 찾기
	var player *Player
	for _, p := range gameServer.Players {
		if p.Session == s {
			player = p
			break
		}
	}
	if player == nil {
		return
	}

	// 게임 찾기
	game, exists := gameServer.Rooms[player.RoomID]
	if !exists || game.Status != GameStateInProgress {
		return
	}

	// 게임 종료
	game.Status = GameStateFinished

	slog.Info("[Win] 게임 승리", "roomID", player.RoomID, "winner", player.PlayerID, "targetNumber", game.TargetNumber, "tryCount", player.GuessCount)

	// 응답
	res := &protocol.Msg_GameWinRes{
		Result: 0, // Success
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))

	// 모든 플레이어에게 게임 결과 알림
	for _, p := range game.PlayersSlice {
		winMsg := &protocol.Msg_GameWinNotify{
			WinnerPlayerID:   player.PlayerID,
			WinnerNickname:   player.Nickname,
			CorrectNumber:    game.TargetNumber,
			TryCount:         uint32(player.GuessCount),
		}
		_ = p.Session.SendRaw(winMsg.BuildTCP(protocol.Err_None))
	}
}

// handleChat - 게임 내 채팅
// 같은 방의 모든 플레이어에게 메시지 전송
func handleChat(s protocol.ISession, req *protocol.Msg_GameChatReq) {
	gameServer.mu.Lock()
	defer gameServer.mu.Unlock()

	// 플레이어 찾기
	var player *Player
	for _, p := range gameServer.Players {
		if p.Session == s {
			player = p
			break
		}
	}
	if player == nil {
		return
	}

	// 게임 찾기
	game, exists := gameServer.Rooms[player.RoomID]
	if !exists {
		return
	}

	slog.Debug("[Chat] 채팅 메시지", "playerID", player.PlayerID, "message", req.Message)

	// 응답
	res := &protocol.Msg_GameChatRes{
		Result: 0, // Success
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))

	// 모든 플레이어에게 채팅 메시지 전송
	for _, p := range game.PlayersSlice {
		chatMsg := &protocol.Msg_GameChatNotify{
			PlayerID: player.PlayerID,
			Nickname: player.Nickname,
			Message:  req.Message,
		}
		_ = p.Session.SendRaw(chatMsg.BuildTCP(protocol.Err_None))
	}
}

// handleHeartBeat - TCP 하트비트 (연결 유지)
func handleHeartBeat(s protocol.ISession, req *protocol.Msg_SystemTCPHeartBitReq) {
	res := &protocol.Msg_SystemTCPHeartBitRes{
		ServerTime: time.Now().UnixMilli(),
	}
	_ = s.SendRaw(res.BuildTCP(protocol.Err_None))
}
