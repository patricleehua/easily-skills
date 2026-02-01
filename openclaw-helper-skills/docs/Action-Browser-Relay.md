# Check Chrome if Existen

if not Existen the going to installed it

WINDOWS:https://www.google.com/chrome/



Linux：

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo dpkg -i google-chrome-stable_current_amd64.deb
```



# Chrome浏览器扩展安装（Browser Relay）

安装命令：

```bash
openclaw browser extension install
```

输出路径：

```
~/.openclaw/browser/chrome-extension
```

下一步：

- Chrome → chrome://extensions

- 开启 Developer mode

- Load unpacked → 选择该目录

- Pin 插件，Badge 显示 ON

---

## 非 root 用户注意

复制插件目录：

```bash
cp -r chrome-extension /home/patrick/下载/
sudo chown -R patrick:patrick chrome-extension/
```

否则权限会报错。

---

## 验证浏览器扩展状态

```bash
openclaw browser status
```



