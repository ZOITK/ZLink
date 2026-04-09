// 자동 생성된 프로토콜
// 버전: 1
// [ 2026-04-09 : 15:57:27 ] 자동 생성됨 (zlink-protocol-gen)

package protocol

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"github.com/vmihailenco/msgpack/v5"
)

// =========================================================================
// --- 변수 및 상수 ---
// =========================================================================
const CurrentVersion = 1
const HeaderSize = 16
const HeaderUdpSize = 20

type ErrorCode uint32

// Error Codes
const (
	Err_None ErrorCode = 0 // 정상
	Err_InvalidValue ErrorCode = 1 // 잘못된 값
	Err_Unauthorized ErrorCode = 2 // 인증 필요
	Err_Server ErrorCode = 3 // 서버 오류
)

// Packet IDs (Cmd_)
const (
	Cmd_SystemTCPHeartBitReq uint32 = 11110001 // TCP Heartbeat / TCP 하트비트
	Cmd_SystemUDPHeartBitReq uint32 = 11110002 // UDP Heartbeat / UDP 하트비트
	Cmd_SystemTCPHeartBitRes uint32 = 11120001 // TCP Heartbeat / TCP 하트비트
	Cmd_SystemUDPHeartBitRes uint32 = 11120002 // UDP Heartbeat / UDP 하트비트
	Cmd_AuthLoginReq uint32 = 12110001 // Login / 로그인
	Cmd_AuthLoginRes uint32 = 12120001 // Login / 로그인
	Cmd_MessageSendReq uint32 = 13110001 // Send Message / 메시지 전송
	Cmd_MessageSendRes uint32 = 13120001 // Send Message / 메시지 전송
	Cmd_MessageReceiveNotify uint32 = 13130002 // Receive Message / 메시지 수신
)

// =========================================================================
// --- 구조체 선언 ---
// =========================================================================
// Msg_SystemTCPHeartBitReq - TCP Heartbeat / TCP 하트비트
type Msg_SystemTCPHeartBitReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	ServerTime int64 `msgpack:"ServerTime"`
}
// Msg_SystemUDPHeartBitReq - UDP Heartbeat / UDP 하트비트
type Msg_SystemUDPHeartBitReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Timestamp int64 `msgpack:"Timestamp"`
}
// Msg_SystemTCPHeartBitRes - TCP Heartbeat / TCP 하트비트
type Msg_SystemTCPHeartBitRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	ServerTime int64 `msgpack:"ServerTime"`
}
// Msg_SystemUDPHeartBitRes - UDP Heartbeat / UDP 하트비트
type Msg_SystemUDPHeartBitRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Timestamp int64 `msgpack:"Timestamp"`
}
// Msg_AuthLoginReq - Login / 로그인
type Msg_AuthLoginReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Nickname string `msgpack:"Nickname"`
}
// Msg_AuthLoginRes - Login / 로그인
type Msg_AuthLoginRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	PlayerID uint32 `msgpack:"PlayerID"`
	Result uint32 `msgpack:"Result"`
}
// Msg_MessageSendReq - Send Message / 메시지 전송
type Msg_MessageSendReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Message string `msgpack:"Message"`
}
// Msg_MessageSendRes - Send Message / 메시지 전송
type Msg_MessageSendRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Result uint32 `msgpack:"Result"`
}
// Msg_MessageReceiveNotify - Receive Message / 메시지 수신
type Msg_MessageReceiveNotify struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	PlayerID uint32 `msgpack:"PlayerID"`
	Nickname string `msgpack:"Nickname"`
	Message string `msgpack:"Message"`
}

// =========================================================================
// --- 공통 인터페이스 ---
// =========================================================================

// ISession - 엔진 세션 기능을 추상화한 인터페이스 (비즈니스 로직용)
type ISession interface {
	ID() uint32
	SendRaw(data []byte) error
	Close()
	GetMetadata() any
	SetMetadata(data any)
}

// Packet - 모든 패킷 구조체가 구현하는 인터페이스
type Packet interface {
	GetID() uint32
}

// =========================================================================
// --- 중앙 집중형 디스패처 (Registration) ---
// =========================================================================

// Register - 엔진 서버에 프로토콜 파서(최초 1회)와 비즈니스 콜백을 등록합니다.
// 여러 번 호출하여 다중 리스너(Multi-listener)를 구성할 수 있습니다.
func Register(srv any, callback func(ISession, any)) {
	type engine interface {
		SetUnmarshaler(func(uint32, []byte) (any, error))
		SetHeaderSize(int, int)
		AddRecvCallback(func(any, any))
	}

	if s, ok := srv.(engine); ok {
		s.SetHeaderSize(HeaderSize, HeaderUdpSize)
		// 파싱 로직은 최초 1회만 등록됨 (엔진 내부에서 처리)
		s.SetUnmarshaler(_Unmarshal)
		// 콜백 리스트에 추가
		s.AddRecvCallback(func(sess any, msg any) {
			callback(sess.(ISession), msg)
		})
	}
}

