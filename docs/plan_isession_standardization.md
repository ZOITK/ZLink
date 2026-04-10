# ZLink ISession 인터페이스 표준화 계획

ZLink 엔진과 자동 생성되는 프로토콜 간의 세션 인터페이스(`ISession`) 불일치를 해결하고, 실무에 필요한 핵심 기능을 표준화합니다.

## 수정 목표
엔진(`session.go`)과 제네레이터(`go_generator.py`)가 생성하는 인터페이스 규격을 일치시켜, 순환 참조 없이도 비즈니스 로직(Handler)에서 세션의 모든 핵심 기능을 사용할 수 있도록 합니다.

## 표준 ISession 규격
```go
type ISession interface {
	ID() uint32
	SendRaw(data []byte) error
	SendRawUDP(data []byte, addr string, port int) error
	Close()
	GetMetadata() any
	SetMetadata(data any)
}
```

## 작업 상세

### 1. ZLink SDK 엔진 수정
- **파일**: `sdk/server/zlink/network/session.go`
- **내용**: `ISession` 인터페이스 정의를 위의 표준 규격으로 통일.

### 2. ZLink 제네레이터 템플릿 수정
- **파일**: `generator/src/generators/go_generator.py`
- **내용**: `protocol.go` 생성 시 포함되는 `ISession` 정의를 표준 규격으로 업데이트.

### 3. 프로토콜 코드 일괄 재생성
- `basic.yaml` (ZLink SDK용) 재생성
- `moduta.yaml` (Moduta 서버용) 재생성

## 검증 계획
- ZLink SDK 빌드 성공 여부 확인
- Moduta 서버 빌드 성공 여부 확인
