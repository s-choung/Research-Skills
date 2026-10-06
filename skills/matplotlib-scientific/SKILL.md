# Matplotlib Scientific Figure Skill

Use when creating matplotlib plots, scientific figures, or data visualizations.
Triggers - matplotlib, plot, figure, 그래프, 플롯, 시각화, visualization, "그려줘", "plot 만들어", scatter, histogram, violin

## Child skills (same folder)

- `rxn-diagram-inset/` - reaction energy diagram with Blender-rendered structure insets next to each state. Read `rxn-diagram-inset/SKILL.md` when the user asks for 인셋 다이어그램, energy diagram with structures, or 다이어그램에 구조 그림. Depends on the standalone `rxn-diagram` skill for the base profile.

## Mandatory Rules

1. **One plot per script** - standalone Python file
2. **ALL text uses FontProperties** - no raw matplotlib text
3. **No Unicode math** - use `$_{sub}$` / `$^{sup}$` / `$\mathregular{_2}$`
4. **No grids, no bold, no `tight_layout()`, no `plt.show()`**
5. **SVG only** at 300 DPI, save to `./output/`
6. **All data within xlim/ylim** with 5-10% padding
7. **Sensible axes sizing — do NOT cram.** Never force `ax.set_position([0.2, 0.2, 0.666, 0.333])` (it squishes data into 1/3 height → labels/legend collide). Use default subplot proportions with `figsize` ≥ `(6.0, 5.4)` (single-panel은 정사각 `(6, 6)` 권장) and let `plt.savefig(..., bbox_inches='tight')` crop. 폰트 위계: **tick = text = legend = annotate 동일 크기, axis label만 한 단계 크게** (예 16 / 18). annotate를 tick보다 작게 두지 말 것. Only use `set_position` for deliberate multi-panel composition.
8. **Integer-typed x/y axes** (year, count, index) MUST use integer ticks - no `2022.5` labels. Use `MaxNLocator(integer=True)` or `set_xticks(np.arange(...))` with 1-year spacing.
9. **Legend OUTSIDE the axes by default.** `loc='best'`는 데이터를 가리는 사고가 반복되어 금지. 기본은 plot 밖 배치: `ax.legend(prop=font_properties_legend, frameon=False, loc='upper left', bbox_to_anchor=(1.02, 1.0))` + `savefig(..., bbox_inches='tight')` (legend 잘림 방지). 항목이 1~2개이고 audit로 데이터와 절대 안 겹침을 확인한 경우에만 내부 배치 허용하되 boxed 스타일(`frameon=True, framealpha=1.0, edgecolor='#bbbbbb', facecolor='white'`) 사용. audit 시 legend bbox와 데이터 포인트 겹침도 검사할 것.
10. **텍스트는 axes 프레임 밖으로 나가면 안 된다 (2026-08-31 사고 재발 방지).** annotate와 끝값 라벨의 bbox가 axes 프레임을 벗어나거나 걸치면 실패다. (a) 라벨이 차지할 공간만큼 xlim/ylim에 여유를 먼저 확보하고, (b) audit에서 텍스트 bbox가 axes `get_window_extent()` 안에 완전히 들어가는지 검사할 것 (아래 audit_frame_overflow). SVG를 HTML에 넣는 경우 브라우저 재조판 여유 26px을 collision box에 추가.

### Frame overflow 검사 (audit_text_overlap과 함께 필수 실행)

```python
def audit_frame_overflow(fig):
    """Texts (annotate 등) whose bbox leaves their axes frame."""
    renderer = fig.canvas.get_renderer()
    bad = []
    for a in fig.get_axes():
        axbb = a.get_window_extent(renderer=renderer)
        for t in a.texts:
            if not t.get_text().strip():
                continue
            bb = t.get_window_extent(renderer=renderer)
            if (bb.x0 < axbb.x0 or bb.x1 > axbb.x1
                    or bb.y0 < axbb.y0 or bb.y1 > axbb.y1):
                bad.append(t.get_text()[:30])
    return bad
```

하나라도 나오면 xlim/ylim 여유 확대 또는 라벨 위치 조정 후 재생성.
예외는 의도적으로 axes 밖에 두는 텍스트(legend, suptitle)뿐.

## Setup (copy to every script)

