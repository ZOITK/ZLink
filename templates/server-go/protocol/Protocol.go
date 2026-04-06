// Package protocol - 자동 생성된 프로토콜
// 버전: 1000009
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
const CurrentVersion = 1000009

type ErrorCode uint32

// Error Codes
const (
	Err_None ErrorCode = 0 // 정상
	Err_InvalidValue ErrorCode = 1 // 패킷 파싱 실패 / 값 오류
	Err_Unauthorized ErrorCode = 2 // 인증 안 된 요청
	Err_Server ErrorCode = 3 // 서버 내부 오류
)

// Packet IDs (Cmd_)
const (
	Cmd_SystemTCPHeartBitReq uint32 = 11110001 // TCP 하트비트
	Cmd_SystemTCPHeartBitRes uint32 = 11120001 // TCP 하트비트
	Cmd_SystemUDPHeartBitReq uint32 = 11210002 // UDP 하트비트
	Cmd_SystemUDPHeartBitRes uint32 = 11220002 // UDP 하트비트
	Cmd_AuthLoginReq uint32 = 12110001 // 로그인
	Cmd_AuthMapTotalUserCountReq uint32 = 12110002 // 맵 동접자 수
	Cmd_AuthLoginRes uint32 = 12120001 // 로그인
	Cmd_AuthMapTotalUserCountRes uint32 = 12120002 // 맵 동접자 수
	Cmd_RoomListReq uint32 = 13110001 // 방 목록 조회
	Cmd_RoomCreateReq uint32 = 13110002 // 방 생성
	Cmd_RoomJoinReq uint32 = 13110003 // 방 입장
	Cmd_RoomFinishInfoListReq uint32 = 13110007 // 완주자 기록 목록
	Cmd_RoomListRes uint32 = 13120001 // 방 목록 조회
	Cmd_RoomCreateRes uint32 = 13120002 // 방 생성
	Cmd_RoomJoinRes uint32 = 13120003 // 방 입장
	Cmd_RoomFinishInfoListRes uint32 = 13120007 // 완주자 기록 목록
	Cmd_RoomRiderUpdateNotify uint32 = 13130004 // 라이더 갱신 알림
	Cmd_RoomClientLeaveNotify uint32 = 13130005 // 퇴장 알림
	Cmd_GameChatReq uint32 = 14110001 // 채팅
	Cmd_GameChatRes uint32 = 14120001 // 채팅
	Cmd_GameChatNotify uint32 = 14130002 // 채팅 알림
	Cmd_GameRiderPosSyncNotify uint32 = 14230003 // 위치 동기화
	Cmd_AdminAdminSetReq uint32 = 15110001 // 관리자 설정
)

