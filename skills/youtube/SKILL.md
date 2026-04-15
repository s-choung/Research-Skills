---
name: youtube
description: Use when the user provides a YouTube URL and wants to extract transcript content as markdown. Triggers - /youtube, YouTube transcript, 유튜브 자막, transcript 추출, 유튜브 내용 가져와.
---

# YouTube Transcript + Smart Frame Capture

YouTube URL에서 transcript(자막), 메타데이터, 주요 장면 스크린샷을 추출하여 Markdown 파일로 저장한다.

## Usage

```
/youtube <youtube_url>
```

## Execution

```bash
python3 ~/.claude/skills/youtube/fetch_transcript.py <URL> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--lang ko,en` | 언어 우선순위 (default: ko,en) |
| `-o ./path` | 출력 디렉토리 |
| `--frames 8` | 캡처할 프레임 수 (0=none, default: 0) |
| `--cookies cookies.txt` | 로그인 필요/연령 제한 영상용 쿠키 파일 |
| `--proxy socks5://...` | IP 차단 우회용 프록시 |

### Smart Frame Capture (`--frames N`)

타임스탬프 자동 선택 전략 (우선순위):

1. **Heatmap peaks** — YouTube "가장 많이 재생된 구간" 데이터에서 peak 지점 캡처
2. **Chapter starts** — heatmap 없으면 챕터 시작점에서 캡처
3. **Uniform interval** — 둘 다 없으면 균등 분할

## Output

```
output/<video_id>_<title>/
├── transcript.md      # 메타데이터 + Key Frames + 타임스탬프 transcript
├── metadata.json      # 제목, 채널, 조회수, 설명, 태그 등
└── frames/            # (--frames 사용 시) 캡처된 주요 장면 이미지
    ├── frame_000_0020.jpg
    └── ...
```

## Requirements

- `yt-dlp` (`brew install yt-dlp`)
- `ffmpeg` (`brew install ffmpeg`) — 프레임 캡처용
- `youtube-transcript-api` (자동 설치됨)

## After Extraction

transcript.md가 생성되면 사용자에게 경로를 알려주고, 내용에 대해 질문이 있는지 물어본다.
