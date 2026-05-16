"""Build v7 benchmark report from v5 data.
Reads v5 HTML, extracts DATA/SUMMARY, preserves code/stdout/stderr/quality,
outputs v7 HTML: OpenAI-style white design, KOR/ENG toggle, chem formula formatting."""

import json, re, os

V5_PATH = '/Users/sean/Library/CloudStorage/GoogleDrive-wjdtjrgus9967@gmail.com/My Drive/Research_2026/playground/108_ase_skill/benchmark/benchmark_report_v5.html'
V7_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'benchmark_report_v7.html')

with open(V5_PATH, 'r') as f:
    content = f.read()

# Extract DATA JSON
data_match = re.search(r'const DATA = ({.*?});\s*\n', content, re.DOTALL)
data = json.loads(data_match.group(1))

# Extract SUMMARY JSON
summary_match = re.search(r'const SUMMARY = ({.*?});\s*\n', content, re.DOTALL)
summary = json.loads(summary_match.group(1))

# English translations for all 50 prompts
EN_PROMPTS = {
    "T01": "Create a Cu FCC bulk and generate a 2×2×2 supercell. Print the cell info and number of atoms.",
    "T02": "Create a Pt(111) 4-layer slab and adsorb a CO molecule on the ontop site. Set vacuum to 10 Å. Print the number of atoms in the final structure.",
    "T03": "Create a monolayer MoS₂ structure. Add 10 Å of vacuum and print the cell size.",
    "T04": "Optimize the H₂O molecule structure using the EMT calculator. Use the BFGS optimizer and print the energy before and after optimization.",
    "T05": "Find the equilibrium lattice constant of Cu FCC bulk via Equation of State (EOS) fitting. Print the equilibrium volume and bulk modulus.",
    "T06": "Run 100-step 300 K Langevin MD on a Cu FCC bulk 2×2×2 supercell. Timestep 5 fs. Print initial/final temperature and energy.",
    "T07": "Run 50-step NVE (VelocityVerlet) MD on Cu FCC bulk. Set initial temperature to 300 K and print initial/final total energy (kinetic+potential) to check energy conservation.",
    "T08": "Calculate the vibrational frequencies of an N₂ molecule. Use the EMT calculator and print the frequency values.",
    "T09": "Save a Cu FCC bulk in VASP POSCAR format, then read it back and print the number of atoms and cell parameters.",
    "T10": "Create a Cu octahedron nanoparticle with length=5. Print the number of atoms and the positions shape.",
    "T11": "Create an Al BCC structure using bulk with a lattice constant of 3.3 Å. Set cubic=True and print the cell and chemical formula.",
    "T12": "Create a Ti HCP bulk structure. Set a=2.95, c/a=1.59 and print the cell vectors and atomic positions.",
    "T13": "Create a diamond-structure Si bulk with lattice constant 5.43 Å. Make a 3×3×3 supercell and print the number of atoms and cell volume.",
    "T14": "Create an NaCl crystal using spacegroup 225 (Fm-3m). Place Na at (0,0,0) and Cl at (0.5,0.5,0.5) with lattice constant 5.64 Å. Print the number of atoms and chemical symbols.",
    "T15": "Create a Cu(100) surface with 3 layers. Size (3,3,3), vacuum 12 Å. Print the number of atoms and cell info.",
    "T16": "Create a Fe BCC(110) surface with 4 layers. size=(2,2,4), vacuum=10 Å. Print the number of atoms and cell size.",
    "T17": "Cut a general Miller index (2,1,1) surface from Cu bulk with 3 layers. Use the surface() function and add 10 Å vacuum. Print the number of atoms and cell.",
    "T18": "Fetch a CH₄ molecule from the ASE G2 database. Print atomic coordinates, bond lengths, and chemical formula.",
    "T19": "Manually create a CO₂ molecule as an Atoms object. Place C at the origin with O atoms at ±1.16 Å. Set cell to 10×10×10 box, pbc=False. Calculate and print interatomic distances using get_distances.",
    "T20": "Create a (6,6) carbon nanotube with length=4. Print the number of atoms and cell info.",
    "T21": "Create an Au icosahedron nanoparticle with noshells=3. Print the number of atoms and center of mass.",
    "T22": "Adsorb an N₂ molecule on the bridge site of a 3-layer Al(111) slab. Height 2.0 Å, vacuum 10 Å. Fetch N₂ via molecule() and print the number of atoms and species in the final structure.",
    "T23": "Create structures with OH adsorbed on Pt(111) 3-layer slab at ontop, bridge, and fcc hollow sites. Attach EMT calculator to each and compute single-point energies. Print comparison of which site has the lowest energy.",
    "T24": "Optimize the Au FCC bulk structure with EMT using the LBFGS optimizer. Set fmax=0.01 and print the number of optimization steps and final energy.",
    "T25": "Simultaneously optimize the lattice constant and atomic positions of Cu FCC bulk. Use FrechetCellFilter with BFGS optimizer, converge to fmax=0.01. Print cell size and energy before and after optimization.",
    "T26": "Optimize Ni FCC bulk using PreconLBFGS with EMT calculator. Set precon='auto', converge to fmax=0.01. Print step count, final energy, and cell parameters.",
    "T27": "Run 200-step 500 K NVT MD on Ag FCC 2×2×2 supercell using the Bussi thermostat. Timestep 5 fs. Record and print temperature every 50 steps.",
    "T28": "Implement a temperature ramp from 300 K to 600 K using Langevin MD on a Cu FCC 2×2×2 supercell. Total 200 steps, timestep 5 fs. Print current temperature every 50 steps.",
    "T29": "Run 200-step VelocityVerlet NVE MD on Pd FCC 2×2×2 supercell at initial temperature 500 K. Timestep 2 fs. Print the difference in total energy (kinetic+potential) between start and end to verify conservation.",
    "T30": "Run 200-step NPT MD on Cu FCC 3×3×3 supercell using NPTBerendsen at 300 K, 1 bar. Timestep 5 fs, taut=100*units.fs, taup=1000*units.fs. Print initial/final cell volume and pressure.",
    "T31": "Run 100-step NPTBerendsen MD on Al FCC 2×2×2 supercell at 500 K, 10 GPa high pressure. Convert pressure units from GPa to eV/Å³. Print initial/final cell volume.",
    "T32": "Calculate the vibrational modes of an H₂O molecule. Use EMT calculator and print each mode's frequency (cm⁻¹) and energy (eV).",
    "T33": "Calculate vibrational frequencies of CH₄ using EMT calculator. First optimize the structure, then perform vibration analysis. Filter and print only real frequencies.",
    "T34": "Compute the NEB path for a Cu adatom on Cu FCC(111) moving from fcc hollow to hcp hollow. Use 5 images with IDPP interpolation. Print the energy barrier (max energy minus initial energy).",
    "T35": "Perform a simple NEB calculation for a third Al atom moving between two other Al atoms. Use EMT calculator. Build initial/final states manually as Atoms objects. Use 3 images with linear interpolation. Print energy of each image.",
    "T36": "Perform EOS fitting for Ag FCC bulk. Vary lattice constant by ±5% over 7 points, compute energies, and fit with Birch-Murnaghan EOS. Print equilibrium lattice constant and bulk modulus in GPa.",
    "T37": "Calculate vibrational frequencies of N₂ with EMT, then use IdealGasThermo to compute Gibbs free energy at 298.15 K, 1 atm. Set geometry='linear', symmetrynumber=2. Print the result.",
    "T38": "Calculate vibrational frequencies of Cu bulk and use HarmonicThermo to obtain the Helmholtz free energy at 300 K. Use EMT calculator. Print the result in eV.",
    "T39": "Save an Au FCC bulk to XYZ format, then read it back and print the atom types and positions.",
    "T40": "Save an NaCl crystal structure in CIF format, read it back, and print the spacegroup info and number of atoms.",
    "T41": "Attach EMT calculator to Cu FCC bulk and run 10-step MD while saving to a trajectory file. Then re-read the trajectory and print the total number of frames and the energy of the last frame.",
    "T42": "Create an ASE database and store Cu bulk, Ag bulk, and Au bulk structures with their EMT energies. Then query all entries with db.select() and print each formula and energy.",
    "T43": "Save Cu slab structures with varying layer counts (2, 3, 4 layers) to an ASE database, adding layers as key-value metadata. Select only layers=3 entries and print the number of atoms.",
    "T44": "Fix the bottom 2 layers of a Cu(111) 4-layer slab using FixAtoms based on tags. Perform BFGS optimization with EMT. Compare and print the coordinates of fixed atoms before and after optimization to confirm they didn't move.",
    "T45": "Apply a FixBondLength constraint to H₂ with bond length fixed at 0.9 Å. Compute energy with EMT and print the bond length and energy before and after applying the constraint.",
    "T46": "Adsorb CO on a Pt(111) 3-layer slab. Fix the bottom layer with FixAtoms and constrain the C-O bond with FixBondLength. Apply both constraints and optimize with BFGS to fmax=0.05. Print final energy and C-O distance.",
    "T47": "Build a NeighborList for a Cu FCC 3×3×3 supercell using natural_cutoffs. Compute the number of neighbors for each atom and print the average coordination number.",
    "T48": "Use get_distances on a Cu FCC bulk 2×2×2 supercell to find distances from atom 0 to all others. Set mic=True for periodic boundary conditions. Print the minimum and maximum distances.",
    "T49": "Find the Cu FCC equilibrium lattice constant via EOS, then build a (111) 4-layer slab with that constant. Attach EMT, fix bottom 2 layers, and relax the surface with BFGS. Print final energy and average z-coordinate per layer.",
    "T50": "For Cu, Ag, and Au, create FCC bulk structures and perform EOS fitting with EMT. Compute the equilibrium lattice constant and bulk modulus for each metal and print a comparison table.",
}

# Build FULL DATA (include code, stdout, stderr, quality + EN prompts)
full_data = {}
for tid, task in data.items():
    ftask = {
        "id": task["id"],
        "category": task["category"],
        "difficulty": task["difficulty"],
        "prompt": task["prompt"],
        "prompt_en": EN_PROMPTS.get(tid, task["prompt"]),
        "tests_api": task.get("tests_api", ""),
        "models": {}
    }
    for mk, mv in task["models"].items():
        ftask["models"][mk] = {
            "provider": mv["provider"],
            "model": mv["model"],
            "condition": mv["condition"],
            "success": mv["success"],
            "quality": mv.get("quality", -1),
            "code": mv.get("code", ""),
            "stdout": mv.get("stdout", ""),
            "stderr": mv.get("stderr", ""),
        }
    full_data[tid] = ftask

# Build SUMMARY
full_summary = {}
for mk, sv in summary.items():
    full_summary[mk] = {
        "provider": sv["provider"],
        "model": sv["model"],
        "condition": sv["condition"],
        "pass_count": sv["pass_count"],
        "total": sv["total"],
    }

data_json = json.dumps(full_data, ensure_ascii=False)
summary_json = json.dumps(full_summary, ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASE Skill Benchmark v7 — Pass Rate Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --void: #000000;
  --ink: #1a1a1a;
  --canvas: #ffffff;
  --chalk: #f1f1f1;
  --fog: #e5e7eb;
  --graphite: #666666;
  --ash: #8f8f8f;
  --green: #16a34a;
  --green-bg: #f0fdf4;
  --green-dark: #15803d;
  --red: #dc2626;
  --red-bg: #fef2f2;
  --red-dark: #b91c1c;
  --amber: #d97706;
  --amber-bg: #fffbeb;
  --mark: #fef08a;
  --font: 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
  --mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
  --radius: 6px;
  --max-w: 1200px;
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: var(--canvas);
  color: var(--ink);
  font-family: var(--font);
  font-weight: 400;
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  padding: 2rem;
  max-width: var(--max-w);
  margin: 0 auto;
}
mark { background: var(--mark); padding: 0 2px; font-weight: 500; border-radius: 2px; }
h1 {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.04em;
  margin-bottom: .25rem;
}
.date { font-size: .8rem; color: var(--ash); margin-bottom: 2rem; }
h2 {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.14px;
  color: var(--graphite);
  margin: 2.5rem 0 1rem;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--fog);
}
p { margin-bottom: 1rem; }
strong { font-weight: 600; }