```python
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
import numpy as np
import os

matplotlib.rcParams['mathtext.default'] = 'regular'

fs, fss, fsss, fsl = 18, 16, 16, 20   # 규칙: tick=text=legend=annotate 동일 크기(16), axis label만 한 단계 크게(18), title 20. annotate를 tick보다 작게(8 등) 두지 말 것.
font_properties_label = fm.FontProperties(family='Arial', size=fs)
font_properties_tick = fm.FontProperties(family='Arial', size=fss)
font_properties_annotate = fm.FontProperties(family='Arial', size=fsss)
font_properties_legend = fm.FontProperties(family='Arial', size=fss)

colors = ['#77AEB3', '#E5885D', '#C7C4B5', '#A1C2DE', '#B4944B']
os.makedirs('./output', exist_ok=True)
```

## Helper Functions (include in every script)

```python
def apply_font_styling(ax):
    for tick in ax.get_xticklabels():
        tick.set_fontproperties(font_properties_tick)
    for tick in ax.get_yticklabels():
        tick.set_fontproperties(font_properties_tick)

def format_axis_labels(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel, fontproperties=font_properties_label)
    ax.set_ylabel(ylabel, fontproperties=font_properties_label)
    apply_font_styling(ax)

def plot_series_with_style(ax, x_data, y_data, color, label, series_index=0):
    zorder = 2 - 0.1 * series_index
    ax.plot(x_data, y_data, color=color, label=label, linewidth=1.5, zorder=zorder)
    ax.scatter(x_data, y_data, color=color, s=100, marker='o', linewidth=1.5, zorder=zorder)

def create_subplot_layout(nrows=1, ncols=1, figsize=(6.0, 5.6)):   # 크게 + 거의 정사각. single-panel은 정사각 (6,6) 권장. 작은 figsize는 텍스트 겹침의 주범.
    return plt.subplots(nrows, ncols, figsize=figsize)

def save_plot(filename, dpi=300):
    if not filename.startswith('plot'):
        filename = f'plot1_{filename}'
    if not filename.endswith('.svg'):
        filename = filename.replace('.png', '.svg').replace('.pdf', '.svg')
        if not filename.endswith('.svg'):
            filename += '.svg'
    plt.savefig(f'./output/{filename}', dpi=dpi, bbox_inches='tight', format='svg')
```

## Math Text Rules

| Wrong | Correct | Case |
|-------|---------|------|
| `CH₄` | `CH$_{4}$` | Chemical subscript |
| `x²` | `x$^{2}$` | Superscript |
| `O₂` | `O$\mathregular{_2}$` | mathregular subscript |
| `10⁻³` | `10$^{-3}$` | Negative exponent |

## Legend: always `frameon=False, prop=font_properties_legend`

## Scientific Notation (for values >1000 or <0.001)

```python
from matplotlib.ticker import FuncFormatter

def scientific_formatter(x, pos):
    if x == 0: return '0'
    exponent = int(np.floor(np.log10(abs(x))))
    coeff = x / 10**exponent
    if coeff == 1: return f'10$^{{{exponent}}}$'
    elif coeff == int(coeff): return f'{int(coeff)}x10$^{{{exponent}}}$'
    else: return f'{coeff:.1f}x10$^{{{exponent}}}$'

ax.yaxis.set_major_formatter(FuncFormatter(scientific_formatter))
```

## Filename: `{num}_plot{n}_{description}.svg` (num = 1~n)

## Audit — 텍스트 겹침 자동 검출 + 수정

플롯 생성 후 **반드시** audit를 실행한다. 텍스트가 겹치는 플롯은 논문/발표에 사용할 수 없다.

### Audit 워크플로

```
1. 플롯 스크립트 실행 → SVG 생성
2. audit 스크립트 실행 → 겹침 검출
3. 겹침 있으면 → 스크립트 수정 → 재생성 → 재audit
4. 겹침 없을 때까지 반복
```

### Audit Helper (매 스크립트 끝에 추가)

플롯 저장 직전에 겹침 검사를 수행하는 함수. `fig`와 `ax`가 있는 상태에서 호출한다.

