// Package protocol - 자동 생성된 프로토콜
// 버전: 2
// 자동 생성됨 (zoit-protocol-gen)

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
const CurrentVersion = 2

type ErrorCode uint32

// Error Codes
const (
	Err_None ErrorCode = 0 // 정상
	Err_InvalidValue ErrorCode = 1 // 잘못된 값
	Err_Unauthorized ErrorCode = 2 // 인증 필요
	Err_NotFound ErrorCode = 3 // 찾을 수 없음
	Err_Server ErrorCode = 4 // 서버 오류
)

// Packet IDs (Cmd_)
const (
	Cmd_SystemTCPHeartBitReq uint32 = 11110001 // TCP 하트비트
	Cmd_SystemTCPHeartBitRes uint32 = 11120001 // TCP 하트비트
	Cmd_AuthLoginReq uint32 = 12110001 // 로그인
	Cmd_AuthLoginRes uint32 = 12120001 // 로그인
	Cmd_RoomSearchReq uint32 = 13110001 // 방 검색
	Cmd_RoomCreateReq uint32 = 13110002 // 방 생성
	Cmd_RoomJoinReq uint32 = 13110003 // 방 입장
	Cmd_RoomSearchRes uint32 = 13120001 // 방 검색
	Cmd_RoomCreateRes uint32 = 13120002 // 방 생성
	Cmd_RoomJoinRes uint32 = 13120003 // 방 입장
	Cmd_RoomPlayerJoinNotify uint32 = 13130004 // 플레이어 입장 알림
	Cmd_RoomGameStartNotify uint32 = 13130005 // 게임 시작 알림
	Cmd_GameGuessReq uint32 = 14110001 // 숫자 맞추기
	Cmd_GameWinReq uint32 = 14110003 // 게임 승리
	Cmd_GameChatReq uint32 = 14110005 // 채팅 메시지 전송
	Cmd_GameGuessRes uint32 = 14120001 // 숫자 맞추기
	Cmd_GameWinRes uint32 = 14120003 // 게임 승리
	Cmd_GameChatRes uint32 = 14120005 // 채팅 메시지 전송
	Cmd_GameGuessNotify uint32 = 14130002 // 상대 숫자 맞추기 알림
	Cmd_GameWinNotify uint32 = 14130004 // 게임 종료 알림
	Cmd_GameChatNotify uint32 = 14130006 // 채팅 메시지 수신
)