// _Unmarshal - 커맨드 ID에 따라 바이트 데이터를 해당 구조체로 자동 파싱 (비공개)
func _Unmarshal(cmd uint32, body []byte) (any, error) {
	switch cmd {
	case Cmd_SystemTCPHeartBitReq:
		msg := &Msg_SystemTCPHeartBitReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_SystemUDPHeartBitReq:
		msg := &Msg_SystemUDPHeartBitReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_SystemTCPHeartBitRes:
		msg := &Msg_SystemTCPHeartBitRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_SystemUDPHeartBitRes:
		msg := &Msg_SystemUDPHeartBitRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_AuthLoginReq:
		msg := &Msg_AuthLoginReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_AuthLoginRes:
		msg := &Msg_AuthLoginRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_MessageSendReq:
		msg := &Msg_MessageSendReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_MessageSendRes:
		msg := &Msg_MessageSendRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_MessageReceiveNotify:
		msg := &Msg_MessageReceiveNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	}
	return nil, fmt.Errorf("unknown command: %d", cmd)
}

// =========================================================================
// --- 시스템 헤더 (정의 기반 동적 생성) ---
// =========================================================================


type Sys_PackHeader struct {
	Version uint32
	Command uint32
	Length uint32
	Error uint32
}
func (h *Sys_PackHeader) Encode() []byte {
	buf := new(bytes.Buffer)
	binary.Write(buf, binary.LittleEndian, h)
	return buf.Bytes()
}
func (h *Sys_PackHeader) Decode(data []byte) error {
	return binary.Read(bytes.NewReader(data), binary.LittleEndian, h)
}

type Sys_PackHeaderUDP struct {
	Version uint32
	Command uint32
	Length uint32
	Sender uint32
	Error uint32
}
func (h *Sys_PackHeaderUDP) Encode() []byte {
	buf := new(bytes.Buffer)
	binary.Write(buf, binary.LittleEndian, h)
	return buf.Bytes()
}
func (h *Sys_PackHeaderUDP) Decode(data []byte) error {
	return binary.Read(bytes.NewReader(data), binary.LittleEndian, h)
}

// =========================================================================
// --- 구조체 관련 함수 (인코딩/디코딩/빌드) ---
// =========================================================================
func (r *Msg_SystemTCPHeartBitReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_SystemTCPHeartBitReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_SystemTCPHeartBitReq) GetID() uint32 { return Cmd_SystemTCPHeartBitReq }
func (p *Msg_SystemTCPHeartBitReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_SystemTCPHeartBitReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_SystemUDPHeartBitReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_SystemUDPHeartBitReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_SystemUDPHeartBitReq) GetID() uint32 { return Cmd_SystemUDPHeartBitReq }
func (p *Msg_SystemUDPHeartBitReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_SystemUDPHeartBitReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_SystemTCPHeartBitRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_SystemTCPHeartBitRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_SystemTCPHeartBitRes) GetID() uint32 { return Cmd_SystemTCPHeartBitRes }
func (p *Msg_SystemTCPHeartBitRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_SystemTCPHeartBitRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_SystemUDPHeartBitRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_SystemUDPHeartBitRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_SystemUDPHeartBitRes) GetID() uint32 { return Cmd_SystemUDPHeartBitRes }
func (p *Msg_SystemUDPHeartBitRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_SystemUDPHeartBitRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_AuthLoginReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_AuthLoginReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_AuthLoginReq) GetID() uint32 { return Cmd_AuthLoginReq }
func (p *Msg_AuthLoginReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_AuthLoginReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_AuthLoginRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_AuthLoginRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_AuthLoginRes) GetID() uint32 { return Cmd_AuthLoginRes }
func (p *Msg_AuthLoginRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_AuthLoginRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_MessageSendReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_MessageSendReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_MessageSendReq) GetID() uint32 { return Cmd_MessageSendReq }
func (p *Msg_MessageSendReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_MessageSendReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_MessageSendRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_MessageSendRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_MessageSendRes) GetID() uint32 { return Cmd_MessageSendRes }
func (p *Msg_MessageSendRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_MessageSendRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_MessageReceiveNotify) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_MessageReceiveNotify) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_MessageReceiveNotify) GetID() uint32 { return Cmd_MessageReceiveNotify }
func (p *Msg_MessageReceiveNotify) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_MessageReceiveNotify) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}