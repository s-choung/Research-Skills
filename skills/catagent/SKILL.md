---
name: catagent
description: Compute catalyst adsorption energies (metal, bimetallic, high-entropy alloy, rutile oxide surfaces) with a machine-learned interatomic potential through CatAgent (https://catagent.schoung.com). Two modes - (1) remote, call the public CatAgent HTTP API and let ccel-mace run MACE/UMA, (2) local, import the vetted catagent_harness.py next to your own MACE install. Triggers - /catagent, "adsorption energy", "흡착 에너지", "binding energy on Pt", "site scan", "HEA OH", "rutile cus", "coverage series", "CO on Cu facets", "catagent"
---

# CatAgent skill

CatAgent turns one plain-language question ("CO adsorption energy on Pt(111) by site")
into a relaxed slab + adsorbate calculation with a machine-learned interatomic
potential (MLIP) and returns numbers, a plot and a rendered structure.
Web UI: https://catagent.schoung.com. Source of this skill:
https://github.com/s-choung/Research-Skills/tree/main/skills/catagent.

Use it when the user wants demo-grade (fmax 0.1 eV/A, 60 steps, 36-atom slab)
adsorption energies in about 1 to 4 minutes, not publication-grade DFT.

## 0. Decide the mode

| Mode | When | What you need |
|---|---|---|
| **Remote** (default) | You have internet and no MLIP installed | `curl` only. Compute runs on ccel-mace (16-core CPU). One job at a time, 6 min hard cap. |
| **Local** | User has `mace-torch` (or `fairchem-core`) installed and wants to keep data local | `catagent_harness.py` from this folder, `ase >= 3.23`, `mace-torch` |

Both modes use the same harness API (section 3), so a script written for one runs in the other.

## 1. Remote mode: HTTP API

Base URL `https://catagent.schoung.com`. All bodies are JSON. Long stages return
`{"jobId": ...}` immediately; poll `GET /api/simjob?id=<jobId>` every 5 s until
`status == "done"`, then read `.result`.

### 1.1 Plan (LLM, ~5 s)

```bash
curl -s https://catagent.schoung.com/api/plan \
  -H 'content-type: application/json' \
  -d '{"message": "Pt(111)에서 CO 흡착 에너지를 ontop, bridge, fcc, hcp site별로 비교해줘.", "model": "openai/gpt-6-luna"}'
```

Response: `{"parsed": {"status": "spec"|"need_clarification", "tags": {...}, "spec": {...}}, "raw": "...", "usage": {...}}`.
If `status` is `need_clarification`, ask the user the listed `questions` and call `/api/plan` again with the answer appended to the message.
Keep the whole `spec` object; every later stage takes it.

### 1.2 Write the script (LLM, ~15 s)

```bash
curl -s https://catagent.schoung.com/api/codewrite \
  -H 'content-type: application/json' \
  -d '{"spec": <spec>, "mlip": "mace-small", "query": "<original question>", "model": "openai/gpt-6-luna"}'
# -> {"jobId": "job_..."}   then poll /api/simjob?id=job_...
```

`result.code` is a python script that only imports from `catagent_harness`.
`mlip` is one of `mace-small` (default, fastest), `mace-medium`, `uma-s`.
You may also write the script yourself with section 3 and skip this call.

### 1.3 Static audit (LLM, ~3 s, optional but recommended)

```bash
curl -s https://catagent.schoung.com/api/audit -H 'content-type: application/json' \
  -d '{"spec": <spec>, "code": "<script>"}'
# poll -> result: {"verdict": "pass"|"fix", "issues": [...], "fix_instruction": "..."}
```

On `fix`, call `/api/codewrite` again with `fixInstruction` and `prevCode`.

### 1.4 Structure preview (no MLIP, ~20 s, optional)

```bash
curl -s https://catagent.schoung.com/api/preview -H 'content-type: application/json' \
  -d '{"code": "<script>", "mlip": "mace-small"}'
# -> {"runId": "run_...", "slabs": ["/live/run_.../preview_slab_0.png", ...], "adsAll": [...]}
```

Show the PNG urls to the user before spending compute. Pass `runId` as `previewRunId` in the next call so the files land in the same run folder.

### 1.5 Simulate (MLIP on ccel-mace, 1 to 4 min)

```bash
curl -s https://catagent.schoung.com/api/simulate -H 'content-type: application/json' \
  -d '{"code": "<script>", "mlip": "mace-small", "taskId": "co_pt111", "previewRunId": "run_..."}'
# -> {"jobId": "job_..."}
curl -s 'https://catagent.schoung.com/api/simjob?id=job_...'
# running: {"status": "running", "queueAhead": 0, "initialRender": "/live/run_.../initial.png"}
# done:    {"status": "done", "result": {"exit": 0, "output": "<stdout>", "runId": "run_...",
#           "render": "/live/run_.../structure.png", "walltime_s": 41.2, "hardware": "ccel-mace (16-core CPU)"}}
```

Tell the user the expected time before starting: `spec.estimated_runtime_s` from the planner, or 4 s per relax with MACE-small (15 s with UMA), two relaxes per case.
`exit != 0` means a python error; the traceback is in `output`. Fix the script (or call `/api/codewrite` with `fixInstruction` set to the traceback) and resubmit. Do not resubmit unchanged code.

### 1.6 Read the numbers

The script prints one line `RESULT_JSON:{...}` with every requested value in eV, plus
`CASE <label> E_ads_eV=<v> converged=<bool>` lines and `[harness] E_ads(...)` lines with
`fmax_final`. Parse `RESULT_JSON` from `output` yourself, or ask the analyzer:

```bash
curl -s https://catagent.schoung.com/api/analyze -H 'content-type: application/json' \
  -d '{"query": "<question>", "spec": <spec>, "stdout": "<output>", "lang": "en"}'
# poll -> result: {"verdict": "success"|"expert_review"|"failed", "conclusion": "...",
#                  "key_numbers": {...}, "physical_check": "..."}
```

Optional plot: `POST /api/resultplot` with `{"query", "spec", "runId"}` returns `/live/<runId>/result_plot.png`.
Files under `/live/<runId>/` (structure.png, structure.extxyz, results.json, result_plot.png) are fetchable with plain GET.

### 1.7 Etiquette

- One simulation at a time per visitor. If `queueAhead > 0`, wait, do not resubmit.
- Do not loop over dozens of surfaces from a script. Six cases per query is the practical limit (about 3 minutes).
- No NEB, no molecular dynamics, no cells beyond 4x4x4, no `steps > 80`. The static auditor rejects these.
- Report every energy with its sign convention and `fmax_final`. Demo-grade means fmax 0.1 eV/A on a 36-atom slab.

## 2. Local mode

```bash
pip install ase mace-torch          # or: pip install fairchem-core for UMA
cp skills/catagent/catagent_harness.py ./
python my_script.py                 # my_script.py imports from catagent_harness
```

`catagent_harness.py` in this folder is the server copy with the MLIP fixed to
`mace-small`. Edit the `_MLIP_KEY` line at the top to `mace-medium` or `uma-s`.
Set `CATAGENT_PREVIEW=1` in the environment to run with a null calculator (structure check only, no MLIP download).

## 3. Harness API (the only imports a script may use)

```python
from catagent_harness import (
    build_slab, build_alloy_slab, build_hea_slab, build_rutile_slab,
    ontop_sites, cus_sites, bridge_o_sites, surface_symbols,
    adsorption_energy, site_scan, ontop_scan,
    gas_energy, reference_energy, free_energy_correction,
    sabatier_activity, reaction_energy, relax, save_structure,
)
```

Allowed extra imports: `json`, `math`, `numpy`, `itertools`, `collections`. Never build a calculator, never call `ase.io.write`, never use `os`/`sys`/`subprocess`/`pickle`.

### Builders

| Function | Notes |
|---|---|
| `build_slab(element="Pt", facet="111", size=(3,3,4), vacuum=10.0)` | fcc 111/100/110/211, hcp 0001, bcc 110/100. Bottom half fixed. |
| `build_alloy_slab(host, dopant, fraction=0.25, mode="random", facet="111", size=(3,3,4), seed=0)` | `mode` random, surface, subsurface, core_shell. Vegard lattice. |
| `build_hea_slab(elements=("Ir","Pd","Pt","Rh","Ru"), fractions=None, facet="111", size=(3,3,4), seed=0)` | random solid solution on fcc lattice |
| `build_rutile_slab(M="Ru", facet="110", layers=3, size=(2,1))` | MO2(110) with bridging-O termination; M in Ru, Ir, Ti, Sn, Mn, Pb, Ge, V, Cr, Os, Rh, Nb, Ta, Mo, W |

### Sites

`"ontop" | "bridge" | "fcc" | "hcp"` (pure metal, first surface cell), `"ontop:<atom index>"`
(any top-layer atom; use `ontop_sites(slab)` to list them), `"cus"` / `"cus:<k>"` and
`"bridge_O"` / `"bridge_O:<k>"` (rutile), or an `(x, y)` tuple in Angstrom.
On alloys and HEAs bare `"ontop"` resolves to the host-element top atom nearest the cell centre.
On stepped facets (211) bare `"ontop"` also resolves to a top-layer atom; bridge/fcc/hcp are undefined there.

### Energies

```python
r = adsorption_energy(slab, adsorbate="CO", site="ontop", scheme=None, fmax=0.1, steps=60)
# r: E_ads_eV (negative = exothermic), E_slab_eV, E_slab_ads_eV, E_ref_eV, scheme,
#    dz_A, converged, fmax_final, atoms (relaxed slab+adsorbate)
site_scan(slab, "CO", sites=("ontop","bridge","fcc","hcp"))   # {site: E_ads_eV}
ontop_scan(slab, "OH", max_sites=9)                            # [{index, symbol, E_ads_eV}, ...]
sabatier_activity(e_ads_list, e_ref_pt111, optimum=0.10)       # HEAgent-style score, 0..1
```

Adsorbates: O, H, N, C, S, CO, NO, N2, OH, OOH, H2O, NH, NH2, NH3, CH3, CHO, CO2, OCHO.

Reference schemes (`scheme`):
- `"che"` (default for O, OH, OOH, H, N): O = H2O - H2, OH = H2O - 1/2 H2, OOH = 2 H2O - 3/2 H2, H = 1/2 H2, N = 1/2 N2. **Positive values are normal here** (O on rutile cus is roughly +1 to +3 eV). Do not call them a sign error.
- `"gas"` (default for CO, NO, NH3, H2O, CO2): the molecule itself. Strong binders come out negative (CO on Pt(111) about -1.8 eV with MACE-MP-0 small).

### Script skeleton the server expects

```python
import json
from catagent_harness import build_slab, site_scan, adsorption_energy, save_structure

def run(fmax, steps, production=False):
    slab = build_slab("Pt", "111", size=(3, 3, 4))
    energies = site_scan(slab, "CO", sites=("ontop", "bridge", "fcc", "hcp"), fmax=fmax, steps=steps)
    best = min(energies, key=energies.get)
    if production:
        for s, e in energies.items():
            print(f"CASE Pt111_{s}_CO E_ads_eV={e} converged=True")
        r = adsorption_energy(slab, "CO", best, fmax=fmax, steps=steps)
        save_structure(r["atoms"], "structure.extxyz")
    return {f"Pt111_{s}_CO_E_ads_eV": e for s, e in energies.items()}

run(fmax=3.0, steps=3)            # smoke test, seconds
print("SMOKE_OK")
result = run(fmax=0.1, steps=60, production=True)
print("RESULT_JSON:" + json.dumps(result, separators=(",", ":")))
```

Rules the auditor enforces: smoke run first, `SMOKE_OK`, exactly one `RESULT_JSON:` line with only numbers, one `save_structure` call, no hard-coded reference energies, no `repeat()`, `steps <= 80`, size at most 4x4x4.

## 4. Worked examples (all verified on catagent.schoung.com, MACE-MP-0 small)

| Question | Result (eV) | Wall time |
|---|---|---|
| CO on Pt(111) by site | ontop -1.76, bridge -1.79, fcc -1.57, hcp -1.56 | 41 s |
| CO on Pt(111) vs Pt3Ni, Pt3Co, Pt3Cu (111) | Pt(111) -1.76 and three alloy values | 191 s |
| OH ontop scan on IrPdPtRhRu(111) + activity score vs Pt(111) | site-resolved list, score in 0..1 | 211 s |
| O on rutile RuO2, IrO2, TiO2, SnO2 (110) cus, che scheme | +2.14, +2.19, +2.90, +3.92 | 212 s |
| H on Pd(111) at 1/9, 1/4, 1 ML | coverage series, che scheme | not timed yet |
| CO on Cu(111), Cu(100), Cu(211) | -0.85, -0.98, -1.11 | 121 s |

## 5. Reporting to the user

Give the table of `E_ads` per case with the scheme named, the most stable case, `fmax_final`
and whether it met 0.1 eV/A, the MLIP used, and the wall time. Say "demo-grade MLIP
estimate" in the first sentence. Link the structure and plot PNGs when they exist.
