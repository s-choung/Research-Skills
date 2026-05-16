Few useful skills for Claude Code and Codex for research-related tasks. (Computational Catalysis POV)

Covers Atomic Simulation Environment (ase skill), scientific figures (matplotlib skill), paper hunting. Works with both Claude Code and Codex. Say "install skills from github.com/s-choung/Research-Skills" and you're set.

5 I reach for the most:

1) /blender-atom-render - Structure file in, ray-traced atoms out. POSCAR/CIF/XYZ supported.
2) /ase - Injects few hundreds lines of ASE knowledge (skill.md file) so the LLM writes correct Atomic Simulation Environment Python scripts. Benchmarked across 9 LLMs x 50 tasks. GPT-5.5 scored 100% even without the skill tho.
3) /matplotlib-scientific - Describe your plot + raw data, get a journal-ready figure. Arial, no grid, clean axis, 300 DPI.
4) /design2html - Type "openai" and get a full styled HTML page. 7 built-in design systems.
5) /humanize - Removes AI writing patterns from your draft. 98% AI-tell reduction. No Em dash and quite compact too.

Dashboard with benchmarks and examples: s-choung.github.io/Research-Skills
Repo: github.com/s-choung/Research-Skills

Star or repost if useful!

---

연구할 때 자주 사용하는 Claude Code / Codex용 스킬들 공유드립니다!

계산화학용 ASE 스크립트, 논문 작성, 피규어 그리기, 논문 찾기 등 매일 하는 연구행위들을 커버합니다. "github.com/s-choung/Research-Skills 여기 스킬 설치해줘" 하면 Claude Code나 Codex에서 바로 사용가능합니다.

자주 쓰는 5개:

1) /blender-atom-render - 구조 파일 넣으면 레이트레이싱 원자 이미지가 나옴. POSCAR/CIF/XYZ 지원.
2) /ase - 이제 입코딩이 아니라 입계산이 가능합니다. 자연어로 분자계산을 할수 있습니다. Atomic Simulation Environment Python 스크립트를 정확하게 짜게 해주고, 9개 LLM x 50개 태스크로 벤치마크 했는데, GPT-5.5는 스킬 없이도 100% 정확하게 코드를 짭니다.
3) /matplotlib-scientific - 플롯 설명과 raw데이터를 넣으면 논문 제출용 피규어 바로 옵니다. Arial, 그리드 없음, 300 DPI.
4) /design2html - "openai" 치면 OpenAI 스타일 HTML 페이지가 나옴. 7개 디자인 시스템 내장.
5) /humanize - AI가 쓴 티 제거. 한국어 98%. AI특유의 과장체와 두루뭉술함과 em dash남용을 대폭 줄입니다.

대시보드 (벤치마크, 예시 포함): s-choung.github.io/Research-Skills
레포: github.com/s-choung/Research-Skills

유용하시면 star나 리포스트 부탁드립니다!