```python
def audit_text_overlap(fig, ax_list=None, margin=2.0):
    """Check all text elements for bounding-box overlap.
    Returns list of (text_a, text_b, overlap_area) tuples.
    margin: extra pixels around each bbox to catch near-misses.
    """
    if ax_list is None:
        ax_list = fig.get_axes()
    renderer = fig.canvas.get_renderer()
    all_texts = []
    for a in ax_list:
        all_texts.extend(a.texts)
        if a.title and a.title.get_text():
            all_texts.append(a.title)
        if a.get_xlabel():
            all_texts.append(a.xaxis.label)
        if a.get_ylabel():
            all_texts.append(a.yaxis.label)
    if fig._suptitle:
        all_texts.append(fig._suptitle)

    bboxes = []
    for t in all_texts:
        if not t.get_text().strip():
            continue
        bb = t.get_window_extent(renderer=renderer)
        bb_expanded = bb.expanded(1 + margin/bb.width if bb.width > 0 else 1,
                                  1 + margin/bb.height if bb.height > 0 else 1)
        bboxes.append((t, bb_expanded))

    overlaps = []
    for i in range(len(bboxes)):
        for j in range(i+1, len(bboxes)):
            ta, ba = bboxes[i]
            tb, bb = bboxes[j]
            if ba.overlaps(bb):
                overlaps.append((ta.get_text()[:30], tb.get_text()[:30]))
    return overlaps
```

### 사용법

```python
# 플롯 코드 끝, plt.savefig() 직전에:
fig.canvas.draw()  # renderer 초기화 필수
overlaps = audit_text_overlap(fig)
if overlaps:
    print("WARNING: Text overlaps detected!")
    for a, b in overlaps:
        print(f"  OVERLAP: '{a}' <-> '{b}'")
else:
    print("AUDIT PASS: No text overlaps.")

plt.savefig(...)
```

### 겹침 발견 시 수정 전략

| 플롯 타입 | 해결법 |
|----------|--------|
| **Pie chart** | annotate의 `xytext` 좌표를 수동 조정. 작은 wedge는 `manual_offsets` dict로 개별 제어. 최후 수단: 작은 wedge 라벨을 legend로 빼기. |
| **Bar chart** | annotation 화살표의 `xytext`를 데이터 영역 밖으로 이동. `title` pad 값 증가. |
| **Stacked bar** | legend를 `bbox_to_anchor=(1.02, 1.0)`로 차트 밖에 배치. annotation은 가장 높은 bar 위에. |
| **Line/Scatter** | `adjustText` 라이브러리 사용: `conda run -n base pip install adjustText` |
| **공통** | `fig.suptitle(y=1.08)` 사용해 title을 figure 위로 분리. `figsize` 확대. |

### adjustText 사용 예시 (scatter/line에서 라벨 다수일 때)

```python
from adjustText import adjust_text
texts = [ax.annotate(label, xy=(x, y), fontproperties=font_properties_annotate)
         for label, x, y in zip(labels, xs, ys)]
adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle='-', color='gray', lw=0.8))
```

### Audit 실패 시 절대 하지 말 것

- `tight_layout()` 호출 — 금지 규칙 위반
- `fontsize` 줄이기 — 가독성 파괴
- 라벨 삭제 — 정보 손실
- `plt.show()` 추가 — 금지 규칙 위반

### Playwright 시각 검증 (최종 확인)

Audit 함수가 pass해도 SVG 렌더링에서 겹칠 수 있다. 최종 확인은 Playwright 스크린샷:

```bash
npx playwright screenshot --viewport-size="800,600" "file:///<URL-encoded-SVG-path>" "<output>.png"
```

생성된 PNG를 `Read` 도구로 열어 시각 확인. 문제 발견 시 스크립트 수정 후 재생성.

## Stacked Bar (상태/사유 분해 barh) — 2026-07 BatAgent 평가에서 확립한 규칙

여러 대상(모델·조건)의 결과를 사유별로 분해해 비교하는 가로 stacked bar 표준.

