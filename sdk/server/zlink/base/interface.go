// Package base - ZLink 프레임워크의 공통 인터페이스 및 기반 정의
package base

const (
	// HeaderSize - ZLink 표준 패킷 헤더 크기 (24 Bytes 고정)
	HeaderSize = 24
	// MagicZO - ZLink 유효성 검증 마법 번호 ('ZO' - 0x4F5A)
	MagicZO uint16 = 0x4F5A
)

// Header - ZLink 표준 24바이트 패킷 헤더 구조
type Header struct {
	Magic     uint16 // [0:2] 'ZO' (0x4F5A)
	Version   uint32 // [2:6] 통신 버전 (확장됨)
	Command   uint32 // [6:10] 제어 커맨드 ID
	Length    uint32 // [10:14] 바디 데이터 길이
	SessionID uint32 // [14:18] UDP: 발신자 매핑 / TCP: 세션 식별
	ErrorCode uint32 // [18:22] 시스템 오류 코드
	Sequence  uint16 // [22:24] 패킷 순서 및 보안 시퀀스 (축소됨)
}

// ISession - 세션의 공통 기능을 정의하는 인터페이스
type ISession interface {
	ID() uint32
	SendRaw(data []byte) error    // TCP 전송
	SendRawUDP(data []byte) error // 바인딩된 UDP 주소로 전송
	Close()
	GetMetadata() any
	SetMetadata(data any)
	IsUDPReady() bool // UDP 주소가 바인딩되어 사용할 수 있는지 확인
}

// IPacket - 모든 패킷 구조체가 구현하는 인터페이스
type IPacket interface {
	GetID() uint32
}

// ProtocolInfo - 엔진이 프로토콜을 이해하기 위해 필요한 정보 뭉치
type ProtocolInfo struct {
	// Unmarshaler - 커맨드ID를 실제 구조체로 변환하는 함수
	Unmarshaler func(cmd uint32, body []byte) (any, error)
	// Packer - 메시지 객체를 전송 가능한 패킷 바이트로 변환하는 함수
	// (isUDP에 따라 헤더 선택, sessionID는 UDP 전송시 SessionID 필드에 사용)
	Packer func(msg any, isUDP bool, sessionID uint32) ([]byte, error)
}
