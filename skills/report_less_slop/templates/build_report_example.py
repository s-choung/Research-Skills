"""Build 002_feature_bench/feature_bench_report.html from results/feature_bench_master.csv
and figures/*.svg, figures/fb_ligands.png. Single standalone file, Korean, openai tokens.
Run: conda run -n base python scripts/build_report.py"""
import base64
import io
import re
from pathlib import Path

import pandas as pd
from PIL import Image

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
FIG = BASE / "figures"
OUT_HTML = BASE / "feature_bench_report.html"
FONT_B64 = (BASE.parent / "001_flexcat" / "repro" / "inter_latin.b64").read_text().strip()
M = pd.read_csv(BASE / "results" / "feature_bench_master.csv")

# ------------------------------------------------------------------ helpers
GLYPHS = {}
_GLYPH_RE = re.compile(r"<path id=\"(ArialMT-[^\"]+)\"[^>]*/>")
_GEOM_ATTRS = ("d", "transform", "points", "viewBox", "width", "height", "x", "y", "x1", "x2", "y1", "y2", "cx", "cy", "r")
_ATTR_RE = re.compile(r"\b(" + "|".join(_GEOM_ATTRS) + r")=\"([^\"]*)\"")
_NUM_RE = re.compile(r"\d+\.\d{3,}")


def _trim(m):
    return f'{m.group(1)}="{_NUM_RE.sub(lambda n: format(float(n.group(0)), ".2f"), m.group(2))}"'


def svg(name):
    p = FIG / f"{name}.svg"
    if not p.exists():
        return f"<div class='note'>그림 {name}이 아직 생성되지 않았습니다.</div>"
    s = p.read_text()
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    for m in _GLYPH_RE.finditer(s):
        GLYPHS.setdefault(m.group(1), m.group(0))
    s = _GLYPH_RE.sub("", s)
    s = re.sub(r"<defs>\s*</defs>", "", s)
    s = _ATTR_RE.sub(_trim, s)
    s = re.sub(r"\n\s+(?=<)", "", s)
    return f"<div class='fig'>{s}</div>"


def png(name, width=1400):
    im = Image.open(FIG / name).convert("RGB")
    if im.width > width:
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    im = im.quantize(255)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    b = base64.b64encode(buf.getvalue()).decode()
    return f"<div class='fig'><img src='data:image/png;base64,{b}' alt='{name}'></div>"


def bl(items):
    parts = ["<ul>"]
    for it in items:
        if isinstance(it, (list, tuple)) and len(it) == 2 and isinstance(it[1], list):
            parts.append(f"<li>{it[0]}{bl(it[1])}</li>")
        else:
            parts.append(f"<li>{it}</li>")
    parts.append("</ul>")
    return "".join(parts)


def cap(n, text):
    return f"<p class='cap'><b>Figure {n}.</b> {text}</p>"


def note(items):
    return f"<div class='note'>{bl(items)}</div>"


def figbox(box_id, dims, variants, caption):
    ctrl = []
    for lab, opts in dims:
        btns = "".join(f"<button type='button' data-v='{v}'{' class=on' if i == 0 else ''}>{t}</button>"
                       for i, (v, t) in enumerate(opts))
        ctrl.append(f"<div class='btngrp'><span class='glab'>{lab}</span>{btns}</div>")
    default = "|".join(o[0][0] for _, o in dims)
    figs = []
    for key, val in variants.items():
        hide = "" if key == default else " hidden"
        figs.append(f"<div class='fv' data-key='{key}'{hide}>{svg(val)}</div>")
    return (f"<div class='figbox' id='{box_id}'><div class='ctrls'>{''.join(ctrl)}</div>"
            f"{''.join(figs)}</div>{caption}")


