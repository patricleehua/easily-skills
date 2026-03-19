---
name: hyperliquid-trading
description: |
  Hyperliquid DEX 命令行交易工具。当用户需要查询 Hyperliquid 市场数据、管理账户、执行交易操作、设置杠杆、转账提现时使用此技能。支持主网和测试网。TRIGGER when: 用户提及 Hyperliquid、HL、衍生品形式(美元、石油、黄金、股票)的价格、永续合约交易、加密货币交易 CLI、查询币价、下单交易、查看持仓、资金费率等。
category: finance 
tags: [trading, dex, cli, api, derivatives]
---

# Hyperliquid Trading CLI

基于 Python SDK 的 Hyperliquid DEX 命令行交易工具，提供完整的市场数据查询、账户管理和交易功能。

## 环境准备

```bash
# 安装依赖
uv sync

# 安装 hyperliquid-trading
uv pip install -e .

# 初始化配置（交互式）
uv run hl init

# 或手动创建 .env
cp .env.example .env
```

## 配置说明

`.env` 文件必需配置：

```env
HL_NETWORK=testnet              # mainnet 或 testnet
HL_ACCOUNT_ADDRESS=0x...        # 钱包地址
HL_SECRET_KEY=0x...             # 私钥（交易必需）
HL_API_SECRET_KEY=              # API钱包私钥（可选）
HL_LOG_LEVEL=INFO               # 日志级别
```

## 多账号管理

支持通过不同的 `.env` 文件管理多个账号，方便在测试网、主网、不同钱包之间切换。

### 环境文件命名

```
.env           # 默认配置（当前使用）
.env.test      # 测试网账号
.env.prod      # 主网账号
.env.wallet1   # 钱包1
.env.wallet2   # 钱包2
```

### 切换账号

**方式一：指定环境文件 (-e)**

```bash
# 使用测试网账号
uv run hl -e .env.test account state

# 使用主网账号交易
uv run hl -e .env.prod trade buy BTC 0.01 -p 65000

# 使用指定钱包
uv run hl -e .env.wallet1 account orders
```

## 命令速查

### 市场数据 (market)

```bash
# 获取价格
uv run hl market prices [COIN1] [COIN2]... [-n mainnet|testnet]

# 查看订单簿
uv run hl market book <COIN> [-d 10] [-n testnet]

# 获取资产参数（含最大杠杆倍率，设置杠杆前可先查询）
uv run hl market context [COIN...] [-n testnet]

# 获取资金费率
uv run hl market funding <COIN> [-n testnet] [-l 10]

# 获取 K 线数据
uv run hl market candles <COIN> [-i 1h] [-H 24 | -d 30] [-n mainnet]
```

### 账户信息 (account)

```bash
# 账户状态（余额、持仓）
uv run hl account state [-a <ADDRESS>]

# 未成交订单
uv run hl account orders [-a <ADDRESS>]

# 成交历史
uv run hl account fills [-a <ADDRESS>] [-l 20]

# 资金费用历史
uv run hl account funding [-a <ADDRESS>] [-l 20]
```

### 交易操作 (trade)

> **注意**：交易会使用该币种上次设置的杠杆倍率。如不确定当前杠杆，建议先执行 `uv run hl leverage set <COIN> <VALUE>` 确认设置。

```bash
# 买入限价单
uv run hl trade buy <COIN> <SIZE> -p <PRICE> [--cloid <ID>]

# 买入市价单（跳过确认）
uv run hl trade buy <COIN> <SIZE> -y

# 卖出限价单
uv run hl trade sell <COIN> <SIZE> -p <PRICE> [--reduce-only]

# 卖出市价单
uv run hl trade sell <COIN> <SIZE> [--reduce-only]

# 取消订单
uv run hl trade cancel <COIN> <ORDER_ID>

# 取消所有订单（跳过确认）
uv run hl trade cancel-all [-c <COIN>] -y

# 修改订单
uv run hl trade modify <COIN> <ORDER_ID> <NEW_SIZE> <NEW_PRICE>

# 平仓
uv run hl trade close <COIN>
```

