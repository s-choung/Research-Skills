#!/usr/bin/env python3
"""Build benchmark_report.html for /blender-atom-render skill.

Reads 8 PNG files from the benchmark folder, base64-encodes them,
and generates a self-contained gallery HTML with KOR/ENG toggle.
"""

import base64
import pathlib

BENCHMARK_DIR = pathlib.Path(__file__).parent
IMAGE_FILES = ["1.png", "3.png", "5.png", "10.png", "12.png", "14.png", "4_1.png", "16.png"]

def encode_image(path: pathlib.Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

def build_html() -> str:
    cards_html = ""
    for fname in IMAGE_FILES:
        img_path = BENCHMARK_DIR / fname
        b64 = encode_image(img_path)
        label = fname.replace(".png", "")
        cards_html += f"""
    <div class="card">
      <img src="data:image/png;base64,{b64}" alt="{label}" loading="lazy">
      <div class="card-label">{label}</div>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>/blender-atom-render Gallery</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --font: 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
  --max-w: 1100px;
  --radius: 6.08px;
  --border: #e5e7eb;
  --gray: #8f8f8f;
  --card-bg: #f9f9f9;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: #fff;
  color: #000;
  font-family: var(--font);
  font-weight: 400;
  font-size: 16px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}}
header {{
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 80px 32px 48px;
  text-align: center;
}}
header h1 {{
  font-size: 40px;
  font-weight: 600;
  letter-spacing: -1.2px;
  line-height: 1.16;
  margin-bottom: 16px;
  font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
}}
header p {{
  font-size: 16px;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.65;
}}
.lang-wrap {{
  position: fixed;
  top: 20px;
  right: 24px;
  z-index: 100;
}}
.lang-toggle {{
  font-size: 13px;
  font-weight: 500;
  color: #666;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 9999px;
  padding: 5px 14px;
  cursor: pointer;
  font-family: var(--font);
  transition: all 0.15s;
}}
.lang-toggle:hover {{ background: #f1f1f1; color: #000; }}
.grid {{
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 32px 80px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}}
.card {{
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--card-bg);
  transition: box-shadow 0.15s;
}}
.card:hover {{
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}}
.card img {{
  width: 100%;
  display: block;
  aspect-ratio: 1;
  object-fit: cover;
}}
.card-label {{
  padding: 10px 14px;
  font-size: 13px;
  font-weight: 500;
  color: var(--gray);
  background: #fff;
  text-align: center;
  font-family: 'JetBrains Mono', 'SF Mono', monospace;
}}
footer {{
  text-align: center;
  padding: 32px;
  font-size: 13px;
  color: var(--gray);
  border-top: 1px solid var(--border);
  max-width: var(--max-w);
  margin: 0 auto;
}}
@media (max-width: 800px) {{
  .grid {{ grid-template-columns: repeat(2, 1fr); }}
  header {{ padding: 56px 16px 36px; }}
  header h1 {{ font-size: 28px; }}
  .grid {{ padding: 0 16px 56px; }}
}}
</style>
</head>
<body>

<div class="lang-wrap">
  <button class="lang-toggle" onclick="toggleLang()" id="langBtn">KOR</button>
</div>

<header>
  <h1>/blender-atom-render</h1>
  <p id="subtitle" data-en="Ray-traced atomic structure renders from POSCAR/CIF files using Blender. CPK colors, metallic materials, white background." data-ko="POSCAR/CIF 파일에서 Blender로 레이트레이싱한 원자 구조 렌더링. CPK 색상, 메탈릭 재질, 흰 배경.">Ray-traced atomic structure renders from POSCAR/CIF files using Blender. CPK colors, metallic materials, white background.</p>
</header>

<div class="grid">
{cards_html}
</div>

<footer>
  <span data-en="Rendered with /blender-atom-render skill" data-ko="/blender-atom-render 스킬로 렌더링">Rendered with /blender-atom-render skill</span>
</footer>

<script>
let lang = new URLSearchParams(window.location.search).get('lang') || 'en';

function setLang(l) {{
  lang = l;
  document.getElementById('langBtn').textContent = lang === 'en' ? 'KOR' : 'ENG';
  document.querySelectorAll('[data-en][data-ko]').forEach(el => {{
    el.textContent = el.getAttribute('data-' + lang);
  }});
}}

function toggleLang() {{
  setLang(lang === 'en' ? 'ko' : 'en');
  const url = new URL(window.location);
  url.searchParams.set('lang', lang);
  history.replaceState(null, '', url);
}}

setLang(lang);
</script>
</body>
</html>"""

if __name__ == "__main__":
    html = build_html()
    out = BENCHMARK_DIR / "benchmark_report.html"
    out.write_text(html, encoding="utf-8")
    print(f"Generated {out} ({len(html):,} bytes)")