- **분해 = 총점 정합 (최우선)**: 막대 구성요소의 합이 문서 어디에나 표기되는 총점과 정확히 일치해야 한다. 총점 dict를 단일 소스로 두고 모든 그림이 같은 dict를 읽는다. 시각 분해(실행 상태)와 표기 점수(채점)가 다른 체계면 독자는 반드시 "왜 다르지?"라고 묻는다 — 분해 기준 자체를 점수 정의에 맞춰 재설계할 것.
- **색 체계**: 성공 계열은 초록 그라데이션 왼쪽부터 진→연 (`#4CAF87` → `#7FC49E` → `#ABD9BC`), 실패 계열은 의미별 분리 — 치명(예: hallucinated import) `#D64550`, 일반 오류 `#E5885D`, 부재 `#C7C4B5`. 성공/실패 경계가 색만으로 읽히게 한다.
- **세그먼트 내 숫자**: 값 ≥6일 때만 중앙에 표기. 진한 배경(진초록·빨강)은 흰 글씨, 연한 배경은 `#1a1a1a`.
- **우측 총점**: x=101.5쯤에 볼드·성공색으로 총점 표기. 축 라벨에 정의를 명시 (`"...; green total = score"`).
- **그룹 구분**: 성격이 다른 행 그룹(framework vs no framework)은 `axhspan` 회색 밴드 + 라운드 bbox 칩 텍스트로 구분. 첫 행(기준 대상)은 y라벨 볼드.
- **범례**: `bbox_to_anchor=(1.10, 0.5)` 바깥 배치. 카테고리 이름에 약어 금지, 괄호로 판정 기준 병기 (`run incomplete (setup valid)`).
- **동일 대상 쌍 비교**: 같은 모델의 두 조건(BatAgent/vanilla)은 인접 2행 쌍으로 배치 (`이름  |  조건` 라벨).

## Categorical Heatmap (대상 × 항목 정오/상태) — 동일 세션 규칙

- **흰 셀 그리드 필수**: minor tick `np.arange(-0.5, n, 1)` + `ax.grid(which="minor", color="white", linewidth=0.7)`, `tick_params(which="minor", length=0)`.
- **카테고리 경계**: 굵은 흰 세로선 (`axvline(b-0.5, color="white", linewidth=2.5)`).
- **축 라벨 약어 금지**: 카테고리 풀네임을 구간 중앙(`(start+end-1)/2`)에 배치. 한 글자 접두어(R/C/G) 노출 금지.
- **카테고리 순서는 의미 순**: 알파벳 정렬 금지 — 서사 순서(예: Reuse → CodeGen → Generalization → Ambiguous → Interview → Rephrased)로 커스텀 key 정렬.
- **이산 색**: `ListedColormap` + `vmin/vmax`를 반 칸 여유로. 정오 2색이면 성공 `#4CAF87` / 실패 `#D64550`.
- **판정 기준을 범례에 명시**: `success (plan correct or computed)`처럼 색이 뜻하는 규칙을 범례 라벨에 적는다.

## Reaction Coordinate Diagram (ΔG ladder) — 2026-09 CeO2 케톤화 캠페인 규칙

- **RDS/최대 스텝 표시는 화살표가 아니라 `fill_between` 음영**: 스텝 구간(x1+HW ~ x2−HW, y1~y2)을
  `color='#D64550', alpha=0.15, linewidth=0, zorder=0.5`로 칠하고, 라벨은 **수치만** (`+76 kJ/mol`) —
  "RDS:" 같은 접두어 금지. 라벨은 음영 영역 중앙 또는 바로 옆에 흰 bbox(alpha 0.6)로 배치.
- **gas 표기는 투입/방출 시점에만**: 방출 가스는 해당 연결선 위 중앙에 작은 회색 라벨, 최종 상태만 전체 조성.
- **다중 버전 figure는 버튼 토글**: 같은 경로의 해상도 변형(예: lumped/int1/int2)이나 엔트로피 처리
  (Campbell vs S_ads=0)는 별도 figure를 늘리지 말고 HTML 버튼 2단 토글로. SVG는 버전별로 전부 생성해두고
  div display 전환. 추정(est) 상태는 점선 + "dashed: ..." 주석, 계산 확정되면 실선 전환과 함께 est 표기 일괄 제거.
- **모드별 라벨 충돌은 모드 조건부 배치**: Campbell/noS처럼 레벨이 크게 이동하는 모드는 같은 라벨 좌표가
  한쪽에서만 충돌한다. `if MODE == 'noS':` 로 above/below flip을 개별 오버라이드.

## Legend 순서 = 데이터 순위 — MANDATORY

여러 곡선(phase diagram 등)의 legend는 입력 순서가 아니라 **기준 조건에서의 값 순서**(예: 실험 창 저압단
0.1 kPa에서의 에너지 높은 순)로 정렬한다. plot 시 `(값, line)` 튜플을 모아 sort 후
`ax.legend([ln...], [ln.get_label()...])`. 독자가 legend만 읽어도 순위가 보이게.

