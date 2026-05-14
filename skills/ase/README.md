# ASE Skill

LLM knowledge augmentation for the [Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/) library. A structured reference that enables LLMs to generate error-free ASE Python scripts.

## Skill Versions

| Version | Lines | Tokens | Description |
|:---:|:---:|:---:|---|
| v1 | 15 | ~200 | Basic cheat sheet (key imports only) |
| v2 | 198 | ~1,800 | Full library reference (recommended for most tasks) |
| v3 | 256 | ~2,200 | v2 + explicit warnings and additional recipes |

## Benchmark Results (v6)

50 ASE tasks across 9 LLMs, comparing vanilla (no context) vs skill-augmented generation.

<div align="center">

| Provider | Model | Vanilla Pass% | Skill Pass% | Delta |
|:---:|---|:---:|:---:|:---:|
| Gemini | flash-lite | 44% (22/50) | 58% (29/50) | +14%p |
| Gemini | flash | 36% (18/50) | 58% (29/50) | +22%p |
| Gemini | pro | 32% (16/50) | 76% (38/50) | **+44%p** |
| OpenAI | gpt-5.4-mini | 82% (41/50) | 90% (45/50) | +8%p |
| OpenAI | gpt-5.4 | 90% (45/50) | 90% (45/50) | 0%p |
| OpenAI | gpt-5.5 | 100% (50/50) | 100% (50/50) | 0%p |
| Claude | Haiku 4.5 | 52% (26/50) | 80% (40/50) | **+28%p** |
| Claude | Sonnet 4.6 | 86% (43/50) | 94% (47/50) | +8%p |
| Claude | Opus 4.7 | 84% (42/50) | 100% (50/50) | **+16%p** |

</div>

Full interactive dashboard: [`benchmark/benchmark_report_v6.html`](benchmark/benchmark_report_v6.html)

## Key Findings

- **Skill v3 is the sweet spot**: 256 lines (~2,200 tokens) closes the gap for most models
- **Biggest gains**: Gemini Pro (+44%p), Haiku 4.5 (+28%p), Opus 4.7 (+16%p)
- **Already strong models gain less**: GPT-5.5 (100% vanilla), GPT-5.4 (90% vanilla) see 0-8%p improvement
- **Vanilla silent failures are the most dangerous**: e.g. Langevin MD with wrong units produces 2.4 billion K instead of 300 K with no Python error

## Files

```
ase_skill_v1.md              # 15-line cheat sheet
ase_skill_v2.md              # 198-line library reference
ase_skill_v3.md              # 256-line reference with warnings (recommended)
benchmark/
  benchmark_report_v6.html   # Interactive pass-rate dashboard
  _build_v6.py               # Builder script (reads v5, outputs v6)
```

## Usage

### As a Claude Code Skill
Copy `ase_skill_v3.md` to your skill directory. When triggered, it provides the LLM with correct import paths, class names, parameter conventions, and common recipes for all ASE modules.

### Run the Dashboard
Open `benchmark/benchmark_report_v6.html` in any browser. Three tabs: Overview (summary table), Heatmap (50 tasks x 18 conditions), Task Explorer (per-task details with filters).

## Author

Seokhyun Choung ([@schoung](https://github.com/schoung))
