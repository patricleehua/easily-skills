import argparse
import base64
import http.client
import json
import os
import sys
import time
import urllib.parse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_BASE = "api.gpt.ge"
MODELS = [
    "nano-banana", "nano-banana-pro", "nano-banana-pro-2k", "nano-banana-pro-4k",
    "gemini-2.5-flash-image",
    "gemini-3-pro-image-preview",
    "gemini-3.1-flash-image-preview", "gemini-3.1-flash-image-preview-0.5k",
    "gemini-3.1-flash-image-preview-2k", "gemini-3.1-flash-image-preview-4k",
]
HTTP_TIMEOUT = 120  # seconds


def _get_conn(api_base, timeout=HTTP_TIMEOUT):
    base = api_base.replace("https://", "").replace("http://", "")
    use_https = api_base.startswith("https://") or not api_base.startswith("http://")
    return http.client.HTTPSConnection(base, timeout=timeout) if use_https else http.client.HTTPConnection(base, timeout=timeout)


def _get_token(args):
    token = args.token or os.getenv("NANOBANANA_TOKEN")
    if not token:
        print("错误: 未提供 API Token。请通过 --token 参数、NANOBANANA_TOKEN 环境变量或 .env 文件提供。", file=sys.stderr)
        sys.exit(1)
    return token


def cmd_generate(args):
    """文生图: POST /v1/images/generations (JSON)"""
    api_base = args.api_base or os.getenv("NANOBANANA_API_BASE", API_BASE)
    token = _get_token(args)

    payload = {"model": args.model, "prompt": args.prompt}
    if args.size:
        payload["size"] = args.size
    if args.aspect_ratio:
        payload["aspect_ratio"] = args.aspect_ratio
    if args.response_format:
        payload["response_format"] = args.response_format

    conn = _get_conn(api_base)
    conn.request("POST", "/v1/images/generations", json.dumps(payload), {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    _handle_response(conn, args, api_base)


def cmd_edit(args):
    """图生图: POST /v1/images/edits (multipart/form-data)"""
    api_base = args.api_base or os.getenv("NANOBANANA_API_BASE", API_BASE)
    token = _get_token(args)

    boundary = "----NanoBananaBoundary7MA4YWxkTrZu0gW"
    raw_parts = []
    raw_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"prompt\"\r\n\r\n{args.prompt}\r\n".encode("utf-8"))
    raw_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\n{args.model}\r\n".encode("utf-8"))

    if args.response_format:
        raw_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"response_format\"\r\n\r\n{args.response_format}\r\n".encode("utf-8"))
    if args.size:
        raw_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"size\"\r\n\r\n{args.size}\r\n".encode("utf-8"))
    if args.aspect_ratio:
        raw_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"aspect_ratio\"\r\n\r\n{args.aspect_ratio}\r\n".encode("utf-8"))

    for img_path in args.images:
        filename = os.path.basename(img_path)
        with open(img_path, "rb") as f:
            file_data = f.read()
        header = f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{filename}\"\r\nContent-Type: application/octet-stream\r\n\r\n"
        raw_parts.append(header.encode("utf-8") + file_data + b"\r\n")

    raw_parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(raw_parts)

    conn = _get_conn(api_base)
    conn.request("POST", "/v1/images/edits", body, {
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    })
    _handle_response(conn, args, api_base)


def _handle_response(conn, args, api_base):
    res = conn.getresponse()
    try:
        data = res.read().decode("utf-8")
    except http.client.IncompleteRead as e:
        data = e.partial.decode("utf-8") if e.partial else ""
        if not data:
            print(f"网络传输中断，未收到有效数据", file=sys.stderr)
            conn.close()
            sys.exit(1)
        print(f"警告: 响应不完整，尝试解析已接收数据...", file=sys.stderr)
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

    # Download images if --download-dir specified
    download_dir = args.download
    if download_dir:
        os.makedirs(download_dir, exist_ok=True)
        for i, item in enumerate(result.get("data", [])):
            if "url" in item:
                _download_image(item["url"], download_dir, f"image_{i}.png", api_base)
            elif "b64_json" in item:
                filepath = os.path.join(download_dir, f"image_{i}.png")
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(item["b64_json"]))
                print(f"已保存: {filepath}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"JSON 已保存到 {args.output}")
    else:
        # Print summary instead of raw base64
        for i, item in enumerate(result.get("data", [])):
            if "url" in item:
                print(f"Image {i}: {item['url']}")
            elif "b64_json" in item:
                print(f"Image {i}: base64 ({len(item['b64_json'])} chars)")
            if "revised_prompt" in item:
                print(f"  Revised prompt: {item['revised_prompt']}")
        if "usage" in result:
            u = result["usage"]
            print(f"Tokens - input: {u.get('input_tokens')}, output: {u.get('output_tokens')}, total: {u.get('total_tokens')}")


def _download_image(url, download_dir, filename, api_base):
    """Download image from URL"""
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
    sub.add_argument("--model", default="nano-banana", choices=MODELS,
                     help="模型名称（默认: nano-banana）")
    sub.add_argument("--size", default=None, help="图片尺寸，如 2:3、4K")
    sub.add_argument("--aspect-ratio", default=None, help="宽高比，如 2:3（nano-banana-pro 可用）")
    sub.add_argument("--response-format", default="url", choices=["url", "b64_json"],
                     help="返回格式（默认: url）")
    sub.add_argument("--api-base", default=None, help="API 地址（默认从环境变量或 api.gpt.ge）")
    sub.add_argument("--token", default=None, help="API Token")
    sub.add_argument("--output", "-o", default=None, help="JSON 输出文件路径")
    sub.add_argument("--download", "-d", default=None,
                     help="图片下载目录（自动下载生成的图片到本地）")


def main():
    parser = argparse.ArgumentParser(
        description="NanoBanana CLI - 文生图 / 图生图工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  # 文生图
  python v36-nanobanana-cli.py generate "一只猫坐在窗台上" --size 2:3 -d ./output

  # 图生图（传入1~6张图片）
  python v36-nanobanana-cli.py edit "把背景换成海边" -d ./output -- image1.png image2.png

  # 使用 nano-banana-pro
  python v36-nanobanana-cli.py generate "城市夜景" --model nano-banana-pro --size 4K --aspect-ratio 16:9
""")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate: 文生图
    gen = subparsers.add_parser("generate", help="文生图（/v1/images/generations）")
    gen.add_argument("prompt", help="文本提示词")
    _add_common_args(gen)

    # edit: 图生图
    edt = subparsers.add_parser("edit", help="图生图（/v1/images/edits）")
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
