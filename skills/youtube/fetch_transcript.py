#!/usr/bin/env python3
"""
YouTube transcript extractor + smart frame capture.

Transcript strategies:
1. youtube-transcript-api (primary) — no browser, no API key, bypasses most restrictions
2. yt-dlp subtitle extraction (fallback) — handles edge cases, supports cookies/proxy
3. Retry with backoff — handles rate limiting (429)
4. Cookie support — age-restricted / login-required videos
5. Proxy support — IP-based blocking workaround

Frame capture strategies (smart timestamp selection):
1. Heatmap peaks — YouTube "most replayed" data, captures at viewer attention peaks
2. Chapter starts — fallback when heatmap unavailable
3. Uniform interval — fallback when neither available
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


# --- Anti-blocking: retry with backoff ---

def retry_with_backoff(fn, max_retries=3, base_delay=2.0):
    """Retry a function with exponential backoff for rate limiting."""
    last_error = None
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            last_error = e
            err_str = str(e).lower()
            # Only retry on rate-limit or transient errors
            if "429" in err_str or "too many" in err_str or "rate" in err_str or "temporarily" in err_str:
                delay = base_delay * (2 ** attempt)
                print(f"  Rate limited, retrying in {delay:.0f}s... (attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
            else:
                raise
    raise last_error


# --- Dependency management ---

def ensure_transcript_api():
    """youtube-transcript-api가 없으면 자동 설치."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        return YouTubeTranscriptApi
    except ImportError:
        print("  Installing youtube-transcript-api...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user",
             "--break-system-packages", "-q", "youtube-transcript-api"],
            capture_output=True, text=True, timeout=60,
        )
        from youtube_transcript_api import YouTubeTranscriptApi
        return YouTubeTranscriptApi


# --- URL parsing ---

def extract_video_id(url: str) -> str:
    for p in [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]:
        m = re.search(p, url)
        if m:
            return m.group(1)
    raise ValueError(f"Invalid YouTube URL: {url}")


# --- Metadata ---

def get_metadata(video_id: str, cookies_file: str = None, proxy: str = None) -> dict:
    cmd = ["yt-dlp", "--dump-json", "--no-download",
           f"https://www.youtube.com/watch?v={video_id}"]
    if cookies_file:
        cmd.extend(["--cookies", cookies_file])
    if proxy:
        cmd.extend(["--proxy", proxy])

    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print(f"  Warning: metadata fetch failed", file=sys.stderr)
        return {"title": video_id, "duration": 0}
    return json.loads(r.stdout)


# --- Transcript extraction: Method 1 (youtube-transcript-api) ---

def get_transcript_via_api(video_id: str, langs: list[str], cookies_file: str = None, proxy: str = None):
    """Primary method: youtube-transcript-api. Most reliable for public videos."""
    YTApi = ensure_transcript_api()
    api = YTApi()

    # Build kwargs for cookie/proxy support (if the library version supports it)
    kwargs = {}
    if cookies_file:
        try:
            # youtube-transcript-api >= 0.6.0 supports cookies
            kwargs["cookies"] = cookies_file
        except Exception:
            pass
    if proxy:
        try:
            kwargs["proxies"] = {"https": proxy, "http": proxy}
        except Exception:
            pass

    def _fetch():
        try:
            transcript = api.fetch(video_id, languages=langs, **kwargs)
            return [{"start": s.start, "text": s.text.strip()} for s in transcript]
        except Exception as e:
            if "no transcripts" not in str(e).lower():
                raise
            # Try without language filter
            transcript = api.fetch(video_id, **kwargs)
            return [{"start": s.start, "text": s.text.strip()} for s in transcript]

    try:
        return retry_with_backoff(_fetch)
    except Exception as e:
        print(f"  API method failed: {e}")
        return []


# --- Transcript extraction: Method 2 (yt-dlp subtitles) ---