### 杠杆管理 (leverage)

```bash
# 设置杠杆
uv run hl leverage set <COIN> <VALUE> [--cross]

# 调整逐仓保证金
uv run hl leverage margin <COIN> <AMOUNT>
```

### 转账提现 (transfer)

```bash
# 内部转账
uv run hl transfer send <DESTINATION> <AMOUNT> [--token USDC]

# 跨链提现（跳过确认）
uv run hl transfer withdraw <DESTINATION> <AMOUNT> -y
```

## 使用示例

### 查询市场

```bash
# 查询 BTC/ETH 价格
uv run hl market prices BTC ETH -n mainnet

# 查询 所有价格（数据量过大，不建议使用）
uv run hl market prices  -n mainnet

# 查看 BTC 订单簿前 5 档
uv run hl market book BTC -d 5 -n mainnet

# 查看 ETH 资金费率
uv run hl market funding ETH -n mainnet -l 5

# 查看 BTC 最近 24 小时 1 小时 K 线
uv run hl market candles BTC -i 1h -H 24 -n mainnet

# 查看 ETH 最近 30 天日 K 线
uv run hl market candles ETH -i 1d -d 30 -n mainnet

# 查看 BTC 最近 1 年周 K 线
uv run hl market candles BTC -i 1w -d 365 -n mainnet

# 查看 BTC 最近 1 年月 K 线
uv run hl market candles BTC -i 1M -d 365 -n mainnet

# 查看 BTC 最近 1 年季度 K 线
uv run hl market candles BTC -i 3M -d 365 -n mainnet

# 查看 BTC 最近 1 年半年 K 线
uv run hl market candles BTC -i 6M -d 365 -n mainnet

# 查询 所有参数（数据量过大，不建议使用）
uv run hl market prices  -n mainnet

# 查询 BTC ETH 资产交易参数
uv run hl market context BTC ETH -n mainnet

# 查询 所有可交易的资产交易参数（数据量过大，不建议使用）
uv run hl market context -n mainnet


```

### 交易操作

```bash
# 测试网买入 0.1 BTC 限价单 @ 65000
uv run hl trade buy BTC 0.1 -p 65000

# 测试网市价卖出 0.05 ETH
uv run hl trade sell ETH 0.05

# 设置 BTC 杠杆为 10x 全仓
uv run hl leverage set BTC 10 --cross

# 平掉 BTC 仓位
uv run hl trade close BTC
```

### 账户查询

```bash
# 查看账户概览
uv run hl account state

# 查看最近 10 笔成交
uv run hl account fills -l 10

# 查看资金费用
uv run hl account funding -l 20
```

## 安全提示

1. **密钥安全**: 永远不要直接读取配置文件
2. **失败兜底**: 交易过程中发生异常最大重试次数不得超过3次，需告警用户协助排查解决
3. **小额测试**: 首次使用建议先用小额测试

## 常见问题

### 网络选择

- `testnet`: 测试网，无风险，用于开发和测试
- `mainnet`: 主网，真实资金，谨慎操作

### 订单类型

- 限价单: 指定价格，`-p <PRICE>`
- 市价单: 不指定价格，按最优价格成交
- Reduce-only: 只减仓，不开新仓

### 全局选项

```bash
# 指定环境文件
uv run hl -e /path/to/.env <command>

# 启用详细日志
uv run hl -v <command>

# 跳过确认（适用于 trade/leverage/transfer 命令）
uv run hl <command> -y
uv run hl <command> --yes

# 查看版本
uv run hl version
```

## 项目结构

```
hyperliquid-trading/
├── scripts/
│   ├── cli.py                 # CLI 主程序
│   ├── config.py              # 配置管理
│   └── hyperliquid_client.py  # SDK 封装
├── .env.example               # 环境变量示例
├── pyproject.toml             # 项目配置
└── SKILL.md                   # 本文档
```

## 参考链接

- [Hyperliquid 官方文档](https://hyperliquid.gitbook.io/hyperliquid-docs/)
- [Python SDK GitHub](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)