## 캡션-본문-Methods 분리 (논문/리포트 figure) — MANDATORY

- **캡션은 그림 설명만**: 무엇이 그려져 있는지 + 조건(T, P) + 버튼/점선/패널 의미. SI 캡션 스타일.
- **수치와 해석은 본문 bullet으로**: RDS 값, 상태 에너지, 샘플링 결과, 순위 비교는 figure 바로 아래 본문에.
- **방법 서술은 Methods로**: "UMA-s relax", "배치 샘플링 최저 구조", "10개 상태 전부 포함" 같은 문구는
  캡션 금지, Methods 섹션에 한 번만.
- **콜론 연결문 금지**: "지표 비교입니다: A와 B" → "지표(A와 B) 비교입니다". 시퀀스 나열도
  "구조입니다: X → Y" 대신 "구조를 반응 순서대로 보여줍니다. X → Y ... 순서입니다".

## Checklist

- [ ] `rcParams['mathtext.default'] = 'regular'` set
- [ ] `ax.set_position([0.2, 0.2, 0.666, 0.333])` done
- [ ] All text uses font_properties_*
- [ ] No grid, no bold, no tight_layout, no plt.show()
- [ ] Legend frameon=False
- [ ] SVG 300 DPI in ./output/
- [ ] All data visible within limits (5-10% padding)
- [ ] Colors from palette in order
- [ ] **Audit pass** — `audit_text_overlap()` returns empty list
- [ ] **Visual verify** — Playwright screenshot shows no overlap

## 이 규칙들은 실제로 반복해서 틀렸다 (2026-09-22 추가)

- **contour의 음수 level은 matplotlib 기본이 dashed다.** level이 전부 음수인 맵(형성 에너지,
  흡착 에너지)은 `linestyles="solid"`를 명시하지 않으면 전부 점선으로 나온다.
- **`aspect="equal"` 축에는 `ax.set_anchor("NW")`를 준다.** 안 주면 apply_aspect가 축을
  재중심화해서 패널 문자와 축 위치가 어긋난다. 위치를 손으로 옮겼으면 `get_position()`으로
  다시 재서 확인한다. 눈으로 "옮겨졌겠지"는 금지.
- **annotation의 zorder를 scatter보다 크게.** leader line이 점 아래로 들어가 잘린 것처럼 보인다.
- **phase diagram은 gradient보다 이산 색 띠.** `BoundaryNorm` + `plt.get_cmap(name, n)`.
  `pcolormesh(..., rasterized=True)`로 SVG 용량을 줄인다.
- **같은 종류의 시계열은 모든 그림에서 같은 xlim과 같은 tick.** 100 ps MD면 전부
  `set_xlim(0, 100)`, `set_xticks([0, 50, 100])`.
- **축 라벨은 그 값의 이름 한 줄.** Δ 약칭을 쓴다: `r"$\Delta$CN(Pd-O)"`, `"O gained by metal (count)"`.
  "OH per cell of that kind" 같은 문장형 라벨 금지.
- **마지막 프레임의 개수는 변화량이 아니다.** frame 0 값을 빼야 Δ다. 빼지 않아 결론 수치가
  70 %에서 28 %로 바뀐 사례가 있다. 축 이름에 Δ를 쓸 거면 데이터도 Δ인지 확인한다.
- **개수를 세는 코드가 무엇을 세는지 확인한다.** `sum(len(s) for s in bonded)`는 원자가 아니라
  bond를 센다. 두 패널의 수가 맞아야 할 때 안 맞으면 먼저 여기를 본다.


## 화학식 라벨 아래 첨자 (2026-10-04 사용자 지시)
그림 안의 화학식은 숫자를 항상 아래 첨자로 쓴다. "Pd17Pt38O22"를 그대로 찍지 않는다.
- matplotlib: `Pd$_{17}$Pt$_{38}$O$_{22}$` (PdPt 프로젝트는 `formula_pil.formula_tex()`).
- PIL 몽타주와 GIF: `03_paper_prep/scripts/formula_pil.draw_formula(draw, xy, s, font, sub_font)`. E_a 같은 기호도 아래 첨자로 그린다.
- 그림을 저장한 뒤 라벨 영역을 잘라 직접 보고 확인한다.
