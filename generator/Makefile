# ZLink Protocol Generator Makefile

.PHONY: gen help gen-sample

# uv 설치 확인
UV := $(shell command -v uv 2> /dev/null)

# 기본 경로
BASIC_SCHEMA = schemas/basic.yaml

# 인자 처리 (대소문자 구분 없이 처리하기 위해 변수 병합)
# 예: make gen schemas=./myschema.yaml output=./out
# 예: make gen sample=1
TARGET_SCHEMA := $(if $(SCHEMAS),$(SCHEMAS),$(schemas))
TARGET_OUTPUT := $(if $(OUTPUT),$(OUTPUT),$(output))
IS_SAMPLE := $(if $(SAMPLE),$(SAMPLE),$(sample))

# 기본 동작: 인자가 없으면 도움말 출력, 있으면 생성 실행
gen:
	@if [ -z "$(UV)" ]; then \
		echo "[ERROR] uv가 설치되어 있지 않습니다."; \
		echo "설치: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	fi
	@if [ -n "$(TARGET_SCHEMA)" ] && [ -n "$(TARGET_OUTPUT)" ]; then \
		echo "🔨 프로토콜 생성 중..."; \
		echo "   - 스키마: $(TARGET_SCHEMA)"; \
		echo "   - 출력경로: $(TARGET_OUTPUT)"; \
		mkdir -p $(TARGET_OUTPUT); \
		uv run python -m src.cli generate \
			--schema $(TARGET_SCHEMA) \
			--go-out $(TARGET_OUTPUT)/protocol.go \
			--py-out $(TARGET_OUTPUT)/protocol.py \
			--cs-out $(TARGET_OUTPUT)/Protocol.cs; \
		echo "✅ 생성 완료!"; \
	elif [ -n "$(IS_SAMPLE)" ]; then \
		$(MAKE) gen-sample; \
	else \
		$(MAKE) help; \
	fi

# 예제 프로토콜 생성 및 엔진 예제 프로젝트 배포 (Requirement 2 단축어)
gen-sample:
	@echo "🔨 예제 프로토콜 생성 및 배포 중..."; \
	echo "   - 스키마: $(BASIC_SCHEMA)"; \
	uv run python -m src.cli generate \
		--schema $(BASIC_SCHEMA) \
		--go-out ../examples/server-go/protocol/protocol.go \
		--py-out ../examples/client-py/protocol/protocol.py \
		--cs-out ../examples/client-unity/protocol/Protocol.cs; \
	echo "✅ 예제 배포 완료!"

help:
	@echo "================================================================================"
	@echo "  ZLink Protocol Generator 사용 방법"
	@echo "================================================================================"
	@echo ""
	@echo "  1. 특정 스키마로 프로토콜 생성"
	@echo "     make gen schemas=./schemas/moduta.yaml output=~/work"
	@echo "     -> 지정된 경로에 protocol.go, protocol.py, Protocol.cs 생성"
	@echo ""
	@echo "  2. 예제용 프로토콜 생성 및 엔진 예제 프로젝트에 배포"
	@echo "     make gen-sample     (또는 make gen sample=1)"
	@echo "     -> schemas/basic.yaml을 사용하여 examples/ 아래의 각 프로젝트로 배포"
	@echo ""
	@echo "  3. 상세 도움말"
	@echo "     make gen"
	@echo ""
	@echo "  * 주의: make 인자 사용 시 '=' 앞뒤에 공백이 없어야 하며, '-' 기호 없이 사용하세요."
	@echo "================================================================================"

# 임의의 인자가 타겟으로 오해받아 에러가 발생하는 것을 방지
%:
	@:
