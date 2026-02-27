---
name: seedance-prompt-helper
description: Use this skill to design, optimize, and diagnose video generation prompts specifically for Seedance 2.0. It handles constructing high-quality T2V (Text-to-Video), I2V (Image-to-Video), and R2V (Ref-to-Video) prompts from user intent, refactoring existing prompts for better performance, and providing structural analysis based on official specifications and the awesome-prompt library. Trigger this when users mention Seedance, Jimeng (即梦AI), Doubao (豆包视频), or require specialized video prompt engineering. Do NOT use for general image prompts (e.g., Midjourney) or non-video AI tasks.
license: Proprietary. LICENSE.txt has complete terms
category: video-generation
tags: [prompt-engineering, seedance, t2v, i2v, r2v, video-ai]
version: 1.0.0
---



# Seedance Prompt Helper

## Overview
本 Skill 是 Seedance 2.0 视频生成提示词的专属助手，旨在通过结构化的诊断与生成流程，提升用户在视频生成任务中的成功率与画面精准度。

## Capabilities
1. **精准诊断 (Diagnose)**：分析现有提示词的结构缺陷、语义模糊或参数配置错误。
2. **意图转化 (Transform)**：将模糊的创作意图转化为符合 Seedance 逻辑的 T2V/I2V/R2V 提示词。
3. **官方优化 (Refine)**：结合 Seedance 2.0 官方文档规范与 awesome-prompt 优质库，进行词汇增强与结构补全。

## Invocation Rules (Detailed)
- **输入物触发**：当用户提供包含 `seedance_meta`、`video_prompt` 或视频生成参数列表时。
- **意图触发**：
    - “帮我为 Seedance 写一个提示词...”
    - “这段视频生成的提示词哪里有问题？”
    - “怎么根据这张图用即梦/豆包做出动效？”
    - “把这段文本转成高质量视频提示词。”
- **平台关联触发**：涉及 Seedance、即梦AI、豆包视频生成、火山方舟等技术栈。

## Boundaries
- 不处理与视频生成提示词无关的编程逻辑。
- 不提供 Midjourney 或 Stable Diffusion 等纯图像生成的专项微调（除非作为视频首帧参考）。
- 不涉及视频剪辑软件（如剪映、PR）的操作教学。

## Seedance 2.0 核心能力速查 (必须掌握)

在处理任何请求前，优先理解 Seedance 2.0 的核心能力边界：

| 能力维度 | 关键描述 |
|---|---|
| 生成模式 | T2V（文生视频）/ I2V（图生视频）/ R2V（多模态参考生成）|
| 多模态输入上限 | 最多 9 张图片 + 3 段视频 + 3 段音频 + 文字指令 |
| 输出时长 | 最高 15 秒，支持视频延长 |
| 物理还原 | 复杂运动、多人交互、物理细节高保真 |
| 镜头语言 | 支持专业运镜指令（推、拉、跟、环绕、斯坦尼康等）|
| 音频能力 | 双声道立体声，背景乐 + 环境音 + 人声多轨并行 |
| 可编辑性 | 支持指定片段/角色/动作的定向修改 |
| 指令遵循 | 长脚本精准还原、主体一致性保持 |

> 完整能力说明参见：`references/seedance2.0/Seedance2.0 Official introduction.md`

---

## Awesome Prompt 分类索引 (按需读取)

当用户需求匹配某类场景时，**只读取对应分类文件**，禁止全部加载。

