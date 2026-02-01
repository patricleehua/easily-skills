



# OpenClaw / Clawdbot 安装与中转API替换（官方脚本）

---

## 4. 安装 Clawdbot（官方一键脚本）

使用官方提供的安装脚本部署：

```shell
curl -fsSL https://openclaw.ai/install.sh | bash
```

---

## 4.1 运行初始化向导（首次配置）提醒用户操作进行反馈

安装完成后运行：

```shell
openclaw onboard --install-daemon
```

向导主要步骤：

- 选择安全选项（理解风险）

- 配置工作区目录

- 设置 Gateway 认证方式

- 其他基本配置

---

## 4.2 检查 OpenClaw 是否安装成功

```bash
which openclaw
openclaw --version
openclaw gateway status
```

---



# 获取 Bot API（Telegram / WhatsApp 等）

你需要像 Telegram Bot / WhatsApp API 一样获取对应 Token。

## TelegramnBot 示例

- 下载telegram
- 顶部搜索`BotFather` / `@BotFather`
- 流程: send`/start` -> send  `/newbot`->pasting your bot name（It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.）-> success -> get bot info
- 获取token: 1234567:ABCDEFGHIXCXCCCCCCCC