/* Language toggle */
.lang-toggle {
  position: fixed; top: 16px; right: 16px; z-index: 1000;
  display: flex; border: 1px solid var(--fog); border-radius: 9999px;
  overflow: hidden; background: var(--canvas); box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.lang-toggle button {
  font-family: var(--font);
  font-size: 13px; font-weight: 500; padding: 5px 14px;
  border: none; cursor: pointer; background: var(--canvas); color: var(--graphite);
  letter-spacing: 0.3px; transition: all .15s;
}
.lang-toggle button.active {
  background: var(--void); color: #fff;
}
.lang-toggle button:hover:not(.active) {
  background: var(--chalk);
}

/* Summary table */
.sum-tbl { border-collapse: collapse; margin: 1rem auto; width: 100%; }
.sum-tbl th {
  font-size: 12px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.14px; color: var(--graphite); text-align: left;
  padding: .6rem .6rem; border-bottom: 1px solid var(--void);
}
.sum-tbl th.r { text-align: right; }
.sum-tbl td {
  padding: .5rem .6rem; border-bottom: 1px solid var(--fog);
  font-family: var(--mono); font-size: .82rem;
}
.sum-tbl td.lbl { font-family: var(--font); font-weight: 400; }
.sum-tbl .r { text-align: right; }
.provider-tag {
  font-size: 10px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.3px; color: var(--ash); padding: 2px 6px;
  border: 1px solid var(--fog); border-radius: 9999px;
}
.delta-pos { color: var(--green-dark); font-weight: 600; }
.delta-neg { color: var(--red-dark); font-weight: 600; }
.delta-zero { color: var(--ash); }

/* Pass bar */
.pass-bar {
  display: inline-block; width: 70px; height: 8px;
  background: var(--fog); border-radius: 4px; overflow: hidden;
  vertical-align: middle; margin-left: 6px;
}
.pass-bar-fill {
  height: 100%; border-radius: 4px;
}

/* Heatmap */
.hm-wrap { overflow-x: auto; margin: 1rem auto; display: flex; justify-content: center; }
.hm-wrap table { border-collapse: collapse; }
.hm-wrap th {
  font-size: 10px; font-weight: 600; letter-spacing: 0;
  padding: 2px 1px; writing-mode: vertical-lr; text-orientation: mixed;
  white-space: nowrap; border-bottom: 1px solid var(--void); color: var(--ash);
}
.hm-wrap td {
  width: 22px; height: 22px; padding: 0; text-align: center;
  font-size: 10px; font-family: var(--mono);
  border: 1px solid var(--canvas); cursor: pointer;
}
.hm-wrap td.pass { background: #dcfce7; color: var(--green-dark); }
.hm-wrap td.fail { background: #fee2e2; color: var(--red-dark); }
.hm-wrap td.row-label {
  width: auto; text-align: right; padding-right: 8px;
  font-family: var(--font); font-size: 12px;
  font-weight: 400; background: none; border: none; white-space: nowrap;
  cursor: pointer; text-decoration: underline; text-decoration-color: var(--fog);
}
.hm-wrap td.row-label:hover { color: var(--green); }
.legend {
  display: flex; gap: 16px; align-items: center;
  font-size: 12px; color: var(--graphite); margin: .5rem auto 1rem;
  justify-content: center;
}
.legend-box {
  display: inline-block; width: 14px; height: 14px;
  margin-right: 4px; vertical-align: middle; border-radius: 3px;
}

/* Task Explorer */
.task-explorer { margin-top: 1rem; }
.task-card {
  border: 1px solid var(--fog); margin-bottom: 4px; background: var(--canvas);
  border-radius: var(--radius);
}
.task-header {
  display: grid; grid-template-columns: 60px 80px 1fr auto;
  align-items: center; gap: 8px; padding: 8px 12px; cursor: pointer;
  font-size: .82rem;
}
.task-header:hover { background: rgba(0,0,0,.015); }
.task-id { font-family: var(--mono); font-weight: 500; font-size: 13px; }
.task-diff { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 9999px; }
.task-diff.L1 { background: var(--green-bg); color: var(--green-dark); }
.task-diff.L2 { background: var(--amber-bg); color: var(--amber); }
.task-diff.L3 { background: var(--red-bg); color: var(--red-dark); }
.task-prompt { font-size: 13px; color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.task-mini-dots { display: flex; gap: 2px; }
.task-mini-dots span {
  width: 8px; height: 8px; border-radius: 50%; display: inline-block;
}
.task-mini-dots span.pass { background: var(--green); }
.task-mini-dots span.fail { background: var(--red); }

.task-body { display: none; padding: 0 12px 12px; }
.task-body.open { display: block; }
.prompt-box {
  background: var(--chalk); padding: 10px 14px; font-size: 13px;
  border-left: 3px solid var(--mark); margin-bottom: 12px; line-height: 1.6;
  border-radius: 0 var(--radius) var(--radius) 0;
}
.prompt-api { font-size: 11px; color: var(--ash); margin-top: 4px; font-family: var(--mono); }

/* Model results grid */
.model-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 6px;
}
.model-result {
  border: 1px solid var(--fog); padding: 8px 10px; font-size: 13px;
  border-radius: var(--radius);
}
.model-result.pass-border { border-left: 3px solid var(--green); }
.model-result.fail-border { border-left: 3px solid var(--red); }
.mr-header {
  display: flex; justify-content: space-between; align-items: center;
}
.mr-model { font-weight: 600; font-size: 12px; }
.mr-cond { font-size: 10px; color: var(--ash); text-transform: uppercase; letter-spacing: 0.3px; margin-left: 4px; }
.mr-badge {
  font-size: 10px; font-weight: 600; padding: 2px 8px;
  border-radius: 9999px; text-transform: uppercase;
}
.mr-badge.pass { background: var(--green-bg); color: var(--green-dark); }
.mr-badge.fail { background: var(--red-bg); color: var(--red-dark); }

/* Quality badge */
.q-badge {
  font-size: 10px; font-weight: 600; padding: 2px 6px;
  border-radius: 9999px; margin-left: 4px;
  letter-spacing: 0.3px;
}
.q-badge.q2 { background: var(--green-bg); color: var(--green-dark); }
.q-badge.q1 { background: var(--amber-bg); color: var(--amber); }
.q-badge.q0 { background: var(--red-bg); color: var(--red-dark); }
.q-badge.qn { background: var(--chalk); color: var(--ash); }

/* Code toggle button */
.code-toggle {
  font-size: 11px; padding: 2px 10px; margin-top: 6px;
  border: 1px solid var(--fog); background: var(--canvas);
  cursor: pointer; font-family: var(--font); font-weight: 500;
  color: var(--graphite); border-radius: 9999px; transition: all .15s;
}
.code-toggle:hover { background: var(--chalk); color: var(--ink); }

/* Code box */
.code-detail { display: none; margin-top: 8px; }
.code-detail.open { display: block; }

.code-box {
  background: #1e1e1e; color: #d4d4d4;
  padding: 12px 14px; font-family: var(--mono);
  font-size: 12px; line-height: 1.6;
  max-height: 300px; overflow-y: auto;
  border-radius: var(--radius); white-space: pre-wrap; word-break: break-all;
  margin-bottom: 4px;
}
.code-box::-webkit-scrollbar { width: 6px; }
.code-box::-webkit-scrollbar-thumb { background: #555; border-radius: 3px; }

/* Stdout box */
.stdout-box {
  background: #052e16; color: #86efac;
  padding: 8px 12px; font-family: var(--mono);
  font-size: 11px; line-height: 1.5;
  max-height: 180px; overflow-y: auto;
  border-radius: var(--radius); white-space: pre-wrap; word-break: break-all;
  margin-bottom: 4px; border-left: 3px solid var(--green);
}
.stdout-box::-webkit-scrollbar { width: 6px; }
.stdout-box::-webkit-scrollbar-thumb { background: var(--green-dark); border-radius: 3px; }

/* Stderr box */
.stderr-box {
  background: #450a0a; color: #fca5a5;
  padding: 8px 12px; font-family: var(--mono);
  font-size: 11px; line-height: 1.5;
  max-height: 180px; overflow-y: auto;
  border-radius: var(--radius); white-space: pre-wrap; word-break: break-all;
  margin-bottom: 4px; border-left: 3px solid var(--red);
}
.stderr-box::-webkit-scrollbar { width: 6px; }
.stderr-box::-webkit-scrollbar-thumb { background: var(--red-dark); border-radius: 3px; }

.output-label {
  font-size: 10px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.3px; color: var(--ash); margin: 6px 0 2px;
}

/* Filter controls */
.filters {
  display: flex; gap: 12px; align-items: center; flex-wrap: wrap;
  margin-bottom: 12px; font-size: 13px;
}
.filters select, .filters input {
  font-family: var(--font);
  font-size: 13px; padding: 4px 10px;
  border: 1px solid var(--fog); background: var(--canvas);
  border-radius: var(--radius);
}
.filters label { color: var(--graphite); font-weight: 500; }

/* Tabs */
.tab-bar {
  display: flex; gap: 0; border-bottom: 1px solid var(--void); margin-bottom: 1rem;
}
.tab-btn {
  padding: 8px 18px; font-size: 13px; font-weight: 500;
  cursor: pointer; border: 1px solid var(--fog); border-bottom: none;
  background: var(--chalk); color: var(--graphite); margin-right: -1px;
  border-radius: var(--radius) var(--radius) 0 0; transition: all .15s;
}
.tab-btn.active {
  background: var(--canvas); color: var(--ink); font-weight: 600;
  border-bottom: 1px solid var(--canvas); position: relative; top: 1px;
}

.tab-content { display: none; }
.tab-content.active { display: block; }

/* Condition filter buttons */
.cond-filter {
  display: flex; gap: 4px; margin-bottom: 8px;
}
.cond-filter button {
  font-size: 12px; padding: 4px 12px; border: 1px solid var(--fog);
  background: var(--canvas); cursor: pointer; font-family: var(--font);
  font-weight: 500; border-radius: 9999px; color: var(--graphite);
  transition: all .15s;
}
.cond-filter button.active { background: var(--void); color: #fff; }
.cond-filter button:hover:not(.active) { background: var(--chalk); }

.foot {
  display: grid; grid-template-columns: 1fr auto;
  border-top: 1px solid var(--fog); padding-top: .75rem;
  margin-top: 3rem; font-size: 12px; color: var(--ash);
}

/* Centered text */
.center-text { text-align: center; }

/* Key finding box */
.key-finding {
  border-top: 2px solid var(--void);
  border-bottom: 2px solid var(--void);
  padding: 1.25rem 0;
  margin: 2rem 0;
  text-align: center;
}
</style>
</head>
<body>

<!-- Language toggle -->
<div class="lang-toggle">
  <button class="active" id="lang-ko" onclick="setLang('ko')">KOR</button>
  <button id="lang-en" onclick="setLang('en')">ENG</button>
</div>

<h1>ASE Skill Benchmark v7</h1>
<p class="date">2026.05 &middot; Seokhyun Choung &middot; Pass Rate Dashboard</p>

<p data-ko="9개 LLM에 250줄 ASE 스킬을 주입한 50-task 벤치마크. <strong>Pass rate</strong>(성공/전체) 기준으로 스킬 유무에 따른 성능 변화를 비교한다."
   data-en="50-task benchmark injecting a 250-line ASE skill into 9 LLMs. Compares performance with and without the skill, measured by <strong>pass rate</strong> (successes / total)."
   class="i18n-html"></p>

<!-- TAB BAR -->
<div class="tab-bar">
  <div class="tab-btn active" onclick="switchTab('overview')" data-ko="Overview" data-en="Overview" class="i18n">Overview</div>
  <div class="tab-btn" onclick="switchTab('heatmap')" data-ko="Heatmap" data-en="Heatmap" class="i18n">Heatmap</div>
  <div class="tab-btn" onclick="switchTab('explorer')" data-ko="Task Explorer" data-en="Task Explorer" class="i18n">Task Explorer</div>
</div>

<!-- ===== TAB 1: OVERVIEW ===== -->
<div id="tab-overview" class="tab-content active">

<h2 data-ko="Overall Results — Pass Rate" data-en="Overall Results — Pass Rate" class="i18n">Overall Results — Pass Rate</h2>
<p class="center-text i18n-html" style="font-size:13px"
   data-ko="Pass Rate = 실행 성공(returncode==0) 비율. 50개 태스크 &times; 9개 모델 &times; 2 조건(w/o Skill / w/ Skill)."
   data-en="Pass Rate = fraction of successful executions (returncode==0). 50 tasks &times; 9 models &times; 2 conditions (w/o Skill / w/ Skill)."></p>

<table class="sum-tbl">
<thead>
<tr>
  <th>Provider</th><th>Model</th>
  <th class="r">w/o Skill Pass%</th>
  <th class="r">w/ Skill Pass%</th>
  <th class="r">Delta</th>
</tr>
</thead>
<tbody id="summary-body"></tbody>
</table>

<div class="key-finding">
<p style="font-size:1rem;margin:0" class="i18n-html"
   data-ko="<strong>Key finding:</strong> ASE 스킬이 가장 큰 효과를 보이는 모델은 <mark>Gemini Pro (+44%p)</mark>와 <mark>Opus 4.7 (+16%p)</mark>이다."
   data-en="<strong>Key finding:</strong> The ASE skill has the greatest impact on <mark>Gemini Pro (+44%p)</mark> and <mark>Opus 4.7 (+16%p)</mark>."></p>
<p style="font-size:13px;margin:.5rem 0 0;color:var(--graphite)" class="i18n-html"
   data-ko="GPT-5.5은 w/o Skill 100%로 스킬 불필요. Haiku 4.5는 스킬로 +28%p 상승."
   data-en="GPT-5.5 achieves 100% w/o Skill, making the skill unnecessary. Haiku 4.5 gains +28%p with the skill."></p>
</div>

</div>

<!-- ===== TAB 2: HEATMAP ===== -->
<div id="tab-heatmap" class="tab-content">

<h2 data-ko="Pass/Fail Heatmap (50 Tasks &times; 18 Conditions)" data-en="Pass/Fail Heatmap (50 Tasks &times; 18 Conditions)" class="i18n-html">Pass/Fail Heatmap (50 Tasks &times; 18 Conditions)</h2>
<div class="legend">
  <span><span class="legend-box" style="background:#dcfce7"></span> Pass</span>
  <span><span class="legend-box" style="background:#fee2e2"></span> Fail</span>
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

<h2 data-ko="Task Explorer — 50 Tasks" data-en="Task Explorer — 50 Tasks" class="i18n">Task Explorer — 50 Tasks</h2>

<div class="filters">
  <label data-ko="Difficulty:" data-en="Difficulty:" class="i18n">Difficulty:</label>
  <select id="filter-diff" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="L1">L1</option>
    <option value="L2">L2</option>
    <option value="L3">L3</option>
  </select>
  <label data-ko="Category:" data-en="Category:" class="i18n">Category:</label>
  <select id="filter-cat" onchange="applyFilters()"></select>
  <label data-ko="Status:" data-en="Status:" class="i18n">Status:</label>
  <select id="filter-status" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="mixed">Mixed</option>
    <option value="all-pass">All pass</option>
    <option value="all-fail">All fail</option>
  </select>
  <label data-ko="Search:" data-en="Search:" class="i18n">Search:</label>
  <input type="text" id="filter-search" placeholder="keyword..." oninput="applyFilters()">
</div>

<div class="cond-filter">
  <button class="active" onclick="toggleCondFilter(this,'all')" data-ko="All" data-en="All" class="i18n">All</button>
  <button onclick="toggleCondFilter(this,'vanilla')" data-ko="w/o Skill only" data-en="w/o Skill only" class="i18n">w/o Skill only</button>
  <button onclick="toggleCondFilter(this,'skill_v3')" data-ko="w/ Skill only" data-en="w/ Skill only" class="i18n">w/ Skill only</button>
</div>

<div id="task-list" class="task-explorer"></div>

</div>

<div class="foot">
  <span>ASE Skill Benchmark v7 / Gemini + OpenAI + Claude / Pass Rate Dashboard</span>
  <span>2026.05</span>
</div>

<script>
const DATA = ''' + data_json + r''';
const SUMMARY = ''' + summary_json + r''';

let currentLang = 'ko';

const COND_LABEL = { "vanilla": "w/o Skill", "skill_v3": "w/ Skill" };
const QUALITY_LABEL = { 2: "Clean", 1: "Warning", 0: "Fail", "-1": "N/A" };
const QUALITY_CLASS = { 2: "q2", 1: "q1", 0: "q0", "-1": "qn" };

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

// ===== CHEMICAL FORMULA FORMATTING =====
function formatChem(text) {
  if (!text) return '';
  // Multiplication sign
  text = text.replace(/(\d+)x(\d+)x(\d+)/g, '$1×$2×$3');
  // Subscripts for chemical formulas (longer patterns first, avoid already-formatted)
  const subs = [
    [/MoS2(?!<)/g, 'MoS<sub>2</sub>'],
    [/Cu2O(?!<)/g, 'Cu<sub>2</sub>O'],
    [/CO2(?!<)/g, 'CO<sub>2</sub>'],
    [/H2O(?!<)/g, 'H<sub>2</sub>O'],
    [/CH4(?!<)/g, 'CH<sub>4</sub>'],
    [/N2(?!<)(?![.\d])/g, 'N<sub>2</sub>'],
    [/H2(?!<)(?![.\d])/g, 'H<sub>2</sub>'],
    [/O2(?!<)(?![.\d])/g, 'O<sub>2</sub>'],
  ];
  subs.forEach(([pat, rep]) => { text = text.replace(pat, rep); });
  // Superscript units
  text = text.replace(/cm\^-1/g, 'cm⁻¹');
  text = text.replace(/Ang\^3/g, 'Å³');
  return text;
}

// ===== LANGUAGE TOGGLE =====
function setLang(lang) {
  currentLang = lang;
  document.getElementById('lang-ko').classList.toggle('active', lang === 'ko');
  document.getElementById('lang-en').classList.toggle('active', lang === 'en');

  // Update i18n text elements
  document.querySelectorAll('.i18n').forEach(el => {
    const val = el.getAttribute('data-' + lang);
    if (val) el.textContent = val;
  });
  // Update i18n-html elements (allow HTML)
  document.querySelectorAll('.i18n-html').forEach(el => {
    const val = el.getAttribute('data-' + lang);
    if (val) el.innerHTML = val;
  });

  // Re-render task list with new language
  renderTaskList();
}

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
    const vColor = vPct >= 80 ? 'var(--green)' : vPct >= 50 ? 'var(--amber)' : 'var(--red)';
    const sColor = sPct >= 80 ? 'var(--green)' : sPct >= 50 ? 'var(--amber)' : 'var(--red)';
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
      td.title = `${tid} | ${c.model} ${COND_LABEL[c.cond] || c.cond} | ${s ? 'PASS' : 'FAIL'}`;
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

function toggleCodeDetail(btn) {
  const detail = btn.nextElementSibling;
  if (detail.classList.contains('open')) {
    detail.classList.remove('open');
    btn.textContent = 'Show Code';
  } else {
    detail.classList.add('open');
    btn.textContent = 'Hide Code';
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
    if (search && !t.prompt.toLowerCase().includes(search) && !tid.toLowerCase().includes(search)
        && !(t.prompt_en && t.prompt_en.toLowerCase().includes(search))) return;

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

    const promptKo = formatChem(escHtml(t.prompt));
    const promptEn = formatChem(escHtml(t.prompt_en || t.prompt));
    const displayPrompt = currentLang === 'en' ? promptEn : promptKo;

    card.innerHTML = `
      <div class="task-header" onclick="this.nextElementSibling.classList.toggle('open')">
        <span class="task-id">${tid}</span>
        <span class="task-diff ${t.difficulty}">${t.difficulty} ${t.category}</span>
        <span class="task-prompt">${displayPrompt}</span>
        <span class="task-mini-dots">${dots}</span>
      </div>
      <div class="task-body">
        <div class="prompt-box">
          ${displayPrompt}
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
      const q = m.quality !== undefined ? m.quality : -1;
      const qClass = QUALITY_CLASS[q] || 'qn';
      const condLabel = COND_LABEL[c.cond] || c.cond;
      const hasCode = m.code && m.code.trim().length > 0;
      const hasStdout = m.stdout && m.stdout.trim().length > 0;
      const hasStderr = m.stderr && m.stderr.trim().length > 0;

      const div = document.createElement('div');
      div.className = `model-result ${s ? 'pass' : 'fail'}-border`;

      let codeHtml = '';
      if (hasCode || hasStdout || hasStderr) {
        codeHtml += `<button class="code-toggle" onclick="toggleCodeDetail(this)">Show Code</button>`;
        codeHtml += `<div class="code-detail">`;
        if (hasCode) {
          codeHtml += `<div class="output-label">Code</div>`;
          codeHtml += `<div class="code-box">${escHtml(m.code)}</div>`;
        }
        if (hasStdout) {
          codeHtml += `<div class="output-label">stdout</div>`;
          codeHtml += `<div class="stdout-box">${escHtml(m.stdout)}</div>`;
        }
        if (hasStderr) {
          codeHtml += `<div class="output-label">stderr</div>`;
          codeHtml += `<div class="stderr-box">${escHtml(m.stderr)}</div>`;
        }
        codeHtml += `</div>`;
      }

      div.innerHTML = `
        <div class="mr-header">
          <div>
            <span class="mr-model">${c.model}</span>
            <span class="mr-cond">${condLabel}</span>
            <span class="q-badge ${qClass}">Q${q}</span>
          </div>
          <span class="mr-badge ${s ? 'pass' : 'fail'}">${s ? 'PASS' : 'FAIL'}</span>
        </div>
        ${codeHtml}
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

// Initial render
renderTaskList();
setLang('ko');
</script>

</body>
</html>'''

with open(V7_PATH, 'w') as f:
    f.write(html)

print(f"v7 HTML written: {os.path.getsize(V7_PATH)} bytes")
print(f"Path: {V7_PATH}")
