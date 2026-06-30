// Package network - 서버 권위 세션 식별 / 바인딩 잠금 / 유휴 리퍼 로직 테스트
//
// 실제 소켓을 열지 않는다. HandlePacket이 []byte와 *net.UDPAddr를 받도록
// 분리되어 있어, 바이트를 직접 먹여 NAT·하이재킹·누수 로직을 검증한다.
package network

import (
	"net"
	"testing"
	"time"

	"github.com/ZOITK/ZLink/sdk/server/zlink/base"
)

// udpPacket - 테스트용 UDP 패킷(헤더만, 바디 없음) 생성 헬퍼
func udpPacket(cmd, sessionID uint32) []byte {
	return base.Pack(cmd, nil, sessionID, 0, 1)
}

// countSessions - 현재 활성 세션 수
func countSessions(s *Server) int {
	n := 0
	s.sessions.Range(func(_, _ any) bool { n++; return true })
	return n
}

// TestGetNextSessionIDOverflow - uint32 오버플로우 시 1001로 회귀하는지
func TestGetNextSessionIDOverflow(t *testing.T) {
	s := &Server{lastSessionID: 0xFFFFFFFF}
	if id := s.getNextSessionID(); id != 1001 {
		t.Fatalf("오버플로우 후 1001 기대, got=%d", id)
	}
}

// TestMixedModeDropsZeroID - 혼합 모드에서 ID=0 UDP는 추측 없이 드롭(세션 생성 안 됨)
func TestMixedModeDropsZeroID(t *testing.T) {
	s := NewServer(8080, 0) // TCP 존재 → 혼합 모드 (Start 호출 안 하므로 바인딩 없음)
	addr := &net.UDPAddr{IP: net.ParseIP("1.2.3.4"), Port: 5001}

	s.HandlePacket(nil, udpPacket(100, 0), addr)

	if n := countSessions(s); n != 0 {
		t.Fatalf("혼합 모드 ID=0은 드롭되어야 함. 생성된 세션 수=%d", n)
	}
}

// TestBindLockPreventsHijack - 바인딩된 세션은 같은 ID·다른 주소 패킷에 주소가 안 바뀜
func TestBindLockPreventsHijack(t *testing.T) {
	s := NewServer(8080, 0)

	// 서버가 발급한 세션을 흉내: id=1001 등록 (conn=nil)
	victim := NewSession(s, nil, 1001)
	s.sessions.Store(uint32(1001), victim)

	addrA := &net.UDPAddr{IP: net.ParseIP("10.0.0.1"), Port: 1111}
	addrB := &net.UDPAddr{IP: net.ParseIP("10.0.0.2"), Port: 2222}

	// 정상 클라가 먼저 바인딩
	s.HandlePacket(nil, udpPacket(100, 1001), addrA)
	if got := victim.GetUDPAddr(); got == nil || got.Port != 1111 {
		t.Fatalf("최초 바인딩 실패: got=%v", got)
	}

	// 공격자가 같은 ID·다른 주소로 → 무시되어 주소 불변이어야 함
	s.HandlePacket(nil, udpPacket(100, 1001), addrB)
	if got := victim.GetUDPAddr(); got.Port != 1111 {
		t.Fatalf("하이재킹 차단 실패: 주소가 port=%d 로 바뀜", got.Port)
	}
}

// TestUnknownIDDropped - 존재하지 않는 ID의 UDP는 드롭
func TestUnknownIDDropped(t *testing.T) {
	s := NewServer(8080, 0)
	addr := &net.UDPAddr{IP: net.ParseIP("1.2.3.4"), Port: 5001}

	s.HandlePacket(nil, udpPacket(100, 9999), addr) // 9999는 미발급

	if n := countSessions(s); n != 0 {
		t.Fatalf("미지 ID는 드롭되어야 함. 세션 수=%d", n)
	}
}

// TestStandaloneSameIPDifferentPort - UDP 단독 모드: 같은 공인 IP라도 포트가 다르면 별도 세션(NAT-safe)
func TestStandaloneSameIPDifferentPort(t *testing.T) {
	s := NewServer(0, 8090) // TCP 없음 → 단독 모드
	ip := net.ParseIP("203.0.113.7")
	a1 := &net.UDPAddr{IP: ip, Port: 40001}
	a2 := &net.UDPAddr{IP: ip, Port: 40002}

	s.HandlePacket(nil, udpPacket(100, 0), a1)
	s.HandlePacket(nil, udpPacket(100, 0), a2)

	if n := countSessions(s); n != 2 {
		t.Fatalf("같은 IP 다른 포트는 세션 2개여야 함(NAT-safe). got=%d", n)
	}
}

// TestReapIdleUDPSession - 유휴 초과한 UDP 전용 세션이 정리되는지
func TestReapIdleUDPSession(t *testing.T) {
	s := NewServer(0, 8090)
	s.UDPIdleTimeout = 50 * time.Millisecond
	addr := &net.UDPAddr{IP: net.ParseIP("198.51.100.5"), Port: 6000}

	s.HandlePacket(nil, udpPacket(100, 0), addr)
	if n := countSessions(s); n != 1 {
		t.Fatalf("세션 생성 실패: got=%d", n)
	}

	// 아직 유휴 아님 → 정리 0
	if r := s.reapIdleUDPSessions(time.Now().UnixNano()); r != 0 {
		t.Fatalf("아직 만료 전인데 %d개 정리됨", r)
	}

	// 충분히 미래 시각 기준 → 유휴 초과로 정리
	future := time.Now().Add(time.Second).UnixNano()
	if r := s.reapIdleUDPSessions(future); r != 1 {
		t.Fatalf("만료 세션 1개 정리 기대, got=%d", r)
	}
	if n := countSessions(s); n != 0 {
		t.Fatalf("정리 후 0개여야 함: got=%d", n)
	}
}

// TestTryBindUDP - 최초 바인딩/같은 주소 허용/다른 주소 거부 단위 검증
func TestTryBindUDP(t *testing.T) {
	sess := NewSession(nil, nil, 1)
	a1 := &net.UDPAddr{IP: net.ParseIP("10.0.0.1"), Port: 100}
	a1same := &net.UDPAddr{IP: net.ParseIP("10.0.0.1"), Port: 100}
	a2 := &net.UDPAddr{IP: net.ParseIP("10.0.0.1"), Port: 200}

	if !sess.TryBindUDP(a1) {
		t.Fatal("최초 바인딩은 true여야 함")
	}
	if !sess.TryBindUDP(a1same) {
		t.Fatal("같은 주소(값 동일)는 true여야 함")
	}
	if sess.TryBindUDP(a2) {
		t.Fatal("잠긴 뒤 다른 주소는 false여야 함")
	}
}
