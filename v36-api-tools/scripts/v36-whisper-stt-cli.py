import argparse
import http.client
import json
import os
import sys
import uuid

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_BASE = "api.gpt.ge"
MODEL = "whisper-large-v3-turbo"
HTTP_TIMEOUT = 300

LANGUAGES = ["zh", "en", "de", "es"]
FORMATS = ["json", "text", "srt", "verbose_json", "vtt"]


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


def _build_multipart(fields, files):
    boundary = uuid.uuid4().hex
    body = b""
    for name, value in fields.items():
        if value is None:
            continue
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        body += f"{value}\r\n".encode()
    for name, (filename, data, mime) in files.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode()
        body += f"Content-Type: {mime}\r\n\r\n".encode()
        body += data
        body += b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


MIME_MAP = {
    ".flac": "audio/flac", ".mp3": "audio/mpeg", ".mp4": "audio/mp4",
    ".mpeg": "audio/mpeg", ".mpga": "audio/mpeg", ".m4a": "audio/mp4",
    ".ogg": "audio/ogg", ".wav": "audio/wav", ".webm": "audio/webm",
}


def cmd_transcribe(args):
    api_base = args.api_base or os.getenv("NANOBANANA_API_BASE", API_BASE)
    token = _get_token(args)

    file_path = args.file
    if not os.path.isfile(file_path):
        print(f"错误: 文件不存在: {file_path}", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(file_path)[1].lower()
    mime = MIME_MAP.get(ext)
    if not mime:
        print(f"错误: 不支持的音频格式: {ext}（支持: {', '.join(MIME_MAP.keys())}）", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "rb") as f:
        file_data = f.read()

    if len(file_data) > 25 * 1024 * 1024:
        print("错误: 文件大小超过 25MB 限制", file=sys.stderr)
        sys.exit(1)

    filename = os.path.basename(file_path)
    fields = {"model": args.model}
    if args.language:
        fields["language"] = args.language
    if args.response_format:
        fields["response_format"] = args.response_format

    body, content_type = _build_multipart(fields, {"file": (filename, file_data, mime)})
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type,
    }

    conn = _get_conn(api_base)
    conn.request("POST", "/v1/audio/transcriptions", body, headers)
    res = conn.getresponse()
    try:
        data = res.read()
    except http.client.IncompleteRead as e:
        data = e.partial or b""
    finally:
        conn.close()

    if res.status != 200:
        print(f"HTTP {res.status}: {data.decode('utf-8', errors='replace')}", file=sys.stderr)
        sys.exit(1)

    resp_text = data.decode("utf-8", errors="replace")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(resp_text)
        print(f"已保存到 {args.output}")

    resp_format = args.response_format or "json"
    if resp_format == "json" or resp_format == "verbose_json":
        try:
            result = json.loads(resp_text)
            text = result.get("text", "")
            print(text)
        except json.JSONDecodeError:
            print(resp_text)
    else:
        print(resp_text)


def main():
    parser = argparse.ArgumentParser(
        description="Whisper STT CLI - 语音转文字 (whisper-large-v3-turbo)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  # 转录中文音频
  python v36-whisper-stt-cli.py transcribe audio.mp3

  # 指定英文 + SRT 格式
  python v36-whisper-stt-cli.py transcribe audio.wav -l en -f srt

  # 输出保存到文件
  python v36-whisper-stt-cli.py transcribe recording.m4a -o result.json
""")
    sub = parser.add_subparsers(dest="command", required=True)

    tr = sub.add_parser("transcribe", help="语音转文字")
    tr.add_argument("file", help="音频文件路径（flac/mp3/mp4/mpeg/mpga/m4a/ogg/wav/webm）")
    tr.add_argument("--model", default=MODEL, help=f"模型名称（默认: {MODEL}）")
    tr.add_argument("-l", "--language", default="zh", choices=LANGUAGES, help="音频语言（默认: zh）")
    tr.add_argument("-f", "--response-format", default=None, choices=FORMATS, help="输出格式（默认: json）")
    tr.add_argument("--api-base", default=None, help="API 地址")
    tr.add_argument("--token", default=None, help="API Token")
    tr.add_argument("-o", "--output", default=None, help="输出文件路径")

    args = parser.parse_args()
    if args.command == "transcribe":
        cmd_transcribe(args)


if __name__ == "__main__":
    main()