// =========================================================================
// --- 구조체 선언 ---
// =========================================================================
// Msg_RoomInfo - 방 정보
type Msg_RoomInfo struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomID uint32 `msgpack:"RoomID"`
	RoomName string `msgpack:"RoomName"`
	HostPlayerID uint32 `msgpack:"HostPlayerID"`
	HostNickname string `msgpack:"HostNickname"`
	PlayerCount uint32 `msgpack:"PlayerCount"`
	Status uint32 `msgpack:"Status"`
	IsMultiplayer uint32 `msgpack:"IsMultiplayer"`
}
// Msg_SystemTCPHeartBitReq - TCP 하트비트
type Msg_SystemTCPHeartBitReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	ServerTime int64 `msgpack:"ServerTime"`
}
// Msg_SystemTCPHeartBitRes - TCP 하트비트
type Msg_SystemTCPHeartBitRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	ServerTime int64 `msgpack:"ServerTime"`
}
// Msg_AuthLoginReq - 로그인
type Msg_AuthLoginReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Nickname string `msgpack:"Nickname"`
}
// Msg_AuthLoginRes - 로그인
type Msg_AuthLoginRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	PlayerID uint32 `msgpack:"PlayerID"`
	Result uint32 `msgpack:"Result"`
}
// Msg_RoomSearchReq - 방 검색
type Msg_RoomSearchReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
}
// Msg_RoomCreateReq - 방 생성
type Msg_RoomCreateReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomName string `msgpack:"RoomName"`
	IsMultiplayer uint32 `msgpack:"IsMultiplayer"`
}
// Msg_RoomJoinReq - 방 입장
type Msg_RoomJoinReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomID uint32 `msgpack:"RoomID"`
}
// Msg_RoomSearchRes - 방 검색
type Msg_RoomSearchRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Rooms []*Msg_RoomInfo `msgpack:"Rooms"`
	Result uint32 `msgpack:"Result"`
}
// Msg_RoomCreateRes - 방 생성
type Msg_RoomCreateRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomID uint32 `msgpack:"RoomID"`
	Result uint32 `msgpack:"Result"`
}
// Msg_RoomJoinRes - 방 입장
type Msg_RoomJoinRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomID uint32 `msgpack:"RoomID"`
	OpponentPlayerID uint32 `msgpack:"OpponentPlayerID"`
	OpponentNickname string `msgpack:"OpponentNickname"`
	Result uint32 `msgpack:"Result"`
}
// Msg_RoomPlayerJoinNotify - 플레이어 입장 알림
type Msg_RoomPlayerJoinNotify struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	PlayerID uint32 `msgpack:"PlayerID"`
	Nickname string `msgpack:"Nickname"`
}
// Msg_RoomGameStartNotify - 게임 시작 알림
type Msg_RoomGameStartNotify struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	TargetNumber uint32 `msgpack:"TargetNumber"`
	MaxNumber uint32 `msgpack:"MaxNumber"`
}
// Msg_GameGuessReq - 숫자 맞추기
type Msg_GameGuessReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	GuessNumber uint32 `msgpack:"GuessNumber"`
}
// Msg_GameWinReq - 게임 승리
type Msg_GameWinReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	GuessNumber uint32 `msgpack:"GuessNumber"`
}
// Msg_GameChatReq - 채팅 메시지 전송
type Msg_GameChatReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Message string `msgpack:"Message"`
}
// Msg_GameGuessRes - 숫자 맞추기
type Msg_GameGuessRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Result uint32 `msgpack:"Result"`
	Hint uint32 `msgpack:"Hint"`
}
// Msg_GameWinRes - 게임 승리
type Msg_GameWinRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Result uint32 `msgpack:"Result"`
}
// Msg_GameChatRes - 채팅 메시지 전송
type Msg_GameChatRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Result uint32 `msgpack:"Result"`
}
// Msg_GameGuessNotify - 상대 숫자 맞추기 알림
type Msg_GameGuessNotify struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	PlayerID uint32 `msgpack:"PlayerID"`
	Nickname string `msgpack:"Nickname"`
	GuessNumber uint32 `msgpack:"GuessNumber"`
	Hint uint32 `msgpack:"Hint"`
}
// Msg_GameWinNotify - 게임 종료 알림
type Msg_GameWinNotify struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	WinnerPlayerID uint32 `msgpack:"WinnerPlayerID"`
	WinnerNickname string `msgpack:"WinnerNickname"`
	CorrectNumber uint32 `msgpack:"CorrectNumber"`
	TryCount uint32 `msgpack:"TryCount"`
}
// Msg_GameChatNotify - 채팅 메시지 수신
type Msg_GameChatNotify struct {
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
	SendRaw(data []byte) error
	Close()
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
		AddRecvCallback(func(any, any))
	}

	if s, ok := srv.(engine); ok {
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
	case Cmd_SystemTCPHeartBitRes:
		msg := &Msg_SystemTCPHeartBitRes{}
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
	case Cmd_RoomSearchReq:
		msg := &Msg_RoomSearchReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomCreateReq:
		msg := &Msg_RoomCreateReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomJoinReq:
		msg := &Msg_RoomJoinReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomSearchRes:
		msg := &Msg_RoomSearchRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomCreateRes:
		msg := &Msg_RoomCreateRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomJoinRes:
		msg := &Msg_RoomJoinRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomPlayerJoinNotify:
		msg := &Msg_RoomPlayerJoinNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomGameStartNotify:
		msg := &Msg_RoomGameStartNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameGuessReq:
		msg := &Msg_GameGuessReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameWinReq:
		msg := &Msg_GameWinReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameChatReq:
		msg := &Msg_GameChatReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameGuessRes:
		msg := &Msg_GameGuessRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameWinRes:
		msg := &Msg_GameWinRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameChatRes:
		msg := &Msg_GameChatRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameGuessNotify:
		msg := &Msg_GameGuessNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameWinNotify:
		msg := &Msg_GameWinNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameChatNotify:
		msg := &Msg_GameChatNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	}
	return nil, fmt.Errorf("unknown command: %d", cmd)
}

