// Package network - 소켓 서버 프레임워크 통합 엔진 (Orchestrator)
package network

import (
	"log/slog"
	"net"

	"github.com/zoit/zo-socket-framework/engine/server-go/pkg/base"
	"github.com/zoit/zo-socket-framework/engine/server-go/pkg/config"
)

// Server - 프레임워크 통합 서버 객체
type Server struct {
	Config     *config.Config
	TCP        *TCPServer
	UDP        *UDPServer
	BufferPool *BufferPool
	
	// Unmarshaler - 바이트를 객체로 바꾸는 함수 (제네레이터가 제공)
	Unmarshaler func(cmd uint32, body []byte) (any, error)
	
	// OnRecvCallbacks - 여러 비즈니스 로직들이 등록할 수 있는 콜백 리스트
	OnRecvCallbacks []func(sess *Session, msg any)

	// 엔진 이벤트 핸들러
	OnConnect func(conn net.Conn)
	OnPacket  func(hdr *base.HeaderUDP, body []byte, addr *net.UDPAddr)
}

// NewServer - 새 서버 인스턴스 생성
func NewServer(cfg *config.Config) *Server {
	s := &Server{
		Config:          cfg,
		BufferPool:      NewBufferPool(),
		OnRecvCallbacks: make([]func(*Session, any), 0),
	}
	
	s.TCP = NewTCPServer("0.0.0.0", cfg.TCPPort, func(conn net.Conn) {
		if s.OnConnect != nil { s.OnConnect(conn) }
	})
	
	s.UDP = NewUDPServer("0.0.0.0", cfg.UDPPort, func(hdr *base.HeaderUDP, body []byte, addr *net.UDPAddr) {
		if s.OnPacket != nil { s.OnPacket(hdr, body, addr) }
	})
	
	return s
}

// AddRecvCallback - 새로운 패킷 리스너를 추가합니다 (+= 개념)
func (s *Server) AddRecvCallback(cb func(any, any)) {
	s.OnRecvCallbacks = append(s.OnRecvCallbacks, func(sess *Session, msg any) {
		cb(sess, msg)
	})
}

// SetUnmarshaler - 제네레이터가 호출하여 파싱 로직을 등록합니다.
func (s *Server) SetUnmarshaler(u func(uint32, []byte) (any, error)) {
	s.Unmarshaler = u
}

// Start, Stop 생략...
func (s *Server) Start() error {
	slog.Info("[Engine] 서버 가동", "tcp", s.Config.TCPPort, "udp", s.Config.UDPPort)
	if err := s.UDP.Listen(); err != nil { return err }
	if err := s.TCP.Listen(); err != nil { return err }
	go s.UDP.Start()
	go s.TCP.Start()
	return nil
}

func (s *Server) Stop() {
	s.TCP.Stop()
	s.UDP.Stop()
	slog.Info("[Engine] 서버 중지 완료")
}
