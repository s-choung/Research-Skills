---
name: ovito-atom-render
description: Render atomic structures with OVITO's CPU ray tracers (OSPRay, Tachyon) on the ccel-mace server. Use for large structures (10k-1M atoms) where Blender EEVEE is too slow or the GPU is unavailable, and for nanoparticle, slab, or MD snapshot panels that need real shadows on a transparent background. Triggers - ovito 렌더, ospray, tachyon, 나노입자 렌더, 큰 구조 렌더, 원자 렌더 서버, 투명배경 구조 그림, 확대 서브피규어, zoom 렌더, matte 스타일, studio 스타일.
---

# ovito-atom-render

Companion to `blender-atom-render`. Blender stays the tool for small systems
and for per-element materials; OVITO is the tool for large structures and for
anything that has to run on the server.

## 결론 먼저

- **렌더는 ccel-mace에서 돈다. Mac은 쓰지 않는다.** Mac은 꺼질 수 있고 GPU도 약하다.
- **ccel-mace에 GPU가 없다.** Blender EEVEE는 llvmpipe 소프트웨어 래스터라이저로 떨어져
  100k 원자에서 32 samples 중 1개에 5분을 넘긴다. 버전을 올려도 같다. 서버에서는
  CPU 엔진(OVITO OSPRay, OVITO Tachyon, Blender Cycles)만 쓴다.
- **배경은 항상 투명이다.** `render_image(alpha=True)`로 뽑으면 RGBA로 저장된다.
  뷰어나 비교 페이지에서 검게 보이는 것은 그 페이지가 깐 배경이지 렌더가 아니다.
- 100k 원자, 1600 px 기준 실측: OSPRay 약 25초, Tachyon 약 21초, Blender Cycles 128 약 76초.

## 환경

| 항목 | 값 |
|---|---|
| 서버 | `ssh ccel-mace` (16 코어, RAM 62 GB, GPU 없음) |
| OVITO | `~/miniconda3/envs/ovito/bin/python` (OVITO 3.13.1) |
| Blender | `~/blender-4.1.1-linux-x64/blender` (Cycles 폴백용) |
| 작업 폴더 | `~/nsa_render/` (`struct/`, `out/`) |
| 구현 | `figure_exp/01_scripts/render_ovito_options.py` |

OVITO 설치가 없으면:
`conda create -y -n ovito -c https://conda.ovito.org -c conda-forge ovito python=3.11`

## 고정 규격 (엔진과 무관하게 항상 같아야 하는 것)

이 다섯 가지가 흔들리면 같은 구조를 두 번 렌더할 때 그림이 달라진다.

- **카메라**: ortho, 바라보는 방향 `(-0.62, 0.62, -0.30)`. 프로젝트 표준 3/4 시점.
- **프레이밍**: `vp.fov = extent * MARGIN / 2`, `MARGIN = 1.05`.
  - autoframe 기본값 1.8은 물체를 화면의 55 %로 만들어 해상도를 절반 넘게 버린다.
    실제로 2000 px 렌더의 유효 영역이 1070 px였다.
- **원소 색과 반지름을 네 종 모두 코드에 명시한다.** 렌더러 기본값에 맡기지 않는다.
  Blender에서 Pt와 Co만 덮어쓰고 Ce와 O를 두었더니 Ce가 Jmol 기본색 `#FFFFC7`,
  즉 거의 흰색으로 나왔다.
- **simulation cell 선 끄기**: `pipeline.source.data.cell.vis.enabled = False`.
  안 끄면 검은 상자 모서리가 그림에 찍힌다.
- **비교용 렌더는 프레이밍 길이를 공유한다.** 0 ps와 100 ps, 두 계를 나란히 놓을
  때 구조마다 autoframe을 다시 잡으면 원자 크기가 달라져 비교가 성립하지 않는다.
  전 구조의 extent 최댓값을 구해 모두에 강제한다.

### 색과 반지름 (NSA 프로젝트 style 4, 2026-07-10 저자 승인)

```python
COLORS = {"Pt": (0.78, 0.79, 0.84), "Co": (0.94, 0.56, 0.63),
          "Ce": (0.98, 0.97, 0.72), "O":  (0.93, 0.16, 0.13)}
RADII  = {"Pt": 1.36, "Co": 1.26, "Ce": 1.83, "O": 0.74}
```

반지름은 공유결합 기준이다. 산화물에서 이온 반지름(O 1.38 > Ce 0.97)으로 바꾸면
표면이 완전히 다르게 보인다. 바꾸려면 저자 확인을 받고 프로젝트 전체에 같이 적용한다.

## 스타일 프리셋 (2026-09-20 저자 검토, 둘 다 채택)

저자가 이 둘을 골랐다. 그림 성격에 따라 그때그때 고른다.

### Matte — 기본값

무광, 반사 거의 없음. 교과서 삽화에 가깝고 원자 위치가 가장 잘 읽힌다.
본문 구조 패널과 확대 서브피규어의 기본값으로 쓴다.

```python
dict(engine="ospray", attrs=dict(
    samples_per_pixel=20, denoising_enabled=True,
    material_type="principled",              # 소문자. "Principled"는 거부된다
    principled_metalness=0.0, principled_roughness=0.85,
    principled_specular_brightness=0.05,
    sky_light_enabled=True, sky_brightness=1.8, sky_turbidity=6.0,
    ambient_brightness=0.25, ambient_light_enabled=True,
    direct_light_enabled=True, direct_light_intensity=0.8,
    direct_light_angular_diameter=0.6))      # 매우 부드러운 그림자
```

### Studio — 입체감이 필요할 때

좁은 광원이라 그림자가 또렷하고 입자 하나하나가 도드라진다. 나노입자 하나를
크게 보여 주는 표지 그림이나 발표 슬라이드에 쓴다.

