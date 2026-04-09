# ZLink Protocol Generator Makefile

.PHONY: gen help

# uv 설치 확인
UV := $(shell command -v uv 2> /dev/null)

# 경로
SCHEMAS_DIR = schemas
OUTPUT_DIR = output

gen:
	@if [ -z "$(UV)" ]; then \
		echo "[ERROR] uv가 설치되어 있지 않습니다."; \
		echo "설치: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	fi
	@FILES=$$(ls $(SCHEMAS_DIR)/*.yaml 2>/dev/null); \
	COUNT=$$(echo $$FILES | wc -w | tr -d ' '); \
	if [ "$$COUNT" -eq 0 ]; then \
		echo "[ERROR] $(SCHEMAS_DIR)에 YAML 파일이 없습니다."; \
		exit 1; \
	elif [ "$$COUNT" -eq 1 ]; then \
		SELECTED=$$FILES; \
	else \
		echo "📋 사용할 스키마를 선택하세요:"; \
		i=1; \
		for f in $$FILES; do \
			echo "  $$i) $$(basename $$f)"; \
			i=$$((i+1)); \
		done; \
		printf "번호 입력 (1-$$COUNT): "; \
		read choice; \
		if ! [ "$$choice" -ge 1 ] 2>/dev/null || ! [ "$$choice" -le "$$COUNT" ] 2>/dev/null; then \
			echo "[ERROR] 잘못된 선택입니다."; exit 1; \
		fi; \
		SELECTED=$$(echo $$FILES | tr ' ' '\n' | sed -n "$${choice}p"); \
	fi; \
	echo "✅ 선택: $$(basename $$SELECTED)"; \
	echo "🔨 프로토콜 생성 중..."; \
	mkdir -p $(OUTPUT_DIR); \
	uv run python -m src.cli generate \
		--schema $$SELECTED \
		--go-out $(OUTPUT_DIR)/Protocol.go \
		--py-out $(OUTPUT_DIR)/Protocol.py \
		--cs-out $(OUTPUT_DIR)/Protocol.cs; \
	echo "✅ 생성 완료:"; \
	echo "   - $(OUTPUT_DIR)/Protocol.go"; \
	echo "   - $(OUTPUT_DIR)/Protocol.py"; \
	echo "   - $(OUTPUT_DIR)/Protocol.cs"; \
	echo "🚚 프로젝트 배포 및 SDK 동기화 중..."; \
	# 1. SDK 내부로 프로토콜 배포 \
	cp $(OUTPUT_DIR)/Protocol.go ../sdk/server/zlink/protocol/; \
	cp $(OUTPUT_DIR)/Protocol.py ../sdk/client/py/zlink/protocol/; \
	cp $(OUTPUT_DIR)/Protocol.cs ../sdk/client/unity/zlink/protocol/; \
	# 2. 예제 프로젝트로 최신 SDK 동기화 (사용자 편의성) \
	mkdir -p ../examples/client-py/zlink && cp -R ../sdk/client/py/zlink/* ../examples/client-py/zlink/; \
	mkdir -p ../examples/client-unity/Assets/zlink && cp -R ../sdk/client/unity/zlink/* ../examples/client-unity/Assets/zlink/; \
	echo "✅ 배포 및 동기화 완료!"

help:
	@echo "ZLink Protocol Generator - 사용 가능한 명령어"
	@echo ""
	@echo "프로토콜 생성:"
	@echo "  make gen                스키마 선택해서 Protocol.* 생성 및 각 프로젝트 배포"
	@echo ""
	@echo "도움말:"
	@echo "  make help               이 메시지 출력"
	@echo ""
	@echo "📝 사용 예시:"
	@echo "  # 프로토콜 생성 및 자동 배포"
	@echo "  make gen"