def get_transcript_via_ytdlp(video_id: str, langs: list[str], cookies_file: str = None, proxy: str = None):
    """Fallback: yt-dlp subtitle download. Better for age-restricted/login-required videos."""
    url = f"https://www.youtube.com/watch?v={video_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        lang_str = ",".join(langs)
        cmd = [
            "yt-dlp",
            "--write-auto-sub", "--write-sub",
            "--sub-lang", lang_str,
            "--skip-download",
            "--convert-subs", "srt",
            "-o", f"{tmpdir}/%(id)s",
            url,
        ]
        if cookies_file:
            cmd.extend(["--cookies", cookies_file])
        if proxy:
            cmd.extend(["--proxy", proxy])

        def _fetch():
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            # Check for subtitle files in language priority order
            for lang in langs:
                srt = Path(tmpdir) / f"{video_id}.{lang}.srt"
                if srt.exists():
                    return parse_srt(srt)
            for f in Path(tmpdir).glob(f"{video_id}*.srt"):
                return parse_srt(f)
            if "429" in r.stderr or "Too Many" in r.stderr:
                raise Exception("Rate limited (429)")
            return []

        try:
            return retry_with_backoff(_fetch)
        except Exception as e:
            print(f"  yt-dlp method failed: {e}")
            return []


# --- SRT parsing ---

def parse_srt(path: Path) -> list[dict]:
    content = path.read_text(encoding="utf-8", errors="replace")
    entries = []
    seen = set()
    for block in re.split(r"\n\s*\n", content.strip()):
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        time_match = re.match(r"(\d{2}):(\d{2}):(\d{2})[,.](\d+)", lines[1])
        if not time_match:
            continue
        h, m, s = int(time_match.group(1)), int(time_match.group(2)), int(time_match.group(3))
        seconds = h * 3600 + m * 60 + s
        text = " ".join(lines[2:])
        text = re.sub(r"<[^>]+>", "", text).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        entries.append({"start": seconds, "text": text})
    return entries


# --- Formatting ---

def format_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"


