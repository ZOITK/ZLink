// Package network - 소켓 서버 프레임워크 통합 엔진 (Orchestrator)
package network

import (
	"fmt"
	"encoding/binary"
	"log/slog"
	"net"
	"sync"
	"sync/atomic"
	"time"

	"github.com/ZOITK/ZLink/sdk/server/zlink/base"
)

// Server - 프레임워크 통합 서버 객체 (TCP/UDP 관리 및 프로토콜 연동)
type Server struct {
	TCPPort       int
	UDPPort       int
	TCP           *TCPServer
	UDP           *UDPServer
	BufferPool    *BufferPool
	lastSessionID uint32

	// UDPIdleTimeout - UDP 전용 세션이 이 시간 동안 무활동이면 만료(누수 방지). 0이면 리퍼 비활성.
	UDPIdleTimeout time.Duration

	// Sessions - 활성화된 세션 통합 관리
	sessions      sync.Map // map[uint32]*Session

	// udpSessions - UDP Standalone 모드 전용: addr.String() -> *Session
	udpSessions   sync.Map

	// Protocol - 엔진이 학습한 프로토콜 정보 (Organic Integration)
	Protocol base.ProtocolInfo

	// 비즈니스 및 이벤트 콜백
	OnRecvCallbacks []func(sess base.ISession, msg any)
	OnSessionOpen   func(sess *Session)
	OnSessionClose  func(sess *Session)
	OnConnect       func(conn net.Conn)
}

// getNextSessionID - 다음 SessionID를 할당합니다 (1001부터 시작, 오버플로우 시 1000으로 회귀)
func (s *Server) getNextSessionID() uint32 {
	id := atomic.AddUint32(&s.lastSessionID, 1)
	if id == 0 {
		// uint32 오버플로우 발생 → 1000으로 리셋
		atomic.StoreUint32(&s.lastSessionID, 1000)
		id = 1001
	}
	return id
}

// SetProtocol - 엔진에 프로토콜 정의를 주입합니다 (유기적 통합)
func (s *Server) SetProtocol(info base.ProtocolInfo) {
	s.Protocol = info
}

// getOrCreateUDPSession - UDP Standalone 모드 전용: UDPAddr로 세션 조회 또는 신규 생성
func (s *Server) getOrCreateUDPSession(addr *net.UDPAddr) *Session {
	key := addr.String()

	id := s.getNextSessionID()
	newSess := NewSession(s, nil, id) // conn=nil (UDP 전용 세션)
	newSess.SetUDPAddr(addr)
	newSess.SetUDPServer(s.UDP)

	actual, loaded := s.udpSessions.LoadOrStore(key, newSess)
	if loaded {
		// 이미 존재 → 새로 만든 세션 폐기, 기존 세션 반환 및 액티비티 갱신
		existing := actual.(*Session)
		existing.LastActivity.Store(time.Now().UnixNano())
		return existing
	}

	// 새로 등록: SessionID 기반 조회도 지원하도록 sessions에도 등록
	s.sessions.Store(id, newSess)
	if s.OnSessionOpen != nil {
		s.OnSessionOpen(newSess)
	}
	return newSess
}

