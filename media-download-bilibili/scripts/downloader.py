import json
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .utils import ensure_video_dir, sanitize_filename

logger = logging.getLogger("bili")


@dataclass
class VideoResult:
    bv_id: str
    title: str
    filepath: Path
    page_num: int | None = None


@dataclass
class DownloadOpts:
    cookies: str | None = None
    cookies_file: str | None = None
    all_pages: bool = False
    max_count: int = 0
    dry_run: bool = False
    verbose: bool = False


def _build_ytdlp_cmd(url: str, output_template: str, opts: DownloadOpts) -> list[str]:
    cmd = [
        "yt-dlp",
        "-o", output_template,
        "--encoding", "utf-8",
        "--merge-output-format", "mp4",
        "--print", "after_move:%(filepath)s",
    ]
    if opts.all_pages:
        cmd.append("--yes-playlist")
    else:
        cmd.append("--no-playlist")

    if opts.max_count > 0:
        cmd.extend(["--playlist-end", str(opts.max_count)])

    if opts.cookies:
        cmd.extend(["--cookies-from-browser", opts.cookies])
    elif opts.cookies_file:
        cmd.extend(["--cookies", opts.cookies_file])

    cmd.append(url)
    return cmd


def _parse_videos_from_stdout(stdout: str, output_dir: Path) -> list[VideoResult]:
    results = []
    for line in stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        filepath = Path(line)
        if not filepath.exists():
            continue
        # extract bv_id and title from filename pattern: {bv_id}_{title}.ext
        stem = filepath.stem
        parts = stem.split("_", 1)
        bv_id = parts[0] if parts else stem
        title = parts[1] if len(parts) > 1 else stem
        results.append(VideoResult(
            bv_id=bv_id,
            title=title,
            filepath=filepath,
        ))
    return results


def dry_run_query(url: str, opts: DownloadOpts) -> list[dict]:
    cmd = ["yt-dlp", "--dump-json", "--flat-playlist"]
    if opts.cookies:
        cmd.extend(["--cookies-from-browser", opts.cookies])
    elif opts.cookies_file:
        cmd.extend(["--cookies", opts.cookies_file])
    if opts.max_count > 0:
        cmd.extend(["--playlist-end", str(opts.max_count)])
    cmd.append(url)

    logger.info("Dry-run query: %s", " ".join(cmd))
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error("Failed to query video info: %s", e.stderr[:500] if e.stderr else "")
        return []

    entries = []
    for line in result.stdout.strip().splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def download(url: str, output_dir: str | Path, opts: DownloadOpts) -> list[VideoResult]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_template = str(output_dir / "%(id)s_%(title)s.%(ext)s")
    cmd = _build_ytdlp_cmd(url, output_template, opts)

    logger.info("Download command: %s", " ".join(cmd))
    print(f"[DL] 开始下载: {url}")
    print(f"[DIR] 输出目录: {output_dir}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=not opts.verbose,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error("Download failed: %s", e.stderr[:500] if e.stderr else "")
        print(f"[FAIL] 下载失败")
        return []

    stdout = result.stdout or ""
    videos = _parse_videos_from_stdout(stdout, output_dir)

    # fallback: scan output_dir for new mp4 files
    if not videos:
        for f in sorted(output_dir.glob("*.mp4")):
            stem = f.stem
            parts = stem.split("_", 1)
            bv_id = parts[0] if parts else stem
            title = parts[1] if len(parts) > 1 else stem
            videos.append(VideoResult(bv_id=bv_id, title=title, filepath=f))

    print(f"[DONE] 下载完成，共 {len(videos)} 个视频文件")
    return videos


def download_space(uid: str, output_dir: str | Path, opts: DownloadOpts) -> list[VideoResult]:
    space_url = f"https://space.bilibili.com/{uid}/video"
    print(f"[SPACE] 下载UP主 {uid} 的全部投稿")
    if opts.max_count == 0:
        print("[WARN] 未限制下载数量，可能耗时较长，建议使用 --max-count")
    space_opts = DownloadOpts(
        cookies=opts.cookies,
        cookies_file=opts.cookies_file,
        all_pages=True,
        max_count=opts.max_count,
        dry_run=opts.dry_run,
        verbose=opts.verbose,
    )
    return download(space_url, output_dir, space_opts)
