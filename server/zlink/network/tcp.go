// Package network - TCP 서버 엔진
package network

import (
	"log/slog"
	"net"
	"strconv"
	"strings"
	"sync/atomic"
	"time"
)

// TCPStats - TCP 통계
type TCPStats struct {
	PacketsRecv atomic.Int64
	PacketsSent atomic.Int64
}

// TCPServer - TCP 서버 엔진
type TCPServer struct {
	host     string
	port     int
	listener net.Listener
	Stats    TCPStats
	
	// 새 연결 발생 시 상위 레이어에서 처리할 핸들러
	onConnect func(conn net.Conn)
}

// NewTCPServer - TCP 서버 인스턴스 생성
func NewTCPServer(host string, port int, onConnect func(conn net.Conn)) *TCPServer {
	return &TCPServer{
		host:      host,
		port:      port,
		onConnect: onConnect,
	}
}

// Listen - 포트 바인딩
func (s *TCPServer) Listen() error {
	addr := s.host + ":" + strconv.Itoa(s.port)
	ln, err := net.Listen("tcp4", addr)
	if err != nil {
		return err
	}
	s.listener = ln
	slog.Info("[TCPServer] 포트 바인딩 완료", "addr", addr)
	return nil
}

// Start - TCP 수락(Accept) 루프 시작
func (s *TCPServer) Start() error {
	if s.listener == nil {
		if err := s.Listen(); err != nil {
			return err
		}
	}
	
	for {
		conn, err := s.listener.Accept()
		if err != nil {
			if strings.Contains(err.Error(), "closed network connection") {
				return nil
			}
			slog.Warn("[TCPServer] Accept 오류", "err", err)
			continue
		}

		// 성능 최적화 설정
		if tc, ok := conn.(*net.TCPConn); ok {
			tc.SetNoDelay(true)
			tc.SetKeepAlive(true)
			tc.SetKeepAlivePeriod(15 * time.Second)
		}

		// 비즈니스 레이어의 세션 생성 핸들러로 전달
		go s.onConnect(conn)
	}
}

// Stop - 서버 중지
func (s *TCPServer) Stop() {
	if s.listener != nil {
		s.listener.Close()
	}
}
