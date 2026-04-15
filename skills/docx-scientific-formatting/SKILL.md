# Scientific Word Document Formatting

python-docx + lxml로 .docx 파일의 과학 기술 문서 포맷팅을 수정할 때 참조하는 스킬.

Triggers: docx 수정, Word 포맷팅, 아래첨자, 위첨자, chemical formula formatting, 화학식 포맷

## Chemical Formula Rules

### Subscript (아래첨자)
- **화학식 숫자**: SnO2 -> SnO<sub>2</sub>, Ti4O7 -> Ti<sub>4</sub>O<sub>7</sub>, H2O, CO2, O3 등
- **이온 화학식**: Ru0.3Ti0.7O2 -> Ru<sub>0.3</sub>Ti<sub>0.7</sub>O<sub>2</sub>
- **텍스트 라벨**: O_bridH -> O<sub>brid</sub>H, Sn_cus -> Sn<sub>cus</sub>, Ni_cus -> Ni<sub>cus</sub>
- **열역학 기호**: eta_TD -> eta<sub>TD</sub>

### Superscript (위첨자)
- **이온 전하**: Ru2+ -> Ru<sup>2+</sup>, Sn4+ -> Sn<sup>4+</sup>, Cl- -> Cl<sup>-</sup>
- **산화 상태**: Fe3+, Cu2+
- **중간체 표기**: O*, O2*, O3* (asterisk는 위첨자 아님, 그대로 유지)

### Italic (이탤릭)
- **오비탈 표기**: 2p, 4d, d(z2), dxy, dxz 등 orbital label은 italic
- **결정면**: (110), (120) 등은 italic 아님 (Miller index)
- **라틴어/외래 표현**: in-situ, operando, a priori 등은 italic

## Unicode -> Word 정식 포맷 변환

Unicode 아래첨자/위첨자 문자를 Word의 `w:vertAlign` 속성으로 변환:

```
Unicode subscript: ₀₁₂₃₄₅₆₇₈₉ₓ -> 0123456789x + vertAlign=subscript
Unicode superscript: ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ -> 0123456789+- + vertAlign=superscript
```

## python-docx 구현 패턴

### Run 분할 (하나의 run에서 일부만 서식 변경)

```python
import copy
from docx.oxml.ns import qn
from lxml import etree

def split_and_format(run_element, before, target, after, fmt):
    """Run을 3개로 분할: before(원본) + target(서식적용) + after(원본)"""
    parent = run_element.getparent()
    idx = list(parent).index(run_element)
    
    # 원본 run: before 텍스트
    t = run_element.find(qn('w:t'))
    t.text = before
    t.set(qn('xml:space'), 'preserve')
    
    # target run: 서식 적용
    fmt_el = copy.deepcopy(run_element)
    fmt_t = fmt_el.find(qn('w:t'))
    fmt_t.text = target
    fmt_t.set(qn('xml:space'), 'preserve')
    rpr = fmt_el.find(qn('w:rPr'))
    if rpr is None:
        rpr = etree.SubElement(fmt_el, qn('w:rPr'))
        fmt_el.insert(0, rpr)
    
    if fmt == 'sub':
        for va in rpr.findall(qn('w:vertAlign')):
            rpr.remove(va)
        va = etree.SubElement(rpr, qn('w:vertAlign'))
        va.set(qn('w:val'), 'subscript')
    elif fmt == 'sup':
        for va in rpr.findall(qn('w:vertAlign')):
            rpr.remove(va)
        va = etree.SubElement(rpr, qn('w:vertAlign'))
        va.set(qn('w:val'), 'superscript')
    elif fmt == 'italic':
        i_el = etree.SubElement(rpr, qn('w:i'))
        i_el.set(qn('w:val'), 'true')
    
    parent.insert(idx + 1, fmt_el)
    
    # after run
    if after:
        rest_el = copy.deepcopy(run_element)
        rest_t = rest_el.find(qn('w:t'))
        rest_t.text = after
        rest_t.set(qn('xml:space'), 'preserve')
        # 서식 초기화 (복사된 원본 서식 유지, vertAlign만 제거)
        rest_rpr = rest_el.find(qn('w:rPr'))
        if rest_rpr is not None:
            for va in rest_rpr.findall(qn('w:vertAlign')):
                rest_rpr.remove(va)
            for it in rest_rpr.findall(qn('w:i')):
                rest_rpr.remove(it)
        parent.insert(idx + 2, rest_el)
```

### 주의사항
- Run 분할 시 **원본 run의 text를 before로 변경**하고, target/after는 **새 run으로 insert**
- `after` 텍스트에 target 문자열이 포함되지 않도록 주의 (중복 방지)
- `xml:space='preserve'` 필수 (공백 보존)
- 기존 `vertAlign` 제거 후 새로 추가 (누적 방지)
- 역순으로 처리하거나, insert 후 index 갱신 필요

## 번역체 주의 (과학 용어)

### 영어 원문 그대로 쓸 것 (한글 음차 금지)
학계에서 한국어로 안 쓰는 용어는 영어 원문 유지:

| 한글 음차 (X) | 영어 원문 (O) |
|---|---|
| 캐릭터라이제이션 | characterization |
| 밸런스 밴드 | valence band |
| 피복률 | coverage |
| 오버레이어 | overlayer |
| 디스크립터 | descriptor |
| 컨덕션 밴드 | conduction band |
| 헤테로정션 | heterojunction |
| 메커니즘 | mechanism |

### 번역체 표현 수정
| 번역체 (X) | 자연스러운 표현 (O) | 원어 |
|---|---|---|
| 진화 메커니즘 | 발생 메커니즘 | evolution mechanism |
| 활성 사이트 | 활성점 | active site |
| 결정적인 역할 | 주요 역할 | crucial role |
