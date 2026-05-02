import argparse
import logging
import sys
from pathlib import Path

from .audio import extract_audio, separate_vocals
from .downloader import DownloadOpts, VideoResult, download, download_space, dry_run_query
from .utils import ResumeTracker, check_env, setup_logging

logger = logging.getLogger("bili")

DEFAULT_OUTPUT = "./bili_downloads"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bili",
        description="B站视频批量下载 + 音频提取 + 人声分离",
    )

    # input
    inp = parser.add_mutually_exclusive_group(required=True)
    inp.add_argument("--url", help="B站视频链接")
    inp.add_argument("--space", help="UP主UID，下载全部投稿")

    # output
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT,
                        help="输出目录 (默认: ./bili_downloads)")

    # processing
    parser.add_argument("--audio-only", action="store_true",
                        help="只保留MP3，删除视频")
    parser.add_argument("--keep-video", action="store_true",
                        help="提取音频同时保留视频")
    parser.add_argument("--vocals", action="store_true",
                        help="生成纯人声MP3/WAV（需要 demucs）")

    # download options
    parser.add_argument("--all-pages", action="store_true",
                        help="下载合集所有分P")
    parser.add_argument("--max-count", type=int, default=0,
                        help="UP主下载上限 (默认: 0=不限制)")
    parser.add_argument("--cookies", default=None,
                        help="从浏览器获取cookies (chrome/edge/firefox)")
    parser.add_argument("--cookies-file", default=None,
                        help="指定 cookies.txt 文件路径")

    # quality & format
    parser.add_argument("--audio-quality", choices=["low", "medium", "high"],
                        default="medium", help="音频质量 (默认: medium)")
    parser.add_argument("--vocal-format", choices=["mp3", "wav"],
                        default="mp3", help="人声输出格式 (默认: mp3)")

    # control
    parser.add_argument("--verbose", action="store_true",
                        help="显示详细输出")
    parser.add_argument("--dry-run", action="store_true",
                        help="只显示下载计划不执行")

    return parser


def _print_dry_run(entries: list[dict]) -> None:
    print(f"\n--- Dry-Run: 共 {len(entries)} 个视频 ---")
    for i, entry in enumerate(entries, 1):
        title = entry.get("title", "未知")
        duration = entry.get("duration", 0)
        bv_id = entry.get("id", "?")
        duration_str = f"{int(duration) // 60}:{int(duration) % 60:02d}" if duration else "未知"
        print(f"  [{i}] {bv_id} | {title} | {duration_str}")
    print()


def _print_summary(output_dir: str) -> None:
    print("\n--- 结果汇总 ---")
    base = Path(output_dir)
    if not base.exists():
        return
    for f in sorted(base.rglob("*")):
        if f.is_file() and f.name != ".bili_resume.json":
            size = f.stat().st_size
            if size > 1024 * 1024:
                size_str = f"{size / (1024 * 1024):.1f}MB"
            else:
                size_str = f"{size / 1024:.1f}KB"
            print(f"  {f.relative_to(base)} ({size_str})")


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    setup_logging(args.verbose)

    # env check
    env = check_env()
    if not env.has_ytdlp:
        print("[FAIL] yt-dlp 未安装。安装: pip install yt-dlp")
        sys.exit(1)
    if not env.has_ffmpeg:
        print("[FAIL] ffmpeg 未安装")
        sys.exit(1)
    if args.vocals and not env.has_demucs:
        print("[WARN] demucs 未安装，人声分离将跳过。安装: uv sync --extra vocals 或 pip install -e \".[vocals]\"")
        args.vocals = False

    logger.info("Environment: yt-dlp=%s, ffmpeg=%s, demucs=%s",
                env.ytdlp_path, env.ffmpeg_path, env.has_demucs)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    opts = DownloadOpts(
        cookies=args.cookies,
        cookies_file=args.cookies_file,
        all_pages=args.all_pages,
        max_count=args.max_count,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

    url = args.url
    is_space = args.space is not None
    if is_space:
        url = f"https://space.bilibili.com/{args.space}/video"

    # dry-run
    if args.dry_run:
        entries = dry_run_query(url, opts)
        _print_dry_run(entries)
        return

    # download
    tracker = ResumeTracker(output_dir)

    if is_space:
        videos = download_space(args.space, str(output_dir), opts)
    else:
        videos = download(url, str(output_dir), opts)

    # filter already downloaded
    new_videos = [v for v in videos if not tracker.is_downloaded(v.bv_id)]
    if new_videos:
        for v in new_videos:
            tracker.mark_downloaded(v.bv_id, v.filepath.name)
    else:
        print("[INFO] 所有视频已下载，跳过")

    # audio extraction
    if args.audio_only or args.keep_video:
        print("\n[AUDIO] 开始提取音频...")
        delete_video = args.audio_only and not args.keep_video
        for v in videos:
            if tracker.is_extracted(v.bv_id):
                logger.info("Skip extracted: %s", v.bv_id)
                continue
            mp3 = extract_audio(v.filepath, v.filepath.parent,
                                quality=args.audio_quality,
                                delete_video=delete_video)
            if mp3:
                tracker.mark_extracted(v.bv_id, mp3.name)

    # vocal separation
    if args.vocals:
        vocals_dir = output_dir / "vocals"
        print(f"\n[VOCAL] 开始人声分离...")
        for v in videos:
            if tracker.is_vocals_done(v.bv_id):
                logger.info("Skip vocals: %s", v.bv_id)
                continue
            # find the extracted mp3
            audio_file = v.filepath.parent / (v.filepath.stem + ".mp3")
            if not audio_file.exists():
                logger.warning("Audio file not found for %s, skipping vocals", v.bv_id)
                continue
            vocal = separate_vocals(audio_file, vocals_dir, fmt=args.vocal_format)
            if vocal:
                tracker.mark_vocals_done(v.bv_id, vocal.name)

    _print_summary(str(output_dir))