// =========================================================================
// --- 구조체 선언 ---
// =========================================================================
// Msg_RecvRoomInfo - 룸 상세 정보
type Msg_RecvRoomInfo struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomIdx uint32 `msgpack:"RoomIdx"`
	Title string `msgpack:"Title"`
	MapUid string `msgpack:"MapUid"`
	HostUserIdx uint32 `msgpack:"HostUserIdx"`
}
// Msg_RoomCreateInfo - 방 생성 정보
type Msg_RoomCreateInfo struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomMaxUser uint32 `msgpack:"RoomMaxUser"`
	Lap uint32 `msgpack:"Lap"`
	Title string `msgpack:"Title"`
	MapUid string `msgpack:"MapUid"`
}
// Msg_RoomFinishInfo - 완주 기록
type Msg_RoomFinishInfo struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	LoginID string `msgpack:"LoginID"`
	Nick string `msgpack:"Nick"`
	RiderIndex uint32 `msgpack:"RiderIndex"`
	FinishTime int64 `msgpack:"FinishTime"`
}
// Msg_RoomJoinInfo - 라이더 참여 정보
type Msg_RoomJoinInfo struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	LoginID string `msgpack:"LoginID"`
	UserIdx uint32 `msgpack:"UserIdx"`
	Nick string `msgpack:"Nick"`
	Distance float32 `msgpack:"Distance"`
	RiderIndex uint32 `msgpack:"RiderIndex"`
}
// Msg_RoomListInfo - 방 정보 요약
type Msg_RoomListInfo struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomIdx uint32 `msgpack:"RoomIdx"`
	Title string `msgpack:"Title"`
	RoomMaxUser uint32 `msgpack:"RoomMaxUser"`
	RoomUserCount uint32 `msgpack:"RoomUserCount"`
}
// Msg_SystemTCPHeartBitReq - TCP 하트비트
type Msg_SystemTCPHeartBitReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	ServerTime float64 `msgpack:"ServerTime"`
}
// Msg_SystemTCPHeartBitRes - TCP 하트비트
type Msg_SystemTCPHeartBitRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	ServerTime float64 `msgpack:"ServerTime"`
}
// Msg_SystemUDPHeartBitReq - UDP 하트비트
type Msg_SystemUDPHeartBitReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Timestamp int64 `msgpack:"Timestamp"`
}
// Msg_SystemUDPHeartBitRes - UDP 하트비트
type Msg_SystemUDPHeartBitRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Timestamp int64 `msgpack:"Timestamp"`
}
// Msg_AuthLoginReq - 로그인
type Msg_AuthLoginReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	LoginID string `msgpack:"LoginID"`
}
// Msg_AuthMapTotalUserCountReq - 맵 동접자 수
type Msg_AuthMapTotalUserCountReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	MapUids []string `msgpack:"MapUids"`
}
// Msg_AuthLoginRes - 로그인
type Msg_AuthLoginRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	UserIdx uint32 `msgpack:"UserIdx"`
	StartTime int64 `msgpack:"StartTime"`
	Result uint32 `msgpack:"Result"`
}
// Msg_AuthMapTotalUserCountRes - 맵 동접자 수
type Msg_AuthMapTotalUserCountRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Counts []uint32 `msgpack:"Counts"`
	Result uint32 `msgpack:"Result"`
}
// Msg_RoomListReq - 방 목록 조회
type Msg_RoomListReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	MapUid string `msgpack:"MapUid"`
}
// Msg_RoomCreateReq - 방 생성
type Msg_RoomCreateReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	CreateInfo *Msg_RoomCreateInfo `msgpack:"CreateInfo"`
	Riders []*Msg_RoomJoinInfo `msgpack:"Riders"`
}
// Msg_RoomJoinReq - 방 입장
type Msg_RoomJoinReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomIdx uint32 `msgpack:"RoomIdx"`
	Riders []*Msg_RoomJoinInfo `msgpack:"Riders"`
}
// Msg_RoomFinishInfoListReq - 완주자 기록 목록
type Msg_RoomFinishInfoListReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomIdx uint32 `msgpack:"RoomIdx"`
}
// Msg_RoomListRes - 방 목록 조회
type Msg_RoomListRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Rooms []*Msg_RoomListInfo `msgpack:"Rooms"`
	Result uint32 `msgpack:"Result"`
}
// Msg_RoomCreateRes - 방 생성
type Msg_RoomCreateRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomIdx uint32 `msgpack:"RoomIdx"`
	Result uint32 `msgpack:"Result"`
}
// Msg_RoomJoinRes - 방 입장
type Msg_RoomJoinRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	RoomInfo *Msg_RecvRoomInfo `msgpack:"RoomInfo"`
	UserIdx uint32 `msgpack:"UserIdx"`
	OtherRiders []*Msg_RoomJoinInfo `msgpack:"OtherRiders"`
	Result uint32 `msgpack:"Result"`
}
// Msg_RoomFinishInfoListRes - 완주자 기록 목록
type Msg_RoomFinishInfoListRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Finishes []*Msg_RoomFinishInfo `msgpack:"Finishes"`
	Result uint32 `msgpack:"Result"`
}
// Msg_RoomRiderUpdateNotify - 라이더 갱신 알림
type Msg_RoomRiderUpdateNotify struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Users []*Msg_RoomJoinInfo `msgpack:"Users"`
}
// Msg_RoomClientLeaveNotify - 퇴장 알림
type Msg_RoomClientLeaveNotify struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	LeaverUserIdx uint32 `msgpack:"LeaverUserIdx"`
	HostUserIdx uint32 `msgpack:"HostUserIdx"`
}
// Msg_GameChatReq - 채팅
type Msg_GameChatReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Message string `msgpack:"Message"`
}
// Msg_GameChatRes - 채팅
type Msg_GameChatRes struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Result uint32 `msgpack:"Result"`
}
// Msg_GameChatNotify - 채팅 알림
type Msg_GameChatNotify struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	UserIdx uint32 `msgpack:"UserIdx"`
	Message string `msgpack:"Message"`
}
// Msg_GameRiderPosSyncNotify - 위치 동기화
type Msg_GameRiderPosSyncNotify struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Timestamp int64 `msgpack:"Timestamp"`
	Riders [][]float32 `msgpack:"Riders"`
}
// Msg_AdminAdminSetReq - 관리자 설정
type Msg_AdminAdminSetReq struct {
	_msgpack struct{} `msgpack:",as_array"` // 데이터 압축 전송용
	Enabled uint32 `msgpack:"Enabled"`
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
	case Cmd_SystemUDPHeartBitReq:
		msg := &Msg_SystemUDPHeartBitReq{}
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
	case Cmd_AuthMapTotalUserCountReq:
		msg := &Msg_AuthMapTotalUserCountReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_AuthLoginRes:
		msg := &Msg_AuthLoginRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_AuthMapTotalUserCountRes:
		msg := &Msg_AuthMapTotalUserCountRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomListReq:
		msg := &Msg_RoomListReq{}
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
	case Cmd_RoomFinishInfoListReq:
		msg := &Msg_RoomFinishInfoListReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomListRes:
		msg := &Msg_RoomListRes{}
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
	case Cmd_RoomFinishInfoListRes:
		msg := &Msg_RoomFinishInfoListRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomRiderUpdateNotify:
		msg := &Msg_RoomRiderUpdateNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_RoomClientLeaveNotify:
		msg := &Msg_RoomClientLeaveNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameChatReq:
		msg := &Msg_GameChatReq{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameChatRes:
		msg := &Msg_GameChatRes{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameChatNotify:
		msg := &Msg_GameChatNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_GameRiderPosSyncNotify:
		msg := &Msg_GameRiderPosSyncNotify{}
		if err := msg.Decode(body); err != nil { return nil, err }
		return msg, nil
	case Cmd_AdminAdminSetReq:
		msg := &Msg_AdminAdminSetReq{}
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
func (r *Msg_RecvRoomInfo) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RecvRoomInfo) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (r *Msg_RoomCreateInfo) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomCreateInfo) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (r *Msg_RoomFinishInfo) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomFinishInfo) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (r *Msg_RoomJoinInfo) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomJoinInfo) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (r *Msg_RoomListInfo) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomListInfo) Decode(data []byte) error {
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
func (r *Msg_AuthMapTotalUserCountReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_AuthMapTotalUserCountReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_AuthMapTotalUserCountReq) GetID() uint32 { return Cmd_AuthMapTotalUserCountReq }
func (p *Msg_AuthMapTotalUserCountReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_AuthMapTotalUserCountReq) BuildUDP(sender uint32) []byte {
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
func (r *Msg_AuthMapTotalUserCountRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_AuthMapTotalUserCountRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_AuthMapTotalUserCountRes) GetID() uint32 { return Cmd_AuthMapTotalUserCountRes }
func (p *Msg_AuthMapTotalUserCountRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_AuthMapTotalUserCountRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomListReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomListReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomListReq) GetID() uint32 { return Cmd_RoomListReq }
func (p *Msg_RoomListReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomListReq) BuildUDP(sender uint32) []byte {
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
func (r *Msg_RoomFinishInfoListReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomFinishInfoListReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomFinishInfoListReq) GetID() uint32 { return Cmd_RoomFinishInfoListReq }
func (p *Msg_RoomFinishInfoListReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomFinishInfoListReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomListRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomListRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomListRes) GetID() uint32 { return Cmd_RoomListRes }
func (p *Msg_RoomListRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomListRes) BuildUDP(sender uint32) []byte {
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
func (r *Msg_RoomFinishInfoListRes) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomFinishInfoListRes) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomFinishInfoListRes) GetID() uint32 { return Cmd_RoomFinishInfoListRes }
func (p *Msg_RoomFinishInfoListRes) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomFinishInfoListRes) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomRiderUpdateNotify) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomRiderUpdateNotify) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomRiderUpdateNotify) GetID() uint32 { return Cmd_RoomRiderUpdateNotify }
func (p *Msg_RoomRiderUpdateNotify) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomRiderUpdateNotify) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_RoomClientLeaveNotify) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_RoomClientLeaveNotify) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_RoomClientLeaveNotify) GetID() uint32 { return Cmd_RoomClientLeaveNotify }
func (p *Msg_RoomClientLeaveNotify) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_RoomClientLeaveNotify) BuildUDP(sender uint32) []byte {
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
func (r *Msg_GameRiderPosSyncNotify) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_GameRiderPosSyncNotify) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_GameRiderPosSyncNotify) GetID() uint32 { return Cmd_GameRiderPosSyncNotify }
func (p *Msg_GameRiderPosSyncNotify) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_GameRiderPosSyncNotify) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}
func (r *Msg_AdminAdminSetReq) Encode() ([]byte, error) {
	return msgpack.Marshal(r)
}

func (r *Msg_AdminAdminSetReq) Decode(data []byte) error {
	return msgpack.Unmarshal(data, r)
}
func (p *Msg_AdminAdminSetReq) GetID() uint32 { return Cmd_AdminAdminSetReq }
func (p *Msg_AdminAdminSetReq) BuildTCP(errCode ErrorCode) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeader{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Error: uint32(errCode)}
	return append(hdr.Encode(), body...)
}
func (p *Msg_AdminAdminSetReq) BuildUDP(sender uint32) []byte {
	body, _ := p.Encode()
	hdr := &Sys_PackHeaderUDP{Version: uint32(CurrentVersion), Command: p.GetID(), Length: uint32(len(body)), Sender: sender, Error: 0}
	return append(hdr.Encode(), body...)
}