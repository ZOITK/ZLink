module zlink-sample

go 1.25.6

require github.com/vmihailenco/msgpack/v5 v5.4.1

// 로컬 zlink 모듈을 참조하도록 설정 (Ultimate Portability)
replace zlink => ./zlink

require zlink v0.0.0

require github.com/vmihailenco/tagparser/v2 v2.0.0 // indirect
