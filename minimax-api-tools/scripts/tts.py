"""MiniMax TTS: sync / async text-to-audio."""

import argparse
import json
import os
import sys

import requests

from .common import add_common_args, check_base_resp, get_api_base, headers

MODELS = [
    "speech-2.8-hd", "speech-2.8-turbo",
    "speech-2.6-hd", "speech-2.6-turbo",
    "speech-02-hd", "speech-02-turbo",
    "speech-01-hd", "speech-01-turbo",
]


def cmd_sync(args):
    """同步语音合成 HTTP: POST /v1/t2a_v2"""
    url = f"{get_api_base(args)}/v1/t2a_v2"
    payload: dict = {
        "model": args.model,
        "text": args.text,
        "stream": False,
        "voice_setting": {"voice_id": args.voice_id},
        "output_format": args.output_format,
    }
    if args.speed is not None:
        payload["voice_setting"]["speed"] = args.speed
    if args.vol is not None:
        payload["voice_setting"]["vol"] = args.vol
    if args.pitch is not None:
        payload["voice_setting"]["pitch"] = args.pitch
    if args.emotion:
        payload["voice_setting"]["emotion"] = args.emotion
    if args.language_boost:
        payload["language_boost"] = args.language_boost
    if args.audio_format:
        payload["audio_setting"] = {"format": args.audio_format, "sample_rate": args.sample_rate or 32000}
    if args.subtitle:
        payload["subtitle_enable"] = True

    resp = requests.post(url, headers={**headers(args), "Content-Type": "application/json"}, json=payload)
    resp.raise_for_status()
    body = resp.json()
    check_base_resp(body)

    data = body.get("data", {})
    extra = body.get("extra_info", {})

    if args.output_format == "url" and data.get("audio"):
        print(f"Audio URL: {data['audio']}")
    elif data.get("audio"):
        print(f"Audio: hex ({len(data['audio'])} chars)")

    if data.get("subtitle_file"):
        print(f"Subtitle: {data['subtitle_file']}")

    if extra:
        print(f"Duration: {extra.get('audio_length', 0)}ms, Format: {extra.get('audio_format')}, "
              f"Chars: {extra.get('usage_characters')}")

    if args.download and data.get("audio"):
        _download_audio(args, data["audio"], extra.get("audio_format", "mp3"))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(body, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}")


