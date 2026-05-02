import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger("bili")

QUALITY_MAP = {
    "low": ["-b:a", "128k"],
    "medium": ["-q:a", "2"],
    "high": ["-b:a", "320k"],
}


def extract_audio(
    video_path: str | Path,
    output_dir: str | Path,
    quality: str = "medium",
    delete_video: bool = False,
) -> Path | None:
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mp3_path = output_dir / (video_path.stem + ".mp3")
    quality_args = QUALITY_MAP.get(quality, QUALITY_MAP["medium"])

    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vn", "-acodec", "libmp3lame",
        *quality_args,
        str(mp3_path), "-y",
    ]

    logger.info("Extract audio: %s -> %s", video_path.name, mp3_path.name)
    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Audio extraction failed for %s: %s", video_path.name,
                     e.stderr.decode("utf-8", errors="ignore")[:200] if e.stderr else "")
        return None

    size_kb = mp3_path.stat().st_size // 1024
    print(f"  [OK] 音频: {mp3_path.name} ({size_kb}KB)")

    if delete_video and video_path.exists():
        video_path.unlink()
        logger.info("Deleted video: %s", video_path.name)

    return mp3_path


def separate_vocals(
    audio_path: str | Path,
    output_dir: str | Path,
    fmt: str = "mp3",
) -> Path | None:
    try:
        import numpy as np
        import soundfile as sf
        import torch
        from demucs.apply import apply_model
        from demucs.pretrained import get_model
    except ImportError:
        logger.warning("demucs 未安装，跳过人声分离。安装: uv sync --extra vocals")
        print("[SKIP] demucs 未安装，跳过人声分离")
        return None

    audio_path = Path(audio_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    basename = audio_path.stem
    print(f"  [VOCAL] 分离人声: {audio_path.name}")

    logger.info("Loading htdemucs model...")
    model = get_model("htdemucs")
    model.eval()

    # ffmpeg -> wav -> soundfile read
    tmp_wav = str(audio_path) + ".tmp.wav"
    try:
        subprocess.run(
            ["ffmpeg", "-i", str(audio_path), "-ar", "44100", "-ac", "2", tmp_wav, "-y"],
            capture_output=True, check=True,
        )
    except subprocess.CalledProcessError:
        logger.error("ffmpeg wav conversion failed for %s", audio_path.name)
        return None

    audio_np, sr = sf.read(tmp_wav)
    if os.path.exists(tmp_wav):
        os.remove(tmp_wav)

    wav = torch.from_numpy(audio_np.T).float()

    if sr != model.samplerate:
        from julius import resample_frac
        wav = resample_frac(wav, sr, model.samplerate)
        sr = model.samplerate

    wav = wav.unsqueeze(0)

    logger.info("Running vocal separation...")
    with torch.no_grad():
        sources = apply_model(model, wav)

    vocals_idx = model.sources.index("vocals")
    vocals = sources[0, vocals_idx]

    # save vocals
    if fmt == "wav":
        out_path = output_dir / f"{basename}_vocals.wav"
        vocals_np = vocals.cpu().numpy().T
        sf.write(str(out_path), vocals_np, sr)
    else:
        wav_path = output_dir / f"{basename}_vocals.wav"
        out_path = output_dir / f"{basename}_vocals.mp3"
        vocals_np = vocals.cpu().numpy().T
        sf.write(str(wav_path), vocals_np, sr)
        try:
            subprocess.run(
                ["ffmpeg", "-i", str(wav_path), "-acodec", "libmp3lame", "-q:a", "2", str(out_path), "-y"],
                capture_output=True, check=True,
            )
        except subprocess.CalledProcessError:
            logger.error("ffmpeg mp3 conversion failed, keeping wav")
            out_path = wav_path
        else:
            wav_path.unlink(missing_ok=True)

    size_kb = out_path.stat().st_size // 1024
    print(f"  [OK] 纯人声: {out_path.name} ({size_kb}KB)")
    return out_path
