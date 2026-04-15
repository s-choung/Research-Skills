---
name: youtube2mp4
description: Use when the user provides a YouTube URL and wants to download the video as an mp4 file (optionally audio-only, resolution-capped, or time-trimmed). Triggers - /youtube2mp4, youtube download, 유튜브 다운로드, mp4 다운, yt-dlp download, 영상 저장.
---

# YouTube to MP4

YouTube URL에서 mp4 영상을 다운로드한다. 해상도 제한, 구간 자르기, 오디오 전용 지원.

## Usage

```
/youtube2mp4 <youtube_url> [options]
```

## Execution

```bash
python3 ~/.claude/skills/youtube2mp4/yt2mp4.py <URL> [options]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--res N` | `1080` | 최대 해상도 (480/720/1080/2160) |
| `--audio` | - | 오디오만 (m4a) |
| `--start HH:MM:SS` | - | 시작 시각 |
| `--end HH:MM:SS` | - | 종료 시각 |
| `-o PATH` | `.` | 출력 디렉토리 |
| `--name NAME` | auto | 출력 파일명 (확장자 제외) |

### Examples

```bash
python3 ~/.claude/skills/youtube2mp4/yt2mp4.py "https://youtu.be/nDL3Ch7Nz8c"
python3 ~/.claude/skills/youtube2mp4/yt2mp4.py "<url>" --res 720 -o ./clips
python3 ~/.claude/skills/youtube2mp4/yt2mp4.py "<url>" --start 00:30 --end 01:45
python3 ~/.claude/skills/youtube2mp4/yt2mp4.py "<url>" --audio
```

## Output

기본 파일명: `<title> [<video_id>].mp4` (또는 `--name` 지정 시 해당 이름).

## Requirements

- `yt-dlp` (`brew install yt-dlp`)
- `ffmpeg` (`brew install ffmpeg`) - merge / section cut용
