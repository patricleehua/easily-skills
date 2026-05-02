import json
import logging
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger("bili")

_ILLEGAL_CHARS = re.compile(r'[\\/:*?"<>|]')
_MAX_FILENAME = 200  # leave room for path prefix on Windows


@dataclass
class EnvReport:
    has_ytdlp: bool = False
    has_ffmpeg: bool = False
    has_demucs: bool = False
    ytdlp_path: str | None = None
    ffmpeg_path: str | None = None


def check_env() -> EnvReport:
    report = EnvReport()
    report.ytdlp_path = shutil.which("yt-dlp")
    report.has_ytdlp = report.ytdlp_path is not None
    report.ffmpeg_path = shutil.which("ffmpeg")
    report.has_ffmpeg = report.ffmpeg_path is not None
    try:
        import demucs  # noqa: F401
        import torch  # noqa: F401
        import soundfile  # noqa: F401
        report.has_demucs = True
    except ImportError:
        report.has_demucs = False
    return report


def sanitize_filename(title: str, bv_id: str, page_num: int | None = None) -> str:
    safe = _ILLEGAL_CHARS.sub("-", title).strip(". ")
    if page_num is not None:
        prefix = f"{bv_id}_P{page_num}"
    else:
        prefix = bv_id
    name = f"{prefix}_{safe}"
    return name[:_MAX_FILENAME]


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logging.basicConfig(level=level, handlers=[handler], force=True)


def ensure_video_dir(output_dir: str | Path, title: str, bv_id: str, page_num: int | None = None) -> Path:
    base = Path(output_dir)
    dirname = sanitize_filename(title, bv_id, page_num)
    video_dir = base / dirname
    video_dir.mkdir(parents=True, exist_ok=True)
    return video_dir


_RESUME_FILE = ".bili_resume.json"


class ResumeTracker:
    def __init__(self, output_dir: str | Path) -> None:
        self._path = Path(output_dir) / _RESUME_FILE
        self._data: dict[str, list[str]] = {"downloaded": [], "extracted": [], "vocals": []}
        if self._path.exists():
            try:
                self._data = json.loads(self._path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def is_downloaded(self, bv_id: str) -> bool:
        return any(bv_id in entry for entry in self._data["downloaded"])

    def mark_downloaded(self, bv_id: str, filename: str) -> None:
        key = f"{bv_id}:{filename}"
        if key not in self._data["downloaded"]:
            self._data["downloaded"].append(key)
            self._save()

    def is_extracted(self, bv_id: str) -> bool:
        return any(bv_id in entry for entry in self._data["extracted"])

    def mark_extracted(self, bv_id: str, filename: str) -> None:
        key = f"{bv_id}:{filename}"
        if key not in self._data["extracted"]:
            self._data["extracted"].append(key)
            self._save()

    def is_vocals_done(self, bv_id: str) -> bool:
        return any(bv_id in entry for entry in self._data["vocals"])

    def mark_vocals_done(self, bv_id: str, filename: str) -> None:
        key = f"{bv_id}:{filename}"
        if key not in self._data["vocals"]:
            self._data["vocals"].append(key)
            self._save()
