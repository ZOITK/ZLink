module github.com/ZOITK/ZLink/examples/game

go 1.25.6

require (
	github.com/vmihailenco/msgpack/v5 v5.4.1
	github.com/ZOITK/ZLink/engine/server-go v0.0.1
)

replace github.com/ZOITK/ZLink/engine/server-go => ../../pkg
