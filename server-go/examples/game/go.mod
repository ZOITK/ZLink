module {{PROJECT_NAME}}

go 1.25.6
{{ENGINE_LOCAL_REPLACE}}
require (
	github.com/vmihailenco/msgpack/v5 v5.4.1
	github.com/ZOITK/ZLink/engine/server-go v0.0.1
)

require github.com/vmihailenco/tagparser/v2 v2.0.0 // indirect
