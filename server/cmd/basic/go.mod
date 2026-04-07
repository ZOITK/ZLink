module github.com/ZOITK/ZLink/examples/basic

go 1.25.6

require (
	github.com/ZOITK/ZLink/engine/server-go v0.0.1
	github.com/vmihailenco/msgpack/v5 v5.4.1
)

require github.com/vmihailenco/tagparser/v2 v2.0.0 // indirect

replace github.com/ZOITK/ZLink/engine/server-go => ../../pkg
