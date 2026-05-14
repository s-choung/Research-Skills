#!/usr/bin/env python3
"""Build matplotlib-scientific benchmark HTML report with embedded images."""
import base64, os

BENCH = os.path.dirname(os.path.abspath(__file__))

def img64(name):
    with open(os.path.join(BENCH, name), 'rb') as f:
        return base64.b64encode(f.read()).decode()

pairs = [
    {
        "title_en": "Scatter Plot",
        "title_ko": "산점도",
        "desc_en": "DFT vs ML energy prediction. Default matplotlib uses bold title, grid, blue dots, red dashed line. Skill version uses Arial, muted palette, no grid, clean spines.",
        "desc_ko": "DFT vs ML 에너지 예측. 기본 matplotlib는 볼드 제목, 그리드, 파란 점, 빨간 선. 스킬 버전은 Arial, 절제된 팔레트, 그리드 없음, 깔끔한 축.",
        "before": "before_scatter.png",
        "after": "after_scatter.png",
    },
    {
        "title_en": "Bar Chart",
        "title_ko": "막대 그래프",
        "desc_en": "LLM benchmark pass rates. Default uses bold title, y-axis grid, saturated colors, boxy legend. Skill version uses set_position layout, frameless legend, spines removed.",
        "desc_ko": "LLM 벤치마크 pass rate. 기본은 볼드 제목, y축 그리드, 채도 높은 색상. 스킬 버전은 set_position 레이아웃, 프레임 없는 범례, 불필요한 축 제거.",
        "before": "before_bar.png",
        "after": "after_bar.png",
    },
    {
        "title_en": "Line Plot",
        "title_ko": "선 그래프",
        "desc_en": "Training convergence curves. Default has grid, dense markers, bold title. Skill version uses sparse markers, clean axes, consistent color palette.",
        "desc_ko": "학습 수렴 곡선. 기본은 그리드, 빽빽한 마커, 볼드 제목. 스킬 버전은 희소 마커, 깔끔한 축, 일관된 색상 팔레트.",
        "before": "before_line.png",
        "after": "after_line.png",
    },
]

rules = [
    ("Arial font via FontProperties", "FontProperties로 Arial 폰트 적용"),
    ("No grid, no bold, no tight_layout()", "그리드/볼드/tight_layout 금지"),
    ("ax.set_position([0.2, 0.2, 0.666, 0.333])", "set_position 고정 레이아웃"),
    ("Muted color palette (#77AEB3, #E5885D, ...)", "절제된 색상 팔레트"),
    ("Legend frameon=False", "범례 프레임 제거"),
    ("Top/right spines removed", "상단/우측 축선 제거"),
    ("SVG output at 300 DPI", "SVG 300 DPI 출력"),
    ("5-10% axis padding", "축 여백 5-10%"),
]

cards_html = ""
for i, p in enumerate(pairs):
    b64_b = img64(p["before"])
    b64_a = img64(p["after"])
    cards_html += f"""
    <div class="pair" data-idx="{i}">
      <div class="pair-header">
        <span class="pair-num">{i+1}</span>
        <span class="pair-title" data-en="{p['title_en']}" data-ko="{p['title_ko']}">{p['title_en']}</span>
      </div>
      <p class="pair-desc" data-en="{p['desc_en']}" data-ko="{p['desc_ko']}">{p['desc_en']}</p>
      <div class="pair-grid">
        <div class="pair-col">
          <div class="pair-label dn" data-en="Before — Default" data-ko="Before — 기본값">Before — Default</div>
          <img src="data:image/png;base64,{b64_b}" alt="before">
        </div>
        <div class="pair-col">
          <div class="pair-label dp" data-en="After — /matplotlib-scientific" data-ko="After — /matplotlib-scientific">After — /matplotlib-scientific</div>
          <img src="data:image/png;base64,{b64_a}" alt="after">
        </div>
      </div>
    </div>
"""

rules_en = "".join(f'<li>{r[0]}</li>' for r in rules)
rules_ko = "".join(f'<li>{r[1]}</li>' for r in rules)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>matplotlib-scientific Benchmark</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --color-void: #000000;
  --color-fog-border: #e5e7eb;
  --color-chalk: #f1f1f1;
  --color-graphite: #666666;
  --color-ash: #8f8f8f;
  --color-canvas: #ffffff;
  --font: 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
  --radius-cards: 6.08px;
  --radius-pill: 9999px;
  --max-w: 1100px;
  --green: #2d6a2e;
  --red: #8b2020;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: var(--color-canvas);
  color: var(--color-void);
  font-family: var(--font);
  font-weight: 400;
  font-size: 16px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
  position: relative;
}}

.wrap {{ max-width: var(--max-w); margin: 0 auto; padding: 80px 32px 60px; }}

.lang-toggle {{ position: absolute; top: 28px; right: 32px; display: flex; gap: 0; }}
.lang-btn {{
  padding: 5px 14px; font-size: 13px; font-weight: 600;
  border: 1px solid var(--color-fog-border); cursor: pointer;
  background: var(--color-chalk); color: var(--color-graphite);
  font-family: var(--font);
}}
.lang-btn.active {{ background: var(--color-void); color: var(--color-canvas); }}
.lang-btn:first-child {{ border-radius: 4px 0 0 4px; }}
.lang-btn:last-child {{ border-radius: 0 4px 4px 0; }}

