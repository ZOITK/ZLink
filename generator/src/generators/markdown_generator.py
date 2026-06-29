# 마크다운 프로토콜 명세서 생성기
#
# moduta.yaml 같은 스키마(SSOT)에서 "사람이 읽는" 프로토콜 명세서(.md)를 생성합니다.
# 코드 생성기(go/cs/py)는 데이터 구조만 만들지만, 이 생성기는 클라이언트 개발자가
# "어떤 메시지를 어떤 순서로(흐름), 각 필드가 무슨 의미인지(설명)" 파악하도록 돕습니다.
#
# 다른 생성기와 달리 ProtocolDef(평면화된 모델)가 아니라 원본 YAML dict를 받습니다.
# 카테고리 그룹·req/res 짝·필드 설명 같은 "문서용 구조"가 원본에 그대로 있기 때문입니다.


def _type_and_desc(f_data):
    """
    필드 정의를 (타입, 설명)으로 분해합니다.
    - "Name: string"                          → ("string", "")
    - "Name: { type: string, desc: '설명' }"   → ("string", "설명")
    (loader.parse_field와 동일한 두 형식 규칙)
    """
    if isinstance(f_data, str):
        return f_data, ""
    return f_data.get("type", ""), f_data.get("desc", "")


def _field_table(fields):
    """필드 dict를 '필드 | 타입 | 설명' 표로 변환합니다."""
    rows = ["| 필드 | 타입 | 설명 |", "|------|------|------|"]
    if not fields:
        rows.append("| _(없음)_ | | |")
        return rows
    for name, fdata in fields.items():
        t, d = _type_and_desc(fdata)
        rows.append(f"| {name} | {t} | {d} |")
    return rows


class MarkdownGenerator:
    """원본 스키마 dict를 받아 마크다운 명세서를 렌더링합니다."""

    def __init__(self, spec: dict):
        self.spec = spec

    # 메시지 클래스 이름 규칙: Msg_<Category><Name><Suffix>
    def _msg_name(self, cat, name, suffix):
        return f"Msg_{cat.capitalize()}{name}{suffix}"

    def render(self) -> str:
        spec = self.spec
        meta = spec.get("metadata", {})
        L = []

        L.append(f"# 프로토콜 명세 (v{meta.get('version', '')})")
        L.append("")
        L.append("> 스키마(SSOT)에서 자동 생성됨 — 직접 수정 금지. `make protocol` 시 갱신됩니다.")
        L.append("")

        # 전역 에러 코드
        errors = spec.get("global_errors", [])
        if errors:
            L.append("## 전역 에러 코드")
            L.append("")
            L.append("| 코드 | 값 | 설명 |")
            L.append("|------|-----|------|")
            for e in errors:
                L.append(f"| Err_{e['name']} | {e['idx']} | {e.get('doc', '')} |")
            L.append("")

        definitions = spec.get("definitions", {})

        # 메시지 목차 (전체 흐름 파악용)
        L.append("## 메시지 목차 (카테고리별)")
        L.append("")
        for cat, content in definitions.items():
            entries = []
            for p in content.get("packets", []):
                kind = "알림" if p.get("type") == "notify" else "요청/응답"
                entries.append(f"`{p['name']}`({kind})")
            L.append(f"- **{cat}**: " + ", ".join(entries))
        L.append("")

        # 카테고리별 상세
        for cat, content in definitions.items():
            L.append("\n---")
            L.append(f"## {cat}")
            L.append("")

            # 공용 구조체
            structs = content.get("structs", {})
            if structs:
                L.append("### 공용 구조체")
                L.append("")
                for sname, sdef in structs.items():
                    L.append(f"**{sname}** — {sdef.get('doc', '')}")
                    L.append("")
                    L += _field_table(sdef.get("fields"))
                    L.append("")

            # 패킷
            for p in content.get("packets", []):
                name = p["name"]
                proto = p.get("proto", "")
                is_notify = p.get("type") == "notify"
                direction = f"[알림 ← 서버] `{proto}`" if is_notify else f"[요청 → 응답] `{proto}`"
                L.append(f"### {name} — {p.get('doc', '')}   {direction}")
                if p.get("desc"):
                    L.append(f"_{p['desc']}_")
                L.append("")

                if is_notify:
                    L.append(f"**알림** `{self._msg_name(cat, name, 'Notify')}`")
                    L.append("")
                    L += _field_table(p.get("fields"))
                    L.append("")
                else:
                    pair = p.get("pair")
                    req = (pair.get("req") if pair else p.get("req", {})).get("fields")
                    res = (pair.get("res") if pair else p.get("res", {})).get("fields")
                    L.append(f"**요청** `{self._msg_name(cat, name, 'Req')}`")
                    L.append("")
                    L += _field_table(req)
                    L.append("")
                    L.append(f"**응답** `{self._msg_name(cat, name, 'Res')}`")
                    L.append("")
                    L += _field_table(res)
                    L.append("")

        return "\n".join(L)