```python
dict(engine="ospray", attrs=dict(
    samples_per_pixel=16, denoising_enabled=True,
    sky_light_enabled=False, ambient_light_enabled=True,
    ambient_brightness=0.55,
    direct_light_enabled=True, direct_light_intensity=1.6,
    direct_light_angular_diameter=0.08,      # 또렷한 그림자
    material_shininess=25.0, material_specular_brightness=0.12))
```

### 채택하지 않은 것 (다시 시도하지 말 것)

| 이름 | 설정 | 왜 뺐나 |
|---|---|---|
| Tachyon AO | AO 0.7, AA 6 | 균일하게 밝고 그림자가 얕다. 빠른 확인용으로만 |
| Principled metal | metalness 0.7 | 전 원소가 금속으로 보인다 |
| Glossy | roughness 0.22 | 플라스틱 모형 느낌 |
| Depth of field | aperture 0.9 | 초점 밖 원자 정보를 잃는다 |
| Tachyon AA 12 | | AA 6과 차이가 없고 시간만 1.6배 |
| Blender Cycles 512 | | 128과 구별되지 않고 시간이 3배 |

## 이 OVITO 빌드의 한계

- **재질을 원소별로 나눌 수 없다.** `principled_*`는 전 원소에 한꺼번에 걸린다.
  Pt만 금속, Ce는 무광이 필요하면 Blender Cycles로 간다.
- **윤곽선(outline) 속성이 없다.** `outlines_enabled` 등은 이 빌드에 존재하지 않는다.
- `material_type`은 소문자 `"standard"` 또는 `"principled"`만 받는다.
- 속성은 하나씩 `setattr`로 걸고 실패를 잡아 출력한다. 빌드마다 있는 속성이 달라서
  한 번에 넘기면 변종 전체가 죽는다.

## 파이프라인 작성 규칙

스타일링은 **pipeline source**에 건다. `compute()` 결과에 걸면
"shared by multiple owners" 오류가 나고, 렌더 시점까지 살아남지도 않는다.

```python
pipeline = import_file(str(xyz))
cell = pipeline.source.data.cell
if cell is not None:
    cell.vis.enabled = False
types = pipeline.source.data.particles_.particle_types_
for t in types.types:
    m = types.type_by_name_(t.name)      # 끝의 밑줄 = 수정 가능한 사본 요청
    m.color, m.radius = COLORS[t.name], RADII[t.name]
```

## 확대 서브피규어

`crop_anchor_zooms.py`가 Co 입자를 union-find로 묶고, Pt가 실제로 붙은 입자만
골라 구형으로 잘라낸다. 자른 조각은 그대로 같은 렌더 스크립트에 넣으면 된다.

- Pt가 Co에 붙었다고 보는 기준 `Pt-Co <= 3.2 A`, 같은 Co 입자로 묶는 기준 `Co-Co <= 3.0 A`.
- 반경 16 Å이면 Co 입자 하나와 그 주변 CeO<sub>2</sub>가 함께 들어온다.
- 확대 조각은 원자 수가 적어 프레이밍이 커지므로, 본체 그림과 원자 크기를 맞추려면
  본체와 같은 `MARGIN`을 쓰되 해상도를 올린다(본체 1600, 확대 1200 정도).

## 구조 정리 (렌더 전에)

표면에 점처럼 박힌 원자는 relax 부족이 아니라 **잉여 원자**인 경우가 많다.
builder의 stoichiometric trim이 양이온 이웃 하나짜리 O를 남긴다. 이런 원자는
아무리 relax해도 사라지지 않는다. 위치가 틀린 것이 아니라 있으면 안 되는 원자다.

- `trim_loose_surface_O.py`: 양이온 이웃이 `MIN_CN` 미만인 O를 지운다.
  NSA 18 nm 입자에서 1,940개가 제거되어 표면이 정리됐다. 초 단위로 끝난다.
- 그래도 거슬리면 그때 shell relax를 건다. 100k 원자 전체는 CPU MLIP로 못 돌리므로
  표면 2.5 Å만 움직이고 경계 7 Å은 고정, 내부는 계산에서 제거한다
  (`shell_relax_run.py`). NequIP-OAM-S 기준 force call 35초, 600 step에 6시간이다.
- **GAFF는 쓸 수 없다.** 유기분자용이라 Ce, Co, Pt 원자 타입이 없다. 같은 비용대의
  대안은 세리아용 Buckingham 퍼텐셜(Gotte, Minervini-Grimes)을 LAMMPS로 돌리는 것이다.

## 실행

```bash
scp render_ovito_options.py ccel-mace:~/nsa_render/
ssh ccel-mace "setsid nohup env R_RES=1600 \
  ~/miniconda3/envs/ovito/bin/python ~/nsa_render/render_ovito_options.py \
  ~/nsa_render/struct/<in>.xyz ~/nsa_render/out <tag> --variants=matte \
  > ~/nsa_render/out/render.log 2>&1 < /dev/null &"
```

- 긴 렌더는 `setsid nohup`으로 띄우고 바로 턴을 끝낸다. ssh 세션이 끊겨도 산다.
- 여러 구조를 돌릴 때는 서버에서 순차 루프로 돌린다. OVITO는 프로세스당 하나만.
- 결과는 `scp`로 받아 `Read`로 눈으로 확인한다. audit 스크립트가 대신해 주지 않는다.

## 관련

- `blender-atom-render` — 작은 계, 원소별 재질이 필요한 경우
- `figure_construction` — 렌더 PNG를 논문 패널에 넣을 때의 규칙
- `matplotlib-scientific-nsa` — NSA 프로젝트 색 규약
