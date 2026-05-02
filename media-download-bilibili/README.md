# bili - B站视频下载与媒体处理

## 安装

```bash
cd scripts
uv sync
```

安装人声分离支持：

```bash
uv sync --extra vocals
```

## 使用

```bash
# 下载视频
uv run bili --url "https://www.bilibili.com/video/BV1xx..."

# 预览不下载
uv run bili --url "https://www.bilibili.com/video/BV1xx..." --dry-run

# 下载并提取高质量 MP3
uv run bili --url "..." --audio-only --audio-quality high

# 下载UP主视频（限10个）
uv run bili --space 123456 --max-count 10 --audio-only

# 提取人声
uv run bili --url "..." --audio-only --vocals

# 查看所有参数
uv run bili --help
```

## 环境要求

- Python >= 3.11
- yt-dlp（自动安装）
- ffmpeg（需手动安装）
- demucs（可选，人声分离）
