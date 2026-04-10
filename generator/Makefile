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
	echo "🔨 선택된 스키마로 프로토콜 생성 중..."; \
	mkdir -p $(OUTPUT_DIR); \
	uv run python -m src.cli generate \
		--schema $$SELECTED \
		--go-out $(OUTPUT_DIR)/protocol.go \
		--py-out $(OUTPUT_DIR)/protocol.py \
		--cs-out $(OUTPUT_DIR)/Protocol.cs; \
	echo "✅ output 폴더에 생성 완료!"; \
	echo "🚚 examples 프로젝트에 배포 중..."; \
	mkdir -p ../examples/server-go/protocol && cp $(OUTPUT_DIR)/protocol.go ../examples/server-go/protocol/; \
	mkdir -p ../examples/client-py/protocol && cp $(OUTPUT_DIR)/protocol.py ../examples/client-py/protocol/; \
	mkdir -p ../examples/client-unity/protocol && cp $(OUTPUT_DIR)/Protocol.cs ../examples/client-unity/protocol/; \
	echo "✅ 생성 및 배포 완료!"

help:
	@echo "ZLink Protocol Generator - 사용 가능한 명령어"
	@echo ""
	@echo "프로토콜 생성:"
	@echo "  make gen                스키마 선택해서 output/에 생성 및 examples에 배포"
	@echo ""
	@echo "출력 위치:"
	@echo "  output/protocol.go      Go 서버 protocol (기본: basic.yaml)"
	@echo "  output/protocol.py      Python 클라이언트 protocol"
	@echo "  output/Protocol.cs      Unity 클라이언트 protocol"
	@echo ""
	@echo "배포 위치:"
	@echo "  examples/server-go/protocol/"
	@echo "  examples/client-py/zlink/protocol/"
	@echo "  examples/client-unity/Assets/Zlink/protocol/"
	@echo ""
	@echo "도움말:"
	@echo "  make help               이 메시지 출력"
	@echo ""
	@echo "📝 사용 예시:"
	@echo "  # basic.yaml로 프로토콜 생성 및 examples에 배포"
	@echo "  make gen"
