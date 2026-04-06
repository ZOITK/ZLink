# 프로젝트 생성 기능 구현 계획 (Zo Socket Framework)

## 목표
현재의 샘플 예제 기반 프레임워크에서 **프로젝트 생성 기능**을 갖춘 프레임워크로 개선

## 요구사항

### 1. 명령어 인터페이스
```bash
# 서버 프로젝트 생성
make server <output-path>
# 예: make server /path/to/zo-moduta-server-go
#     make server zo-moduta-server-go (상대경로)

# 클라이언트 프로젝트 생성
make client <language> <output-path>
# 예: make client python ../zo-moduta-client-python
#     make client csharp ../zo-moduta-client-unity
```

### 2. 생성 구조
#### 서버 (Go만)
- Go 서버 보일러플레이트 (TCP/UDP 통신 준비)
- engine 폴더를 **복사하여** 내부 모듈로 포함
- **기본 Protocol.go 생성** (빈 구조체/함수로 컴파일 가능 상태)
- go.mod: engine 의존성 상대경로로 설정
- 사용자는 나중에 `make gen`으로 실제 프로토콜로 교체 가능

#### 클라이언트 (Python, Unity3D C#만)
**Python:**
- Python 클라이언트 보일러플레이트
- engine 폴더를 **복사하여** 포함
- **기본 Protocol.py 생성** (빈 클래스로 실행 가능 상태)
- 패키지 구조 (추후 PyPI 배포 가능)
- 사용자는 나중에 `make gen`으로 실제 프로토콜로 교체 가능

**Unity3D C# (Assets 폴더 지원):**
- Assets/구조로 생성 가능
- engine 폴더를 **Assets 내부에 복사**하여 포함
- **기본 Protocol.cs 생성** (빈 클래스로 컴파일 가능 상태)
- .gitignore, .meta 파일 포함
- 사용자는 나중에 `make gen`으로 실제 프로토콜로 교체 가능

### 3. 모듈화 전략
- **현재**: 각 생성된 프로젝트마다 engine 폴더 전체 복사
- **미래**: GitHub에서 engine을 별도 모듈로 import 가능하도록 설계
- go.mod, pyproject.toml 등에 명확한 의존성 표시

### 4. 생성 파일 구조 예시

**서버 (Go):**
```
[output-path]/
├── go.mod
├── main.go
├── engine/
│   ├── server-go/
│   └── ...
├── .gitignore
└── README.md
```

**Python 클라이언트:**
```
[output-path]/
├── pyproject.toml
├── main.py
├── engine/
│   ├── client-python/
│   └── ...
├── .gitignore
└── README.md
```

**Unity3D C# 클라이언트:**
```
[output-path]/Assets/
├── ZoSocket/
│   ├── Client/
│   └── Protocol/
│       └── Protocol.cs (나중에 make gen으로 생성)
└── engine/ (복사된 engine 폴더)
    └── client-csharp/
```

## 구현 단계

| 단계 | 작업 | 검증 |
|------|------|------|
| 1 | Makefile 명령어 파싱 추가 (server, client) | make help에 새 명령어 표시 |
| 2 | 서버 (Go) 생성 기능 구현 | `make server test-server` 실행 후 폴더 및 engine 복사 확인 |
| 3 | 클라이언트 (Python) 생성 기능 구현 | `make client python test-client-py` 실행 후 폴더 및 engine 복사 확인 |
| 4 | 클라이언트 (Unity3D C#) 생성 기능 구현 | `make client csharp test-unity` 실행 후 Assets 구조 및 engine 복사 확인 |
| 5 | 통합 테스트 | 각 프로젝트에서 실제 동작 테스트 |

## 기술적 고려사항
- **경로 처리**: 절대경로/상대경로 모두 지원
- **기존 폴더 처리**: 충돌 시 사용자 확인 후 처리
- **Protocol 파일**: 자동 생성 여부 선택 (초기화 시점의 스키마 적용)
- **의존성**: engine 폴더 링크 또는 복사 (go.mod, pyproject.toml으로 관리)

## 협의 항목
1. ✅ 파라미터 기반 경로 입력
2. ✅ 모듈화 (내부 패키지 기반)
3. ✅ Go, Python, Unity3D C# 지원
4. ✅ Unity Assets 폴더 지원

→ **다음 단계**: 구현 승인 후 Makefile 수정 및 생성 스크립트 작성
