# ZLink Server Makefile

.PHONY: build run help

# 기본 타겟
build:
	@echo "🔨 Building server examples..."
	@cd cmd/basic && go build -o server_bin main.go && cd ../..
	@cd cmd/game && go build -o server_bin main.go && cd ../..
	@echo "✅ Build complete: cmd/basic/server_bin, cmd/game/server_bin"

run:
	@if [ -z "$(EXAMPLE)" ]; then \
		EXAMPLE=basic; \
	fi; \
	echo "🚀 Running server: $(EXAMPLE)"; \
	cd cmd/$(EXAMPLE) && go run main.go

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
	@echo "  # 프로토콜 생성 (먼저 수행)"
	@echo "  cd ../generator && make gen"
	@echo ""
	@echo "  # 서버 빌드"
	@echo "  make build"
	@echo ""
	@echo "  # 서버 실행"
	@echo "  make run                # basic 서버"
	@echo "  make run EXAMPLE=game   # game 서버"
