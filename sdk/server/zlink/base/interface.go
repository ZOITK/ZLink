// Package base - ZLink 프레임워크의 공통 인터페이스 및 기반 정의
package base

import (
	"encoding/binary"
)

const (
	// HeaderSize - ZLink 표준 패킷 헤더 크기 (24 Bytes 고정)
	HeaderSize = 24
	// MagicZO - ZLink 유효성 검증 마법 번호 ('ZO' - 0x4F5A)
	MagicZO uint16 = 0x4F5A
	// UnassignedSessionID - 할당되지 않은 세션 ID (기본값 0)
	UnassignedSessionID uint32 = 0
)

// Pack - ZLink 표준 24바이트 패킷을 조립합니다. (SSOT)
func Pack(cmd uint32, body []byte, sessionID uint32, errCode uint32, version uint32) []byte {
	buf := make([]byte, HeaderSize+len(body))
	// Offset 0-1: Magic (0x4F5A)
	binary.LittleEndian.PutUint16(buf[0:2], MagicZO)
	// Offset 2-5: Version
	binary.LittleEndian.PutUint32(buf[2:6], version)
	// Offset 6-9: Command ID
	binary.LittleEndian.PutUint32(buf[6:10], cmd)
	// Offset 10-13: Body Length
	binary.LittleEndian.PutUint32(buf[10:14], uint32(len(body)))
	// Offset 14-17: Session ID / Sender ID
	binary.LittleEndian.PutUint32(buf[14:18], sessionID)
	// Offset 18-21: Error Code
	binary.LittleEndian.PutUint32(buf[18:22], errCode)
	// Offset 22-23: Sequence (Reserved)

	if len(body) > 0 {
		copy(buf[HeaderSize:], body)
	}
	return buf
}

// Header - ZLink 표준 24바이트 패킷 헤더 구조
type Header struct {
	Magic     uint16 // [0:2] 'ZO' (0x4F5A)
	Version   uint32 // [2:6] 통신 버전
	Command   uint32 // [6:10] 제어 커맨드 ID
	Length    uint32 // [10:14] 바디 데이터 길이
	SessionID uint32 // [14:18] 세션 식별자
	ErrorCode uint32 // [18:22] 시스템 오류 코드
	Sequence  uint16 // [22:24] 시퀀스
}

// ISession - 세션의 공통 기능을 정의하는 인터페이스
type ISession interface {
	ID() uint32
	SendRaw(data []byte) error    // TCP 전송
	SendRawUDP(data []byte) error // 바인딩된 UDP 주소로 전송
	Close()
	GetMetadata() any
	SetMetadata(data any)
	IsUDPReady() bool
}

// IPacket - 모든 패킷 구조체가 구현하는 인터페이스
type IPacket interface {
	GetID() uint32
}

// ProtocolInfo - 엔진이 프로토콜을 이해하기 위해 필요한 정보
type ProtocolInfo struct {
	Unmarshaler func(cmd uint32, body []byte) (any, error)
	Packer      func(msg any, isUDP bool, sessionID uint32) ([]byte, error)
}
