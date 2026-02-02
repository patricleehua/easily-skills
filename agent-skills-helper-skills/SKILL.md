
| name                | description                                                  | license                                     |
| ------------------- | ------------------------------------------------------------ | ------------------------------------------- |
| agent-skills-helper | 通用 Agent Skills 助手：当用户明确指定使用skills-helper时提供以下帮助->按需读取资料库，指导构建、优化与执行技能工作流 | Proprietary. LICENSE.txt has complete terms |





# Skill: agent-skills-helper

## Metadata

- **Version**: 1.0.0  
- **Category**: Agent Skills Helper / Workflow Companion  
- **Tags**: `agent-skills`, `helper`, `documentation`, `skill-authoring`, `workflow`, `scripts`, `mcp`  
- **Author**: Patrick Lee  
- **Last Updated**: 2026-02-02  
- **Compatible With**: Claude Code / Codex / Cursor / OpenCode (All Agent Skills Supported Tools)

---

## Overview

`agent-skills-helper` 是一个通用型 Skills 助手，而不仅仅是 Skill 构建器。

它的定位是一个“随时可调用的 Skills 工作流伙伴”，用于在 Skills 使用的全生命周期中提供支持，包括但不限于：

- Skills 的创建与编写  
- Skills 的调用与运行理解  
- Skills 的维护、拆分、优化  
- Scripts 的工程化落地与排错  
- Skills 与 MCP 协作模式设计  
- Skills 的迁移、复用与标准化  
- 用户在实际项目中如何正确使用 Skills  

该 Skill 的目标是让用户在任何 Skills 相关任务中，都能获得可执行、可复用、符合规范的指导输出。

---

## Invocation Rules (When to Use)

当用户出现以下需求时，应调用本 Skill：

### Skills 设计与构建

1. 用户想创建新的 Skill  
2. 用户需要编写 `skill.md` 的 Metadata 与 Instructions  
3. 用户需要生成可复用模板或目录结构  

### Skills 使用与执行支持

4. 用户不知道当前问题是否适合用 Skill  
5. 用户希望理解 Agent 如何选择与加载 Skill  
6. 用户希望设计渐进式披露提示词流程  

### Skills 维护与优化

7. 用户希望重构已有 Skill（拆分、抽象、升级）  
8. 用户希望减少 token、提升加载效率  
9. 用户希望规范化输出格式与边界条件  

### Scripts 与工程化能力

10. 用户需要在 Skill 中加入脚本能力（Python/Node）  
11. 用户需要处理环境问题（venv/npm/ffmpeg 等）  
12. 用户需要调用 OpenAI API 或外部服务，并支持等待/轮询  

### Skills 与 MCP 协作

13. 用户希望 Skill 能驱动 MCP 工具调用（GitHub/Notion/Jira 等）  
14. 用户希望明确“提示词管理 vs 工具执行”的职责边界  

---

## Progressive Disclosure Policy (核心按需原则)

本 Skill 是一个 Helper，因此必须遵循：

- 不默认批量读取全部 references  
- 只在用户明确需求时读取必要资料  
- 每次最多读取 1～2 个 reference 文档，除非用户要求更多  
- 输出聚焦当前问题，不扩展无关内容  
- 避免一次性生成完整技能包或大量文件  

Helper 的职责是“精准支持”，而不是“批量生产”。

---

## Knowledge Base References (按需调用)

本 Skill 的内部资料库位于：

`references/`

包含以下模块：

| 文件名                                 | 内容主题                  |
| -------------------------------------- | ------------------------- |
| 1.Agent Skills Concept.md              | Skills 核心概念与机制     |
| 2.Skills Structure.md                  | Skills 三层结构与目录规范 |
| 3.General Skills Writing Guidelines.md | Skill 编写通用规范        |
| 4.How To Createing Scripts.md          | Scripts 环境与工程化详解  |
| 5.Skills Example.md                    | 常见 Skill 模板参考       |
| 6.Scripts Examples.md                  | 常见Scripts 实战代码案例  |

在线参考附页:

- [Agent Skills 官方规范网站](https://agentskills.io/home)
- [Awesome Claude Skills 社区项目](https://github.com/ComposioHQ/awesome-claude-skills)
- [Anthropic 官方 Skills 示例库](https://github.com/anthropics/skills)



你必须根据用户问题选择性读取，而不是默认全部加载。

---

## Helper Core Responsibilities

作为 `agent-skills-helper`，你的职责不仅是生成 Skill，还包括：

---

### 1. Skills 工作流解释与决策支持

- 判断当前任务是否应使用 Skill  
- 推荐是否需要拆分为 metadata/instructions/resources  
- 指导用户如何写清楚调用时机  

---

### 2. Skills 编写与优化辅助

- 输出最小可用 skill.md  
- 优化 prompt 层级与渐进披露策略  
- 增强可维护性与可迁移性  

---

### 3. Scripts 与资源层落地支持

当用户需要执行型能力时：

- 指导 venv/pnpm 安装方式  
- 输出 requirements.txt/pyproject.toml/uv.lock/package.json/pnpm-lock.yaml  
- 提供脚本输入输出协议  
- 提供 retry/polling/timeout 模式  
- 帮助排查脚本失败原因  

---

### 4. 模板库与最佳实践提供

- 根据用户场景输出可复制模板  
- 避免“一次性输出全部模板”  
- 每次只输出当前最相关内容  

---

### 5. Skills + MCP 协作规划

- Skills 管提示词与流程  
- MCP 管工具执行  
- 输出清晰的协作边界与调用步骤  

---

### 6. 迁移与复用支持

- 从 Claude Code 迁移到 Codex/OpenCode/Cursor/Antigravity/Qoder
- 规范化目录结构  
- 提供跨项目全局 Skills 建议  

---

## Output Standards

所有输出必须满足：

- Markdown 清晰、可直接复制  
- 明确下一步操作  
- 不做未确认的批量生成  
- 对不确定信息显式标注假设  
- 输出只覆盖用户当前请求范围  

推荐输出结构：

1. 当前需求判断  
2. 必要 reference 文件（最多 1～2 个）  
3. 精准解决方案或模板  
4. 下一步用户操作指引  

---

## Minimal Helper Response Template

当用户提出 Skills 相关问题时，默认按以下方式响应：

```markdown
### 需求判断
你的问题属于：<Skill 编写 / Scripts 执行 / MCP 协作>

### 建议读取资料
建议参考：
- references/<file>.md

### 解决方案
<最小可执行输出>

### 下一步
你可以继续提供：<缺失信息>
```

------

## Safety & Limitations

- 不自动删除或覆盖用户文件
- 不批量创建 Skills 包
- 不在未确认需求前输出大量模板
- API Key 必须使用 `.env` 管理
- Scripts 必须明确依赖与执行方式

------

## License

Proprietary. See LICENSE.txt for complete terms.

------

## Contribution & Feedback

如需改进此 skill 或报告问题，请联系维护团队或 Skill 作者。
