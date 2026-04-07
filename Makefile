# Zoit Socket Framework (ZPP v7.0) Makefile

# 경로 정의
SCHEMAS_DIR = schemas
GENERATOR_DIR = generator
ENGINE_DIR = engine
TEMPLATES_DIR = templates
SCRIPTS_DIR = scripts

# 생성 대상 경로
GO_SRV_OUT = $(TEMPLATES_DIR)/server-go/protocol
GO_CLI_OUT = $(TEMPLATES_DIR)/client-go/protocol
CS_OUT = $(TEMPLATES_DIR)/client-csharp/Protocol
PY_OUT = $(TEMPLATES_DIR)/client-python/protocol

# uv 설치 확인
UV := $(shell command -v uv 2> /dev/null)

# Python 명령어
PYTHON := python3

.PHONY: all gen check-uv check-python server client help

all: gen

# uv 존재 여부 확인 및 안내
check-uv:
ifndef UV
	@echo "[ERROR] uv가 설치되어 있지 않습니다."
	@echo "설치 방법 (macOS/Linux): curl -LsSf https://astral.sh/uv/install.sh | sh"
	@exit 1
endif

# Python 존재 여부 확인 및 안내
check-python:
	@command -v $(PYTHON) > /dev/null 2>&1 || { \
		echo "[ERROR] Python3이 설치되어 있지 않습니다."; \
		exit 1; \
	}

# 프로토콜 코드 생성 및 배포 (대화형 선택)
gen: check-uv
	@FILES=$$(ls $(SCHEMAS_DIR)/*.yaml 2>/dev/null); \
	COUNT=$$(echo $$FILES | wc -w | tr -d ' '); \
	if [ "$$COUNT" -eq 0 ]; then \
		echo "[ERROR] schemas/ 폴더에 .yaml 파일이 없습니다."; \
		exit 1; \
	elif [ "$$COUNT" -eq 1 ]; then \
		SELECTED_SCHEMA=$$FILES; \
	else \
		echo "[Makefile] 사용할 스키마 파일을 선택하세요:"; \
		i=1; \
		for f in $$FILES; do \
			echo "  $$i) $$(basename $$f)"; \
			i=$$((i+1)); \
		done; \
		printf "번호 입력 (1-$$COUNT): "; \
		read choice < /dev/tty; \
		if ! [ "$$choice" -ge 1 ] 2>/dev/null || ! [ "$$choice" -le "$$COUNT" ] 2>/dev/null; then \
			echo "[ERROR] 잘못된 선택입니다."; exit 1; \
		fi; \
		SELECTED_SCHEMA=$$(echo $$FILES | tr ' ' '\n' | sed -n "$${choice}p"); \
	fi; \
	echo "[Makefile] 선택된 스키마: $$SELECTED_SCHEMA"; \
	echo "[Makefile] 프로토콜 코드 생성 시작 (using uv)..."; \
	mkdir -p $(GO_SRV_OUT) $(GO_CLI_OUT) $(CS_OUT) $(PY_OUT); \
	cd $(GENERATOR_DIR) && uv run python -m src.cli generate \
		--schema ../$$SELECTED_SCHEMA \
		--go-out ../$(GO_SRV_OUT)/Protocol.go \
		--cs-out ../$(CS_OUT)/Protocol.cs \
		--py-out ../$(PY_OUT)/Protocol.py; \
	cp $(GO_SRV_OUT)/Protocol.go $(GO_CLI_OUT)/Protocol.go; \
	echo "[Makefile] 모든 프로젝트에 프로토콜 코드가 배포되었습니다."

# Go 서버 프로젝트 생성
server: check-python
	@if [ -z "$(OUTPUT)" ]; then \
		echo "[ERROR] 사용법: make server OUTPUT=<output-path> [ENGINE_VERSION=...] [ENGINE_LOCAL=...]"; \
		echo "  예: make server OUTPUT=../zo-moduta-server-go"; \
		echo "  예: make server OUTPUT=../zo-moduta-server-go ENGINE_VERSION=v0.2.0"; \
		echo "  예: make server OUTPUT=../zo-moduta-server-go ENGINE_LOCAL=./engine/server-go"; \
		exit 1; \
	fi
	@echo "[Makefile] Go 서버 프로젝트 생성..."
	@$(PYTHON) $(SCRIPTS_DIR)/project_generator.py server $(OUTPUT) \
		--engine-version "$(ENGINE_VERSION)" \
		--engine-local "$(ENGINE_LOCAL)"

# 클라이언트 프로젝트 생성
client: check-python
	@if [ -z "$(LANG)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "[ERROR] 사용법: make client LANG=<language> OUTPUT=<output-path> [ENGINE_VERSION=...] [ENGINE_LOCAL=...]"; \
		echo "  지원 언어: python, csharp"; \
		echo "  예: make client LANG=python OUTPUT=../zo-moduta-client-python"; \
		echo "  예: make client LANG=csharp OUTPUT=../zo-moduta-client-unity"; \
		exit 1; \
	fi
	@echo "[Makefile] $(LANG) 클라이언트 프로젝트 생성..."
	@$(PYTHON) $(SCRIPTS_DIR)/project_generator.py client $(LANG) $(OUTPUT) \
		--engine-version "$(ENGINE_VERSION)" \
		--engine-local "$(ENGINE_LOCAL)"

# 도움말
help:
	@echo "Zo Socket Framework 사용 가능한 명령어:"
	@echo ""
	@echo "📋 프로토콜 생성:"
	@echo "  make gen   - 대화형 메뉴를 통해 스키마를 선택하고 프로토콜 코드를 생성합니다."
	@echo "  make all   - 기본 작업을 수행합니다 (gen)."
	@echo ""
	@echo "🚀 프로젝트 생성:"
	@echo "  make server OUTPUT=<path>                - Go 서버 프로젝트 생성"
	@echo "  make client LANG=python OUTPUT=<path>   - Python 클라이언트 생성"
	@echo "  make client LANG=csharp OUTPUT=<path>   - Unity3D C# 클라이언트 생성"
	@echo ""
	@echo "📝 예시:"
	@echo "  make server OUTPUT=../zo-moduta-server-go"
	@echo "  make client LANG=python OUTPUT=../zo-moduta-client-python"
	@echo "  make client LANG=csharp OUTPUT=../zo-moduta-client-unity"
