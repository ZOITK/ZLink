module zlink-example-server

go 1.25.6

replace zlink => ../../sdk/server/zlink

require (
	github.com/vmihailenco/msgpack/v5 v5.4.1
	zlink v0.0.0
)

require github.com/vmihailenco/tagparser/v2 v2.0.0 // indirect