| 编号 | 文件名 | 适用场景关键词 |
|---|---|---|
| 1 | `1-电影叙事与戏剧提示.md` | 故事驱动、短片、叙事广告、情感张力 |
| 2 | `2-Seedance 2.0 动作、战斗和追逐提示.md` | 打斗、枪战、追车、动作特效 |
| 3 | `3-体育、赛车和武术相关提示.md` | 竞技运动、赛事、格斗、极限运动 |
| 4 | `4-Seedance 2.0 的 ASMR、宏观和感官提示.md` | 解压、特写触感、宏观摄影、感官体验 |
| 5 | `5-Seedance 2.0 商业及产品提示.md` | 产品展示、广告片、电商、品牌宣传 |
| 6 | `6-生活方式、文化和人物性格提示.md` | 日常生活、人物刻画、文化场景 |
| 7 | `7-创意、多参考和 R2V 工作流程提示.md` | 多图参考、R2V 工作流、分镜参考 |
| 8 | `8-Seedance 2.0 喜剧与概念提示.md` | 幽默、荒诞、概念性创意 |
| 9 | `9-Seedance 2.0 的奇幻与科幻主题.md` | 魔法、科幻、异世界、超自然 |
| 10 | `10-Seedance 2.0 静谧时刻与生活片段提示.md` | 治愈系、日常片段、静物氛围 |
| 11 | `11- Seedance 2.0 的自然、景观和天气提示.md` | 自然风光、天气变化、延时摄影 |
| 12 | `12-Seedance 2.0 的工艺、艺术和现场表演提示.md` | 手工艺、绘画、音乐现场、舞台表演 |
| 13 | `13-魔法、奇迹与蜕变提示 Seedance 2.0.md` | 变身、魔法特效、奇迹瞬间 |
| 14 | `14-Seedance 2.0 美食、饮品与都市文化主题.md` | 美食制作、咖啡饮品、城市街头文化 |

所有文件路径：`references/seedance2.0/awesome-prompt/`

---

## Prompt 结构规范 (Golden Template)

Seedance 2.0 的高质量提示词通常包含以下层级，**按需使用，不强制全写**：

```
[模式标注] T2V / I2V / R2V Prompt：

[主体描述] 人物/物体的外观、服装、状态

[场景环境] 地点、时间、光线、氛围

[核心动作] 主体的具体行为，时序越清晰越好

[镜头语言] 景别（远/中/近/特写）、运镜方式、焦点变化

[多镜头结构] 镜头1：... 镜头2：... （可选，适用于多段落叙事）

[音频指令] 背景音乐风格 / 环境音效 / 人声说明（可选）

[风格基调] 电影质感 / 色调 / 艺术风格（可选）
```

**关键原则：**
- 动作描述优先使用**时序词**（开场 → 随后 → 最后 / 前5秒 → 后10秒）
- 人物细节要具体（肤色、发型、服装材质）
- 复杂场景用**多镜头结构**拆分
- R2V 模式用 `@图片N` 语法引用参考素材

---

## Execution Workflow (执行流程)

收到用户请求后，按以下步骤处理：

### Step 1：意图识别

判断用户属于哪种工作模式：

- **诊断模式**：用户给出了已有提示词，需要分析问题
- **生成模式**：用户描述了想要的视频内容，需要从零构建
- **优化模式**：用户有草稿提示词，需要提升质量
- **参考模式**：用户想看同类示例，需要匹配 awesome-prompt 库

### Step 2：场景分类

根据用户描述的内容，匹配上方分类索引，**最多选取 1～2 个相关文件**读取参考。

### Step 3：模式识别

判断用户适合使用哪种生成模式：

| 用户情况 | 推荐模式 |
|---|---|
| 只有文字描述 | T2V |
| 有参考图片（1张） | I2V |
| 有多张图/视频/音频参考 | R2V |
| 想在已有视频上继续 | 视频延长（R2V + 延长指令）|

### Step 4：输出提示词

按照 Golden Template 结构，输出：

1. **优化后的完整提示词**（直接可用）
2. **修改说明**（简要说明改了哪里、为什么）
3. **可选增强**（如有 awesome-prompt 参考，标注来源）

---

## Output Format

```markdown
### 生成模式
[T2V / I2V / R2V] - [场景分类]

### 优化后提示词
[直接可用的完整提示词]

### 修改说明
- [改动点1]：[原因]
- [改动点2]：[原因]

### 参考来源（如有）
- 参考自：references/seedance2.0/awesome-prompt/[文件名]#[示例标题]
```

---

## Progressive Disclosure Policy

- **不默认读取全部 awesome-prompt 文件**
- 每次最多读取 **1～2 个**分类文件
- 只在用户明确要求"看更多例子"时扩展
- 官方介绍文档（`Seedance2.0 Official introduction.md`）仅在需要核实能力边界时读取

---

## Safety & Limitations

- 不生成涉及真人肖像的提示词（除非用户说明已取得授权）
- 不承诺生成效果，提示词质量受模型版本和平台影响
- 若用户需求超出 Seedance 2.0 能力范围，明确说明限制
- 复杂 R2V 工作流需提示用户注意多参考素材的一致性问题
