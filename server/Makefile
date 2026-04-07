# ZLink Server Makefile

.PHONY: build run help

# 빌드
build:
	@echo "🔨 Building server examples..."
	@cd cmd/basic && go build -o server_bin main.go && echo "✅ cmd/basic/server_bin" && cd ../..
	@cd cmd/game && go build -o server_bin main.go && echo "✅ cmd/game/server_bin" && cd ../..

# 실행 (기본값: basic)
run:
	@example=$${EXAMPLE:-basic}; \
	echo "🚀 Running server: $$example"; \
	cd cmd/$$example && go run main.go

help:
	@echo "ZLink Server - 사용 가능한 명령어"
	@echo ""
	@echo "빌드:"
	@echo "  make build              서버 빌드 (basic, game)"
	@echo ""
	@echo "실행:"
	@echo "  make run                basic 서버 실행 (기본값)"
	@echo "  make run EXAMPLE=game   game 서버 실행"
	@echo ""
	@echo "도움말:"
	@echo "  make help               이 메시지 출력"
	@echo ""
	@echo "📝 사용 예시:"
	@echo "  # 1. 프로토콜 생성"
	@echo "  cd ../generator && make gen"
	@echo ""
	@echo "  # 2. 서버 빌드"
	@echo "  make build"
	@echo ""
	@echo "  # 3. 서버 실행"
	@echo "  make run                # basic 서버"
	@echo "  make run EXAMPLE=game   # game 서버"
