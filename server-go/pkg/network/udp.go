// Package network - UDP 서버 엔진
package network

import (
	"log/slog"
	"net"
	"strconv"
	"strings"
	"sync/atomic"

	"github.com/ZOITK/ZLink/engine/server-go/base"
)

// UDPStats - UDP 통계
type UDPStats struct {
	PacketsRecv atomic.Int64
	PacketsSent atomic.Int64
}

// UDPServer - UDP 서버 엔진
type UDPServer struct {
	host     string
	port     int
	conn     *net.UDPConn
	Stats    UDPStats
	
	// 패킷 수신 시 처리할 핸들러
	onPacket func(hdr *base.HeaderUDP, body []byte, addr *net.UDPAddr)
}

// NewUDPServer - UDP 서버 인스턴스 생성
func NewUDPServer(host string, port int, onPacket func(hdr *base.HeaderUDP, body []byte, addr *net.UDPAddr)) *UDPServer {
	return &UDPServer{
		host:     host,
		port:     port,
		onPacket: onPacket,
	}
}

// Listen - UDP 포트 바인딩
func (s *UDPServer) Listen() error {
	addr := s.host + ":" + strconv.Itoa(s.port)
	udpAddr, err := net.ResolveUDPAddr("udp4", addr)
	if err != nil {
		return err
	}
	
	conn, err := net.ListenUDP("udp4", udpAddr)
	if err != nil {
		return err
	}
	s.conn = conn
	slog.Info("[UDPServer] 포트 바인딩 완료", "addr", addr)
	return nil
}

// Start - UDP 패킷 수신 루프 시작
func (s *UDPServer) Start() error {
	if s.conn == nil {
		if err := s.Listen(); err != nil {
			return err
		}
	}
	
	buf := make([]byte, 2048) // 최대 패킷 크기 (MTU 고려)
	for {
		n, addr, err := s.conn.ReadFromUDP(buf)
		if err != nil {
			if strings.Contains(err.Error(), "use of closed network connection") {
				return nil
			}
			slog.Warn("[UDPServer] ReadFromUDP 오류", "err", err)
			continue
		}

		s.Stats.PacketsRecv.Add(1)
		
		// 최소 헤더 크기 확인
		if n < base.UDPHeaderSize {
			continue
		}

		hdr := &base.HeaderUDP{}
		if err := hdr.Decode(buf[:base.UDPHeaderSize]); err != nil {
			continue
		}

		body := buf[base.UDPHeaderSize:n]
		s.onPacket(hdr, body, addr)
	}
}

// SendTo - 특정 주소로 데이터 전송
func (s *UDPServer) SendTo(data []byte, ip string, port int) {
	if s.conn == nil {
		return
	}
	
	addr, err := net.ResolveUDPAddr("udp4", ip+":"+strconv.Itoa(port))
	if err != nil {
		return
	}
	
	_, err = s.conn.WriteToUDP(data, addr)
	if err == nil {
		s.Stats.PacketsSent.Add(1)
	}
}

// Stop - 서버 중지
func (s *UDPServer) Stop() {
	if s.conn != nil {
		s.conn.Close()
	}
}
