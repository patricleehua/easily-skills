---
name: bili-download
description: >
  Use this skill when the user wants to **download Bilibili videos**, **extract audio from B站视频**,
  or **separate vocals from downloaded audio**. Triggers on mentions of bilibili download,
  B站下载, B站音频提取, 人声分离, or when the user provides a bilibili URL and asks to save media.
  Do NOT use for general video downloading from other platforms or unrelated media tasks.
license: Apache-2.0
---

## Skill 说明

B站视频下载与媒体处理工具，支持：

1. 单视频 / UP主批量下载（yt-dlp）
2. 视频提取 MP3 音频（ffmpeg）
3. 人声分离，去除背景音乐（demucs，可选）

---

## 环境要求

### 必需依赖

- Python >= 3.11
- yt-dlp（B站视频下载）
- ffmpeg（音视频处理）

### 可选依赖

- torch + demucs + soundfile（人声分离，安装: `uv sync --extra vocals`）

### 环境自检

运行脚本前，确认环境就绪：

```bash
uv run python scripts/check_env.py
```

---

## 脚本调用

### 入口

```
scripts/cli.py::main
```

优先使用 `uv run bili`，无 uv 时可直接 `python -m scripts.cli`。

### 1. 首次安装

```bash
uv sync          # 或 pip install -e .
```

安装人声分离支持：

```bash
uv sync --extra vocals   # 或 pip install -e ".[vocals]"
```

### 2. 基本用法

```bash
# 下载视频
uv run bili --url "https://www.bilibili.com/video/BV1xx..."

# 预览不下载（dry-run）
uv run bili --url "https://www.bilibili.com/video/BV1xx..." --dry-run

# 下载并提取高质量 MP3，不保留视频
uv run bili --url "https://www.bilibili.com/video/BV1xx..." --audio-only --audio-quality high

# 下载并提取音频，同时保留视频
uv run bili --url "https://www.bilibili.com/video/BV1xx..." --keep-video

# 提取人声（需 demucs）
uv run bili --url "https://www.bilibili.com/video/BV1xx..." --audio-only --vocals

# 下载UP主全部投稿（限制10个）
uv run bili --space 123456 --max-count 10 --audio-only

# 指定输出目录
uv run bili --url "..." -o /path/to/output

# 使用浏览器 cookies（大会员视频）
uv run bili --url "..." --cookies chrome

# 指定 cookies 文件
uv run bili --url "..." --cookies-file cookies.txt

# 显示详细输出
uv run bili --url "..." --verbose
```

### 3. 完整参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url URL` | B站视频链接 | 必填（与 --space 二选一） |
| `--space UID` | UP主UID，下载全部投稿 | 必填（与 --url 二选一） |
| `-o, --output DIR` | 输出目录 | `./bili_downloads` |
| `--audio-only` | 只保留 MP3，删除视频 | false |
| `--keep-video` | 提取音频同时保留视频 | false |
| `--vocals` | 生成纯人声（需 demucs） | false |
| `--all-pages` | 下载合集所有分P | false |
| `--max-count N` | UP主下载上限 | 0（不限制） |
| `--cookies BROWSER` | 浏览器 cookies（chrome/edge/firefox） | 无 |
| `--cookies-file FILE` | cookies.txt 文件路径 | 无 |
| `--audio-quality` | 音频质量：low/medium/high | medium |
| `--vocal-format` | 人声格式：mp3/wav | mp3 |
| `--verbose` | 显示详细输出 | false |
| `--dry-run` | 只显示计划不执行 | false |

---

## 输出约定

### 目录结构

```
bili_downloads/
├── BV1xx_Python教程/
│   ├── BV1xx_Python教程.mp4
│   ├── BV1xx_Python教程.mp3
│   └── ...
├── vocals/
│   └── BV1xx_Python教程_vocals.mp3
└── .bili_resume.json
```

### 断点续传

`.bili_resume.json` 记录已完成的下载/提取/人声分离状态，重复运行自动跳过已完成项。

### stdout 输出

- `[DL]` 下载进度
- `[OK]` 操作成功
- `[FAIL]` 操作失败
- `[SKIP]` 跳过（依赖缺失）
- `[WARN]` 警告

### 失败约定

- stderr 输出错误详情（`--verbose` 模式）
- exit code 非 0
- 缺少必需依赖时立即退出并提示安装方式
- 缺少可选依赖时跳过对应功能并打印 `[SKIP]`

---

## 约束

- yt-dlp 和 ffmpeg 为硬依赖，缺失时不可运行
- demucs 为可选依赖，缺失时跳过人声分离而非退出
- 文件名自动清理非法字符，BV号前缀避免重名
- 不硬编码任何密钥或敏感信息