def table(headers, rows, bold_first=True):
    h = "".join(f"<th>{x}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    return f"<div class='tbl'><table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>"


def cell(panel, split, s, model, col):
    r = M[(M.panel == panel) & (M.split == split) & (M["set"] == s) & (M.model == model)]
    return float(r[col].iloc[0]) if len(r) else float("nan")


def f2(v):
    if v != v:
        return ""
    return "0.00" if abs(v) < 0.005 else f"{v:.2f}"


# ------------------------------------------------------------------ dims
MODELS = ["TabPFN", "Stack", "GP", "HistGB", "ExtraTrees", "Ridge"]
METRIC_DIM = ("지표", [("rho", "Spearman rho"), ("r2", "R2"), ("mae", "MAE")])
MODEL_DIM = ("모델", [(m, m) for m in MODELS])
PANEL_DIM = ("패널", [("suz8", "Suzuki 8종"), ("bh4", "Buchwald 4종"), ("suz11", "Suzuki 11종")])
PANEL2_DIM = ("패널", [("suz8", "Suzuki 8종"), ("bh4", "Buchwald 4종")])
SPLIT_DIM = ("분할", [("random10", "random 10-fold"), ("lolo", "leave-one-ligand-out")])
LOLO_DIM = ("점수", [("percond", "조건 셀 안 리간드 순위"), ("lig", "리간드 평균 순위"), ("row", "행 단위 rho")])
PAR_MODEL_DIM = ("모델", [(m, m) for m in ["TabPFN", "GP", "HistGB", "Ridge"]])

FIG2 = {f"{m}|{k}": f"fb_floor__{m}__{k}" for m in MODELS for k in ("rho", "r2", "mae")}
FIG3 = {f"{p}|{s}|{k}": f"fb_models__{p}__{s}__{k}" for p in ("suz8", "bh4", "suz11") for s in ("random10", "lolo") for k in ("rho", "r2", "mae")}
FIG4 = {f"{p}|{k}": f"fb_lolo__{p}__{k}" for p in ("suz8", "bh4") for k in ("percond", "lig", "row")}
FIG5 = {f"{p}|{s}|{m}": f"fb_parity__{p}__{s}__{m}" for p in ("suz8", "bh4") for s in ("random10", "lolo") for m in ("TabPFN", "GP", "HistGB", "Ridge")}
FIG6 = {k: f"fb_cross__{k}" for k in ("percond", "lig")}

# ------------------------------------------------------------------ tables
SETS = ["cond only", "cond+k4", "cond+e4", "cond+k4+e4", "cond+onehot"]
SET_KO = {"cond only": "조건만", "cond+k4": "조건 + Kraken 입체 4", "cond+e4": "조건 + Kraken 전자 4",
          "cond+k4+e4": "조건 + Kraken 입체 4 + 전자 4", "cond+onehot": "조건 + 리간드 one-hot"}


def king_table():
    rows = []
    for p, lab in [("suz11", "Suzuki 11종"), ("suz8", "Suzuki 8종 (Kraken)"), ("bh4", "Buchwald 4종")]:
        d = M[(M.panel == p) & (M.split == "random10")]
        best = d.sort_values("rho", ascending=False).iloc[0]
        floor = d[d["set"] == "cond only"].rho.max()
        ceil = d[d["set"] == "cond+onehot"].rho.max()
        kr = d[d["set"].isin(["cond+k4", "cond+e4", "cond+k4+e4"])].rho.max()
        rows.append([lab, f"{floor:.2f}", f"{kr:.2f}" if kr == kr else "없음", f"{ceil:.2f}", f"{best.model}, {SET_KO[best['set']]}", f"{best.rho:.3f} / {best.r2:.3f} / {best.mae:.1f}"])
    return table(["패널", "바닥 (조건만) rho", "Kraken 세트 최고 rho", "천장 (one-hot) rho", "1위 조합", "rho / R2 / MAE"], rows)


def lolo_table():
    rows = []
    for p, lab in [("suz8", "Suzuki 8종"), ("bh4", "Buchwald 4종")]:
        for s in ["cond only", "cond+k4", "cond+e4", "cond+k4+e4", "cond+onehot"]:
            vals = [f2(cell(p, "lolo", s, m, "percond_rho")) for m in MODELS]
            rows.append([f"{lab}, {SET_KO[s]}"] + vals)
    return table(["패널, 세트"] + MODELS, rows)


def full_table():
    d = M.sort_values(["panel", "split", "set", "model"])
    rows = []
    for _, r in d.iterrows():
        rows.append([r.panel, r.split, r["set"], r.model, f"{r.rho:.3f}", f"{r.r2:.3f}", f"{r.mae:.1f}",
                     f2(r.lig_rho), f2(r.percond_rho), f"{r.fit_s:.0f}"])
    return table(["panel", "split", "set", "model", "rho", "R2", "MAE", "lig_rho", "percond_rho", "fit s"], rows)


def fit_table():
    rows = []
    for m in MODELS:
        v = [M[(M.panel == p) & (M.split == "random10") & (M["set"] == "cond+k4+e4") & (M.model == m)].fit_s for p in ("suz8", "bh4")]
        v11 = M[(M.panel == "suz11") & (M.split == "random10") & (M["set"] == "cond+onehot") & (M.model == m)].fit_s
        rows.append([m] + [f"{x.iloc[0]:.0f}" if len(x) else "" for x in (v11, *v)])
    return table(["모델", "Suzuki 11종 (5280행, one-hot)", "Suzuki 8종 (3860행)", "Buchwald 4종 (3955행)"], rows)


# ------------------------------------------------------------------ text
SUMMARY = [
    ("본 리간드의 수율 순위는 TabPFN에 조건 one-hot과 Kraken descriptor를 넣은 조합이 Kraken이 있는 두 패널에서 1위입니다.", [
        "random 10-fold Spearman rho는 Suzuki 8종 0.935(입체 4 + 전자 4), Buchwald 4종 0.972(입체 4)이고, 입체 4 + 전자 4는 Buchwald에서 0.971입니다. Stack이 0.005 안쪽으로 뒤따릅니다.",
        "Kraken이 없는 Suzuki 11종에서는 조건 + 리간드 one-hot의 Stack 0.911, TabPFN 0.909가 1위입니다.",
        "Kraken 숫자 8개는 리간드 one-hot 천장(0.921, 0.970)과 같거나 약간 높습니다. 본 리간드에서는 descriptor가 리간드 신원표 역할까지만 합니다.",
    ]),
    ("안 본 리간드의 순위는 Suzuki, Buchwald 어느 쪽에서도 Kraken 세트가 잡지 못합니다.", [
        "leave-one-ligand-out에서 조건 셀 안 리간드 순위 rho는 Suzuki 8종 -0.13에서 +0.14, Buchwald 4종 -0.75에서 -0.04입니다. 0 근처는 순위 정보가 없다는 뜻입니다.",
        "같은 Kraken 입체 4 + 전자 4 세트가 flexcat에서는 신규 46종 외부 rho 0.69(GP)를 냈습니다. 차이는 학습에 쓰인 리간드 수(62 대 8, 4)입니다.",
    ]),
    ("데이터셋마다 king이 다르지 않습니다. 본 리간드는 TabPFN, 안 본 리간드는 GP가 0에 가장 가깝고, Ridge는 어디서도 상호작용을 잡지 못합니다.", [
        "Ridge는 세트를 바꿔도 Suzuki에서 rho 0.71에서 0.72에 머뭅니다. 리간드 x 조건 상호작용이 선형 가법 모델 밖에 있습니다.",
        "GP는 bench62 초기값으로는 수율 패널에서 분산이 0으로 붕괴했고, 초기 length scale 10, noise 0.3으로 바꾼 뒤에야 0.92에서 0.96이 나왔습니다 (Methods).",
    ]),
    ("Buchwald에서는 전자 4를 넣으면 안 본 리간드 예측이 나빠집니다. GP 행 단위 rho 0.82에서 0.67, Ridge R2 0.51에서 0.04입니다.", [
        "리간드가 4종이라 하나를 빼면 남은 3점 밖으로 외삽하게 됩니다. 입체 4는 같은 조건에서 0.80을 유지합니다.",
    ]),
    ("2단계(Pd 착물 MACE 블록, morfeus 입체)는 이 결과 위에서 결정합니다. 1단계 비용은 RunPod pod 3대, 약 1.9달러였습니다.", []),
]

Q_INTRO = [
    ("질문은 001_flexcat과 같습니다. 타깃(TOF 또는 수율, SN)마다 안 본 리간드의 순위 rho를 가장 높이는 feature 세트와 모델은 무엇인가.", [
        "하위 질문은 세 개입니다. 어떤 descriptor 블록이 이기는가, 어떤 모델이 이기는가, 데이터셋마다 king이 다른가.",
        "수율은 활성 척도이므로 TOF 쪽 타깃으로 취급합니다. SN은 flexcat에만 있습니다.",
    ]),
    ("이 문서는 Suzuki와 Buchwald 두 수율 데이터셋의 1단계 결과입니다. flexcat 결과는 001 리포트 v2에 있고, section 2.4에서 대조합니다.", [
        "1단계 블록은 조건 one-hot, 리간드 one-hot, Kraken 입체 4, Kraken 전자 4입니다. DFT와 MLIP 계산 블록은 2단계로 미룹니다.",
    ]),
    ("보조 진단으로 조건만 아는 모델(바닥)과 리간드 one-hot까지 아는 모델(천장)을 같은 표에 둡니다. 세트 점수가 리간드 덕인지 조건 덕인지 이 둘 사이에서 읽습니다.", []),
]

DATASET_ROWS = [
    ["Suzuki (Perera 2018)", "5280", "11 (Kraken 8)", "친전자체 7 x 친핵체 4 x 염기 8 x 용매 6", "수율 (%)", "suz11, suz8"],
    ["Buchwald (Ahneman 2018)", "3955", "4 (Kraken 4)", "아릴할라이드 15 x 염기 3 x 첨가제 22", "수율 (%)", "bh4"],
    ["flexcat 1.0 + 2.0 (대조)", "680 + 92", "62 (Kraken 57)", "무차원 연속 조건 6", "SN, TOF", "001 bench62"],
]

LIG_ROWS = [
    ["P(tBu)<sub>3</sub>", "Suzuki", "8", "13"], ["AmPhos", "Suzuki", "216", "18"], ["P(Ph)<sub>3</sub>", "Suzuki", "17", "19"],
    ["P(Cy)<sub>3</sub>", "Suzuki", "11", "19"], ["P(o-Tol)<sub>3</sub>", "Suzuki", "9", "22"], ["CataCXium A", "Suzuki", "10", "25"],
    ["SPhos", "Suzuki", "3", "29"], ["XPhos", "Suzuki, Buchwald", "1", "34"], ["dtbpf", "Suzuki", "없음 (Fe 이좌)", "28"],
    ["dppf", "Suzuki", "없음 (Fe 이좌)", "36"], ["Xantphos", "Suzuki", "없음 (이좌)", "42"],
    ["tBuXPhos", "Buchwald", "90", "30"], ["tBuBrettPhos", "Buchwald", "89", "34"], ["AdBrettPhos", "Buchwald", "347", "46"],
]

R21 = [
    ("Suzuki 11종은 바닥과 천장의 간격이 가장 큽니다. 조건만으로 rho 0.70(TabPFN), 리간드 one-hot을 더하면 0.91(Stack 0.911, TabPFN 0.909)입니다.", [
        "R2로는 0.51에서 0.85, MAE로는 14.7에서 7.7 %p입니다. 이 데이터셋에서는 리간드가 수율 분산의 절반 가까이를 설명합니다.",
        "Kraken 세트는 이좌 리간드 3종(dppf, dtbpf, Xantphos)에 값이 없어 이 패널에서는 돌리지 않았습니다.",
    ]),
    ("Suzuki 8종에서는 Kraken 숫자 4개가 one-hot 천장에 닿습니다. 입체 4 0.933, 전자 4 0.930, 둘 다 0.935, one-hot 0.921(TabPFN)입니다.", [
        "입체 4와 전자 4가 거의 같은 점수를 냅니다. 리간드 8종을 서로 구별하는 숫자라면 무엇이든 같은 일을 한다는 뜻이고, random 10-fold는 descriptor의 화학적 질을 가리지 못합니다.",
        "바닥이 0.80으로 11종 패널(0.70)보다 높습니다. 이좌 리간드 3종이 빠지면서 조건 효과가 상대적으로 커졌습니다.",
    ]),
    ("Buchwald 4종은 바닥이 0.87로 가장 높고, 어떤 리간드 표현을 더해도 0.97에서 멈춥니다.", [
        "조건 인자 셀이 990개(15 x 3 x 22)이고 리간드는 4종이라, 조건 one-hot만으로 R2 0.73이 나옵니다.",
        "Kraken 세트와 one-hot의 차이는 0.002 안쪽입니다. 4종은 어떤 4차원 벡터로도 완전히 구별되므로 표현 방식이 점수에 영향을 주지 않습니다.",
    ]),
    ("MAE 버튼으로 보면 순서가 같습니다. Suzuki 8종 TabPFN 12.3에서 6.4 %p, Buchwald 9.9에서 4.2 %p입니다.", []),
]

R22 = [
    ("TabPFN이 세 패널의 random 10-fold에서 모두 1위 또는 1위와 0.005 이내입니다. Stack(GP + HistGB + TabPFN 평균)은 Suzuki 11종에서만 0.002 앞섭니다.", [
        "TabPFN 학습 시간은 셀당 11에서 26초입니다. GP는 같은 셀에 184에서 1063초가 들었습니다 (Methods 표).",
    ]),
    ("GP는 Buchwald에서 TabPFN에 0.01 뒤(0.960 대 0.972), Suzuki 8종 Kraken 세트에서 0.02에서 0.04 뒤(0.895에서 0.916)입니다.", [
        "GP는 연속 열이 4개뿐일 때 가장 낮습니다(입체 4 0.895, 전자 4 0.899). 8개(0.916)나 one-hot(0.914)에서는 회복합니다. Matern 커널 하나가 조건 one-hot 25열과 연속 4열을 같은 length scale로 다루기 때문입니다.",
    ]),
    ("트리 모델(HistGB, ExtraTrees)은 0.91 부근에서 서로 같고 TabPFN보다 0.02 낮습니다. Buchwald에서는 차이가 0.04에서 0.06으로 커집니다.", []),
    ("Ridge는 세트를 바꿔도 점수가 거의 움직이지 않습니다. Suzuki 11종 0.61에서 0.71, 8종 0.71에서 0.72, Buchwald 0.81에서 0.86입니다.", [
        "Ridge에서 one-hot과 Kraken 입체 4 + 전자 4의 점수가 소수 셋째 자리까지 같습니다(Suzuki 8종 0.723 대 0.723, Buchwald 0.861 대 0.861). 선형 모델은 리간드 주효과만 배우고, 그 주효과는 리간드를 구별하는 어떤 표현으로도 같습니다.",
        "TabPFN과 Ridge의 차이(0.93 대 0.72)가 곧 리간드 x 조건 상호작용의 크기입니다.",
    ]),
    ("leave-one-ligand-out 버튼으로 바꾸면 모든 모델의 행 단위 rho가 0.78에서 0.85 사이로 모입니다. 조건 효과가 행 순위의 대부분을 정하기 때문에, 이 분할에서는 행 단위 점수로 모델을 가릴 수 없습니다.", []),
]

R23 = [
    ("조건만 아는 모델의 조건 셀 안 리간드 순위 rho는 -0.59에서 -1.00입니다. 이 값이 이 점수의 바닥이고, 0에 가까워질수록 안 본 리간드에 대한 정보가 있다는 뜻입니다.", [
        "빠진 리간드가 셀에서 가장 좋은 리간드이면 그 리간드 없이 학습한 조건 평균은 낮게 나오고, 나머지 리간드 예측은 그대로라 순위가 뒤집힙니다. 데이터의 성질이지 모델의 결함이 아닙니다.",
        "리간드 one-hot도 같은 값을 냅니다(Suzuki 8종 -0.40에서 -0.94). 안 본 리간드는 0 벡터라 조건만 아는 모델과 같아집니다.",
    ]),
    ("Suzuki 8종에서 Kraken 세트는 이 점수를 -0.13에서 +0.14로 올립니다. 바닥에서는 벗어나지만 0을 넘지 못합니다.", [
        "GP가 가장 높습니다(전자 4 +0.14, 입체 4 + 전자 4 +0.03). TabPFN은 -0.05에서 -0.27, ExtraTrees는 -0.12에서 -0.16입니다.",
        "리간드 평균 순위(lig_rho)도 -0.55에서 +0.26 사이에서 흩어지고, 8점 위의 값이라 p값이 0.05를 넘는 셀이 대부분입니다.",
    ]),
    ("Buchwald 4종에서 TabPFN은 Kraken 세트를 넣어도 -0.74에서 -0.75로 조건만 아는 모델(-0.80)과 같습니다. 학습 밖 리간드에 대해 descriptor를 쓰지 않고 조건 평균으로 되돌아갑니다.", [
        "GP는 -0.04에서 -0.09로 0에 가장 가깝지만, 그 대가로 행 단위 rho가 0.82(조건만)에서 0.67(전자 4), 0.72(입체 4 + 전자 4)로 떨어집니다.",
        "Ridge도 전자 4에서 R2 0.51에서 0.04로 무너집니다. 4종 중 하나를 빼면 전자 descriptor의 학습 범위가 3점이 되고 빠진 리간드는 그 밖에 놓입니다.",
    ]),
    ("parity 그림(Figure 5)에서 보면 leave-one-ligand-out의 TabPFN은 리간드별 rho가 0.67(P(o-Tol)<sub>3</sub>)에서 0.91(CataCXium A) 사이입니다. 리간드 안에서 조건 순위는 잘 맞고, 리간드 사이의 높낮이가 어긋납니다.", []),
]

R24 = [
    ("같은 Kraken 입체 4 + 전자 4 세트로 flexcat은 신규 46종 외부 rho 0.69(GP), 0.63(TabPFN)을 냈고, Suzuki와 Buchwald는 0 근처입니다.", [
        "flexcat 점수는 001 bench62_master.csv의 kraken57 패널 ext_rho이고, Suzuki와 Buchwald는 이 문서의 percond_rho입니다. 둘 다 같은 조건에서 안 본 리간드의 순위를 묻는 점수입니다.",
    ]),
    ("차이의 첫째 원인은 descriptor에서 활성으로 가는 사상을 배울 리간드 수입니다. flexcat은 16종으로 배워 46종에 시험했고, Suzuki는 7종으로 배워 1종에, Buchwald는 3종으로 배워 1종에 시험했습니다.", [
        "둘째 원인은 flexcat의 리간드가 단좌 포스핀으로 넓게 퍼져 있어 8차원 Kraken 공간에서 보간이 되는 반면, Buchwald 4종은 서로 비슷한 biaryl 포스핀이라 남은 3점이 한 방향에 몰려 있다는 점입니다.",
    ]),
    ("flexcat의 champion(speciation 2-state + MACE BE + S1)은 Rh 착물 계산이라 Pd 반응에 옮길 수 없습니다. 수율 데이터에서 같은 질문을 하려면 Pd-L 착물 블록이 필요하고, 이것이 2단계의 이유입니다.", []),
]

INTERESTING = [
    ("데이터셋별", [
        "Suzuki 11종은 리간드가 rho 0.70에서 0.91을 채우고, Buchwald 4종은 조건이 0.87을 먼저 채웁니다. 리간드 선택 실험의 가치가 Suzuki 쪽이 큽니다.",
        "Suzuki 11종에서 8종으로 갈 때 바닥이 0.70에서 0.80으로 오르는 이유는 Xantphos입니다. Xantphos는 평균 수율 15.9 %p, 수율 0 행이 19 %로 11종 중 가장 낮고, Kraken이 없어 8종 패널에서 빠집니다.",
        "Buchwald는 leave-one-ligand-out에서 전자 4를 넣으면 나빠지고, 입체 4만 넣으면 행 단위 rho가 유지됩니다. XPhos의 <sup>31</sup>P NMR 값(306.8)이 나머지 3종(255.1에서 271.3) 밖에 있어, XPhos를 뺀 fold에서 전자 4의 외삽 폭이 가장 큽니다.",
    ]),
    ("모델별", [
        "TabPFN은 본 리간드에서 1위이지만 안 본 리간드에서는 조건 평균으로 후퇴합니다. Buchwald percond_rho -0.75가 그 증거입니다.",
        "GP는 안 본 리간드에서 유일하게 양수 percond_rho(Suzuki 8종 전자 4 +0.14)를 내지만, bench62 초기값으로는 수율 패널에서 커널 상수가 1e-5로 붕괴해 R2 0이 나왔습니다. 초기값을 바꾼 뒤에야 비교가 가능했습니다.",
        "Stack은 TabPFN과 0.005 이내이고 학습 시간은 세 모델의 합입니다. 수율 패널에서는 TabPFN 단독으로 충분합니다.",
        "ExtraTrees는 조건만 아는 leave-one-ligand-out에서 percond_rho가 정확히 -1.00입니다. 조건 one-hot 트리는 셀마다 상수를 예측하므로 빠진 리간드 하나와 나머지 순위가 항상 뒤집힙니다.",
    ]),
    ("feature별", [
        "본 리간드에서 입체 4와 전자 4는 교환 가능합니다. 어느 쪽이든 8종을 구별하면 되고, 둘을 합쳐도 0.002 밖에 오르지 않습니다.",
        "안 본 리간드에서만 입체와 전자의 차이가 드러납니다. Suzuki는 전자 4가, Buchwald는 입체 4가 덜 해롭습니다. 리간드가 8종, 4종이라 이 차이를 결론으로 삼지는 않습니다.",
        "리간드 one-hot은 leave-one-ligand-out에서 조건만 아는 모델과 같은 점수를 냅니다. 안 본 리간드 실험에는 one-hot 열이 아무 정보도 주지 않는다는 것을 수치로 확인했습니다.",
    ]),
]

METHODS = [
    ("<b>데이터.</b> Suzuki는 Perera 2018의 5280행(리간드 없는 행 제외), Buchwald는 Ahneman 2018의 3955행입니다. 000_data/assemble_rxn_yields.py가 원 csv에서 조성 열과 수율을 뽑고 Kraken 표에서 descriptor 8개를 리간드 이름으로 붙였습니다. 이좌 리간드 3종(dppf, dtbpf, Xantphos)은 Kraken에 없어 Suzuki 8종 패널에서 뺐습니다."),
    ("<b>Feature 블록.</b> 조건은 조성 인자(Suzuki 친전자체, 친핵체, 염기, 용매. Buchwald 아릴할라이드, 염기, 첨가제)의 one-hot입니다. Kraken 입체 4는 vbur_vbur_boltz, vbur_ovbur_max_boltz, sterimol_B5_boltz, sterimol_L_boltz이고, 전자 4는 vmin_vmin_boltz, fmo_e_homo_boltz, nbo_P_boltz, nmr_P_boltz입니다. 모두 Boltzmann 평균값이고 실험 비용은 0입니다."),
    ("<b>분할.</b> random 10-fold는 행 단위 KFold(seed 0)입니다. leave-one-ligand-out은 리간드 하나의 전체 행을 빼고 나머지로 학습해 그 리간드 행을 예측합니다. 두 분할 모두 fold 예측을 이어 붙여 한 번에 채점합니다."),
    ("<b>점수.</b> rho는 Spearman 순위 상관, R2는 채점 행 평균 대비 설명 분산, MAE는 %p 단위 평균 절대 오차입니다. leave-one-ligand-out에는 두 점수를 더 둡니다. percond_rho는 조건 셀마다 그 안의 리간드 순위 rho를 구해 평균한 값이고, 리간드 2종 이상이 있는 셀만 셉니다. lig_rho는 같은 모델의 조건만 세트 예측을 측정과 예측에서 뺀 뒤 리간드 평균의 순위 상관을 구한 값입니다."),
    ("<b>모델.</b> bench62 정의와 같습니다. Ridge(alpha 1, StandardScaler), HistGB(400회, 학습률 0.05, leaf 15, L2 1.0), ExtraTrees(500그루, min_leaf 2), GP(ConstantKernel x Matern 2.5 + White, normalize_y), TabPFN v2 회귀(로컬 체크포인트), Stack(GP, HistGB, TabPFN fold 예측의 평균)입니다."),
    ("<b>GP 초기값.</b> bench62의 초기값(length scale 1, noise 0.01)은 3500행 이상 one-hot 입력에서 최적화가 ConstantKernel 1e-5로 수렴해 모든 예측이 평균이 되었습니다(logs/gp_fullsize_test.log). 수율 패널에서는 초기 length scale 10, noise 0.3으로 두었고, 이 설정으로 돌린 lane만 결과에 넣었습니다. flexcat 패널의 GP는 bench62 값 그대로입니다."),
    ("<b>실행.</b> RunPod community pod 3대(A5000급)에서 lane 3개(fast: Ridge, HistGB, ExtraTrees, TabPFN 전체. gp_suz2, gp_bh2: GP)로 나눠 돌렸고, 결과는 900초마다 Hugging Face에 올린 뒤 로컬에서 합쳤습니다(scripts/merge_results.py). 총 비용 약 1.9달러입니다. 셀 138개 = 수율 패널 3 x 분할 2 x 세트(5 또는 2) x 모델 5 + Stack 18."),
    ("<b>그림.</b> 막대 그림은 scripts/fig_*.py가 feature_bench_master.csv에서 그렸고, parity는 results/preds/의 fold 예측을 읽었습니다. 리간드 구조는 RDKit ETKDG + MMFF 배좌를 Blender io_mesh_atomic으로 렌더했습니다. dppf와 dtbpf는 Fe를 빼고 Cp 반쪽 둘을 그렸습니다."),
]

LIMITS = [
    ("리간드 수가 8과 4라 leave-one-ligand-out 점수는 p값이 큰 값이 대부분이고, 세트 사이 차이를 결론으로 쓰지 않습니다.", []),
    ("Kraken이 없는 이좌 리간드 3종은 descriptor 비교에서 빠졌습니다. 2단계에서 Pd 착물 계산으로 채울 수 있습니다.", []),
    ("2단계 후보는 Pd-L 착물의 MACE-OMOL 결합 에너지와 morfeus 입체 4입니다. flexcat champion과 같은 구조의 세트를 수율 데이터에서 만드는 것이 목표입니다.", []),
    ("003_llm_bench는 이 세 데이터셋에서 LLM의 조성 선택 능력을 재는 별도 캠페인이고, 이 결과의 surrogate 기준선(TabPFN, GP)을 그대로 씁니다.", []),
    ("001에서 넘어온 TODO: ORCA DFT BE가 없는 리간드 7종(L23, L40, L60, L64, L65, L68, L69)이 끝나면 flexcat_ligands.csv를 다시 뽑고 dft62 패널을 돌립니다.", []),
]

# ------------------------------------------------------------------ page
BODY = f"""
<h1 class="sec">요약</h1>
{note(SUMMARY)}
{king_table()}
<p class="cap">표 1. 패널별 random 10-fold 바닥, Kraken 세트 최고, 천장, 1위 조합. 값은 Spearman rho이고 1위 조합 열은 rho, R2, MAE(%p)입니다.</p>

<h1 class="sec">1. 질문과 설계</h1>
{note(Q_INTRO)}
<h2>1.1 데이터셋</h2>
{table(["데이터셋", "행", "리간드", "조건 인자", "타깃", "패널"], DATASET_ROWS)}
<p class="cap">표 2. 데이터셋 세 개의 크기와 조건 구조. 패널 이름은 이후 그림의 버튼 이름과 같습니다.</p>
<h2>1.2 리간드</h2>
{png("fb_ligands.png")}
{cap(1, "Suzuki와 Buchwald 데이터셋의 포스핀 리간드 14종. 위 두 줄이 Suzuki, 아래 줄이 Buchwald이고 XPhos는 양쪽에 있습니다. 라벨의 숫자는 Kraken ID이며, ID가 없는 3종은 이좌 리간드입니다. 구조는 RDKit 배좌이고 dppf와 dtbpf는 Fe를 뺀 Cp 반쪽 둘입니다. 아래는 원소 범례입니다.")}
{table(["리간드", "데이터셋", "Kraken ID", "무거운 원자 수"], LIG_ROWS)}
<p class="cap">표 3. 리간드 14종의 소속과 Kraken ID. Kraken ID가 없는 리간드는 Suzuki 8종 패널에서 제외됩니다.</p>
<h2>1.3 feature 세트와 모델</h2>
{note([
    ("세트 5개. 조건만, 조건 + 리간드 one-hot, 조건 + Kraken 입체 4, 조건 + Kraken 전자 4, 조건 + Kraken 입체 4 + 전자 4.", [
        "조건만이 바닥, 리간드 one-hot이 천장입니다. leave-one-ligand-out에서는 안 본 리간드의 one-hot이 0 벡터가 되므로 천장이 바닥과 같아집니다.",
    ]),
    ("모델 6개. Ridge, HistGB, ExtraTrees, GP(Matern), TabPFN, Stack. 정의는 001 bench62와 같고 GP 초기값만 다릅니다 (Methods).", []),
    ("분할 2개. random 10-fold는 본 리간드의 새 조건, leave-one-ligand-out은 안 본 리간드입니다.", []),
])}

<h1 class="sec">2. 결과</h1>
<h2>2.1 데이터셋별 바닥, 천장, Kraken</h2>
{figbox("f2", [MODEL_DIM, METRIC_DIM], FIG2, cap(2, "패널 세 개의 random 10-fold 점수를 feature 세트별로 나란히 둔 막대 그림입니다. 모델 버튼과 지표 버튼으로 바꿔 봅니다. Suzuki 11종에는 조건만과 one-hot 두 세트만 있고, Stack에는 조건만 세트가 없습니다. 막대 위 숫자는 값입니다."))}
{note(R21)}
<h2>2.2 모델별 비교</h2>
{figbox("f3", [PANEL_DIM, SPLIT_DIM, METRIC_DIM], FIG3, cap(3, "한 패널 안에서 feature 세트별로 모델 6개의 점수를 나란히 둔 막대 그림입니다. 패널, 분할, 지표 버튼으로 바꿔 봅니다. 가로선은 0입니다."))}
{note(R22)}
<h2>2.3 안 본 리간드의 순위</h2>
{figbox("f4", [PANEL2_DIM, LOLO_DIM], FIG4, cap(4, "leave-one-ligand-out에서 feature 세트별, 모델별 점수입니다. 점수 버튼은 조건 셀 안 리간드 순위 rho(percond_rho), 조건 효과를 뺀 리간드 평균 순위 rho(lig_rho), 행 단위 rho를 바꿉니다. 조건만 세트에는 lig_rho가 정의되지 않습니다."))}
{lolo_table()}
<p class="cap">표 4. leave-one-ligand-out의 조건 셀 안 리간드 순위 rho(percond_rho). 행은 패널과 세트, 열은 모델입니다.</p>
{figbox("f5", [PANEL2_DIM, SPLIT_DIM, PAR_MODEL_DIM], FIG5, cap(5, "조건 + Kraken 입체 4 + 전자 4 세트의 fold 예측 대 측정 수율입니다. 점 색은 리간드이고 범례의 괄호는 그 리간드 행만의 Spearman rho입니다. 대각선은 예측과 측정이 같은 선입니다. 패널, 분할, 모델 버튼으로 바꿔 봅니다."))}
{note(R23)}
<h2>2.4 flexcat과의 대조</h2>
{figbox("f6", [("점수", [("percond", "같은 조건에서 리간드 순위"), ("lig", "리간드 평균 순위")])], FIG6, cap(6, "같은 Kraken 입체 4 + 전자 4 세트의 안 본 리간드 점수를 데이터셋 세 개에서 모델별로 둔 막대 그림입니다. flexcat 막대는 001 bench62의 kraken57 패널 외부 rho(SN, 신규 46종)이고 두 번째 버튼에서도 같은 값입니다. Suzuki와 Buchwald 막대는 leave-one-ligand-out의 percond_rho 또는 lig_rho입니다."))}
{note(R24)}

<h1 class="sec">3. 흥미로운 결과</h1>
{note(INTERESTING)}

<h1 class="sec">4. Methods</h1>
{"".join(f"<p>{m}</p>" for m in METHODS)}
{fit_table()}
<p class="cap">표 5. 모델별 셀 하나의 학습 시간(초, 10 fold 합). Suzuki 11종은 one-hot 세트, 나머지는 입체 4 + 전자 4 세트입니다. Stack은 세 모델의 예측 평균이라 시간이 0입니다.</p>

<h1 class="sec">5. 한계와 다음 단계</h1>
{note(LIMITS)}

<h1 class="sec">6. 부록</h1>
<details class="arch"><summary>전체 결과 표 138셀 펼치기</summary>
{full_table()}
<p class="cap">표 6. feature_bench_master.csv 전체. lig_rho와 percond_rho는 leave-one-ligand-out에만 있습니다.</p>
</details>
"""

STYLE = f"""
@font-face{{font-family:'Inter';font-style:normal;font-weight:400 600;font-display:swap;
 src:url(data:font/woff2;base64,{FONT_B64}) format('woff2')}}
:root{{--color-void:#000000;--color-fog-border:#e5e7eb;--color-chalk:#f1f1f1;
 --color-graphite:#555555;--color-canvas:#ffffff;
 --font:'Inter',ui-sans-serif,system-ui,-apple-system,'Apple SD Gothic Neo','Noto Sans KR',sans-serif;
 --text-caption:14px;--text-body:16px;--text-heading:22px;--text-heading-lg:28px;--text-display:44px;
 --radius-cards:6px;--radius-full:9999px;--page-max-width:1100px}}
*{{box-sizing:border-box}} *{{scrollbar-width:none}} *::-webkit-scrollbar{{display:none}}
html,body{{margin:0;background:var(--color-canvas);color:var(--color-void)}}
body{{font-family:var(--font);font-size:var(--text-body);line-height:1.6;font-feature-settings:"calt","liga";
 word-break:keep-all;line-break:strict;overflow-wrap:break-word}}
nav{{position:sticky;top:0;z-index:5;height:64px;background:var(--color-canvas);display:flex;align-items:center;
 justify-content:space-between;padding:0 24px;box-shadow:0 1px 0 var(--color-fog-border)}}
nav .brand{{font-weight:600;font-size:15px}}
nav .meta{{font-size:var(--text-caption);color:var(--color-graphite)}}
.wrap{{max-width:var(--page-max-width);margin:0 auto;padding:0 32px}}
.hero{{padding:80px 0 40px}}
.hero h1{{font-size:var(--text-display);line-height:1.16;letter-spacing:-0.03em;font-weight:600;margin:0 0 20px;max-width:100%;text-wrap:balance}}
.hero .lead{{font-size:18px;color:var(--color-graphite);margin:0}}
h1.sec{{font-size:var(--text-heading-lg);line-height:1.21;letter-spacing:-0.01em;font-weight:600;margin:80px 0 24px;
 padding-top:32px;box-shadow:0 -1px 0 var(--color-fog-border);text-wrap:balance}}
h2{{font-size:var(--text-heading);line-height:1.26;font-weight:600;margin:48px 0 14px;text-wrap:balance}}
p{{margin:14px 0}}
.note{{background:#f7f7f8;border-radius:var(--radius-cards);padding:24px 28px;margin:20px 0 28px;font-size:15.5px;line-height:1.62}}
.cap{{font-size:var(--text-caption);color:var(--color-graphite);line-height:1.6;margin:8px 0 20px}}
ul{{margin:6px 0 4px;padding-left:20px}} li{{margin:6px 0}} ul ul{{font-size:.96em;margin-top:4px}} ul ul li{{margin:4px 0;color:#333}}
.tbl{{margin:12px 0 8px}}
table{{border-collapse:collapse;width:100%;font-size:14px;line-height:1.45}}
th,td{{padding:8px 10px;text-align:center;vertical-align:middle;box-shadow:inset 0 -1px 0 var(--color-fog-border)}}
th{{font-weight:600;font-size:13.5px;color:var(--color-void)}}
th:first-child,td:first-child{{text-align:left}}
.fig{{margin:16px 0 8px}} .fig svg,.fig img{{max-width:100%;height:auto;display:block;margin:0 auto}}
.fig svg{{max-width:min(100%,860px)}} .fig img{{max-width:min(100%,1000px)}}
svg text{{font-family:Arial,Helvetica,"Liberation Sans","Nimbus Sans",sans-serif !important}}
[hidden]{{display:none !important}}
.figbox{{margin:18px 0 0}}
.ctrls{{display:flex;flex-wrap:wrap;gap:18px;align-items:center;margin:0 0 8px}}
.btngrp{{display:flex;align-items:center;gap:6px;flex-wrap:wrap}}
.glab{{font-size:13.5px;color:var(--color-graphite);margin-right:2px}}
.btngrp button{{font:inherit;font-size:13.5px;padding:5px 12px;border-radius:var(--radius-full);border:0;
 background:var(--color-chalk);color:var(--color-void);cursor:pointer}}
.btngrp button:hover{{background:#e4e4e6}}
.btngrp button.on{{background:var(--color-void);color:#fff}}
details.arch{{margin:12px 0 0}}
details.arch>summary{{cursor:pointer;font-weight:600;padding:12px 0;font-size:15.5px}}
sub{{font-size:0.72em;line-height:0}}
footer{{margin:96px 0 48px;padding-top:24px;box-shadow:0 -1px 0 var(--color-fog-border);font-size:var(--text-caption);color:var(--color-graphite)}}
@media (max-width:760px){{.wrap{{padding:0 18px}} .hero{{padding:48px 0 24px}} .hero h1{{font-size:32px}} table{{font-size:13.5px}} th,td{{padding:6px 6px}}}}
"""

SCRIPT = """
function fvSync(box){
  var key = Array.prototype.map.call(box.querySelectorAll('.btngrp'), function(g){
    var b = g.querySelector('button.on') || g.querySelector('button');
    return b.getAttribute('data-v');
  }).join('|');
  Array.prototype.forEach.call(box.querySelectorAll('.fv'), function(d){
    d.hidden = (d.getAttribute('data-key') !== key);
  });
}
document.addEventListener('click', function(e){
  var b = e.target.closest ? e.target.closest('.btngrp button') : null;
  if(!b) return;
  var g = b.parentNode;
  Array.prototype.forEach.call(g.querySelectorAll('button'), function(x){ x.classList.remove('on'); });
  b.classList.add('on');
  fvSync(g.parentNode.parentNode);
});
Array.prototype.forEach.call(document.querySelectorAll('.figbox'), fvSync);
"""


def glyph_pool():
    if not GLYPHS:
        return ""
    return f"<svg width='0' height='0' aria-hidden='true' style='position:absolute'><defs>{''.join(GLYPHS[k] for k in sorted(GLYPHS))}</defs></svg>"


html = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Feature bench, Suzuki and Buchwald</title>
<style>{STYLE}</style></head>
<body>
{glyph_pool()}
<nav><div><span class="brand">165 SDL</span> <span class="meta">002 feature bench</span></div><div class="meta">2026-09-09</div></nav>
<div class="wrap">
<div class="hero">
<h1>수율 데이터셋에서의 리간드 feature와 모델 벤치마크</h1>
<p class="lead">flexcat에서 세운 프로토콜을 Suzuki(5280행, 리간드 11종)와 Buchwald(3955행, 리간드 4종)에 그대로 적용해, 본 리간드와 안 본 리간드에서 수율 순위를 가장 잘 맞히는 feature 세트와 모델을 찾은 1단계 결과입니다. 모든 수치는 results/feature_bench_master.csv에서 다시 계산했습니다.</p>
</div>
{BODY}
<footer>scripts/build_report.py가 results/feature_bench_master.csv, results/preds/, figures/에서 생성했습니다. 그림은 scripts/fig_*.py, 리간드 렌더는 scripts/render_ligands.sh입니다. API 지출 없음, RunPod 약 1.9달러.</footer>
</div>
<script>{SCRIPT}</script>
</body></html>
"""
OUT_HTML.write_text(html)
print("wrote", OUT_HTML, f"{OUT_HTML.stat().st_size / 1e6:.2f} MB")
