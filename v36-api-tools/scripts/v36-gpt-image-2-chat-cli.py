import argparse
import base64
import http.client
import json
import os
import re
import sys
import urllib.parse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_BASE = "api.gpt.ge"
MODELS = ["gpt-image-2-c", "gpt-image-2"]
HTTP_TIMEOUT = 300  # seconds


def _get_conn(api_base, timeout=HTTP_TIMEOUT):
    base = api_base.replace("https://", "").replace("http://", "")
    use_https = api_base.startswith("https://") or not api_base.startswith("http://")
    return http.client.HTTPSConnection(base, timeout=timeout) if use_https else http.client.HTTPConnection(base, timeout=timeout)


def _get_token(args):
    token = args.token or os.getenv("V36_API_KEY")
    if not token:
        print("错误: 未提供 API Token。请通过 --token 参数、V36_API_KEY 环境变量或 .env 文件提供。", file=sys.stderr)
        sys.exit(1)
    return token


def cmd_generate(args):
    """文生图: POST /v1/chat/completions"""
    api_base = args.api_base or os.getenv("V36_API_BASE", API_BASE)
    token = _get_token(args)

    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": args.prompt}],
        "stream": args.stream,
    }
    if args.max_tokens:
        payload["max_tokens"] = args.max_tokens

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    conn = _get_conn(api_base)
    conn.request("POST", "/v1/chat/completions", json.dumps(payload), headers)

    if args.stream:
        _handle_streaming(conn, args, api_base)
    else:
        _handle_non_streaming(conn, args, api_base)


def cmd_edit(args):
    """图生图: POST /v1/chat/completions with base64 images"""
    api_base = args.api_base or os.getenv("V36_API_BASE", API_BASE)
    token = _get_token(args)

    content = [{"type": "text", "text": args.prompt}]
    for img_path in args.images:
        with open(img_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(img_path)[1].lower()
        mime_map = {
            ".png": "image/png", ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp",
        }
        mime = mime_map.get(ext, "image/png")
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{file_data}"}
        })

    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": content}],
        "stream": args.stream,
    }
    if args.max_tokens:
        payload["max_tokens"] = args.max_tokens

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    conn = _get_conn(api_base)
    conn.request("POST", "/v1/chat/completions", json.dumps(payload), headers)

    if args.stream:
        _handle_streaming(conn, args, api_base)
    else:
        _handle_non_streaming(conn, args, api_base)


# ---------------------------------------------------------------------------
# Response handlers
# ---------------------------------------------------------------------------

def _handle_streaming(conn, args, api_base):
    """Parse SSE stream: show progress, collect content, extract images"""
    res = conn.getresponse()
    try:
        raw = res.read()
    except http.client.IncompleteRead as e:
        raw = e.partial or b""
    finally:
        conn.close()

    if res.status != 200:
        print(f"\nHTTP {res.status}: {raw.decode('utf-8', errors='replace')}", file=sys.stderr)
        sys.exit(1)

    text = raw.decode("utf-8", errors="replace")
    full_content = ""
    usage_info = None

    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("data: "):
            continue
        data_str = line[6:]
        if data_str == "[DONE]":
            break
        try:
            obj = json.loads(data_str)
        except json.JSONDecodeError:
            continue

        choice = obj.get("choices", [{}])[0]
        delta = choice.get("delta", {})
        content = delta.get("content", "")
        if content:
            full_content += content
            print(content, end="", flush=True)

        if "usage" in obj:
            usage_info = obj["usage"]

    print()  # newline after streaming output

    # Extract images from markdown ![image](url) or ![...](url)
    image_urls = re.findall(r'!\[[^\]]*\]\((https?://[^\)]+)\)', full_content)

    if args.download and image_urls:
        os.makedirs(args.download, exist_ok=True)
        for i, url in enumerate(image_urls):
            _download_image(url, args.download, f"image_{i}.png", api_base)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({"content": full_content, "usage": usage_info, "image_urls": image_urls}, f, ensure_ascii=False, indent=2)
        print(f"JSON 已保存到 {args.output}")

    if usage_info:
        print(f"Tokens - prompt: {usage_info.get('prompt_tokens')}, completion: {usage_info.get('completion_tokens')}, total: {usage_info.get('total_tokens')}")


