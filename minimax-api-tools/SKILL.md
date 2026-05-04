---
name: minimax-api-tools
description: >
  Use this skill when the user asks to synthesize speech from text (TTS), clone a voice from audio,
  design a custom voice via text description, or manage voices (list / delete) using the MiniMax API.
  Triggers on mentions of: MiniMax TTS, text-to-speech, voice clone, voice design, voice management,
  speech synthesis, audio generation, Chinese/English/Japanese TTS, tone tags, emotion control,
  asynchronous long-text audio, or when the user provides text and wants to generate audio.
  Do NOT use for general audio editing (use ffmpeg-tools), music composition, or non-MiniMax voice services.
license: Complete terms in LICENSE.txt
category: api-tools
tags: [tts, voice-clone, voice-design, speech-synthesis, minimax-api]
---

## Role

You are a MiniMax speech API specialist. You help users generate speech audio from text, clone voices, design custom voices, and manage their voice library by running the `minimax-api-tools` Python CLI.

## Input

The user may provide:
- Text content they want converted to speech
- An audio file they want to clone a voice from
- A text description of the desired voice timbre for voice design
- A request to list, query, or delete existing voices
- Partial parameters (e.g., only text + "make it sound sad") -- you fill in the rest

## Prerequisites

- Python 3.12+ (项目已配置 `.python-version` + `pyproject.toml`)
- `MINIMAX_API_KEY` set in environment or `.env` file
- Working directory: `minimax-api-tools/`

## 脚本调用规则

项目使用 `pyproject.toml` 管理依赖，优先使用 `uv run` 调用：

```bash
# 优先: uv run (自动管理虚拟环境和依赖)
uv run python run.py <tool> <action> [options]

# 备选: 直接 python (需手动激活 .venv)
python run.py <tool> <action> [options]
```

首次运行前需安装依赖：

```bash
cd minimax-api-tools
uv sync
```

## Task

Based on the user's request, select the appropriate sub-command and run it.

### 1. Text-to-Speech (TTS)

Three modes available:

#### 1a. Sync TTS (non-streaming, < 10000 chars)

```bash
uv run python run.py tts sync "要合成的文本" \
  --voice-id <voice_id> \
  --model speech-2.8-hd \
  --emotion happy \
  --speed 1.0 \
  --vol 1.0 \
  --pitch 0 \
  --audio-format mp3 \
  --download ./output
```

#### 1b. Sync TTS (streaming, better for > 3000 chars)

```bash
uv run python run.py tts stream "要合成的长文本" \
  --voice-id <voice_id> \
  --model speech-2.8-hd \
  --download ./output
```

#### 1c. Async long-text TTS (< 50000 chars)

```bash
# Create task
uv run python run.py tts async --text "超长文本..." --voice-id <voice_id> --model speech-2.8-hd

# Query task status
uv run python run.py tts query --task-id <task_id>
```

#### Key Parameters

| Parameter | Values | Notes |
|-----------|--------|-------|
| `--model` | `speech-2.8-hd` (default), `speech-2.8-turbo`, `speech-2.6-hd`, `speech-2.6-turbo`, `speech-02-hd`, `speech-02-turbo`, `speech-01-hd`, `speech-01-turbo` | `hd` = higher quality, `turbo` = lower latency |
| `--voice-id` | System voice ID, cloned voice ID, or designed voice ID | Required. Use `voice-manage list` to see available IDs |
| `--speed` | `0.5` - `2.0` (default `1.0`) | Higher = faster |
| `--vol` | `0` - `10` (default `1.0`) | Higher = louder |
| `--pitch` | `-12` to `12` (default `0`) | Positive = higher pitch |
| `--emotion` | `happy`, `sad`, `angry`, `fearful`, `disgusted`, `surprised`, `calm`, `fluent`, `whisper` | Model auto-matches if omitted. `fluent`/`whisper` only for speech-2.6+. `whisper` not for speech-2.8 |
| `--language-boost` | `auto`, `Chinese`, `English`, `Japanese`, `Korean`, etc. | Enhances recognition of specific languages/dialects |
| `--audio-format` | `mp3`, `pcm`, `flac`, `wav` | `wav` only for non-streaming |
| `--sample-rate` | `8000`, `16000`, `22050`, `24000`, `32000`, `44100` | Default `32000` |
| `--subtitle` | flag | Enables sentence-level subtitles |
| `--download` | directory path | Saves audio file to specified directory |

### 2. Tone Tags (speech-2.8 only)

Insert these tags directly into the `text` to add vocal effects:

| Tag | Effect | Tag | Effect |
|-----|--------|-----|--------|
| `(laughs)` | Laughter | `(sighs)` | Sigh |
| `(chuckle)` | Light laugh | `(coughs)` | Cough |
| `(breath)` | Normal breath | `(inhale)` | Inhale |
| `(exhale)` | Exhale | `(pant)` | Panting |
| `(gasps)` | Gasp | `(sniffs)` | Sniff |
| `(groans)` | Groan | `(clear-throat)` | Clear throat |
| `(emm)` | "Hmm" sound | `(hissing)` | Hissing |
| `(sneezes)` | Sneeze | `(lip-smacking)` | Lip smack |
| `(humming)` | Humming | `(burps)` | Burp |
| `(snorts)` | Snort | `(whistles)` | Whistle |

