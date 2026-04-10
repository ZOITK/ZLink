module zlink-example-server

go 1.25.6

// 로컬 개발 환경을 위해 zlink 모듈을 로컬 폴더로 연결합니다.
replace zlink => ../../sdk/server/zlink

require (
	github.com/vmihailenco/msgpack/v5 v5.4.1
	zlink v0.0.0
)

require github.com/vmihailenco/tagparser/v2 v2.0.0 // indirect
