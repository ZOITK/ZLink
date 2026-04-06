// Package base - ZPP 프레임워크의 공통 기반 규격
package base

import (
	"encoding/binary"
	"fmt"
)

// ZPP 스펙 상수
const (
	TCPHeaderSize = 16
	UDPHeaderSize = 20
)

// HeaderTCP - TCP 패킷 헤더 (16 bytes)
// [Version(4)][Command(4)][Length(4)][Error(4)]
type HeaderTCP struct {
	Version uint32
	Command uint32
	Length  uint32
	Error   uint32
}

// Encode - 헤더를 바이트 슬라이스로 변환 (Big Endian)
func (h *HeaderTCP) Encode() []byte {
	buf := make([]byte, TCPHeaderSize)
	binary.BigEndian.PutUint32(buf[0:4], h.Version)
	binary.BigEndian.PutUint32(buf[4:8], h.Command)
	binary.BigEndian.PutUint32(buf[8:12], h.Length)
	binary.BigEndian.PutUint32(buf[12:16], h.Error)
	return buf
}

// Decode - 바이트 슬라이스로부터 헤더 정보 추출 (Big Endian)
func (h *HeaderTCP) Decode(data []byte) error {
	if len(data) < TCPHeaderSize {
		return fmt.Errorf("데이터 길이가 부족합니다 (필요: %d, 수신: %d)", TCPHeaderSize, len(data))
	}
	h.Version = binary.BigEndian.Uint32(data[0:4])
	h.Command = binary.BigEndian.Uint32(data[4:8])
	h.Length = binary.BigEndian.Uint32(data[8:12])
	h.Error = binary.BigEndian.Uint32(data[12:16])
	return nil
}

// HeaderUDP - UDP 패킷 헤더 (20 bytes)
// [Version(4)][Command(4)][Length(4)][Sender(4)][Error(4)]
type HeaderUDP struct {
	Version uint32
	Command uint32
	Length  uint32
	Sender  uint32
	Error   uint32
}

// Encode - 헤더를 바이트 슬라이스로 변환 (Big Endian)
func (h *HeaderUDP) Encode() []byte {
	buf := make([]byte, UDPHeaderSize)
	binary.BigEndian.PutUint32(buf[0:4], h.Version)
	binary.BigEndian.PutUint32(buf[4:8], h.Command)
	binary.BigEndian.PutUint32(buf[8:12], h.Length)
	binary.BigEndian.PutUint32(buf[12:16], h.Sender)
	binary.BigEndian.PutUint32(buf[16:20], h.Error)
	return buf
}

// Decode - 바이트 슬라이스로부터 헤더 정보 추출 (Big Endian)
func (h *HeaderUDP) Decode(data []byte) error {
	if len(data) < UDPHeaderSize {
		return fmt.Errorf("데이터 길이가 부족합니다 (필요: %d, 수신: %d)", UDPHeaderSize, len(data))
	}
	h.Version = binary.BigEndian.Uint32(data[0:4])
	h.Command = binary.BigEndian.Uint32(data[4:8])
	h.Length = binary.BigEndian.Uint32(data[8:12])
	h.Sender = binary.BigEndian.Uint32(data[12:16])
	h.Error = binary.BigEndian.Uint32(data[16:20])
	return nil
}
