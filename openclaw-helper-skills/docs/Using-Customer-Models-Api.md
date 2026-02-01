# 替换原有 API 配置（重点）

配置目录：

```bash
~/.openclaw
```

主配置文件：

```bash
~/.openclaw/openclaw.json
```

---

## 备份配置文件（必须）

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
```

---

## 配置生效

```bash
source ~/.bashrc
```

---

# 配置环境变量（API Key）

追加到 bashrc：

```bash
echo 'export CLOUDCODE_API_KEY="sk-4596409ffbe2451a9a18ab3d8fdcee80"' >> ~/.bashrc
```

重新加载：

```bash
source ~/.bashrc
```

确认是否写入：

```bash
tail -n 2 ~/.bashrc
```

---



# 示例中转信息（已验证格式可用）

**请替换以下信息为自己的**

- **中转 API**：`http://137.0.0.1:8001/v1/messages`

- **协议**：Anthropic Messages（`/v1/messages`）

- **模型名**：`sonnet4.5`

- **认证**：`Authorization: Bearer <key>`

---

## OpenClaw 内必须写成：

- `api: "anthropic-messages"`

- `baseUrl: "http://137.0.0.1:8001"`（不要带 `/v1`）

- `models[].id: "sonnet4.5"`

---

# 最重要映射关系（官方 Sonnet4.5 替换）

**其他厂商/模型同理接入**

| 官方目标                 | 你中转暴露                          | OpenClaw 配置位置                     |
| ------------------------ | ----------------------------------- | ------------------------------------- |
| Claude Sonnet 4.5        | `model="sonnet4.5"`                 | `models.providers.proxy.models[0].id` |
| Anthropic `/v1/messages` | `http://137.0.0.1:8001/v1/messages` | `baseUrl` + `api: anthropic-messages` |

---

## baseUrl 拼接规则（必须记住）

- OpenClaw 会自动请求 `/v1/messages`

- 所以 baseUrl 必须是：

```bash
http://137.0.0.1:8001
```

否则写成：

```bash
http://137.0.0.1:8001/v1
```

会变成：

```
/v1/v1/messages ❌ 必挂
```



# 配置第三方 API（Proxy 中转）

⚠️ 以下 JSON 为关键配置，你数据不改，仅整理：

```json
{
  "meta": {
    "lastTouchedVersion": "2026.1.29",
    "lastTouchedAt": "2026-01-31T15:36:46.415Z"
  },
  "env": { "shellEnv": { "enabled": true } },

  "wizard": {
    "lastRunAt": "2026-01-31T14:51:39.357Z",
    "lastRunVersion": "2026.1.29",
    "lastRunCommand": "onboard",
    "lastRunMode": "local"
  },

  "auth": {
    "profiles": {
      "anthropic:default": {
        "provider": "anthropic",
        "mode": "api_key"
      }
    }
  },

  "agents": {
    "defaults": {
      "workspace": "/root/.openclaw/workspace",
      "compaction": { "mode": "safeguard" },
      "maxConcurrent": 4,
      "subagents": { "maxConcurrent": 8 },

      "model": {
        "primary": "proxy/sonnet4.5"
      }
    }
  },

  "models": {
    "mode": "merge",
    "providers": {
      "proxy": {
        "baseUrl": "http://35.212.251.72:8045",
        "apiKey": "${CLOUDCODE_API_KEY}",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "sonnet4.5",
            "name": "Claude Sonnet 4.5 Proxy",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 65536
          }
        ]
      }
    }
  },

  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",
      "botToken": "（建议你尽快更换）",
      "groupPolicy": "allowlist",
      "streamMode": "partial"
    }
  },

  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan",
    "controlUi": { "allowInsecureAuth": true },
    "auth": { "mode": "token", "token": "xxxx" }
  },

  "plugins": {
    "entries": {
      "telegram": { "enabled": true }
    }
  }
}
```

---

# 5) 一键验证“替换是否生效”

---

## 5.1 配置是否正确加载

```bash
openclaw doctor /openclaw gateway restart
```

不应再出现：

- Config invalid

- MissingEnvVar

---

## 5.2 Gateway 是否监听端口

```bash
ss -lntp | grep 18789
```

---

## 5.3 模型是否切换成 proxy/sonnet4.5

```bash
openclaw status
```

你需要看到：

- Sessions 默认模型出现 `sonnet4.5`

- 或 `proxy/sonnet4.5`

⚠️ 注意：旧 session 可能仍显示旧模型。