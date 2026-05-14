# pptx-too-heavy

PPTX 파일 내 무거운 이미지를 찾아 용량순 3열 그리드 HTML 리포트로 보여주는 스킬.

## What it does

1. PPTX를 zip으로 열어 모든 미디어 파일 크기 분석
2. 슬라이드별 미디어 매핑 (어떤 이미지가 어떤 슬라이드에 쓰이는지)
3. 큰 이미지 추출 (기본 2MB+), EMF/TIF → PNG 변환
4. 용량 내림차순 3열 그리드 다크모드 HTML 리포트 생성 + 브라우저 오픈

## Usage

```
/pptx-too-heavy presentation.pptx
```

Or natural language:
```
이 pptx 왜 이렇게 무거워? 이미지 분석해줘
```

## Dependencies

- `python-pptx`, `Pillow`
- EMF 변환: `brew install libreoffice imagemagick` (optional)

## File Structure

```
pptx-too-heavy/
├── SKILL.md
├── README.md
└── scripts/
    └── analyze.py
```