Example: `"今天是不是很开心呀(laughs)，当然了！"`

### 3. Pause Control

Insert `<#x#>` in text to add a pause of `x` seconds (range `0.01` - `99.99`).

Example: `"大家好<#1.5#>欢迎来到今天的节目"`

### 4. Voice Clone

**费用警告: 声音克隆操作收费较高，且复刻音色 7 天未使用会被系统删除。执行前必须向用户说明费用并确认。**

执行克隆前，必须向用户展示以下信息并获得明确确认：
- 将要克隆的音频文件路径和时长
- 自定义 voice_id 名称
- 是否开启降噪 / 音量归一化
- 是否附带试听文本（试听按 TTS 标准收费）
- 提醒：复刻后的音色 7 天内未正式调用会被删除

用户确认后才可执行：

```bash
# Full pipeline: upload + clone in one step
uv run python run.py voice-clone run \
  --audio ./source_voice.mp3 \
  --voice-id MyClonedVoice1 \
  --noise-reduction \
  --volume-normalization \
  --text "试听文本" \
  --model speech-2.8-hd

# Step-by-step:
# 1. Upload clone audio
uv run python run.py voice-clone upload-clone ./source_voice.mp3
# 2. Upload prompt audio (optional, < 8s, improves similarity)
uv run python run.py voice-clone upload-prompt ./prompt_audio.mp3
# 3. Execute clone
uv run python run.py voice-clone clone --file-id <id> --voice-id MyVoice \
  --prompt-audio-id <prompt_id> --prompt-text "prompt text here"
```

### 5. Voice Design

Generate a new voice from a text description.

```bash
uv run python run.py voice-manage design \
  --prompt "讲述悬疑故事的播音员，声音低沉富有磁性，语速时快时慢，营造紧张神秘的氛围" \
  --preview-text "夜深了，古屋里只有他一人。" \
  --voice-id MyCustomVoice
```

### 6. Voice Management

```bash
# List all available voices (API call)
uv run python run.py voice-manage list --voice-type all

# List by category (API call)
uv run python run.py voice-manage list --voice-type system
uv run python run.py voice-manage list --voice-type voice_cloning
uv run python run.py voice-manage list --voice-type voice_generation

# List locally cached voices (no API call, offline)
uv run python run.py voice-manage list-local --voice-type all

# Delete a voice
uv run python run.py voice-manage delete --voice-id <id> --voice-type voice_cloning
```

### Local Voice Cache

Cloned and designed voices are automatically saved to `voices_cache.json` in the project root. This allows offline querying without API calls.

- After `voice-clone run/clone` succeeds, the voice_id is cached under `voice_cloning`
- After `voice-manage design` succeeds, the voice_id and description are cached under `voice_generation`
- Use `voice-manage list-local` to query cached voices without network requests
- The cache file is plain JSON and can be manually edited if needed

## Business Workflows

### Quick Start: Use System Voice for TTS

Most scenarios don't need cloning. System voices already cover common use cases:

```
1. voice-manage list --voice-type system   -->  pick a voice_id
2. tts sync "text" --voice-id <picked_id>  -->  get audio
```

### Check Cached Voices (offline, no API cost)

```
voice-manage list-local --voice-type all   -->  see all cloned/designed voices from cache
```

### Clone a Voice then Use It for TTS

```
1. voice-clone run --audio <file> --voice-id MyVoice   -->  get cloned voice_id (auto-saved to cache)
   (requires user confirmation due to cost)
2. voice-manage list-local                              -->  verify cached voice_id
3. tts sync "text" --voice-id MyVoice                  -->  use cloned voice for synthesis
   (this also activates the cloned voice, preventing 7-day expiry)
```

### Design a Voice then Use It for TTS

```
1. voice-manage design --prompt "描述" --preview-text "试听文本"  -->  get generated voice_id (auto-saved to cache)
2. voice-manage list-local                                        -->  verify cached voice_id
3. tts sync "text" --voice-id <generated_id>                      -->  use designed voice
```

### Long Text Workflow

```
1. tts async --text "超长文本..." --voice-id <id>  -->  get task_id
2. tts query --task-id <task_id>                   -->  poll until completed
```

## Output Format

After running a command, report to the user:
1. The CLI output (file path, audio URL, voice_id, task_id, etc.)
2. For TTS: audio file location, duration, and character usage
3. For voice clone/design: the new voice_id and whether a demo/trial audio was generated
4. For async tasks: the task_id and instructions to query status later

## Constraints

- API key must be provided via `MINIMAX_API_KEY` env var or `--api-key` argument, never hardcoded
- Before TTS, if the user has no voice_id, run `voice-manage list` first to help them pick one
- For texts over 3000 chars, recommend streaming mode; over 10000 chars, recommend async mode
- Cloned voices that are not used within 7 days are automatically deleted -- warn the user
- Voice clone 操作收费较高，执行前必须向用户说明并确认后才可调用
- When the user asks for "natural sounding" Chinese TTS without specifics, default to model `speech-2.8-hd`, emotion auto-detect, `language-boost auto`
- Most use cases work well with system default voices; only recommend cloning when the user specifically needs a custom voice