// =========================================================================
// --- 시스템 헤더 (내부 동작용) ---
// =========================================================================

type Sys_PackHeader struct {
    Version uint32
    Command uint32
    Length  uint32
    Error   uint32
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
    Length  uint32
    Sender  uint32
    Error   uint32
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
func (r *Msg_RoomInfo) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomInfo) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
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
func (r *Msg_RoomSearchReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomSearchReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomSearchReq) GetID() uint32 { return Cmd_RoomSearchReq }
func (p *Msg_RoomSearchReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomSearchReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomCreateReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomCreateReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomCreateReq) GetID() uint32 { return Cmd_RoomCreateReq }
func (p *Msg_RoomCreateReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomCreateReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomJoinReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomJoinReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomJoinReq) GetID() uint32 { return Cmd_RoomJoinReq }
func (p *Msg_RoomJoinReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomJoinReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomSearchRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomSearchRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomSearchRes) GetID() uint32 { return Cmd_RoomSearchRes }
func (p *Msg_RoomSearchRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomSearchRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomCreateRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomCreateRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomCreateRes) GetID() uint32 { return Cmd_RoomCreateRes }
func (p *Msg_RoomCreateRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomCreateRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomJoinRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomJoinRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomJoinRes) GetID() uint32 { return Cmd_RoomJoinRes }
func (p *Msg_RoomJoinRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomJoinRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomPlayerJoinNotify) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomPlayerJoinNotify) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomPlayerJoinNotify) GetID() uint32 { return Cmd_RoomPlayerJoinNotify }
func (p *Msg_RoomPlayerJoinNotify) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomPlayerJoinNotify) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomGameStartNotify) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomGameStartNotify) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomGameStartNotify) GetID() uint32 { return Cmd_RoomGameStartNotify }
func (p *Msg_RoomGameStartNotify) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomGameStartNotify) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_GameGuessReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameGuessReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameGuessReq) GetID() uint32 { return Cmd_GameGuessReq }
func (p *Msg_GameGuessReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameGuessReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_GameWinReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameWinReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameWinReq) GetID() uint32 { return Cmd_GameWinReq }
func (p *Msg_GameWinReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameWinReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_GameChatReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameChatReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameChatReq) GetID() uint32 { return Cmd_GameChatReq }
func (p *Msg_GameChatReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameChatReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_GameGuessRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameGuessRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameGuessRes) GetID() uint32 { return Cmd_GameGuessRes }
func (p *Msg_GameGuessRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameGuessRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_GameWinRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameWinRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameWinRes) GetID() uint32 { return Cmd_GameWinRes }
func (p *Msg_GameWinRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameWinRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_GameChatRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameChatRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameChatRes) GetID() uint32 { return Cmd_GameChatRes }
func (p *Msg_GameChatRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameChatRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_GameGuessNotify) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameGuessNotify) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameGuessNotify) GetID() uint32 { return Cmd_GameGuessNotify }
func (p *Msg_GameGuessNotify) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameGuessNotify) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_GameWinNotify) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameWinNotify) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameWinNotify) GetID() uint32 { return Cmd_GameWinNotify }
func (p *Msg_GameWinNotify) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameWinNotify) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_GameChatNotify) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameChatNotify) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameChatNotify) GetID() uint32 { return Cmd_GameChatNotify }
func (p *Msg_GameChatNotify) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameChatNotify) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}