// HandlePacket - 수신된 원시 패킷을 프로토콜 정의에 따라 자동으로 메시지로 변환하여 전달
func (s *Server) HandlePacket(sess base.ISession, data []byte, addr *net.UDPAddr) {
	// 1. 헤더 유효성 및 기본 정보 추출
	if len(data) < base.HeaderSize {
		return
	}

	magic := binary.LittleEndian.Uint16(data[0:2])
	if magic != base.MagicZO {
		return
	}

	cmd := binary.LittleEndian.Uint32(data[6:10])
	sessionID := binary.LittleEndian.Uint32(data[14:18])
	// 2. [서버 권위 세션 식별] 정합성 판단은 100% 서버가 한다.
	//    클라가 '송신을 참는' 식의 책임을 지지 않으며, 서버 발급 ID가 없는
	//    UDP는 신뢰하지 않고 드롭한다. (IP 추측 휴리스틱 제거)
	if sess == nil && addr != nil {
		if sessionID > 0 {
			// 2-1. 정규 ID 경로: 서버가 발급한 세션에만 바인딩 (최초 1회 잠금)
			if val, ok := s.sessions.Load(sessionID); ok {
				realSess := val.(*Session)
				if realSess.TryBindUDP(addr) {
					sess = realSess
				} else {
					// 잠긴 세션에 다른 주소 → 하이재킹/오발신/NAT 재매핑 → 드롭
					return
				}
			} else {
				// 미지(만료/위조) ID → 드롭
				return
			}
		} else if s.TCP == nil {
			// 2-2. UDP 단독 모드: ID=0은 정상. 주소(IP:port) 기준으로 세션 식별.
			//      full addr 키라 같은 공인 IP의 다른 단말(다른 port)은 자연히 분리됨(NAT-safe).
			sess = s.getOrCreateUDPSession(addr)
		} else {
			// 2-3. 혼합 모드에서 ID=0 → 클라가 아직 ID를 학습하기 전. 추측하지 않고 드롭.
			return
		}
	}

	// 세션을 찾지 못한 경우 드롭 (TCPBound에서만 발생)
	if sess == nil {
		return
	}

	// 3. 바디 추출
	body := data[base.HeaderSize:]

	// 4. 언마샬링
	if s.Protocol.Unmarshaler == nil {
		return
	}
	msg, err := s.Protocol.Unmarshaler(cmd, body)
	if err != nil {
		return
	}

	// 5. 비즈니스 콜백 호출
	for _, cb := range s.OnRecvCallbacks {
		cb(sess, msg)
	}
}

// Send - 메시지를 프로토콜 정의에 따라 포장하여 전송 (유기적/투명 송신)
func (s *Server) Send(sess base.ISession, msg any) error {
	if sess == nil {
		return fmt.Errorf("세션이 없습니다")
	}
	if s.Protocol.Packer == nil {
		return fmt.Errorf("프로토콜 패커(Packer)가 설정되지 않았습니다")
	}

	// 1. 객체를 패킷 바이트로 변환 (UDP 우선 순위 또는 바인딩 여부에 따라 자동 결정 가능)
	// 현재는 명시적으로 호출자가 ISession 인터페이스를 통해 결정하거나 내부 정책을 따름
	useUDP := sess.IsUDPReady()
	data, err := s.Protocol.Packer(msg, useUDP, sess.ID())
	if err != nil {
		return err
	}

	// 2. 실제 전송
	if useUDP {
		return sess.SendRawUDP(data)
	}
	return sess.SendRaw(data)
}

// BroadcastUDP - 바인딩된 모든 UDP 사용자에게 메시지 전송
func (s *Server) BroadcastUDP(msg any) {
	s.sessions.Range(func(key, value any) bool {
		sess := value.(*Session)
		if sess.IsUDPReady() {
			s.Send(sess, msg)
		}
		return true
	})
}

// NewServer - 새 서버 인스턴스 생성
// tcpPort=0이면 TCP 서버 미생성, udpPort=0이면 UDP 서버 미생성
func NewServer(tcpPort, udpPort int) *Server {
	s := &Server{
		TCPPort:         tcpPort,
		UDPPort:         udpPort,
		BufferPool:      NewBufferPool(),
		OnRecvCallbacks: make([]func(sess base.ISession, msg any), 0),
		lastSessionID:   1000,
		UDPIdleTimeout:  60 * time.Second, // UDP 전용 세션 기본 유휴 만료(누수 방지)
	}

	// TCP 포트가 0이 아니면 TCP 서버 생성
	if tcpPort != 0 {
		s.TCP = NewTCPServer("0.0.0.0", tcpPort, s.handleNewConnection)
	}

	// UDP 포트가 0이 아니면 UDP 서버 생성
	if udpPort != 0 {
		s.UDP = NewUDPServer("0.0.0.0", udpPort, func(data []byte, addr *net.UDPAddr) {
			s.HandlePacket(nil, data, addr)
		})
	}

	return s
}

