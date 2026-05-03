---
name: v36-api-tools
description: Execute v36-api CLI scripts for image generation, image editing, and speech-to-text transcription via NanoBanana / GPT-Image-2 / Whisper API. Use this skill when the user asks to generate images from text prompts, edit images with prompts, transcribe audio to text, use NanoBanana/nano-banana-pro/gpt-image-2/whisper models, or requests any v36-api related operations. Triggers on mentions of v36-api, nanobanana, gpt-image-2, whisper, text-to-image, image-to-image, speech-to-text, audio transcription, or when user wants to run v36 CLI scripts. Do NOT use for text-to-speech, video processing, or non-v36 API tasks.
tags: [image-generation, nanobanana, gpt-image-2, whisper, speech-to-text, v36-api, cli]
---

# v36-api-tools

通过 CLI 脚本调用 v36-api 接口，当前支持 NanoBanana / GPT-Image-2 图片生成与编辑，以及 Whisper 语音转文字。

## 环境要求

- Python 3.9+
- 可选依赖: `python-dotenv`（用于加载 .env）
- 环境变量: `NANOBANANA_TOKEN`（必须）, `NANOBANANA_API_BASE`（可选，默认 api.gpt.ge）

## 脚本调用规则

### NanoBanana CLI (nanobanana-cli)

脚本路径: `scripts/v36-nanobanana-cli.py`

**文生图 (generate)**

```bash
python scripts/v36-nanobanana-cli.py generate "<提示词>" --model nano-banana --size "2:3" --response-format url -d <下载目录>
```

**图生图 (edit)**

```bash
python scripts/v36-nanobanana-cli.py edit "<编辑提示词>" --model nano-banana --response-format url -d <下载目录> -- <图片1> <图片2>
```

**重要**: 必须加 `--response-format url`，避免 API 返回 2MB+ base64 导致传输中断。脚本默认已设为 url。

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model` | 模型名称（见下表） | nano-banana |
| `--size` | 图片尺寸或比例 | - |
| `--aspect-ratio` | 宽高比（仅 pro/gemini-3+ 系列可用） | - |
| `--response-format` | url 或 b64_json | url |
| `--download`, `-d` | 图片下载目录 | - |
| `--output`, `-o` | JSON 输出文件路径 | - |
| `--token` | API Token（优先用环境变量） | - |
| `--api-base` | API 地址 | api.gpt.ge |

### 可用模型

| 模型 | 系列 | size 支持 |
|------|------|-----------|
| `nano-banana` | gemini-2.5-flash-image | 比例: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |
| `nano-banana-pro` | gemini-3-pro-image-preview | 1K, 2K, 4K |
| `nano-banana-pro-2k` | gemini-3-pro-image-preview (2K) | 比例（尺寸固定 2K） |
| `nano-banana-pro-4k` | gemini-3-pro-image-preview (4K) | 比例（尺寸固定 4K） |
| `gemini-2.5-flash-image` | gemini-2.5 | 比例 |
| `gemini-3-pro-image-preview` | gemini-3 | 1K, 2K, 4K |
| `gemini-3.1-flash-image-preview` | gemini-3.1-flash | 0.5K, 1K, 2K, 4K |
| `gemini-3.1-flash-image-preview-0.5k` | gemini-3.1-flash (0.5K) | 比例 |
| `gemini-3.1-flash-image-preview-2k` | gemini-3.1-flash (2K) | 比例 |
| `gemini-3.1-flash-image-preview-4k` | gemini-3.1-flash (4K) | 比例 |

### size 使用规则

- **nano-banana / gemini-2.5 系列**: `--size "2:3"` 传比例
- **pro / gemini-3+ 系列**: `--size 4K --aspect-ratio "16:9"` 传分辨率+比例
- **模型名带 -2k/-4k 后缀的**: 不需要传 aspect_ratio，尺寸已固定，只需传比例

### GPT-Image-2 CLI (gpt-image-2-chat-cli)

脚本路径: `scripts/v36-gpt-image-2-chat-cli.py`

走 `/v1/chat/completions` 端点，默认流式输出，实时显示生成进度。

**文生图 (generate)**

```bash
python scripts/v36-gpt-image-2-chat-cli.py generate "<提示词>" -d <下载目录>
```

**图生图 (edit)**

```bash
python scripts/v36-gpt-image-2-chat-cli.py edit "<编辑提示词>" -d <下载目录> -- <图片1> [图片2 ...]
```

### GPT-Image-2 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model` | 模型名称（见下表） | gpt-image-2-c |
| `--max-tokens` | 最大 tokens | 3800 |
| `--download`, `-d` | 图片下载目录 | - |
| `--output`, `-o` | JSON 输出文件路径 | - |
| `--no-stream` | 禁用流式输出 | 默认流式 |
| `--token` | API Token（优先用环境变量） | - |
| `--api-base` | API 地址 | api.gpt.ge |

### GPT-Image-2 可用模型

| 模型 | 说明 |
|------|------|
| `gpt-image-2-c` | GPT-Image-2（默认） |
| `gpt-image-2` | GPT-Image-2 原始模型名 |

### 响应格式

- 流式模式下实时显示进度（`🏃 进度：xx%`），完成后输出 `![image](url)` markdown 格式的图片链接
- 图片 URL 自动从 content 中提取，配合 `-d` 参数下载到本地

### Whisper STT CLI (whisper-stt-cli)

脚本路径: `scripts/v36-whisper-stt-cli.py`

走 `/v1/audio/transcriptions` 端点，将音频文件转为文字。

**语音转文字 (transcribe)**

```bash
# 默认中文转录
python scripts/v36-whisper-stt-cli.py transcribe <音频文件>

# 指定英文 + SRT 格式
python scripts/v36-whisper-stt-cli.py transcribe <音频文件> -l en -f srt

# 保存结果到文件
python scripts/v36-whisper-stt-cli.py transcribe <音频文件> -o result.json
```

### Whisper 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-l`, `--language` | 音频语言（zh/en/de/es） | zh |
| `-f`, `--response-format` | 输出格式（json/text/srt/verbose_json/vtt） | json |
| `--model` | 模型名称 | whisper-large-v3-turbo |
| `-o`, `--output` | 输出文件路径 | - |
| `--token` | API Token（优先用环境变量） | - |
| `--api-base` | API 地址 | api.gpt.ge |

### 支持的音频格式

| 格式 | 扩展名 | 大小限制 |
|------|--------|----------|
| FLAC | .flac | 25MB |
| MP3 | .mp3 | 25MB |
| MP4 Audio | .mp4, .m4a | 25MB |
| MPEG | .mpeg, .mpga | 25MB |
| OGG | .ogg | 25MB |
| WAV | .wav | 25MB |
| WebM | .webm | 25MB |

## 扩展方式

后续新增 v36-api 脚本时：
1. 将脚本放入 `scripts/` 目录
2. 在本文件中补充对应的调用规则说明