def sanitize(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    return re.sub(r"\s+", "_", name.strip())[:80]


# --- Smart frame capture ---

def pick_timestamps(meta: dict, num_frames: int = 8) -> list[dict]:
    """Pick best timestamps for frame capture using heatmap > chapters > uniform."""
    duration = meta.get("duration", 0)
    if duration <= 0:
        return []

    heatmap = meta.get("heatmap")
    chapters = meta.get("chapters")

    # Strategy 1: Heatmap peaks (most replayed segments)
    if heatmap:
        # Find local peaks: points higher than both neighbors
        peaks = []
        for i in range(1, len(heatmap) - 1):
            v = heatmap[i]["value"]
            if v > heatmap[i-1]["value"] and v > heatmap[i+1]["value"]:
                mid = (heatmap[i]["start_time"] + heatmap[i]["end_time"]) / 2
                peaks.append({"time": mid, "value": v, "source": "heatmap_peak"})

        if not peaks:
            # No local peaks — just take top N by value
            sorted_hm = sorted(heatmap, key=lambda x: x["value"], reverse=True)
            for h in sorted_hm[:num_frames]:
                mid = (h["start_time"] + h["end_time"]) / 2
                peaks.append({"time": mid, "value": h["value"], "source": "heatmap_top"})

        # Sort by value descending, take top N
        peaks.sort(key=lambda x: x["value"], reverse=True)
        selected = peaks[:num_frames]
        # Sort by time for sequential capture
        selected.sort(key=lambda x: x["time"])
        return selected

    # Strategy 2: Chapter start points
    if chapters and len(chapters) > 1:
        selected = []
        # Skip very short chapters, pick chapter starts + a bit offset (5s in)
        for ch in chapters:
            t = ch["start_time"] + 5  # 5s after chapter start for settled frame
            if t < duration:
                selected.append({
                    "time": t,
                    "value": 0,
                    "source": f"chapter: {ch['title']}",
                })
        # If too many, sample uniformly
        if len(selected) > num_frames:
            step = len(selected) / num_frames
            selected = [selected[int(i * step)] for i in range(num_frames)]
        return selected

    # Strategy 3: Uniform interval
    margin = min(10, duration * 0.03)
    interval = (duration - 2 * margin) / max(num_frames - 1, 1)
    return [
        {"time": margin + i * interval, "value": 0, "source": "uniform"}
        for i in range(num_frames)
    ]


def capture_frames(video_id: str, timestamps: list[dict], output_dir: Path,
                   cookies_file: str = None, proxy: str = None) -> list[dict]:
    """Download low-quality video and extract frames at given timestamps."""
    if not timestamps:
        return []

    frames_dir = output_dir / "frames"
    frames_dir.mkdir(exist_ok=True)

    url = f"https://www.youtube.com/watch?v={video_id}"
    tmp_video = output_dir / "_tmp_video.mp4"

    # Step 1: Download low-quality video
    if not tmp_video.exists():
        print("  Downloading low-res video...")
        dl_cmd = [
            "yt-dlp",
            "-f", "bv*[height<=480][ext=mp4]/bv*[height<=480]/worst[ext=mp4]/worst",
            "-o", str(tmp_video),
            "--no-playlist", "--quiet", "--no-warnings",
            url,
        ]
        if cookies_file:
            dl_cmd.extend(["--cookies", cookies_file])
        if proxy:
            dl_cmd.extend(["--proxy", proxy])

        dl_result = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=300)
        if dl_result.returncode != 0 or not tmp_video.exists():
            downloaded = list(output_dir.glob("_tmp_video.*"))
            if downloaded:
                tmp_video = downloaded[0]
            else:
                print(f"  Warning: video download failed")
                return []

    # Step 2: Extract frames with ffmpeg
    captured = []
    for i, ts_info in enumerate(timestamps):
        ts = ts_info["time"]
        ts_str = format_ts(ts).replace(":", "")
        output_path = frames_dir / f"frame_{i:03d}_{ts_str}.jpg"

        if output_path.exists():
            captured.append({**ts_info, "path": output_path})
            continue

        ff_cmd = [
            "ffmpeg", "-ss", str(ts),
            "-i", str(tmp_video),
            "-frames:v", "1", "-q:v", "2", "-y",
            str(output_path),
        ]
        try:
            r = subprocess.run(ff_cmd, capture_output=True, text=True, timeout=30)
            if r.returncode == 0 and output_path.exists():
                captured.append({**ts_info, "path": output_path})
                print(f"  Frame {i+1}/{len(timestamps)} @ {format_ts(ts)} ({ts_info['source']})")
            else:
                print(f"  Warning: frame {i+1} capture failed")
        except Exception as e:
            print(f"  Warning: frame {i+1} error: {e}")

    # Clean up temp video
    try:
        tmp_video.unlink()
    except Exception:
        pass

    return captured


# --- Main ---

