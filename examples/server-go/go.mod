module server-go

go 1.25.6

require github.com/vmihailenco/msgpack/v5 v5.4.1

// 로컬 SDK 모듈을 참조하도록 상대 경로 수정
replace zlink => ../../sdk/server/zlink

require zlink v0.0.0

require github.com/vmihailenco/tagparser/v2 v2.0.0 // indirect
