module server-example

go 1.25.6

replace github.com/zoit/zo-socket-framework/engine/server-go => ./engine

require (
	github.com/vmihailenco/msgpack/v5 v5.4.1
	github.com/zoit/zo-socket-framework/engine/server-go v0.0.0-00010101000000-000000000000
)

require github.com/vmihailenco/tagparser/v2 v2.0.0 // indirect
