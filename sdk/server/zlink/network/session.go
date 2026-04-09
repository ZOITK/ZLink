// Package network - 고성능 네트워크 세션 관리
package network

import (
	"fmt"
	"io"
	"log/slog"
	"net"
	"sync"
	"sync/atomic"

	"zlink/base"
)

// Session - 클라이언트 연결 세션 (Infrastructure SDK)
type Session struct {
	mu         sync.Mutex
	conn       net.Conn
	udpServer  *UDPServer
	UDPChecked atomic.Bool
	Metadata   any
	RemoteAddr string
}

// NewSession - 새 세션 생성
func NewSession(conn net.Conn) *Session {
	addr := ""
	if conn != nil { addr = conn.RemoteAddr().String() }
	return &Session{ conn: conn, RemoteAddr: addr }
}

func (s *Session) SetUDPServer(server *UDPServer) { s.udpServer = server }
func (s *Session) GetConn() net.Conn { return s.conn }

// SendRaw - 원시 바이트 전송 (TCP)
func (s *Session) SendRaw(data []byte) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.conn == nil { return fmt.Errorf("연결 없음") }
	_, err := s.conn.Write(data)
	return err
}

// SendRawUDP - 원시 바이트 UDP 전송
func (s *Session) SendRawUDP(data []byte, addr string, port int) error {
	if s.udpServer == nil { return fmt.Errorf("UDP 서버 없음") }
	s.udpServer.SendTo(data, addr, port)
	return nil
}

func (s *Session) Close() {
	if s.conn != nil { s.conn.Close() }
}

// HandleConnection - 세션의 패킷 수신 루프를 시작합니다.
// 서버에 설정된 Unmarshaler와 OnRecvPacket을 사용하여 자동으로 비즈니스 로직을 연결합니다.
func (s *Session) HandleConnection(srv *Server) {
	for {
		// 1. 패킷 파싱 (엔진 기본 파서 사용)
		cmd, body, err := s.tcpParser(srv)
		if err != nil {
			if err != io.EOF { slog.Warn("[Session] 데이터 읽기 실패", "err", err, "addr", s.RemoteAddr) }
			break
		}
		
		// 2. 자동 객체 변환 및 등록된 모든 비즈니스 로직 호출
		if srv.Unmarshaler != nil {
			msg, err := srv.Unmarshaler(cmd, body)
			if err == nil && msg != nil {
				// 등록된 모든 리스너에게 객체 전달
				for _, callback := range srv.OnRecvCallbacks {
					callback(s, msg)
				}
			}
		}

		// 3. 버퍼 반납
		if body != nil { srv.BufferPool.PutBody(body) }
	}
}

// tcpParser - 내부용 패킷 읽기 도구
func (s *Session) tcpParser(srv *Server) (uint32, []byte, error) {
	pool := srv.BufferPool
	hdrSize := srv.TCPHeaderSize
	hdrBuf := pool.GetHeader() // GetHeader는 충분한 크기(예: 64바이트)를 반환한다고 가정함
	defer pool.PutHeader(hdrBuf)

	// 정해진 크기만큼 헤더 읽기
	if _, err := io.ReadFull(s.conn, hdrBuf[:hdrSize]); err != nil { return 0, nil, err }

	hdr := &base.HeaderTCP{}
	if err := hdr.Decode(hdrBuf[:hdrSize]); err != nil { return 0, nil, err }

	var body []byte
	if hdr.Length > 0 {
		body = pool.GetBody(hdr.Length)
		if _, err := io.ReadFull(s.conn, body); err != nil {
			pool.PutBody(body)
			return 0, nil, err
		}
	}
	return hdr.Command, body, nil
}
