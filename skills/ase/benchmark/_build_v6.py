"""Build v6 benchmark report from v5 data.
Reads v5 HTML, extracts DATA/SUMMARY, strips code/stdout/stderr/quality,
outputs a simplified v6 HTML with pass/fail only (no quality score)."""

import json, re, os

V5_PATH = '/Users/sean/Library/CloudStorage/GoogleDrive-wjdtjrgus9967@gmail.com/My Drive/Research_2026/playground/108_ase_skill/benchmark/benchmark_report_v5.html'
V6_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'benchmark_report_v6.html')

with open(V5_PATH, 'r') as f:
    content = f.read()

# Extract DATA JSON
data_match = re.search(r'const DATA = ({.*?});\s*\n', content, re.DOTALL)
data = json.loads(data_match.group(1))

# Extract SUMMARY JSON
summary_match = re.search(r'const SUMMARY = ({.*?});\s*\n', content, re.DOTALL)
summary = json.loads(summary_match.group(1))

# Build simplified DATA (no code, stdout, stderr, quality)
simplified_data = {}
for tid, task in data.items():
    stask = {
        "id": task["id"],
        "category": task["category"],
        "difficulty": task["difficulty"],
        "prompt": task["prompt"],
        "tests_api": task.get("tests_api", ""),
        "models": {}
    }
    for mk, mv in task["models"].items():
        stask["models"][mk] = {
            "provider": mv["provider"],
            "model": mv["model"],
            "condition": mv["condition"],
            "success": mv["success"],
        }
    simplified_data[tid] = stask

# Build simplified SUMMARY (no quality)
simplified_summary = {}
for mk, sv in summary.items():
    simplified_summary[mk] = {
        "provider": sv["provider"],
        "model": sv["model"],
        "condition": sv["condition"],
        "pass_count": sv["pass_count"],
        "total": sv["total"],
    }

data_json = json.dumps(simplified_data, ensure_ascii=False)
summary_json = json.dumps(simplified_summary, ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASE Skill Benchmark v6 — Pass Rate Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=IBM+Plex+Sans+KR:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --ink: #1a1a17;
  --paper: #fafaf7;
  --muted: #6b6b63;
  --rule: #d4d4cd;
  --mark: #ffe14d;
  --green: #2d6a2e;
  --red: #8b2020;
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: var(--paper);
  color: var(--ink);
  font-family: 'IBM Plex Sans KR', sans-serif;
  font-weight: 300;
  font-size: 15px;
  line-height: 1.75;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
mark { background: var(--mark); padding: 0 2px; font-weight: 400; }
h1 {
  font-family: 'DM Serif Display', serif;
  font-size: 2.4rem;
  font-weight: 400;
  line-height: 1.15;
  letter-spacing: -1px;
  margin-bottom: .25rem;
}
.date { font-size: .8rem; color: var(--muted); margin-bottom: 2rem; }
h2 {
  font-size: .75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--muted);
  margin: 2.5rem 0 1rem;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--rule);
}
p { margin-bottom: 1rem; }
strong { font-weight: 600; }

/* Summary table */
.sum-tbl { border-collapse: collapse; margin: 1rem auto; }
.sum-tbl th {
  font-size: .7rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: 2px; color: var(--muted); text-align: left;
  padding: .5rem .6rem; border-bottom: 1px solid var(--ink);
}
.sum-tbl th.r { text-align: right; }
.sum-tbl td {
  padding: .45rem .6rem; border-bottom: 1px solid var(--rule);
  font-family: 'JetBrains Mono', monospace; font-size: .82rem;
}
.sum-tbl td.lbl { font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; }
.sum-tbl .r { text-align: right; }
.provider-tag {
  font-size: .6rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: 1px; color: var(--muted); padding: 1px 4px;
  border: 1px solid var(--rule);
}
.delta-pos { color: var(--green); font-weight: 600; }
.delta-neg { color: var(--red); font-weight: 600; }
.delta-zero { color: var(--muted); }

