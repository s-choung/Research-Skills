---
name: pptx-too-heavy
description: PPTX 파일의 무거운 이미지를 분석하여 용량순 3열 그리드 HTML 리포트를 생성. 슬라이드별 미디어 매핑, EMF/TIF 변환, 해상도/용량 표시. Triggers - /pptx-too-heavy, "pptx 무거워", "pptx 용량", "슬라이드 이미지 분석", "heavy images", "pptx 이미지 크기", "발표자료 용량 줄이기", "pptx analyze images".
---

# PPTX Too Heavy

PPTX 파일 내 무거운 이미지를 찾아 시각적 HTML 리포트로 보여주는 스킬.

## 하는 일

1. PPTX를 zip으로 열어 모든 미디어 파일 크기 분석
2. 슬라이드별 미디어 매핑 (어떤 이미지가 어떤 슬라이드에 쓰이는지)
3. 큰 이미지 추출 (기본 2MB+)
4. EMF → PDF → PNG 변환 (LibreOffice + ImageMagick)
5. TIF → PNG 변환
6. 용량 내림차순 3열 그리드 다크모드 HTML 생성
7. 브라우저에서 열기

## 사용법

```bash
conda run -n base python ~/.claude/skills/pptx-too-heavy/scripts/analyze.py "<pptx_path>"
```

### 옵션

| 플래그 | 기본값 | 설명 |
|--------|--------|------|
| `--threshold` | `2.0` | 포함할 최소 MB |
| `--output` | `/tmp/pptx_heavy_<name>` | 출력 디렉토리 |

## 실행 예시

```bash
# 분석 + HTML 생성
conda run -n base python ~/.claude/skills/pptx-too-heavy/scripts/analyze.py "발표자료.pptx"

# 1MB 이상까지 포함
conda run -n base python ~/.claude/skills/pptx-too-heavy/scripts/analyze.py "발표자료.pptx" --threshold 1

# 결과 열기
open /tmp/pptx_heavy_발표자료/heavy_images.html
```

## 의존성

- `python-pptx`, `Pillow` (conda base에 설치됨)
- LibreOffice (EMF 변환용, `/Applications/LibreOffice.app`)
- ImageMagick `magick` (PDF→PNG 렌더링용)
- EMF 없으면 LibreOffice/ImageMagick 없어도 동작 (해당 이미지만 "미리보기 불가")

## HTML 출력 구조

- 다크모드 3열 그리드
- 각 카드: 썸네일, 파일명, 용량(색상 코딩), 해상도, 사용 슬라이드+텍스트
- 용량 색상: 빨강(5MB+), 주황(3-5MB), 노랑(2-3MB)
- EMF/TIF 등 특수 포맷은 배지 표시

## Claude 워크플로

1. 유저가 PPTX 경로를 주면 `conda run -n base python` 으로 스크립트 실행
2. 완료 후 `open <html_path>` 로 브라우저에서 열기
3. 유저가 어떤 이미지를 지울지/줄일지 결정하면 후속 작업 진행
