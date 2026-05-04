"""MiniMax API common helpers."""

import json
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_BASE = "https://api.minimaxi.com"
VOICE_CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "voices_cache.json")


def get_api_key(args) -> str:
    key = getattr(args, "api_key", None) or os.getenv("MINIMAX_API_KEY")
    if not key:
        print("Error: 未提供 API Key。请通过 --api-key 参数、MINIMAX_API_KEY 环境变量或 .env 文件提供。", file=sys.stderr)
        sys.exit(1)
    return key


def get_api_base(args) -> str:
    return getattr(args, "api_base", None) or os.getenv("MINIMAX_API_BASE", API_BASE)


def headers(args) -> dict:
    return {"Authorization": f"Bearer {get_api_key(args)}"}


def add_common_args(sub):
    sub.add_argument("--api-key", default=None, help="MiniMax API Key（优先用环境变量）")
    sub.add_argument("--api-base", default=None, help="API 地址（默认从环境变量或 https://api.minimaxi.com）")


def check_base_resp(body: dict):
    code = body.get("base_resp", {}).get("status_code", -1)
    if code != 0:
        print(f"API error: {body}", file=sys.stderr)
        sys.exit(1)


def load_voice_cache() -> dict:
    if os.path.isfile(VOICE_CACHE_FILE):
        with open(VOICE_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"voice_cloning": [], "voice_generation": []}


def save_voice_cache(cache: dict):
    with open(VOICE_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def cache_voice(voice_id: str, voice_type: str, description: list[str] | None = None, **extra):
    cache = load_voice_cache()
    key = voice_type  # "voice_cloning" or "voice_generation"
    if key not in cache:
        cache[key] = []
    from datetime import date
    entry = {"voice_id": voice_id, "created_time": str(date.today())}
    if description:
        entry["description"] = description
    entry.update(extra)
    # avoid duplicates
    cache[key] = [v for v in cache[key] if v.get("voice_id") != voice_id]
    cache[key].append(entry)
    save_voice_cache(cache)
    return entry