// handleNewConnection - 내부용 세션 라이프사이클 관리자
func (s *Server) handleNewConnection(conn net.Conn) {
	id := s.getNextSessionID()
	sess := NewSession(s, conn, id)
	sess.SetUDPServer(s.UDP) // UDP 엔진 연결

	s.sessions.Store(id, sess) // 보관

	if s.OnSessionOpen != nil {
		s.OnSessionOpen(sess)
	}

	go func() {
		sess.Start() // 수신 루프 (Blocking)
		// 루프 종료 시 (연결 끊김) 정리
		s.sessions.Delete(id)

		// 활성 세션이 모두 끊어지면 SessionID를 1000으로 초기화
		activeCount := 0
		s.sessions.Range(func(key, value any) bool {
			activeCount++
			return true
		})
		if activeCount == 0 {
			atomic.StoreUint32(&s.lastSessionID, 1000)
		}

		if s.OnSessionClose != nil {
			s.OnSessionClose(sess)
		}
	}()
}

// removeUDPSession - UDP 전용 세션을 sessions/udpSessions 양쪽에서 제거하고 종료 콜백을 호출합니다.
func (s *Server) removeUDPSession(sess *Session) {
	s.sessions.Delete(sess.ID())
	if addr := sess.GetUDPAddr(); addr != nil {
		s.udpSessions.Delete(addr.String())
	}
	if s.OnSessionClose != nil {
		s.OnSessionClose(sess)
	}
}

// reapIdleUDPSessions - 기준 시각(now, UnixNano) 대비 유휴 초과한 UDP 전용 세션을 한 번 정리합니다.
// TCP 세션(conn!=nil)은 자체 수명관리(수신 루프 EOF) 대상이라 건드리지 않습니다.
// 반환값은 정리된 세션 수(테스트/관측용).
func (s *Server) reapIdleUDPSessions(now int64) int {
	timeout := int64(s.UDPIdleTimeout)
	if timeout <= 0 {
		return 0
	}
	reaped := 0
	s.sessions.Range(func(key, value any) bool {
		sess := value.(*Session)
		if sess.conn != nil {
			return true // TCP 세션은 제외
		}
		if now-sess.LastActivity.Load() > timeout {
			s.removeUDPSession(sess)
			reaped++
		}
		return true
	})
	return reaped
}

// startReaper - 유휴 UDP 세션 정리 고루틴을 가동합니다. (UDPIdleTimeout>0일 때만)
func (s *Server) startReaper() {
	if s.UDPIdleTimeout <= 0 {
		return
	}
	// 점검 주기: 타임아웃의 1/2 (최소 1초)
	interval := s.UDPIdleTimeout / 2
	if interval < time.Second {
		interval = time.Second
	}
	go func() {
		ticker := time.NewTicker(interval)
		defer ticker.Stop()
		for range ticker.C {
			s.reapIdleUDPSessions(time.Now().UnixNano())
		}
	}()
}

// AddRecvCallback - 새로운 데이터 수신 콜백 등록
func (s *Server) AddRecvCallback(cb func(sess base.ISession, msg any)) {
	s.OnRecvCallbacks = append(s.OnRecvCallbacks, cb)
}

// Start - 통합 서버 가동 (TCP/UDP 모드에 따라 결정)
func (s *Server) Start() error {
	// UDP 서버가 있으면 기동 (TCP 유무에 따라 블로킹 방식 결정)
	if s.UDP != nil {
		s.startReaper() // 유휴 UDP 세션 누수 방지
		if s.TCP == nil {
			// Standalone 모드: UDP가 메인 블로킹 루프
			slog.Info("[zLink/Engine] Standalone UDP 서버 기동", "port", s.UDPPort)
			return s.UDP.Start()
		}
		// 혼합 모드: UDP를 비동기로 기동
		go func() {
			if err := s.UDP.Start(); err != nil {
				slog.Error("[zLink/Engine] UDP 서버 가동 실패", "err", err)
			}
		}()
	}

	if s.TCP == nil {
		return fmt.Errorf("TCP와 UDP 서버가 모두 없습니다")
	}

	// TCP 서버가 메인 블로킹 루프
	return s.TCP.Start()
}

// Stop - 서버 중지
func (s *Server) Stop() {
	if s.TCP != nil {
		s.TCP.Stop()
	}
	if s.UDP != nil {
		s.UDP.Stop()
	}
}
