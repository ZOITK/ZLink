// Package network - 고성능 네트워크 세션 관리
package network

import (
	"encoding/binary"
	"fmt"
	"io"
	"log/slog"
	"net"
	"sync"
	"sync/atomic"
	"time"

	"zlink/base"
)

// ISession - 이제 base 패키지의 ISession을 사용합니다.
type ISession = base.ISession

// Session - 클라이언트 연결 세션 (Infrastructure SDK)
type Session struct {
	id           uint32
	mu           sync.Mutex
	conn         net.Conn      // TCP 연결 (nil일 수 있음)
	udpAddr      *net.UDPAddr  // 바인딩된 UDP 주소 (nil일 수 있음)
	server       *Server
	udpServer    *UDPServer    // 공용 UDP 전송 엔진
	LastActivity atomic.Int64  // 마지막 활동 시간 (UnixNano)
	Metadata     any
	RemoteAddr   string        // 대표 주소 문자열
}

// NewSession - 새 세션 생성
func NewSession(srv *Server, conn net.Conn, id uint32) *Session {
	addr := ""
	if conn != nil {
		addr = conn.RemoteAddr().String()
	}
	return &Session{
		id:         id,
		conn:       conn,
		server:     srv,
		RemoteAddr: addr,
	}
}

func (s *Session) ID() uint32           { return s.id }
func (s *Session) GetMetadata() any     { return s.Metadata }
func (s *Session) SetMetadata(data any) { s.Metadata = data }

func (s *Session) SetUDPServer(server *UDPServer) { s.udpServer = server }
func (s *Session) GetConn() net.Conn              { return s.conn }

// SetUDPAddr - UDP 주소를 바인딩합니다. (엔진에 의해 호출됨)
func (s *Session) SetUDPAddr(addr *net.UDPAddr) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.udpAddr = addr
	s.LastActivity.Store(time.Now().UnixNano())
}

// IsUDPReady - UDP 전송이 가능한 상태인지 확인합니다.
func (s *Session) IsUDPReady() bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.udpAddr != nil
}

// SendRaw - 원시 바이트 전송 (TCP)
func (s *Session) SendRaw(data []byte) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.conn == nil {
		return fmt.Errorf("연결 없음")
	}
	_, err := s.conn.Write(data)
	return err
}

// SendRawUDP - 바인딩된 UDP 주소로 원시 데이터 전송
func (s *Session) SendRawUDP(data []byte) error {
	s.mu.Lock()
	addr := s.udpAddr
	s.mu.Unlock()

	if addr == nil || s.udpServer == nil {
		return fmt.Errorf("UDP 바인딩되지 않았거나 서버가 설정되지 않음")
	}
	s.udpServer.SendTo(data, addr.IP.String(), addr.Port)
	return nil
}

func (s *Session) Close() {
	if s.conn != nil {
		s.conn.Close()
	}
}

// Start - 세션의 패킷 수신 루프를 시작합니다.
func (s *Session) Start() {
	for {
		// 1. 패킷 완성 (Framing)
		packet, err := s.tcpParser()
		if err != nil {
			if err != io.EOF {
				slog.Warn("[zLink/Session] 데이터 읽기 실패", "err", err, "addr", s.RemoteAddr)
			}
			break
		}

		// 2. 엔진의 통합 핸들러에 위임 (Organic Integration)
		s.server.HandlePacket(s, packet, nil)

		// 3. 임시 패킷 데이터는 GC 대상이 됨 (필요시 BufferPool로 관리 가능하지만 우선 단순화)
	}
	s.Close()
}

// tcpParser - 완성된 패킷 한 덩어리를 만들어냅니다. (ZLink 24B 표준 규격)
func (s *Session) tcpParser() ([]byte, error) {
	pool := s.server.BufferPool
	hdrSize := base.HeaderSize

	// 1. 헤더 먼저 읽기
	hdrBuf := pool.GetHeader()
	defer pool.PutHeader(hdrBuf)

	if _, err := io.ReadFull(s.conn, hdrBuf[:hdrSize]); err != nil {
		return nil, err
	}

	// 2. 유효성 검증 (Magic Number 'ZO') 및 길이 파악
	magic := binary.LittleEndian.Uint16(hdrBuf[0:2])
	if magic != base.MagicZO {
		return nil, fmt.Errorf("invalid magic number: %x", magic)
	}

	length := binary.LittleEndian.Uint32(hdrBuf[10:14]) // ZLink 표준 오프셋 10 (Version 4B 확장 반영)

	// 3. 전체 패킷 덩어리 생성 (Header + Body)
	fullPacket := make([]byte, hdrSize+int(length))
	copy(fullPacket[:hdrSize], hdrBuf[:hdrSize])

	if length > 0 {
		if _, err := io.ReadFull(s.conn, fullPacket[hdrSize:]); err != nil {
			return nil, err
		}
	}

	return fullPacket, nil
}
