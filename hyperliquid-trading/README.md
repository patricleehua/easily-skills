# Hyperliquid Trading CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Hyperliquid SDK](https://img.shields.io/badge/Hyperliquid-SDK-green.svg)](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)

A powerful command-line trading tool for Hyperliquid DEX, built with Python SDK. Provides comprehensive market data queries, account management, and trading operations for both Mainnet and Testnet.

基于 Python SDK 的 Hyperliquid DEX 命令行交易工具，提供完整的市场数据查询、账户管理和交易功能，支持主网和测试网。

---

## Table of Contents | 目录

- [English](#english)
- [中文](#中文)

---

<a name="english"></a>

## English

### Features

- **Market Data**: Real-time prices, order book, asset info, funding rates, K-line data
- **Account Management**: Balance, positions, orders, trade history, funding fees
- **Trading Operations**: Place/cancel/modify orders, market/limit orders
- **Leverage Management**: Adjust leverage, margin operations (cross/isolated)
- **Transfers**: Internal transfers, cross-chain withdrawals
- **Multi-Account**: Switch between multiple accounts via different `.env` files
- **Dual Network**: Mainnet and Testnet support

### Installation

```bash
# Install dependencies
uv sync

# Install the package
uv pip install -e .
```

### Quick Start

```bash
# Initialize configuration (interactive)
uv run hl init

# Or manually create .env
cp .env.example .env
```

Edit `.env` with your credentials:

```env
HL_NETWORK=testnet              # mainnet or testnet
HL_ACCOUNT_ADDRESS=0x...        # Wallet address
HL_SECRET_KEY=0x...             # Private key (required for trading)
HL_API_SECRET_KEY=              # API wallet key (optional)
HL_LOG_LEVEL=INFO               # Log level
```

### Usage Examples

```bash
# Get prices
uv run hl market prices BTC ETH -n mainnet

# View order book
uv run hl market book BTC -d 5 -n mainnet

# Get funding rates
uv run hl market funding ETH -n mainnet -l 5

# Get K-line data
uv run hl market candles BTC -i 1h -H 24 -n mainnet

# Check account state
uv run hl account state

# View open orders
uv run hl account orders

# Place a limit order
uv run hl trade buy BTC 0.01 -p 65000

# Place a market order
uv run hl trade sell ETH 0.05 -y

# Set leverage (10x cross margin)
uv run hl leverage set BTC 10 --cross

# Close position
uv run hl trade close BTC

# Internal transfer
uv run hl transfer send <ADDRESS> 100 --token USDC
```

### Command Reference

#### Market Data (`market`)

| Command | Description |
|---------|-------------|
| `hl market prices [COIN...]` | Get market prices |
| `hl market book <COIN> -d <N>` | View order book (N = depth) |
| `hl market context [COIN...]` | Get asset trading parameters |
| `hl market funding <COIN>` | Get funding rates |
| `hl market candles <COIN> -i <INTERVAL>` | Get K-line data |

#### Account (`account`)

| Command | Description |
|---------|-------------|
| `hl account state` | View account state (balance, positions) |
| `hl account orders` | View open orders |
| `hl account fills` | View trade history |
| `hl account funding` | View funding fee history |

#### Trading (`trade`)

| Command | Description |
|---------|-------------|
| `hl trade buy <COIN> <SIZE> -p <PRICE>` | Buy limit order |
| `hl trade buy <COIN> <SIZE> -y` | Buy market order |
| `hl trade sell <COIN> <SIZE> -p <PRICE>` | Sell limit order |
| `hl trade sell <COIN> <SIZE>` | Sell market order |
| `hl trade cancel <COIN> <ORDER_ID>` | Cancel order |
| `hl trade cancel-all -c <COIN> -y` | Cancel all orders |
| `hl trade modify <COIN> <ID> <SIZE> <PRICE>` | Modify order |
| `hl trade close <COIN>` | Close position |

#### Leverage (`leverage`)

| Command | Description |
|---------|-------------|
| `hl leverage set <COIN> <VALUE> [--cross]` | Set leverage |
| `hl leverage margin <COIN> <AMOUNT>` | Adjust isolated margin |

#### Transfer (`transfer`)

| Command | Description |
|---------|-------------|
| `hl transfer send <DEST> <AMOUNT>` | Internal transfer |
| `hl transfer withdraw <DEST> <AMOUNT>` | Cross-chain withdrawal |

### Multi-Account Support

```bash
# Environment file naming
.env           # Default
.env.test      # Testnet account
.env.prod      # Mainnet account
.env.wallet1   # Wallet 1

# Switch accounts with -e flag
uv run hl -e .env.test account state
uv run hl -e .env.prod trade buy BTC 0.01 -p 65000
```

### Global Options

```bash
hl -e /path/to/.env <command>   # Specify env file
hl -v <command>                  # Verbose logging
hl <command> -y                  # Skip confirmation
hl version                       # Show version
```

### Security Notes

1. **Key Security**: Never commit private keys to repositories
2. **Test First**: Always verify operations on Testnet before Mainnet
3. **Small Amounts**: Start with small amounts for initial testing
4. **API Wallet**: Consider using an API wallet instead of your main wallet

---

<a name="中文"></a>

## 中文

### 功能特性

- **市场数据**: 实时价格、订单簿、资产信息、资金费率、K线数据
- **账户管理**: 余额、持仓、订单、成交历史、资金费用
- **交易功能**: 下单、撤单、修改订单、市价/限价单
- **杠杆管理**: 调整杠杆、保证金操作（全仓/逐仓）
- **转账功能**: 内部转账、跨链提现
- **多账号管理**: 通过不同的 `.env` 文件切换账号
- **双网支持**: 主网(Mainnet)和测试网(Testnet)

### 安装

```bash
# 安装依赖
uv sync

# 安装包
uv pip install -e .
```

### 快速开始

```bash
# 初始化配置（交互式）
uv run hl init

# 或手动创建 .env
cp .env.example .env
```

编辑 `.env` 文件填入配置：

```env
HL_NETWORK=testnet              # mainnet 或 testnet
HL_ACCOUNT_ADDRESS=0x...        # 钱包地址
HL_SECRET_KEY=0x...             # 私钥（交易必需）
HL_API_SECRET_KEY=              # API钱包私钥（可选）
HL_LOG_LEVEL=INFO               # 日志级别
```

### 使用示例

```bash
# 获取价格
uv run hl market prices BTC ETH -n mainnet

# 查看订单簿
uv run hl market book BTC -d 5 -n mainnet

# 获取资金费率
uv run hl market funding ETH -n mainnet -l 5

# 获取K线数据
uv run hl market candles BTC -i 1h -H 24 -n mainnet

# 查看账户状态
uv run hl account state

# 查看未成交订单
uv run hl account orders

# 下限价单
uv run hl trade buy BTC 0.01 -p 65000

# 下市价单
uv run hl trade sell ETH 0.05 -y

# 设置杠杆（10x全仓）
uv run hl leverage set BTC 10 --cross

# 平仓
uv run hl trade close BTC

# 内部转账
uv run hl transfer send <ADDRESS> 100 --token USDC
```

### 命令速查

#### 市场数据 (`market`)

| 命令 | 说明 |
|------|------|
| `hl market prices [COIN...]` | 获取市场价格 |
| `hl market book <COIN> -d <N>` | 查看订单簿 (N = 档位) |
| `hl market context [COIN...]` | 获取资产交易参数 |
| `hl market funding <COIN>` | 获取资金费率 |
| `hl market candles <COIN> -i <周期>` | 获取K线数据 |

#### 账户 (`account`)

| 命令 | 说明 |
|------|------|
| `hl account state` | 查看账户状态（余额、持仓） |
| `hl account orders` | 查看未成交订单 |
| `hl account fills` | 查看成交历史 |
| `hl account funding` | 查看资金费用历史 |

#### 交易 (`trade`)

| 命令 | 说明 |
|------|------|
| `hl trade buy <COIN> <SIZE> -p <PRICE>` | 买入限价单 |
| `hl trade buy <COIN> <SIZE> -y` | 买入市价单 |
| `hl trade sell <COIN> <SIZE> -p <PRICE>` | 卖出限价单 |
| `hl trade sell <COIN> <SIZE>` | 卖出市价单 |
| `hl trade cancel <COIN> <ORDER_ID>` | 撤销订单 |
| `hl trade cancel-all -c <COIN> -y` | 撤销所有订单 |
| `hl trade modify <COIN> <ID> <SIZE> <PRICE>` | 修改订单 |
| `hl trade close <COIN>` | 平仓 |

#### 杠杆 (`leverage`)

| 命令 | 说明 |
|------|------|
| `hl leverage set <COIN> <VALUE> [--cross]` | 设置杠杆 |
| `hl leverage margin <COIN> <AMOUNT>` | 调整逐仓保证金 |

#### 转账 (`transfer`)

| 命令 | 说明 |
|------|------|
| `hl transfer send <DEST> <AMOUNT>` | 内部转账 |
| `hl transfer withdraw <DEST> <AMOUNT>` | 跨链提现 |

### 多账号管理

```bash
# 环境文件命名
.env           # 默认配置
.env.test      # 测试网账号
.env.prod      # 主网账号
.env.wallet1   # 钱包1

# 使用 -e 参数切换账号
uv run hl -e .env.test account state
uv run hl -e .env.prod trade buy BTC 0.01 -p 65000
```

### 全局选项

```bash
hl -e /path/to/.env <command>   # 指定环境文件
hl -v <command>                  # 详细日志
hl <command> -y                  # 跳过确认
hl version                       # 查看版本
```

### 安全提示

1. **密钥安全**: 永远不要将私钥提交到代码仓库
2. **先测后用**: 在主网操作前务必先在测试网验证
3. **小额测试**: 首次使用建议先用小额测试
4. **API钱包**: 建议使用 API 钱包而非主钱包进行交易

---

## Project Structure | 项目结构

```
hyperliquid-trading/
├── scripts/
│   ├── cli.py                 # CLI main entry | CLI主程序
│   ├── config.py              # Configuration management | 配置管理
│   └── hyperliquid_client.py  # SDK wrapper | SDK封装
├── .env.example               # Environment template | 环境变量模板
├── pyproject.toml             # Project config | 项目配置
├── SKILL.md                   # Claude Code skill doc | Claude技能文档
└── README.md                  # This file | 本文档
```

## Dependencies | 依赖

- hyperliquid-python-sdk >= 0.22.0
- click >= 8.1.0
- rich >= 13.0.0
- python-dotenv >= 1.0.0

## References | 参考链接

- [Hyperliquid Documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/)
- [Python SDK GitHub](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)

## License

[MIT](LICENSE)

---

<p align="center">
  <b>Trade responsibly. Use at your own risk.</b><br>
  <b>交易有风险，使用需谨慎。</b>
</p>
