// Package base - Pack 함수 회귀 테스트 (소켓 불필요, 순수 바이트 검증)
package base

import (
	"encoding/binary"
	"testing"
)

// TestPackRoundtrip - Pack이 24바이트 헤더 각 필드를 규격대로 채우는지 라운드트립 검증
func TestPackRoundtrip(t *testing.T) {
	body := []byte("hello-zlink")
	data := Pack(42, body, 1001, 7, 3)

	if len(data) != HeaderSize+len(body) {
		t.Fatalf("전체 길이 불일치: got=%d want=%d", len(data), HeaderSize+len(body))
	}
	if got := binary.LittleEndian.Uint16(data[0:2]); got != MagicZO {
		t.Errorf("magic 불일치: got=%x want=%x", got, MagicZO)
	}
	if got := binary.LittleEndian.Uint32(data[2:6]); got != 3 {
		t.Errorf("version 불일치: got=%d", got)
	}
	if got := binary.LittleEndian.Uint32(data[6:10]); got != 42 {
		t.Errorf("command 불일치: got=%d", got)
	}
	if got := binary.LittleEndian.Uint32(data[10:14]); got != uint32(len(body)) {
		t.Errorf("length 불일치: got=%d want=%d", got, len(body))
	}
	if got := binary.LittleEndian.Uint32(data[14:18]); got != 1001 {
		t.Errorf("sessionID 불일치: got=%d", got)
	}
	if got := binary.LittleEndian.Uint32(data[18:22]); got != 7 {
		t.Errorf("errCode 불일치: got=%d", got)
	}
	if got := string(data[HeaderSize:]); got != string(body) {
		t.Errorf("body 불일치: got=%q want=%q", got, string(body))
	}
}

// TestPackEmptyBody - 빈 바디면 헤더만 생성되고 length=0 인지 검증
func TestPackEmptyBody(t *testing.T) {
	data := Pack(1, nil, 0, 0, 1)
	if len(data) != HeaderSize {
		t.Fatalf("빈 바디인데 길이=%d (헤더 %d 기대)", len(data), HeaderSize)
	}
	if got := binary.LittleEndian.Uint32(data[10:14]); got != 0 {
		t.Errorf("length는 0이어야 함: got=%d", got)
	}
}
