"""MiniMax voice clone: upload audio -> clone voice -> optional preview."""

import argparse

import requests

from .common import add_common_args, cache_voice, check_base_resp, get_api_base, headers


def upload_clone_audio(args) -> int:
    url = f"{get_api_base(args)}/v1/files/upload"
    with open(args.file, "rb") as f:
        resp = requests.post(url, headers=headers(args), files={"file": f}, data={"purpose": "voice_clone"})
    resp.raise_for_status()
    body = resp.json()
    check_base_resp(body)
    file_id = body["file"]["file_id"]
    print(f"Clone audio uploaded, file_id={file_id}")
    return file_id


def upload_prompt_audio(args) -> int:
    url = f"{get_api_base(args)}/v1/files/upload"
    with open(args.file, "rb") as f:
        resp = requests.post(url, headers=headers(args), files={"file": f}, data={"purpose": "prompt_audio"})
    resp.raise_for_status()
    body = resp.json()
    check_base_resp(body)
    file_id = body["file"]["file_id"]
    print(f"Prompt audio uploaded, file_id={file_id}")
    return file_id


def clone_voice(args, file_id: int, voice_id: str) -> dict:
    url = f"{get_api_base(args)}/v1/voice_clone"
    payload: dict = {
        "file_id": file_id,
        "voice_id": voice_id,
        "need_noise_reduction": getattr(args, "noise_reduction", False),
        "need_volume_normalization": getattr(args, "volume_normalization", False),
    }
    if getattr(args, "prompt_audio_id", None) and getattr(args, "prompt_text", None):
        payload["clone_prompt"] = {"prompt_audio": args.prompt_audio_id, "prompt_text": args.prompt_text}
    if getattr(args, "text", None):
        payload["text"] = args.text
    if getattr(args, "model", None):
        payload["model"] = args.model
    if getattr(args, "language_boost", None):
        payload["language_boost"] = args.language_boost
    resp = requests.post(url, headers={**headers(args), "Content-Type": "application/json"}, json=payload)
    resp.raise_for_status()
    body = resp.json()
    check_base_resp(body)
    return body


def _print_clone_result(result: dict, voice_id: str):
    print(f"Clone success, voice_id={voice_id} registered")
    if result.get("demo_audio"):
        print(f"Demo audio: {result['demo_audio']}")
    cache_voice(voice_id, "voice_cloning")
    print(f"Voice cached to voices_cache.json")


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description="MiniMax voice clone tool")
    sub = parser.add_subparsers(dest="action", required=True)

    # upload-clone
    p_uc = sub.add_parser("upload-clone", help="上传复刻音频")
    p_uc.add_argument("file", help="音频文件路径 (mp3/m4a/wav, 10s~5min)")
    add_common_args(p_uc)

    # upload-prompt
    p_up = sub.add_parser("upload-prompt", help="上传示例音频")
    p_up.add_argument("file", help="音频文件路径 (mp3/m4a/wav, <8s)")
    add_common_args(p_up)

    # clone
    p_cl = sub.add_parser("clone", help="执行音色复刻")
    p_cl.add_argument("--file-id", type=int, required=True, help="复刻音频 file_id")
    p_cl.add_argument("--voice-id", required=True, help="自定义 voice_id")
    p_cl.add_argument("--prompt-audio-id", type=int, help="示例音频 file_id")
    p_cl.add_argument("--prompt-text", help="示例音频对应文本")
    p_cl.add_argument("--text", help="试听文本")
    p_cl.add_argument("--model", help="试听模型 (speech-2.8-hd 等)")
    p_cl.add_argument("--language-boost", help="语言增强 (auto/Chinese 等)")
    p_cl.add_argument("--noise-reduction", action="store_true", help="开启降噪")
    p_cl.add_argument("--volume-normalization", action="store_true", help="开启音量归一化")
    add_common_args(p_cl)

    # full pipeline
    p_all = sub.add_parser("run", help="一键复刻: 上传音频并复刻")
    p_all.add_argument("--audio", required=True, help="复刻音频文件路径")
    p_all.add_argument("--voice-id", required=True, help="自定义 voice_id")
    p_all.add_argument("--prompt-audio", help="示例音频文件路径")
    p_all.add_argument("--prompt-text", help="示例音频对应文本")
    p_all.add_argument("--text", help="试听文本")
    p_all.add_argument("--model", help="试听模型")
    p_all.add_argument("--language-boost", help="语言增强")
    p_all.add_argument("--noise-reduction", action="store_true", help="开启降噪")
    p_all.add_argument("--volume-normalization", action="store_true", help="开启音量归一化")
    add_common_args(p_all)

    args = parser.parse_args(argv)

    if args.action == "upload-clone":
        upload_clone_audio(args)
    elif args.action == "upload-prompt":
        upload_prompt_audio(args)
    elif args.action == "clone":
        result = clone_voice(args, args.file_id, args.voice_id)
        _print_clone_result(result, args.voice_id)
    elif args.action == "run":
        file_id = upload_clone_audio(args)
        if args.prompt_audio:
            upload_prompt_audio(args)
        result = clone_voice(args, file_id, args.voice_id)
        _print_clone_result(result, args.voice_id)


if __name__ == "__main__":
    main()