def cmd_sync_stream(args):
    """同步流式语音合成: POST /v1/t2a_v2 stream=true"""
    url = f"{get_api_base(args)}/v1/t2a_v2"
    payload: dict = {
        "model": args.model,
        "text": args.text,
        "stream": True,
        "voice_setting": {"voice_id": args.voice_id},
    }
    if args.speed is not None:
        payload["voice_setting"]["speed"] = args.speed
    if args.vol is not None:
        payload["voice_setting"]["vol"] = args.vol
    if args.pitch is not None:
        payload["voice_setting"]["pitch"] = args.pitch
    if args.emotion:
        payload["voice_setting"]["emotion"] = args.emotion
    if args.language_boost:
        payload["language_boost"] = args.language_boost
    if args.audio_format:
        payload["audio_setting"] = {"format": args.audio_format, "sample_rate": args.sample_rate or 32000}

    audio_chunks: list[bytes] = []
    audio_format = "mp3"

    with requests.post(url, headers={**headers(args), "Content-Type": "application/json"}, json=payload, stream=True) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            text = line.decode("utf-8")
            if not text.startswith("data:"):
                continue
            chunk_str = text[5:].strip()
            if not chunk_str:
                continue
            try:
                chunk = json.loads(chunk_str)
            except json.JSONDecodeError:
                continue
            code = chunk.get("base_resp", {}).get("status_code", -1)
            if code != 0:
                print(f"Stream error: {chunk}", file=sys.stderr)
                sys.exit(1)
            data = chunk.get("data", {})
            if data.get("audio"):
                audio_chunks.append(bytes.fromhex(data["audio"]))
            if data.get("status") == 2:
                extra = chunk.get("extra_info", {})
                audio_format = extra.get("audio_format", "mp3")
                print(f"Duration: {extra.get('audio_length', 0)}ms, Chars: {extra.get('usage_characters')}")

    if args.download and audio_chunks:
        out_path = os.path.join(args.download, f"tts_output.{audio_format}")
        os.makedirs(args.download, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(b"".join(audio_chunks))
        print(f"Saved to {out_path}")
    elif audio_chunks:
        print(f"Stream done, {len(audio_chunks)} chunks, format={audio_format}")


def cmd_async_create(args):
    """异步长文本合成: POST /v1/t2a_async_v2"""
    url = f"{get_api_base(args)}/v1/t2a_async_v2"
    payload: dict = {
        "model": args.model,
        "voice_setting": {"voice_id": args.voice_id},
    }
    if args.text:
        payload["text"] = args.text
    elif args.text_file_id:
        payload["text_file_id"] = args.text_file_id
    else:
        print("Error: --text or --text-file-id required", file=sys.stderr)
        sys.exit(1)
    if args.language_boost:
        payload["language_boost"] = args.language_boost
    if args.speed is not None:
        payload["voice_setting"]["speed"] = args.speed
    if args.vol is not None:
        payload["voice_setting"]["vol"] = args.vol
    if args.pitch is not None:
        payload["voice_setting"]["pitch"] = args.pitch
    if args.audio_format or args.sample_rate:
        payload["audio_setting"] = {"format": args.audio_format or "mp3", "sample_rate": args.sample_rate or 32000}

    resp = requests.post(url, headers={**headers(args), "Content-Type": "application/json"}, json=payload)
    resp.raise_for_status()
    body = resp.json()
    check_base_resp(body)
    print(f"Async task created, task_id={body.get('task_id')}, file_id={body.get('file_id')}, "
          f"chars={body.get('usage_characters')}")


def cmd_async_query(args):
    """查询异步任务: GET /v1/query/t2a_async_query_v2"""
    url = f"{get_api_base(args)}/v1/query/t2a_async_query_v2"
    resp = requests.get(url, headers=headers(args), params={"task_id": args.task_id})
    resp.raise_for_status()
    body = resp.json()
    check_base_resp(body)
    status = body.get("status", "unknown")
    print(f"Task {args.task_id}: status={status}")
    if body.get("file_id"):
        print(f"  file_id={body['file_id']}")


def _download_audio(args, audio_src: str, fmt: str):
    """Download audio from URL or hex."""
    os.makedirs(args.download, exist_ok=True)
    if audio_src.startswith("http"):
        resp = requests.get(audio_src)
        resp.raise_for_status()
        out_path = os.path.join(args.download, f"tts_output.{fmt}")
        with open(out_path, "wb") as f:
            f.write(resp.content)
        print(f"Downloaded: {out_path}")


def _add_tts_args(sub):
    sub.add_argument("--model", default="speech-2.8-hd", choices=MODELS, help="模型")
    sub.add_argument("--voice-id", required=True, help="音色 ID")
    sub.add_argument("--speed", type=float, default=None, help="语速 [0.5,2]")
    sub.add_argument("--vol", type=float, default=None, help="音量 (0,10]")
    sub.add_argument("--pitch", type=int, default=None, help="语调 [-12,12]")
    sub.add_argument("--emotion", default=None,
                     choices=["happy", "sad", "angry", "fearful", "disgusted", "surprised", "calm", "fluent", "whisper"],
                     help="情绪")
    sub.add_argument("--language-boost", default=None, help="语言增强 (auto/Chinese 等)")
    sub.add_argument("--audio-format", default=None, choices=["mp3", "pcm", "flac", "wav"], help="音频格式")
    sub.add_argument("--sample-rate", type=int, default=None, help="采样率")
    sub.add_argument("--download", "-d", default=None, help="下载目录")
    sub.add_argument("--output", "-o", default=None, help="JSON 输出文件")
    add_common_args(sub)


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description="MiniMax TTS tool")
    sub = parser.add_subparsers(dest="action", required=True)

    # sync (non-stream)
    p_sync = sub.add_parser("sync", help="同步语音合成 (非流式)")
    p_sync.add_argument("text", help="合成文本 (<10000字符)")
    p_sync.add_argument("--output-format", default="hex", choices=["hex", "url"], help="输出格式 (默认 hex)")
    p_sync.add_argument("--subtitle", action="store_true", help="开启字幕")
    _add_tts_args(p_sync)

    # sync stream
    p_stream = sub.add_parser("stream", help="同步语音合成 (流式)")
    p_stream.add_argument("text", help="合成文本")
    _add_tts_args(p_stream)

    # async create
    p_async = sub.add_parser("async", help="创建异步长文本合成任务")
    p_async.add_argument("--text", default=None, help="合成文本 (<50000字符)")
    p_async.add_argument("--text-file-id", type=int, default=None, help="文本文件 file_id")
    _add_tts_args(p_async)

    # async query
    p_query = sub.add_parser("query", help="查询异步任务状态")
    p_query.add_argument("--task-id", type=int, required=True, help="任务 ID")
    add_common_args(p_query)

    args = parser.parse_args(argv)

    if args.action == "sync":
        cmd_sync(args)
    elif args.action == "stream":
        cmd_sync_stream(args)
    elif args.action == "async":
        cmd_async_create(args)
    elif args.action == "query":
        cmd_async_query(args)


if __name__ == "__main__":
    main()
