---
name: openclaw-helper
description: >
  Use this skill when the user needs troubleshooting or configuration help
  with OpenClaw / ClawBot / BoltBot (e.g., installation failures, runtime errors,
  trigger misfires, bot integration, MCP connection issues).
  Always check local OpenClaw docs first; if not found, perform a web search.
  Ask follow-up questions when needed and provide step-by-step executable fixes.
  Do NOT use for general coding questions unrelated to OpenClaw.
license: Proprietary. LICENSE.txt has complete terms
version: 1.0.0
category: Assessment / Support
tags: [openclaw, clawbot, boltb ot, troubleshooting, docs]
author: Nomor Internal
last_update: 2026-02-01
---




# Skill: openclaw-helper

## Description

`openclaw-helper` 是专为解决用户在使用 **OpenClaw / ClawBot / BoltBot** 过程中可能遇到的各类问题而设计的辅助技能。

它的核心目标是：

- 快速理解用户问题
- 优先查阅本项目已有知识库（docs 文件夹）
- 提供现实、准确、可执行的解决方案
- 在缺少信息时主动与用户交互补充
- 必要时引导用户访问官方资源

该 Skill 主要作为一份“动态帮助文档系统”，结合内部资料 + 外部信息，为用户实现需求。

------

## Skill Directory Structure

```
skills/openclaw-helper/
│
├── skill.md                  # Skill 主说明（本文件）
├── LICENSE.txt               # Proprietary License
│
├── docs/                     # 核心知识库（优先检索）
│   ├── Action-Browser-Relay.md
│   ├── Minefield (Common Pitfalls).md
│   ├── OpenClaw-Installed.md
│   └── Using-Customer-Models-Api.md
│
├── examples/                 # 示例对话/案例（可后续补充）
│
└── manifest.yaml (optional)  # Skill 注册信息（如系统需要）
```

------

## Knowledge Sources Priority

当用户提出问题时，必须按照以下顺序查找信息：

### 1. 本地 Skill Docs（最高优先级）

Skill 在 `docs/` 下维护的文件包括：

- **OpenClaw-Installed.md**
   → 安装、部署、环境配置问题
- **Minefield (Common Pitfalls).md**
   → 常见坑、错误模式、注意事项
- **Action-Browser-Relay.md**
   → Browser Relay 激活/插件相关问题
- **Using-Customer-Models-Api.md**
   → 如何接入用户自定义模型 API

Skill 必须动态检索这些文件内容并使用其中知识回答。

------

### 2. 官方互联网资源（次优先）

若 docs 中未覆盖用户问题，则：

- 去互联网检索 OpenClaw 官方文档/issue/论坛
  - [OpenClaw 官网](https://openclaw.ai/)
  - [官方帮助文档](https://docs.openclaw.ai/)
  - [Only-Agent社区](https://clawbook.fun/)
- 优先引用可信来源（官网、GitHub、官方 FAQ）

同时建议用户参考：

- 官方文档入口（可提供 URL）
- Release Notes / Known Issues

------

### 3. 用户交互排查（信息不足时）

如果仍然无法定位问题，Skill 必须主动询问用户补充信息（需要给出如何具体获取的操作/或者自行去执行命令），例如：

- 报错日志全文
- 当前版本号
- 配置文件片段
- 操作步骤复现路径
- 系统环境（Linux/Windows/Docker）

并通过比对用户信息逐步推理定位。

------

### 4. 用户提供材料后即时完善

当用户提供新资料后：

- Skill 应立即整合到当前排查逻辑中
- 输出更准确的解决方案
- 必要时提示用户将信息补充进 docs 形成知识闭环

------

## Supported Capabilities

### Troubleshooting

Skill 可帮助解决：

- OpenClaw 安装失败
- ClawBot/BoltBot 启动异常
- Action Relay 配置错误
- API 调用失败
- 常见 Minefield 陷阱问题

------

### Configuration Assistance

若用户提出：

> “我需要修改配置”

Skill 可以：

- 指导用户定位配置文件路径
- 给出推荐配置片段
- 解释参数含义
- 提醒修改后的验证步骤

但不会直接修改用户系统，仅提供操作建议。

------

### Official Reference Guidance

若 Skill 无法获取足够上下文：

- 可以明确说明 docs 未覆盖
- 引导用户去官网查阅
- 用户可复制内容回来继续分析

示例：

> “你可以打开官方文档这一节，把相关段落复制给我，我可以继续帮你排查。”

------

## Interaction Pattern (Standard Workflow)

Skill 必须遵循以下工作流：

```
1. 理解用户问题
2. 检索 docs/ 内最相关文件
3. 若找到 → 引用并给解决方案
4. 若未找到 → 搜索互联网官方资料
5. 若仍无法定位 → 向用户索要日志/配置/步骤
6. 用户补充 → 再分析 → 输出最终方案
7. 必要时沉淀进 docs
```

------

## Example User Queries

### 安装类

> “OpenClaw 安装时报错 missing dependency”

→ 查 `OpenClaw-Installed.md`

------

### Action Relay 类

> “Browser relay 连不上”

→ 查 `Action-Browser-Relay.md`

------

### 常见坑

> “运行没报错但行为不对”

→ 查 `Minefield (Common Pitfalls).md`

------

### 用户模型接入

> “怎么接自己的模型 API？”

→ 查 `Using-Customer-Models-Api.md`

---

**License**: Proprietary. See LICENSE.txt for complete terms.