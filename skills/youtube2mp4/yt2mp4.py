#!/usr/bin/env python3
"""
yt2mp4: YouTube URL에서 mp4 영상을 다운로드한다.

Usage:
    python yt2mp4.py <youtube_url> [--res 1080] [--audio] [--start 00:30] [--end 01:20] [-o ./path]
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def extract_video_id(url: str) -> str:
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    raise ValueError(f"유효한 YouTube URL이 아닙니다: {url}")


def check_requirements():
    missing = [t for t in ("yt-dlp", "ffmpeg") if shutil.which(t) is None]
    if missing:
        print(f"[ERROR] 필수 도구 없음: {', '.join(missing)}")
        print("        brew install " + " ".join(missing))
        sys.exit(1)


def build_format(res: int, audio_only: bool) -> str:
    if audio_only:
        return "bestaudio[ext=m4a]/bestaudio"
    return (
        f"bv*[height<={res}][ext=mp4]+ba[ext=m4a]/"
        f"b[height<={res}][ext=mp4]/"
        f"bv*[height<={res}]+ba/"
        f"b[height<={res}]/best"
    )


def download(url: str, output_dir: Path, res: int, audio_only: bool,
             start: str | None, end: str | None, filename: str | None) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    if filename:
        out_template = str(output_dir / f"{filename}.%(ext)s")
    else:
        out_template = str(output_dir / "%(title).80s [%(id)s].%(ext)s")

    cmd = [
        "yt-dlp",
        "-f", build_format(res, audio_only),
        "--merge-output-format", "m4a" if audio_only else "mp4",
        "-o", out_template,
        "--no-playlist",
        "--no-mtime",
    ]

    if start or end:
        section = f"*{start or '0'}-{end or 'inf'}"
        cmd += ["--download-sections", section, "--force-keyframes-at-cuts"]

    if audio_only:
        cmd += ["-x", "--audio-format", "m4a"]

    cmd += ["--print", "after_move:filepath", url]

    print(f"[yt2mp4] downloading: {url}")
    print(f"         format: {'audio' if audio_only else f'mp4 <= {res}p'}")
    if start or end:
        print(f"         section: {start or '0'} -> {end or 'end'}")
    print(f"         output: {output_dir}")
    print()

    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        print(f"[ERROR] yt-dlp 실패 (exit {result.returncode})")
        sys.exit(result.returncode)

    return output_dir


def main():
    parser = argparse.ArgumentParser(description="YouTube URL에서 mp4 다운로드")
    parser.add_argument("url", help="YouTube URL 또는 video ID")
    parser.add_argument("--res", type=int, default=1080,
                        help="최대 해상도 (default: 1080)")
    parser.add_argument("--audio", action="store_true",
                        help="오디오만 (m4a)")
    parser.add_argument("--start", type=str, default=None,
                        help="시작 시각 (e.g. 00:30 or 30)")
    parser.add_argument("--end", type=str, default=None,
                        help="종료 시각 (e.g. 01:20 or 80)")
    parser.add_argument("-o", "--output-dir", type=str, default=".",
                        help="출력 디렉토리 (default: 현재 디렉토리)")
    parser.add_argument("--name", type=str, default=None,
                        help="출력 파일명 (확장자 제외)")

    args = parser.parse_args()
    check_requirements()

    video_id = extract_video_id(args.url)
    canonical = f"https://www.youtube.com/watch?v={video_id}"

    out_dir = download(
        url=canonical,
        output_dir=Path(args.output_dir).expanduser().resolve(),
        res=args.res,
        audio_only=args.audio,
        start=args.start,
        end=args.end,
        filename=args.name,
    )

    print()
    print(f"[DONE] {out_dir}")


if __name__ == "__main__":
    main()