/* Pass bar */
.pass-bar {
  display: inline-block; width: 70px; height: 10px;
  background: var(--rule); border-radius: 2px; overflow: hidden;
  vertical-align: middle; margin-left: 6px;
}
.pass-bar-fill {
  height: 100%; border-radius: 2px;
}

/* Heatmap */
.hm-wrap { overflow-x: auto; margin: 1rem auto; display: flex; justify-content: center; }
.hm-wrap table { border-collapse: collapse; }
.hm-wrap th {
  font-size: .55rem; font-weight: 600; letter-spacing: 0;
  padding: 2px 1px; writing-mode: vertical-lr; text-orientation: mixed;
  white-space: nowrap; border-bottom: 1px solid var(--ink); color: var(--muted);
}
.hm-wrap td {
  width: 22px; height: 22px; padding: 0; text-align: center;
  font-size: .6rem; font-family: 'JetBrains Mono', monospace;
  border: 1px solid var(--paper); cursor: pointer;
}
.hm-wrap td.pass { background: #bde0bd; color: var(--green); }
.hm-wrap td.fail { background: #e8b0b0; color: var(--red); }
.hm-wrap td.row-label {
  width: auto; text-align: right; padding-right: 8px;
  font-family: 'IBM Plex Sans KR', sans-serif; font-size: .72rem;
  font-weight: 400; background: none; border: none; white-space: nowrap;
  cursor: pointer; text-decoration: underline; text-decoration-color: var(--rule);
}
.hm-wrap td.row-label:hover { color: var(--green); }
.legend {
  display: flex; gap: 16px; align-items: center;
  font-size: .72rem; color: var(--muted); margin: .5rem auto 1rem;
  justify-content: center;
}
.legend-box {
  display: inline-block; width: 14px; height: 14px;
  margin-right: 4px; vertical-align: middle; border-radius: 2px;
}

/* Task Explorer */
.task-explorer { margin-top: 1rem; }
.task-card {
  border: 1px solid var(--rule); margin-bottom: 4px; background: #fff;
}
.task-header {
  display: grid; grid-template-columns: 70px 70px 1fr auto;
  align-items: center; gap: 8px; padding: 8px 12px; cursor: pointer;
  font-size: .82rem;
}
.task-header:hover { background: #f5f5f0; }
.task-id { font-family: 'JetBrains Mono', monospace; font-weight: 500; }
.task-diff { font-size: .7rem; font-weight: 600; padding: 1px 6px; border-radius: 3px; }
.task-diff.L1 { background: #e8f5e9; color: #2e7d32; }
.task-diff.L2 { background: #fff3e0; color: #e65100; }
.task-diff.L3 { background: #fce4ec; color: #c62828; }
.task-prompt { font-size: .78rem; color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.task-mini-dots { display: flex; gap: 2px; }
.task-mini-dots span {
  width: 8px; height: 8px; border-radius: 50%; display: inline-block;
}
.task-mini-dots span.pass { background: #2d6a2e; }
.task-mini-dots span.fail { background: #8b2020; }

.task-body { display: none; padding: 0 12px 12px; }
.task-body.open { display: block; }
.prompt-box {
  background: #f0f0eb; padding: 10px 14px; font-size: .82rem;
  border-left: 3px solid var(--mark); margin-bottom: 12px; line-height: 1.6;
}
.prompt-api { font-size: .7rem; color: var(--muted); margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

/* Model results grid */
.model-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 6px;
}
.model-result {
  border: 1px solid var(--rule); padding: 6px 8px; font-size: .75rem;
}
.model-result.pass-border { border-left: 3px solid var(--green); }
.model-result.fail-border { border-left: 3px solid var(--red); }
.mr-header {
  display: flex; justify-content: space-between; align-items: center;
}
.mr-model { font-weight: 600; font-size: .72rem; }
.mr-cond { font-size: .6rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
.mr-badge {
  font-size: .6rem; font-weight: 600; padding: 1px 6px;
  border-radius: 3px; text-transform: uppercase;
}
.mr-badge.pass { background: #e8f5e9; color: #2e7d32; }
.mr-badge.fail { background: #fce4ec; color: #c62828; }

/* Filter controls */
.filters {
  display: flex; gap: 12px; align-items: center; flex-wrap: wrap;
  margin-bottom: 12px; font-size: .78rem;
}
.filters select, .filters input {
  font-family: 'IBM Plex Sans KR', sans-serif;
  font-size: .78rem; padding: 4px 8px;
  border: 1px solid var(--rule); background: #fff;
}
.filters label { color: var(--muted); font-weight: 400; }

/* Tabs */
.tab-bar {
  display: flex; gap: 0; border-bottom: 1px solid var(--ink); margin-bottom: 1rem;
}
.tab-btn {
  padding: 8px 16px; font-size: .78rem; font-weight: 400;
  cursor: pointer; border: 1px solid var(--rule); border-bottom: none;
  background: #f5f5f0; color: var(--muted); margin-right: -1px;
}
.tab-btn.active {
  background: var(--paper); color: var(--ink); font-weight: 600;
  border-bottom: 1px solid var(--paper); position: relative; top: 1px;
}
.tab-content { display: none; }
.tab-content.active { display: block; }

/* Condition filter buttons */
.cond-filter {
  display: flex; gap: 4px; margin-bottom: 8px;
}
.cond-filter button {
  font-size: .68rem; padding: 3px 10px; border: 1px solid var(--rule);
  background: #fff; cursor: pointer; font-family: 'IBM Plex Sans KR', sans-serif;
}
.cond-filter button.active { background: var(--ink); color: #fff; }

.foot {
  display: grid; grid-template-columns: 1fr auto;
  border-top: 1px solid var(--rule); padding-top: .75rem;
  margin-top: 3rem; font-size: .7rem; color: var(--muted);
}

/* Centered text */
.center-text { text-align: center; }
</style>
</head>
<body>

<h1>ASE Skill Benchmark v6</h1>
<p class="date">2026.05.14 &middot; Seokhyun Choung &middot; Pass Rate Dashboard</p>

<p>9개 LLM에 250줄 ASE 스킬을 주입한 50-task 벤치마크. <strong>Pass rate</strong>(성공/전체) 기준으로 스킬 유무에 따른 성능 변화를 비교한다.</p>

<!-- TAB BAR -->
<div class="tab-bar">
  <div class="tab-btn active" onclick="switchTab('overview')">Overview</div>
  <div class="tab-btn" onclick="switchTab('heatmap')">Heatmap</div>
  <div class="tab-btn" onclick="switchTab('explorer')">Task Explorer</div>
</div>

<!-- ===== TAB 1: OVERVIEW ===== -->
<div id="tab-overview" class="tab-content active">

<h2>Overall Results — Pass Rate</h2>
<p class="center-text" style="font-size:.82rem">Pass Rate = 실행 성공(returncode==0) 비율. 50개 태스크 x 9개 모델 x 2 조건(Vanilla / Skill v3).</p>

<table class="sum-tbl">
<thead>
<tr>
  <th>Provider</th><th>Model</th>
  <th class="r">Vanilla Pass%</th>
  <th class="r">Skill Pass%</th>
  <th class="r">Delta</th>
</tr>
</thead>
<tbody id="summary-body"></tbody>
</table>

<div style="border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);padding:1rem 0;margin:2rem 0;text-align:center">
<p style="font-size:1.02rem;margin:0"><strong>Key finding:</strong> ASE 스킬이 가장 큰 효과를 보이는 모델은 <mark>Gemini Pro (+44%p)</mark>와 <mark>Opus 4.7 (+16%p)</mark>이다.</p>
<p style="font-size:.88rem;margin:.5rem 0 0;color:var(--muted)">GPT-5.5은 vanilla 100%로 스킬 불필요. Haiku 4.5는 스킬로 +28%p 상승.</p>
</div>

</div>

<!-- ===== TAB 2: HEATMAP ===== -->
<div id="tab-heatmap" class="tab-content">

<h2>Pass/Fail Heatmap (50 Tasks x 18 Conditions)</h2>
<div class="legend">
  <span><span class="legend-box" style="background:#bde0bd"></span> Pass</span>
  <span><span class="legend-box" style="background:#e8b0b0"></span> Fail</span>
</div>

<div class="hm-wrap">
<table>
<thead><tr><th style="writing-mode:horizontal-tb;border:none"></th></tr></thead>
<tbody id="heatmap-body"></tbody>
</table>
</div>

</div>

<!-- ===== TAB 3: TASK EXPLORER ===== -->
<div id="tab-explorer" class="tab-content">

<h2>Task Explorer — 50 Tasks</h2>

<div class="filters">
  <label>Difficulty:</label>
  <select id="filter-diff" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="L1">L1</option>
    <option value="L2">L2</option>
    <option value="L3">L3</option>
  </select>
  <label>Category:</label>
  <select id="filter-cat" onchange="applyFilters()"></select>
  <label>Status:</label>
  <select id="filter-status" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="mixed">Mixed</option>
    <option value="all-pass">All pass</option>
    <option value="all-fail">All fail</option>
  </select>
  <label>Search:</label>
  <input type="text" id="filter-search" placeholder="keyword..." oninput="applyFilters()">
</div>

<div class="cond-filter">
  <button class="active" onclick="toggleCondFilter(this,'all')">All</button>
  <button onclick="toggleCondFilter(this,'vanilla')">Vanilla only</button>
  <button onclick="toggleCondFilter(this,'skill_v3')">Skill only</button>
</div>

<div id="task-list" class="task-explorer"></div>

</div>

<div class="foot">
  <span>ASE Skill Benchmark v6 / Gemini + OpenAI + Claude / Pass Rate Dashboard</span>
  <span>2026.05</span>
</div>

<script>
const DATA = ''' + data_json + r''';
const SUMMARY = ''' + summary_json + r''';

const MODEL_KEYS = [
  { provider: "Gemini", model: "flash-lite", van: "flash-lite_vanilla", skill: "flash-lite_skill_v3" },
  { provider: "Gemini", model: "flash", van: "flash_vanilla", skill: "flash_skill_v3" },
  { provider: "Gemini", model: "pro", van: "pro_vanilla", skill: "pro_skill_v3" },
  { provider: "OpenAI", model: "gpt-5.4-mini", van: "gpt-5.4-mini_vanilla", skill: "gpt-5.4-mini_skill_v3" },
  { provider: "OpenAI", model: "gpt-5.4", van: "gpt-5.4_vanilla", skill: "gpt-5.4_skill_v3" },
  { provider: "OpenAI", model: "gpt-5.5", van: "gpt-5.5_vanilla", skill: "gpt-5.5_skill_v3" },
  { provider: "Claude", model: "Haiku 4.5", van: "Haiku 4.5_vanilla", skill: "Haiku 4.5_skill_v3" },
  { provider: "Claude", model: "Sonnet 4.6", van: "Sonnet 4.6_vanilla", skill: "Sonnet 4.6_skill_v3" },
  { provider: "Claude", model: "Opus 4.7", van: "Opus 4.7_vanilla", skill: "Opus 4.7_skill_v3" },
];

const CONDITIONS = [];
MODEL_KEYS.forEach(mk => {
  CONDITIONS.push({ key: mk.van, provider: mk.provider, model: mk.model, cond: "vanilla" });
  CONDITIONS.push({ key: mk.skill, provider: mk.provider, model: mk.model, cond: "skill_v3" });
});

const COND_SHORT = {
  "flash-lite_vanilla":"fl-v", "flash-lite_skill_v3":"fl-s",
  "flash_vanilla":"fh-v", "flash_skill_v3":"fh-s",
  "pro_vanilla":"pr-v", "pro_skill_v3":"pr-s",
  "gpt-5.4-mini_vanilla":"mi-v", "gpt-5.4-mini_skill_v3":"mi-s",
  "gpt-5.4_vanilla":"54-v", "gpt-5.4_skill_v3":"54-s",
  "gpt-5.5_vanilla":"55-v", "gpt-5.5_skill_v3":"55-s",
  "Haiku 4.5_vanilla":"hk-v", "Haiku 4.5_skill_v3":"hk-s",
  "Sonnet 4.6_vanilla":"sn-v", "Sonnet 4.6_skill_v3":"sn-s",
  "Opus 4.7_vanilla":"op-v", "Opus 4.7_skill_v3":"op-s",
};

// ===== TAB SWITCHING =====
function switchTab(name) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  event.target.classList.add('active');
}

// ===== SUMMARY TABLE =====
(function buildSummary() {
  const tbody = document.getElementById('summary-body');
  MODEL_KEYS.forEach(mk => {
    const vs = SUMMARY[mk.van];
    const ss = SUMMARY[mk.skill];
    const vPct = (vs.pass_count / vs.total * 100).toFixed(0);
    const sPct = (ss.pass_count / ss.total * 100).toFixed(0);
    const delta = ss.pass_count - vs.pass_count;
    const deltaPct = (delta / vs.total * 100).toFixed(0);
    const dClass = delta > 0 ? "delta-pos" : delta < 0 ? "delta-neg" : "delta-zero";
    const vColor = vPct >= 80 ? 'var(--green)' : vPct >= 50 ? '#c4920a' : 'var(--red)';
    const sColor = sPct >= 80 ? 'var(--green)' : sPct >= 50 ? '#c4920a' : 'var(--red)';
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td class="lbl"><span class="provider-tag">${mk.provider}</span></td>
      <td class="lbl">${mk.model}</td>
      <td class="r">${vs.pass_count}/${vs.total} (${vPct}%)<span class="pass-bar"><span class="pass-bar-fill" style="width:${vPct}%;background:${vColor}"></span></span></td>
      <td class="r">${ss.pass_count}/${ss.total} (${sPct}%)<span class="pass-bar"><span class="pass-bar-fill" style="width:${sPct}%;background:${sColor}"></span></span></td>
      <td class="r ${dClass}">${delta>0?'+':''}${deltaPct}%p</td>
    `;
    tbody.appendChild(tr);
  });
})();

// ===== HEATMAP =====
(function buildHeatmap() {
  const table = document.querySelector('#tab-heatmap .hm-wrap table');
  const thead = table.querySelector('thead tr');
  thead.innerHTML = '<th style="writing-mode:horizontal-tb;border:none"></th>';
  CONDITIONS.forEach(c => {
    const th = document.createElement('th');
    th.textContent = COND_SHORT[c.key] || c.key;
    thead.appendChild(th);
  });

  const tbody = document.getElementById('heatmap-body');
  const taskIds = Object.keys(DATA).sort((a,b) => parseInt(a.slice(1)) - parseInt(b.slice(1)));
  taskIds.forEach(tid => {
    const tr = document.createElement('tr');
    const labelTd = document.createElement('td');
    labelTd.className = 'row-label';
    labelTd.textContent = tid + ' ' + DATA[tid].category;
    labelTd.onclick = () => { switchTab('explorer'); openTask(tid); };
    tr.appendChild(labelTd);
    CONDITIONS.forEach(c => {
      const td = document.createElement('td');
      const s = DATA[tid].models[c.key]?.success;
      td.className = s ? 'pass' : 'fail';
      td.textContent = s ? 'P' : 'F';
      td.title = `${tid} | ${c.model} ${c.cond} | ${s ? 'PASS' : 'FAIL'}`;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
})();

// ===== TASK EXPLORER =====
let currentCondFilter = 'all';

function toggleCondFilter(btn, val) {
  currentCondFilter = val;
  document.querySelectorAll('.cond-filter button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderTaskList();
}

function applyFilters() { renderTaskList(); }

function openTask(tid) {
  const card = document.getElementById('card-'+tid);
  if (card) {
    const body = card.querySelector('.task-body');
    body.classList.add('open');
    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function renderTaskList() {
  const diff = document.getElementById('filter-diff').value;
  const cat = document.getElementById('filter-cat').value;
  const status = document.getElementById('filter-status').value;
  const search = document.getElementById('filter-search').value.toLowerCase();
  const container = document.getElementById('task-list');
  container.innerHTML = '';

  const taskIds = Object.keys(DATA).sort((a,b) => parseInt(a.slice(1)) - parseInt(b.slice(1)));
  taskIds.forEach(tid => {
    const t = DATA[tid];
    if (diff !== 'all' && t.difficulty !== diff) return;
    if (cat !== 'all' && t.category !== cat) return;
    if (search && !t.prompt.toLowerCase().includes(search) && !tid.toLowerCase().includes(search)) return;

    const condKeys = CONDITIONS.filter(c => {
      if (currentCondFilter === 'vanilla') return c.cond === 'vanilla';
      if (currentCondFilter === 'skill_v3') return c.cond === 'skill_v3';
      return true;
    });

    const successes = condKeys.map(c => t.models[c.key]?.success);
    const allPass = successes.every(s => s === true);
    const allFail = successes.every(s => s !== true);
    if (status === 'mixed' && (allPass || allFail)) return;
    if (status === 'all-pass' && !allPass) return;
    if (status === 'all-fail' && !allFail) return;

    const card = document.createElement('div');
    card.className = 'task-card';
    card.id = 'card-' + tid;

    const dots = CONDITIONS.map(c => {
      const s = t.models[c.key]?.success;
      return `<span class="${s ? 'pass' : 'fail'}"></span>`;
    }).join('');

    card.innerHTML = `
      <div class="task-header" onclick="this.nextElementSibling.classList.toggle('open')">
        <span class="task-id">${tid}</span>
        <span class="task-diff ${t.difficulty}">${t.difficulty} ${t.category}</span>
        <span class="task-prompt">${escHtml(t.prompt)}</span>
        <span class="task-mini-dots">${dots}</span>
      </div>
      <div class="task-body">
        <div class="prompt-box">
          ${escHtml(t.prompt)}
          <div class="prompt-api">API: ${escHtml(t.tests_api)}</div>
        </div>
        <div class="model-grid" id="grid-${tid}"></div>
      </div>
    `;
    container.appendChild(card);

    const grid = card.querySelector('.model-grid');
    condKeys.forEach(c => {
      const m = t.models[c.key];
      if (!m) return;
      const s = m.success;
      const div = document.createElement('div');
      div.className = `model-result ${s ? 'pass' : 'fail'}-border`;
      div.innerHTML = `
        <div class="mr-header">
          <div>
            <span class="mr-model">${c.model}</span>
            <span class="mr-cond">${c.cond}</span>
          </div>
          <span class="mr-badge ${s ? 'pass' : 'fail'}">${s ? 'PASS' : 'FAIL'}</span>
        </div>
      `;
      grid.appendChild(div);
    });
  });
}

function escHtml(s) {
  if (!s) return '';
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

// Build category filter
(function() {
  const cats = new Set();
  Object.values(DATA).forEach(t => cats.add(t.category));
  const sel = document.getElementById('filter-cat');
  sel.innerHTML = '<option value="all">All</option>';
  [...cats].sort().forEach(c => {
    sel.innerHTML += `<option value="${c}">${c}</option>`;
  });
})();

renderTaskList();
</script>

</body>
</html>'''

with open(V6_PATH, 'w') as f:
    f.write(html)

print(f"v6 HTML written: {os.path.getsize(V6_PATH)} bytes")
print(f"Path: {V6_PATH}")
