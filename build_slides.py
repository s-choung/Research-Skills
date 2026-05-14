#!/usr/bin/env python3
"""Build LinkedIn carousel slides with embedded images."""
import base64

def img(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

mpl = img('/tmp/slide-mpl.png')
hum = img('/tmp/slide-hum.png')
d2h = img('/tmp/slide-d2h.png')
ase = img('/tmp/slide-ase.png')
blender = img('/Users/sean/Research-Skills/skills/blender-atom-render/benchmark/12.png')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Research-Skills LinkedIn Carousel</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #e8e8e8; font-family: 'Inter', sans-serif; }}
.slide {{
  width: 1080px; height: 1080px;
  background: #fff; margin: 20px auto;
  position: relative; overflow: hidden;
  page-break-after: always;
}}
@media print {{
  body {{ background: white; }}
  .slide {{ margin: 0; box-shadow: none; }}
  @page {{ size: 1080px 1080px; margin: 0; }}
}}
.pad {{ padding: 80px; height: 100%; display: flex; flex-direction: column; }}
.brand {{ font-size: 18px; font-weight: 700; color: #bbb; letter-spacing: 1px; text-transform: uppercase; }}
.foot {{ position: absolute; bottom: 48px; left: 80px; right: 80px; display: flex; justify-content: space-between; font-size: 16px; color: #bbb; font-weight: 500; }}
.dots span {{ width: 10px; height: 10px; border-radius: 50%; background: #ddd; display: inline-block; margin: 0 4px; }}
.dots span.on {{ background: #000; }}
.tag {{ display: inline-block; font-size: 16px; font-weight: 700; border-radius: 100px; padding: 8px 20px; margin-right: 8px; margin-bottom: 8px; }}
.tag-r {{ color: #1a5fa0; background: #e8f0fe; }}
.tag-w {{ color: #8b2020; background: #fce8e8; }}
.tag-d {{ color: #2d6a2e; background: #e8f5e9; }}
.tag-m {{ color: #7b1fa2; background: #f3e5f5; }}
.tag-u {{ color: #92722a; background: #fef6e0; }}
.img-box {{ border-radius: 16px; overflow: hidden; border: 2px solid #eee; }}
.img-box img {{ width: 100%; display: block; }}
</style>
</head>
<body>

<!-- 1. Cover -->
<div class="slide" style="background: #000; color: #fff;">
  <div class="pad">
    <div class="brand" style="color: #666;">Open Source</div>
    <div style="margin-top: auto; margin-bottom: 40px;">
      <div style="font-size: 80px; font-weight: 800; line-height: 1.05; letter-spacing: -3px;">Research-<br>Skills</div>
    </div>
    <div style="font-size: 28px; font-weight: 400; color: #999; line-height: 1.5; margin-bottom: auto;">
      17 agent skills for research.<br>Claude Code + Codex.
    </div>
    <div>
      <span class="tag tag-r">Research</span>
      <span class="tag tag-w">Writing</span>
      <span class="tag tag-d">Design</span>
      <span class="tag tag-m">Media</span>
      <span class="tag tag-u">Utility</span>
    </div>
  </div>
  <div class="foot" style="color:#555;">
    <span>Dr. Seokhyun Choung</span>
    <span class="dots"><span class="on" style="background:#fff"></span><span></span><span></span><span></span><span></span><span></span><span></span></span>
  </div>
</div>

<!-- 2. /ase -->
<div class="slide">
  <div class="pad">
    <div class="brand">Research-Skills</div>
    <div style="margin-top: 40px;">
      <span class="tag tag-r">Research</span>
    </div>
    <div style="font-size: 56px; font-weight: 800; letter-spacing: -2px; margin: 20px 0; font-family: 'SF Mono','JetBrains Mono',monospace;">/ase</div>
    <div style="font-size: 26px; color: #444; line-height: 1.5; margin-bottom: 32px;">ASE script knowledge injection.<br>9 LLMs tested, 50 tasks.</div>
    <div class="img-box" style="flex:1; display:flex;">
      <img src="data:image/png;base64,{ase}" style="object-fit: cover; object-position: top;">
    </div>
  </div>
  <div class="foot">
    <span>github.com/s-choung/Research-Skills</span>
    <span class="dots"><span></span><span class="on"></span><span></span><span></span><span></span><span></span><span></span></span>
  </div>
</div>

<!-- 3. /matplotlib-scientific -->
<div class="slide">
  <div class="pad">
    <div class="brand">Research-Skills</div>
    <div style="margin-top: 40px;">
      <span class="tag tag-r">Research</span>
    </div>
    <div style="font-size: 48px; font-weight: 800; letter-spacing: -2px; margin: 20px 0; font-family: 'SF Mono','JetBrains Mono',monospace;">/matplotlib-scientific</div>
    <div style="font-size: 26px; color: #444; line-height: 1.5; margin-bottom: 32px;">Journal-ready figures. One command.</div>
    <div class="img-box" style="flex:1; display:flex;">
      <img src="data:image/png;base64,{mpl}" style="object-fit: cover; object-position: top;">
    </div>
  </div>
  <div class="foot">
    <span>github.com/s-choung/Research-Skills</span>
    <span class="dots"><span></span><span></span><span class="on"></span><span></span><span></span><span></span><span></span></span>
  </div>
</div>

<!-- 4. /humanize -->
<div class="slide">
  <div class="pad">
    <div class="brand">Research-Skills</div>
    <div style="margin-top: 40px;">
      <span class="tag tag-w">Writing</span>
    </div>
    <div style="font-size: 56px; font-weight: 800; letter-spacing: -2px; margin: 20px 0; font-family: 'SF Mono','JetBrains Mono',monospace;">/humanize</div>
    <div style="font-size: 26px; color: #444; line-height: 1.5; margin-bottom: 32px;">AI-tell removal. KOR + ENG.</div>
    <div style="display:flex; gap: 48px; margin-bottom: 32px;">
      <div><div style="font-size: 18px; color: #999; font-weight: 600; text-transform: uppercase;">Korean</div><div style="font-size: 72px; font-weight: 800; color: #2d6a2e; letter-spacing: -3px;">-98%</div></div>
      <div><div style="font-size: 18px; color: #999; font-weight: 600; text-transform: uppercase;">English</div><div style="font-size: 72px; font-weight: 800; color: #2d6a2e; letter-spacing: -3px;">-96%</div></div>
    </div>
    <div class="img-box" style="flex:1; display:flex;">
      <img src="data:image/png;base64,{hum}" style="object-fit: cover; object-position: top;">
    </div>
  </div>
  <div class="foot">
    <span>github.com/s-choung/Research-Skills</span>
    <span class="dots"><span></span><span></span><span></span><span class="on"></span><span></span><span></span><span></span></span>
  </div>
</div>

<!-- 5. /design2html -->
<div class="slide">
  <div class="pad">
    <div class="brand">Research-Skills</div>
    <div style="margin-top: 40px;">
      <span class="tag tag-d">Design</span>
    </div>
    <div style="font-size: 56px; font-weight: 800; letter-spacing: -2px; margin: 20px 0; font-family: 'SF Mono','JetBrains Mono',monospace;">/design2html</div>
    <div style="font-size: 26px; color: #444; line-height: 1.5; margin-bottom: 32px;">7 built-in styles. Same content, different look.</div>
    <div class="img-box" style="flex:1; display:flex;">
      <img src="data:image/png;base64,{d2h}" style="object-fit: cover; object-position: top;">
    </div>
  </div>
  <div class="foot">
    <span>github.com/s-choung/Research-Skills</span>
    <span class="dots"><span></span><span></span><span></span><span></span><span class="on"></span><span></span><span></span></span>
  </div>
</div>

<!-- 6. /blender-atom-render -->
<div class="slide">
  <div class="pad">
    <div class="brand">Research-Skills</div>
    <div style="margin-top: 40px;">
      <span class="tag tag-d">Design</span>
    </div>
    <div style="font-size: 44px; font-weight: 800; letter-spacing: -2px; margin: 20px 0; font-family: 'SF Mono','JetBrains Mono',monospace;">/blender-atom-render</div>
    <div style="font-size: 26px; color: #444; line-height: 1.5; margin-bottom: 32px;">Ray-traced atoms from structure files.</div>
    <div class="img-box" style="flex:1; display:flex; background: #f5f5f5;">
      <img src="data:image/png;base64,{blender}" style="object-fit: contain; margin: auto; max-height: 100%;">
    </div>
  </div>
  <div class="foot">
    <span>github.com/s-choung/Research-Skills</span>
    <span class="dots"><span></span><span></span><span></span><span></span><span></span><span class="on"></span><span></span></span>
  </div>
</div>

<!-- 7. CTA -->
<div class="slide" style="background: #000; color: #fff;">
  <div class="pad">
    <div class="brand" style="color: #666;">Open Source</div>
    <div style="margin-top: auto;">
      <div style="font-size: 72px; font-weight: 800; line-height: 1.1; letter-spacing: -3px; margin-bottom: 48px;">Clone it.<br>Use it.<br>Build on it.</div>
    </div>
    <div style="font-size: 28px; font-weight: 500; font-family: 'SF Mono',monospace; color: #ccc; margin-bottom: 24px;">github.com/s-choung/<br>Research-Skills</div>
    <div style="font-size: 22px; color: #666; margin-bottom: auto;">Claude Code + Codex compatible.</div>
  </div>
  <div class="foot" style="color:#555;">
    <span>Dr. Seokhyun Choung</span>
    <span class="dots"><span></span><span></span><span></span><span></span><span></span><span></span><span class="on" style="background:#fff"></span></span>
  </div>
</div>

</body>
</html>"""

with open('/Users/sean/Research-Skills/linkedin-slides.html', 'w') as f:
    f.write(html)
print(f"Done. {len(html)//1024} KB")