def main():
    import argparse

    parser = argparse.ArgumentParser(description="YouTube transcript extractor")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--output-dir", "-o", help="Output directory")
    parser.add_argument("--lang", default="ko,en", help="Languages, comma-separated (default: ko,en)")
    parser.add_argument("--cookies", help="Path to cookies.txt (for age-restricted/login-required videos)")
    parser.add_argument("--proxy", help="Proxy URL (e.g., socks5://127.0.0.1:1080)")
    parser.add_argument("--retries", type=int, default=3, help="Max retries on rate limit (default: 3)")
    parser.add_argument("--frames", type=int, default=0,
                        help="Number of frames to capture (0=none, default: 0). "
                             "Uses heatmap peaks > chapter starts > uniform interval.")
    parser.add_argument("--no-frames", action="store_true", help="Explicitly skip frame capture")

    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    langs = args.lang.split(",")

    # Metadata
    print(f"Fetching metadata for {video_id}...")
    meta = get_metadata(video_id, args.cookies, args.proxy)
    title = meta.get("title", video_id)
    channel = meta.get("channel", meta.get("uploader", "Unknown"))
    duration = meta.get("duration", 0)
    upload_date = meta.get("upload_date", "")
    print(f"  Title: {title}")
    print(f"  Duration: {format_ts(duration)}")

    # Output dir
    if args.output_dir:
        out = Path(args.output_dir)
    else:
        out = Path.cwd() / "output" / f"{video_id}_{sanitize(title)}"
    out.mkdir(parents=True, exist_ok=True)

    # Transcript with fallback chain
    print(f"Fetching transcript ({args.lang})...")

    # Method 1: youtube-transcript-api (fastest, most reliable)
    entries = get_transcript_via_api(video_id, langs, args.cookies, args.proxy)

    # Method 2: yt-dlp subtitle extraction (handles more edge cases)
    if not entries:
        print("  Trying yt-dlp fallback...")
        entries = get_transcript_via_ytdlp(video_id, langs, args.cookies, args.proxy)

    if entries:
        print(f"  Found {len(entries)} entries")
    else:
        print("  ERROR: Could not fetch transcript from any source.")
        print("  Tips:")
        print("    - Use --cookies cookies.txt for login-required videos")
        print("    - Use --proxy socks5://... to bypass IP blocks")
        print("    - Check if the video has subtitles enabled")

    # Frame capture
    captured_frames = []
    if args.frames > 0 and not args.no_frames:
        print(f"Selecting {args.frames} frame timestamps...")
        timestamps = pick_timestamps(meta, num_frames=args.frames)
        if timestamps:
            src = timestamps[0]["source"].split(":")[0]
            print(f"  Strategy: {src} ({len(timestamps)} points)")
            print(f"Capturing frames...")
            captured_frames = capture_frames(
                video_id, timestamps, out, args.cookies, args.proxy
            )
            print(f"  {len(captured_frames)} frames captured")

    # Build Markdown
    lines = [f"# {title}\n"]
    lines.append(f"- **Channel**: {channel}")
    lines.append(f"- **URL**: https://www.youtube.com/watch?v={video_id}")
    lines.append(f"- **Duration**: {format_ts(duration)}")
    if upload_date and len(upload_date) == 8:
        lines.append(f"- **Upload Date**: {upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}")
    lines.append("")

    # Key frames section
    if captured_frames:
        lines.append("## Key Frames\n")
        for fr in captured_frames:
            ts_label = format_ts(fr["time"])
            fname = Path(fr["path"]).name
            source_label = fr["source"]
            lines.append(f"### @ {ts_label} — {source_label}")
            lines.append(f"![{ts_label}](frames/{fname})\n")
        lines.append("")

    lines.append("## Transcript\n")
    if entries:
        for e in entries:
            lines.append(f"**[{format_ts(e['start'])}]** {e['text']}\n")
    else:
        lines.append("*Transcript not available.*\n")

    md_path = out / "transcript.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    # Save metadata JSON
    meta_save = {
        k: meta.get(k)
        for k in ["title", "channel", "uploader", "duration", "upload_date",
                   "view_count", "like_count", "description", "tags", "categories"]
        if meta.get(k) is not None
    }
    meta_save["video_id"] = video_id
    meta_save["url"] = f"https://www.youtube.com/watch?v={video_id}"
    if captured_frames:
        meta_save["captured_frames"] = [
            {"time": fr["time"], "source": fr["source"], "file": Path(fr["path"]).name}
            for fr in captured_frames
        ]
    (out / "metadata.json").write_text(
        json.dumps(meta_save, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\nDone!")
    print(f"  {md_path}")
    print(f"  {out / 'metadata.json'}")
    print(f"  {len(entries)} transcript entries")
    if captured_frames:
        print(f"  {len(captured_frames)} frames in {out}/frames/")


if __name__ == "__main__":
    main()
