# ⚠️ 雷区（高频踩坑）

---

## Telegram 配对未批准 → 机器人不回消息

表现：

- 卡在“配对中”

- 机器人不响应

解决：

```bash
openclaw pairing approve --channel <channel> <code>
```



---

## 第三方 API baseUrl 写错（不能带 /v1）

❌ 错误：

```json
"baseUrl": "https://api.example.com/v1"
```

会导致：

- Invalid endpoint

- 拼成 /v1/v1/messages

正确：

```json
"baseUrl": "https://api.antigravity.ai"
```



## vps/wsl/虚拟机 部署后无法访问



1.配置文件未放开

check  openclaw.json shuld be like this:

`~/.openclaw/openclaw.json`

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan", //checking is lan
    "controlUi": { "allowInsecureAuth": true },//had?
    "auth": { "mode": "token", "token": "xxxx" }
  }
}
```

2.早期版本未知异常，需要解决



## openclaw无法操作浏览器





需要手动打开浏览器，然后激活扩展插件，提示插件被控制，否则无法操作浏览器