def _handle_non_streaming(conn, args, api_base):
    """Parse regular JSON response"""
    res = conn.getresponse()
    try:
        data = res.read().decode("utf-8")
    except http.client.IncompleteRead as e:
        data = (e.partial or b"").decode("utf-8")
        if not data:
            print("网络传输中断，未收到有效数据", file=sys.stderr)
            conn.close()
            sys.exit(1)
        print("警告: 响应不完整，尝试解析已接收数据...", file=sys.stderr)
    finally:
        conn.close()

    if res.status != 200:
        print(f"HTTP {res.status}: {data}", file=sys.stderr)
        sys.exit(1)

    try:
        result = json.loads(data)
    except json.JSONDecodeError:
        print(data)
        return

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"JSON 已保存到 {args.output}")

    choices = result.get("choices", [])
    full_content = ""
    for choice in choices:
        msg = choice.get("message", {})
        content = msg.get("content", "")
        if isinstance(content, list):
            for part in content:
                if part.get("type") == "text":
                    full_content += part.get("text", "")
                    print(part.get("text", ""))
        elif isinstance(content, str):
            full_content += content
            print(content)

    image_urls = re.findall(r'!\[[^\]]*\]\((https?://[^\)]+)\)', full_content)
    if args.download and image_urls:
        os.makedirs(args.download, exist_ok=True)
        for i, url in enumerate(image_urls):
            _download_image(url, args.download, f"image_{i}.png", api_base)

    if "usage" in result:
        u = result["usage"]
        print(f"Tokens - prompt: {u.get('prompt_tokens')}, completion: {u.get('completion_tokens')}, total: {u.get('total_tokens')}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _download_image(url, download_dir, filename, api_base):
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc or api_base.replace("https://", "").replace("http://", "")
    path = parsed.path
    if parsed.query:
        path += "?" + parsed.query

    use_https = url.startswith("https://") or not url.startswith("http://")
    conn = http.client.HTTPSConnection(host, timeout=HTTP_TIMEOUT) if use_https else http.client.HTTPConnection(host, timeout=HTTP_TIMEOUT)
    conn.request("GET", path)
    res = conn.getresponse()

    filepath = os.path.join(download_dir, filename)
    with open(filepath, "wb") as f:
        f.write(res.read())
    conn.close()
    print(f"已下载: {filepath}")


def _add_common_args(sub):
    sub.add_argument("--model", default="gpt-image-2-c", choices=MODELS,
                     help="模型名称（默认: gpt-image-2-c）")
    sub.add_argument("--max-tokens", type=int, default=3800, help="最大 tokens（默认: 3800）")
    sub.add_argument("--api-base", default=None, help="API 地址（默认从环境变量或 api.gpt.ge）")
    sub.add_argument("--token", default=None, help="API Token")
    sub.add_argument("--output", "-o", default=None, help="JSON 输出文件路径")
    sub.add_argument("--download", "-d", default=None,
                     help="图片下载目录（自动下载生成的图片到本地）")
    sub.add_argument("--no-stream", dest="stream", action="store_false",
                     help="禁用流式输出")
    sub.set_defaults(stream=True)


def main():
    parser = argparse.ArgumentParser(
        description="GPT-Image-2 CLI - 文生图 / 图生图 (via /v1/chat/completions)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  # 文生图
  python v36-gpt-image-2-chat-cli.py generate "一只猫坐在窗台上" -d ./output

  # 图生图（传入1~6张图片）
  python v36-gpt-image-2-chat-cli.py edit "把背景换成海边" -d ./output -- image1.png image2.png

  # 非流式模式
  python v36-gpt-image-2-chat-cli.py generate "城市夜景" --no-stream -o result.json
""")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("generate", help="文生图")
    gen.add_argument("prompt", help="文本提示词")
    _add_common_args(gen)

    edt = subparsers.add_parser("edit", help="图生图")
    edt.add_argument("prompt", help="编辑提示词")
    edt.add_argument("images", nargs="+", help="输入图片路径（1~6张）")
    _add_common_args(edt)

    args = parser.parse_args()
    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "edit":
        cmd_edit(args)


if __name__ == "__main__":
    main()
