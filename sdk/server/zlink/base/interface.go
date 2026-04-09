// Package base - 프레임워크 전역에서 사용하는 공용 규격 정의
package base

// ISession - 엔진 세션 기능을 추상화한 인터페이스 (비즈니스 로직용)
// 이 인터페이스는 순환 참조를 방지하기 위해 base 패키지에 선언하며,
// 엔진(network)과 제네레이터 결과물(protocol) 양쪽에서 참조합니다.
type ISession interface {
	ID() uint32
	SendRaw(data []byte) error
	SendRawUDP(data []byte, addr string, port int) error
	Close()
	GetMetadata() any
	SetMetadata(data any)
}

// IPacket - 모든 패킷 구조체가 구현하는 인터페이스
type IPacket interface {
	GetID() uint32
}