h1 {{
  font-size: 40px; font-weight: 600;
  line-height: 1.16; letter-spacing: -1.2px;
  margin-bottom: 12px;
}}
.subtitle {{ font-size: 15px; color: var(--color-graphite); margin-bottom: 48px; }}

.section-label {{
  font-size: 13px; font-weight: 600;
  letter-spacing: 0.143px; color: var(--color-graphite);
  text-transform: uppercase;
  margin-bottom: 24px; padding-bottom: 10px;
  border-bottom: 1px solid var(--color-fog-border);
}}

.pair {{
  margin-bottom: 56px;
}}
.pair-header {{
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 8px;
}}
.pair-num {{
  font-size: 13px; font-weight: 600;
  color: var(--color-canvas); background: var(--color-void);
  width: 24px; height: 24px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}}
.pair-title {{ font-size: 20px; font-weight: 600; }}
.pair-desc {{ font-size: 14px; color: var(--color-graphite); margin-bottom: 20px; line-height: 1.6; }}
.pair-grid {{
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 20px;
}}
.pair-col {{ text-align: center; }}
.pair-label {{
  font-size: 13px; font-weight: 600;
  letter-spacing: 0.143px; text-transform: uppercase;
  margin-bottom: 12px;
}}
.pair-label.dn {{ color: var(--red); }}
.pair-label.dp {{ color: var(--green); }}
.pair-col img {{
  width: 100%; max-width: 460px;
  border: 1px solid var(--color-fog-border);
  border-radius: var(--radius-cards);
}}

.rules {{
  border: 1px solid var(--color-fog-border);
  border-radius: var(--radius-cards);
  padding: 28px 32px;
  margin-bottom: 48px;
}}
.rules-title {{
  font-size: 16px; font-weight: 600; margin-bottom: 16px;
}}
.rules ul {{
  list-style: none; padding: 0;
}}
.rules li {{
  font-size: 14px; color: var(--color-graphite);
  padding: 6px 0;
  border-bottom: 1px solid var(--color-fog-border);
}}
.rules li:last-child {{ border-bottom: none; }}
.rules li::before {{
  content: ''; display: inline-block;
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--color-void); margin-right: 10px;
  vertical-align: middle;
}}

.foot {{
  border-top: 1px solid var(--color-fog-border);
  padding-top: 24px; margin-top: 24px;
  display: flex; justify-content: space-between;
  font-size: 13px; color: var(--color-graphite);
}}
.foot a {{
  font-weight: 500; color: var(--color-void); text-decoration: none;
}}
.foot a:hover {{ text-decoration: underline; }}

@media (max-width: 700px) {{
  .wrap {{ padding: 60px 16px 40px; }}
  h1 {{ font-size: 28px; }}
  .pair-grid {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>

<div class="lang-toggle">
  <div class="lang-btn" onclick="setLang('ko')">KOR</div>
  <div class="lang-btn active" onclick="setLang('en')">ENG</div>
</div>

<div class="wrap">

<h1>/matplotlib-scientific</h1>
<p class="subtitle" data-en="Before/After comparison: default matplotlib vs publication-quality figures with the /matplotlib-scientific skill." data-ko="Before/After 비교: 기본 matplotlib vs /matplotlib-scientific 스킬 적용 논문용 그래프.">Before/After comparison: default matplotlib vs publication-quality figures with the /matplotlib-scientific skill.</p>

<div class="rules">
  <div class="rules-title" data-en="Skill Rules Applied" data-ko="적용된 스킬 규칙">Skill Rules Applied</div>
  <ul id="rules-list">
    {rules_en}
  </ul>
</div>

<div class="section-label" data-en="Before / After Comparison" data-ko="Before / After 비교">Before / After Comparison</div>

{cards_html}

<div class="foot">
  <span>matplotlib-scientific benchmark &middot; 2026</span>
  <a href="https://github.com/s-choung/Research-Skills/tree/master/skills/matplotlib-scientific">View on GitHub</a>
</div>

</div>

<script>
const RULES_EN = `{rules_en}`;
const RULES_KO = `{rules_ko}`;

function setLang(lang) {{
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
  document.querySelector('.lang-btn[onclick*="'+lang+'"]').classList.add('active');
  document.querySelectorAll('[data-en][data-ko]').forEach(el => {{
    el.innerHTML = el.getAttribute('data-'+lang);
  }});
  document.getElementById('rules-list').innerHTML = lang === 'ko' ? RULES_KO : RULES_EN;
}}
(function(){{
  const p = new URLSearchParams(window.location.search);
  if (p.get('lang') === 'ko') setLang('ko');
}})();
</script>
</body>
</html>"""

out = os.path.join(BENCH, "benchmark_report.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Report: {out} ({os.path.getsize(out)//1024} KB)")
