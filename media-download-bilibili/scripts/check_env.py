import shutil
import sys


def main():
    errors = []
    if sys.version_info < (3, 11):
        errors.append(f"Python 3.11+ required, got {sys.version_info.major}.{sys.version_info.minor}")

    for cmd in ("yt-dlp", "ffmpeg"):
        if not shutil.which(cmd):
            errors.append(f"{cmd} not found in PATH")

    try:
        import demucs  # noqa: F401
        import soundfile  # noqa: F401
        import torch  # noqa: F401
        has_demucs = True
    except ImportError:
        has_demucs = False

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        sys.exit(1)

    print("[OK] yt-dlp: " + shutil.which("yt-dlp"))
    print("[OK] ffmpeg: " + shutil.which("ffmpeg"))
    print(f"[{'OK' if has_demucs else 'SKIP'}] demucs: {'available' if has_demucs else 'not installed (optional)'}")
    print("环境检查通过")


if __name__ == "__main__":
    main()
