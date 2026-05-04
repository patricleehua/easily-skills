"""MiniMax voice management: query / delete / design."""

import argparse
import json
import sys

import requests

from .common import add_common_args, cache_voice, check_base_resp, get_api_base, headers, load_voice_cache


def cmd_list(args):
    """查询可用音色: POST /v1/get_voice"""
    url = f"{get_api_base(args)}/v1/get_voice"
    payload = {"voice_type": args.voice_type}
    resp = requests.post(url, headers={**headers(args), "Content-Type": "application/json"}, json=payload)
    resp.raise_for_status()
    body = resp.json()
    check_base_resp(body)

    for v in body.get("system_voice", []):
        desc = "; ".join(v.get("description", []))
        print(f"  [system] {v['voice_id']}  {v.get('voice_name', '')}  {desc}")

    for v in body.get("voice_cloning", []):
        print(f"  [cloned] {v['voice_id']}  created={v.get('created_time', '')}")

    for v in body.get("voice_generation", []):
        print(f"  [generated] {v['voice_id']}  created={v.get('created_time', '')}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(body, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}")


def cmd_list_local(args):
    """查询本地缓存的音色 (无需 API 调用)"""
    cache = load_voice_cache()
    voice_type = args.voice_type

    types_to_show = ["voice_cloning", "voice_generation"] if voice_type == "all" else [voice_type]
    has_any = False
    for vt in types_to_show:
        voices = cache.get(vt, [])
        if not voices:
            continue
        label = "cloned" if vt == "voice_cloning" else "generated"
        for v in voices:
            desc = "; ".join(v.get("description", []))
            print(f"  [{label}] {v['voice_id']}  created={v.get('created_time', '')}  {desc}")
            has_any = True

    if not has_any:
        print("No cached voices found. Run voice-clone or voice-design first.")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}")


def cmd_delete(args):
    """删除音色: POST /v1/delete_voice"""
    url = f"{get_api_base(args)}/v1/delete_voice"
    payload = {"voice_type": args.voice_type, "voice_id": args.voice_id}
    resp = requests.post(url, headers={**headers(args), "Content-Type": "application/json"}, json=payload)
    resp.raise_for_status()
    body = resp.json()
    check_base_resp(body)
    print(f"Deleted voice_id={body.get('voice_id')}, created_time={body.get('created_time')}")


def cmd_design(args):
    """音色设计: POST /v1/voice_design"""
    url = f"{get_api_base(args)}/v1/voice_design"
    payload: dict = {
        "prompt": args.prompt,
        "preview_text": args.preview_text,
    }
    if args.voice_id:
        payload["voice_id"] = args.voice_id
    resp = requests.post(url, headers={**headers(args), "Content-Type": "application/json"}, json=payload)
    resp.raise_for_status()
    body = resp.json()
    check_base_resp(body)
    vid = body.get("voice_id", args.voice_id or "")
    print(f"Voice designed, voice_id={vid}")
    if body.get("trial_audio"):
        print(f"Trial audio: hex ({len(body['trial_audio'])} chars)")
    cache_voice(vid, "voice_generation", description=[args.prompt])
    print(f"Voice cached to voices_cache.json")


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description="MiniMax voice management tool")
    sub = parser.add_subparsers(dest="action", required=True)

    # list
    p_list = sub.add_parser("list", help="查询可用音色")
    p_list.add_argument("--voice-type", default="all",
                        choices=["system", "voice_cloning", "voice_generation", "all"],
                        help="音色类型 (默认 all)")
    p_list.add_argument("--output", "-o", default=None, help="JSON 输出文件")
    add_common_args(p_list)

    # list-local (offline, from cache)
    p_local = sub.add_parser("list-local", help="查询本地缓存的音色 (无需 API)")
    p_local.add_argument("--voice-type", default="all",
                         choices=["voice_cloning", "voice_generation", "all"],
                         help="音色类型 (默认 all)")
    p_local.add_argument("--output", "-o", default=None, help="JSON 输出文件")

    # delete
    p_del = sub.add_parser("delete", help="删除音色")
    p_del.add_argument("--voice-id", required=True, help="音色 ID")
    p_del.add_argument("--voice-type", required=True, choices=["voice_cloning", "voice_generation"],
                       help="音色类型")
    add_common_args(p_del)

    # design
    p_design = sub.add_parser("design", help="音色设计 (文本描述生成音色)")
    p_design.add_argument("--prompt", required=True, help="音色描述")
    p_design.add_argument("--preview-text", required=True, help="试听文本")
    p_design.add_argument("--voice-id", default=None, help="自定义 voice_id (可选)")
    add_common_args(p_design)

    args = parser.parse_args(argv)

    if args.action == "list":
        cmd_list(args)
    elif args.action == "list-local":
        cmd_list_local(args)
    elif args.action == "delete":
        cmd_delete(args)
    elif args.action == "design":
        cmd_design(args)


if __name__ == "__main__":
    main()
