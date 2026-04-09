// Package network - 고성능 버퍼 풀링
package network

import (
	"sync"
	 "github.com/ZOITK/ZLink/sdk/server/zlink/base"
)

// BufferPool - 바이트 슬라이스 재사용을 위한 풀
type BufferPool struct {
	headerPool sync.Pool
	bodyPool   sync.Pool
}

// NewBufferPool - 새 버퍼 풀 생성
func NewBufferPool() *BufferPool {
	return &BufferPool{
		headerPool: sync.Pool{
			New: func() any {
				return make([]byte, base.TCPHeaderSize) // 16 bytes (UDP 20 bytes도 커버 가능)
			},
		},
		bodyPool: sync.Pool{
			New: func() any {
				// 기본 바디 크기 (필요시 동적으로 조절 가능)
				return make([]byte, 1024)
			},
		},
	}
}

// GetHeader - 헤더용 버퍼 획득 (고정 크기)
func (p *BufferPool) GetHeader() []byte {
	return p.headerPool.Get().([]byte)
}

// PutHeader - 헤더용 버퍼 반납
func (p *BufferPool) PutHeader(b []byte) {
	if cap(b) >= base.TCPHeaderSize {
		p.headerPool.Put(b[:base.TCPHeaderSize])
	}
}

// GetBody - 바디용 버퍼 획득 (가변 크기 대응)
func (p *BufferPool) GetBody(size uint32) []byte {
	if size <= 1024 {
		return p.bodyPool.Get().([]byte)[:size]
	}
	// 1024보다 큰 경우는 새로 할당 (임계값 조정 가능)
	return make([]byte, size)
}

// PutBody - 바디용 버퍼 반납
func (p *BufferPool) PutBody(b []byte) {
	if cap(b) == 1024 {
		p.bodyPool.Put(b[:1024])
	}
}
