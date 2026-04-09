// Package network - 소켓 서버 프레임워크 통합 엔진 (Orchestrator)
package network

import (
	"log/slog"
	"net"
	"sync/atomic"

	 "github.com/ZOITK/ZLink/sdk/server/zlink/base"
)

// Server - 프레임워크 통합 서버 객체
type Server struct {
	TCPPort       int
	UDPPort       int
	TCP           *TCPServer
	UDP           *UDPServer
	BufferPool    *BufferPool
	lastSessionID uint32
	
	// Unmarshaler - 바이트를 객체로 바꾸는 함수 (제네레이터가 제공)
	Unmarshaler func(cmd uint32, body []byte) (any, error)
	
	// OnRecvCallbacks - 여러 비즈니스 로직들이 등록할 수 있는 콜백 리스트
	OnRecvCallbacks []func(sess *Session, msg any)

	// 고수준 엔진 이벤트 핸들러 (사용자용)
	OnSessionOpen  func(sess *Session)
	OnSessionClose func(sess *Session)

	// 저수준 엔진 이벤트 핸들러 (내부/고급용)
	OnConnect func(conn net.Conn)
	OnPacket  func(hdr *base.HeaderUDP, body []byte, addr *net.UDPAddr)

	// 헤더 정보 (제네레이터에 의해 설정됨)
	TCPHeaderSize int
	UDPHeaderSize int

	// TCPHeaderDecoder - 주입받은 헤더 해석용 함수 (바이트 -> 명령ID, 바디길이, 에러코드)
	TCPHeaderDecoder func(data []byte) (uint32, uint32, uint32, error)
}

// NewServer - 새 서버 인스턴스 생성
// 사용자의 의견에 따라 포트 정보를 외부(애플리케이션)에서 직접 주입받습니다.
func NewServer(tcpPort, udpPort int) *Server {
	s := &Server{
		TCPPort:         tcpPort,
		UDPPort:         udpPort,
		BufferPool:      NewBufferPool(),
		OnRecvCallbacks: make([]func(*Session, any), 0),
		TCPHeaderSize:   base.TCPHeaderSize, // 기본값
		UDPHeaderSize:   base.UDPHeaderSize, // 기본값
	}
	
	// TCP 서버 초기화 시 세션 라이프사이클 자동화 핸들러 등록
	s.TCP = NewTCPServer("0.0.0.0", tcpPort, s.handleNewConnection)
	
	s.UDP = NewUDPServer("0.0.0.0", udpPort, func(data []byte, addr *net.UDPAddr) {
		// [정규화] 저수준 패킷 훅이 있으면 원시 데이터 그대로 전달
		if s.OnPacket != nil {
			// 기존 OnPacket의 hdr 인자를 nil로 보내거나, OnPacket 자체의 시그니처 변경 고려 (현재는 nil 전달)
			s.OnPacket(nil, data, addr)
		}
	})
	
	return s
}

// handleNewConnection - 내부용 세션 라이프사이클 관리자
func (s *Server) handleNewConnection(conn net.Conn) {
	// 1. 소켓 연결 즉시 로깅
	remoteAddr := conn.RemoteAddr().String()
	slog.Info("[zLink/Engine] 새로운 TCP 연결 수락", "addr", remoteAddr)

	// 2. 저수준 훅 호출 (커스텀 처리가 필요한 경우)
	if s.OnConnect != nil {
		s.OnConnect(conn)
		return
	}

	// 3. 표준 세션 생성 및 초기화
	id := atomic.AddUint32(&s.lastSessionID, 1)
	sess := NewSession(id, conn)
	sess.SetUDPServer(s.UDP)

	// 4. 엔진 레벨 세션 오픈 이벤트
	if s.OnSessionOpen != nil {
		s.OnSessionOpen(sess)
	}

	// 5. 통신 루프 시작 (블로킹)
	slog.Info("[zLink/Session] 세션 통신 시작", "session_id", id, "addr", remoteAddr)
	sess.HandleConnection(s)

	// 6. 엔진 레벨 세션 종료 이벤트
	if s.OnSessionClose != nil {
		s.OnSessionClose(sess)
	}

	// 7. 자원 정리 및 종료 로깅
	sess.Close()
	slog.Info("[zLink/Session] 세션 연결 종료", "session_id", id, "addr", remoteAddr)
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

// SetHeaderInfo - 제네레이터가 호출하여 헤더 크기와 디코더를 설정합니다.
func (s *Server) SetHeaderInfo(tcpSize, udpSize int, decoder func([]byte) (uint32, uint32, uint32, error)) {
	s.TCPHeaderSize = tcpSize
	s.UDPHeaderSize = udpSize
	s.TCPHeaderDecoder = decoder
}

// Start, Stop 생략...
func (s *Server) Start() error {
	slog.Info("[zLink/Engine] 서버 가동 시작", "tcp", s.TCPPort, "udp", s.UDPPort)
	if err := s.UDP.Listen(); err != nil { return err }
	if err := s.TCP.Listen(); err != nil { return err }
	go s.UDP.Start()
	go s.TCP.Start()
	return nil
}

func (s *Server) Stop() {
	s.TCP.Stop()
	s.UDP.Stop()
	slog.Info("[zLink/Engine] 서버 중지 완료")
}
