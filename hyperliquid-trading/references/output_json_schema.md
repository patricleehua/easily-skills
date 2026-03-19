# Hyperliquid CLI JSON Output Schema

本文档记录所有支持 `--json` 参数的命令的输出结构，便于其他系统集成和脚本化处理。

## 使用方式

```bash
# 使用 --json 参数输出原始 JSON
uv run hl --json <command>

# 简写 -j
uv run hl -j <command>
```

---

## Market Commands

### market prices

获取市场价格。

**命令**: `hl --json market prices [COIN...] [-n mainnet|testnet]`

**输出结构**:
```json
{
  "BTC": "69388.5",
  "ETH": "2117.05"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `{COIN}` | string | 币种名称 -> 价格字符串的映射 |

**示例**:
```bash
# 获取指定币种价格
uv run hl --json market prices BTC ETH -n mainnet

# 获取所有价格
uv run hl --json market prices -n mainnet
```

---

### market book

获取订单簿数据。

**命令**: `hl --json market book <COIN> [-d depth] [-n mainnet|testnet]`

**输出结构**:
```json
{
  "coin": "BTC",
  "time": 1773936113818,
  "levels": [
    [
      {
        "px": "69388.0",
        "sz": "11.91507",
        "n": 34
      }
    ],
    [
      {
        "px": "69389.0",
        "sz": "0.51105",
        "n": 2
      }
    ]
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `coin` | string | 币种名称 |
| `time` | number | 时间戳 (毫秒) |
| `levels` | array | 订单簿层级 `[bids, asks]` |
| `levels[0]` | array | 买单列表 (Bids) |
| `levels[1]` | array | 卖单列表 (Asks) |
| `px` | string | 价格 |
| `sz` | string | 数量 |
| `n` | number | 订单数量 |

**示例**:
```bash
uv run hl --json market book BTC -d 10 -n mainnet
```

---

### market context

获取资产交易参数。

**命令**: `hl --json market context [COIN...] [-n mainnet|testnet]`

**输出结构**:
```json
{
  "universe": [
    {
      "szDecimals": 5,
      "name": "BTC",
      "maxLeverage": 40,
      "marginTableId": 56
    },
    {
      "szDecimals": 4,
      "name": "ETH",
      "maxLeverage": 25,
      "marginTableId": 55
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `universe` | array | 资产列表 |
| `name` | string | 币种名称 |
| `szDecimals` | number | 数量小数位 |
| `maxLeverage` | number | 最大杠杆倍数 |
| `marginTableId` | number | 保证金表 ID |

**示例**:
```bash
# 获取指定币种参数
uv run hl --json market context BTC ETH -n mainnet

# 获取所有资产参数
uv run hl --json market context -n mainnet
```

---

### market candles

获取 K 线数据。

**命令**: `hl --json market candles <COIN> [-i interval] [-H hours | -d days] [-n mainnet|testnet] [-l limit]`

**输出结构**:
```json
{
  "coin": "BTC",
  "interval": "1h",
  "candles": [
    {
      "t": 1773849600000,
      "T": 1773853199999,
      "s": "BTC",
      "i": "1h",
      "o": "71442.0",
      "c": "71293.0",
      "h": "71568.0",
      "l": "71000.0",
      "v": "1915.60108",
      "n": 28398
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `coin` | string | 币种名称 |
| `interval` | string | K 线周期 |
| `candles` | array | K 线数据列表 |
| `t` | number | 开始时间戳 (毫秒) |
| `T` | number | 结束时间戳 (毫秒) |
| `s` | string | 币种符号 |
| `i` | string | 周期间隔 |
| `o` | string | 开盘价 |
| `c` | string | 收盘价 |
| `h` | string | 最高价 |
| `l` | string | 最低价 |
| `v` | string | 成交量 |
| `n` | number | 成交笔数 |

**支持的周期**:
- 原生: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
- 聚合: `1w` (周), `1M` (月), `3M` (季度), `6M` (半年)

**示例**:
```bash
# 24小时 1小时 K 线
uv run hl --json market candles BTC -i 1h -H 24 -n mainnet

# 30天 日 K 线
uv run hl --json market candles ETH -i 1d -d 30 -n mainnet

# 1年 周 K 线
uv run hl --json market candles BTC -i 1w -d 365 -n mainnet
```

---

### market funding

获取资金费率历史。

**命令**: `hl --json market funding <COIN> [-n mainnet|testnet] [-l limit]`

**输出结构**:
```json
{
  "coin": "BTC",
  "funding": [
    {
      "coin": "BTC",
      "fundingRate": "0.0000125",
      "premium": "-0.0003397585",
      "time": 1773853200066
    },
    {
      "coin": "BTC",
      "fundingRate": "0.0000125",
      "premium": "-0.0003601456",
      "time": 1773856800052
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `coin` | string | 币种名称 |
| `funding` | array | 资金费率记录列表 |
| `fundingRate` | string | 资金费率 (小数形式) |
| `premium` | string | 溢价率 (小数形式) |
| `time` | number | 时间戳 (毫秒) |

**示例**:
```bash
uv run hl --json market funding BTC -n mainnet -l 10
```

---

## Account Commands

### account state

获取账户状态（余额、持仓）。

**命令**: `hl --json account state [-a address]`

**输出结构**:
```json
{
  "assetPositions": [
    {
      "position": {
        "coin": "BTC",
        "entryPx": "65000.0",
        "szi": "0.1",
        "unrealizedPnl": "100.5",
        "leverage": {
          "type": "cross",
          "value": 10
        }
      }
    }
  ],
  "crossMarginSummary": {
    "accountValue": "10000.0",
    "totalMarginUsed": "500.0",
    "withdrawable": "9500.0"
  },
  "marginSummary": {
    "accountValue": "10000.0",
    "totalMarginUsed": "500.0",
    "totalNtlPos": "6500.0",
    "totalRawUsd": "10000.0"
  },
  "withdrawable": "9500.0"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `assetPositions` | array | 持仓列表 |
| `position.coin` | string | 币种名称 |
| `position.entryPx` | string | 入场价格 |
| `position.szi` | string | 持仓数量 (正数多头, 负数空头) |
| `position.unrealizedPnl` | string | 未实现盈亏 |
| `position.leverage.type` | string | 杠杆类型 (`cross`/`isolated`) |
| `position.leverage.value` | number | 杠杆倍数 |
| `crossMarginSummary.accountValue` | string | 账户价值 |
| `crossMarginSummary.totalMarginUsed` | string | 已用保证金 |
| `crossMarginSummary.withdrawable` | string | 可提取金额 |

**示例**:
```bash
# 查询当前账户
uv run hl --json account state

# 查询指定地址
uv run hl --json account state -a 0x...
```

---

### account orders

获取未成交订单。

**命令**: `hl --json account orders [-a address]`

**输出结构**:
```json
{
  "orders": [
    {
      "coin": "BTC",
      "side": "B",
      "sz": "0.1",
      "limitPx": "65000.0",
      "oid": 12345678,
      "timestamp": 1773853200000,
      "orderType": "limit"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `orders` | array | 订单列表 |
| `coin` | string | 币种名称 |
| `side` | string | 方向 (`B`=买入, `A`=卖出) |
| `sz` | string | 数量 |
| `limitPx` | string | 限价 |
| `oid` | number | 订单 ID |
| `timestamp` | number | 时间戳 (毫秒) |
| `orderType` | string | 订单类型 |

**示例**:
```bash
uv run hl --json account orders
```

---

### account fills

获取成交历史。

**命令**: `hl --json account fills [-a address] [-l limit]`

**输出结构**:
```json
{
  "fills": [
    {
      "coin": "BTC",
      "side": "B",
      "sz": "0.1",
      "px": "65000.0",
      "time": 1773853200000,
      "closedPnl": "0.0",
      "hash": "0x...",
      "oid": 12345678,
      "crossed": true,
      "fee": "0.00005",
      "startPosition": "0.0",
      "dir": "Open"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `fills` | array | 成交记录列表 |
| `coin` | string | 币种名称 |
| `side` | string | 方向 (`B`=买入, `A`=卖出) |
| `sz` | string | 数量 |
| `px` | string | 成交价格 |
| `time` | number | 时间戳 (毫秒) |
| `closedPnl` | string | 已实现盈亏 |
| `hash` | string | 交易哈希 |
| `oid` | number | 订单 ID |
| `crossed` | boolean | 是否吃单 |
| `fee` | string | 手续费 |
| `dir` | string | 方向 (`Open`/`Close`) |

**示例**:
```bash
uv run hl --json account fills -l 20
```

---

### account funding

获取资金费用历史。

**命令**: `hl --json account funding [-a address] [-l limit]`

**输出结构**:
```json
{
  "funding": [
    {
      "coin": "BTC",
      "fundingPayment": "-0.00125",
      "time": 1773853200000
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `funding` | array | 资金费用记录列表 |
| `coin` | string | 币种名称 |
| `fundingPayment` | string | 资金费用 (正数收入, 负数支出) |
| `time` | number | 时间戳 (毫秒) |

**示例**:
```bash
uv run hl --json account funding -l 20
```

---

### account rewards

获取质押奖励历史。

**命令**: `hl --json account rewards [-a address] [-l limit]`

**输出结构**:
```json
{
  "rewards": [
    {
      "time": 1736726400073,
      "source": "delegation",
      "totalAmount": "0.73117184"
    },
    {
      "time": 1736726400073,
      "source": "commission",
      "totalAmount": "130.76445876"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `rewards` | array | 奖励记录列表 |
| `time` | number | 时间戳 (毫秒) |
| `source` | string | 奖励来源 (`delegation`/`commission`) |
| `totalAmount` | string | 奖励数量 (HYPE) |

**示例**:
```bash
uv run hl --json account rewards -l 20
```

---

## Staking Commands

### staking validators

获取验证者列表。

**命令**: `hl --json staking validators [-l limit] [--sort stake|commission|name]`

**输出结构**:
```json
{
  "validators": [
    {
      "name": "Validator Name",
      "validator": "0x5ac99df645f3414876c816caa18b2d234024b487",
      "stake": "12060.16529862",
      "commission": "0.05",
      "nDelegations": 150
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `validators` | array | 验证者列表 |
| `name` | string | 验证者名称 |
| `validator` | string | 验证者地址 |
| `stake` | string | 质押数量 (HYPE) |
| `commission` | string | 佣金率 (小数形式, 0.05 = 5%) |
| `nDelegations` | number | 委托人数 |

**示例**:
```bash
# 按质押量排序
uv run hl --json staking validators -l 30 --sort stake

# 按佣金排序
uv run hl --json staking validators --sort commission
```

---

### staking summary

获取质押摘要。

**命令**: `hl --json staking summary [-a address]`

**输出结构**:
```json
{
  "delegated": "12060.16529862",
  "undelegated": "0.0",
  "totalPendingWithdrawal": "0.0",
  "nPendingWithdrawals": 0
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `delegated` | string | 已质押数量 (HYPE) |
| `undelegated` | string | 待解除数量 (HYPE) |
| `totalPendingWithdrawal` | string | 待提取总额 (HYPE) |
| `nPendingWithdrawals` | number | 待提取次数 |

**示例**:
```bash
uv run hl --json staking summary
```

---

### staking delegations

获取质押委托列表。

**命令**: `hl --json staking delegations [-a address]`

**输出结构**:
```json
{
  "delegations": [
    {
      "validator": "0x5ac99df645f3414876c816caa18b2d234024b487",
      "amount": "12060.16529862",
      "lockedUntilTimestamp": 1735466781353
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `delegations` | array | 委托列表 |
| `validator` | string | 验证者地址 |
| `amount` | string | 委托数量 (HYPE) |
| `lockedUntilTimestamp` | number | 锁定截止时间戳 (毫秒) |

**示例**:
```bash
uv run hl --json staking delegations
```

---

### staking rewards

获取质押奖励历史。

**命令**: `hl --json staking rewards [-a address] [-l limit]`

**输出结构**:
```json
{
  "rewards": [
    {
      "time": 1736726400073,
      "source": "delegation",
      "totalAmount": "0.73117184"
    },
    {
      "time": 1736726400073,
      "source": "commission",
      "totalAmount": "130.76445876"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `rewards` | array | 奖励记录列表 |
| `time` | number | 时间戳 (毫秒) |
| `source` | string | 奖励来源 |
| `totalAmount` | string | 奖励数量 (HYPE) |

**示例**:
```bash
uv run hl --json staking rewards -l 50
```

---

### staking history

获取质押历史记录。

**命令**: `hl --json staking history [-a address] [-l limit]`

**输出结构**:
```json
{
  "history": [
    {
      "time": 1735380381353,
      "hash": "0x55492465cb523f90815a041a226ba90147008d4b221a24ae8dc35a0dbede4ea4",
      "delta": {
        "delegate": {
          "validator": "0x5ac99df645f3414876c816caa18b2d234024b487",
          "amount": "10000.0",
          "isUndelegate": false
        }
      }
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `history` | array | 历史记录列表 |
| `time` | number | 时间戳 (毫秒) |
| `hash` | string | 交易哈希 |
| `delta.delegate.validator` | string | 验证者地址 |
| `delta.delegate.amount` | string | 操作数量 (HYPE) |
| `delta.delegate.isUndelegate` | boolean | 是否为解除质押 |

**示例**:
```bash
uv run hl --json staking history -l 20
```

---

## 空数据返回

当查询结果为空时，各命令返回结构：

| 命令 | 空结果 |
|------|--------|
| `market prices` | `{}` |
| `market book` | `{"coin": "XXX", "time": 0, "levels": [[], []]}` |
| `market context` | `{"universe": []}` |
| `market candles` | `{"coin": "XXX", "interval": "1h", "candles": []}` |
| `market funding` | `{"coin": "XXX", "funding": []}` |
| `account orders` | `{"orders": []}` |
| `account fills` | `{"fills": []}` |
| `account funding` | `{"funding": []}` |
| `account rewards` | `{"rewards": []}` |
| `staking validators` | `{"validators": []}` |
| `staking delegations` | `{"delegations": []}` |
| `staking rewards` | `{"rewards": []}` |
| `staking history` | `{"history": []}` |

---

## 错误处理

当发生错误时，CLI 会返回非零退出码，并输出错误信息到 stderr。

```bash
# 检查命令是否成功
uv run hl --json market prices BTC
if [ $? -eq 0 ]; then
  echo "Success"
else
  echo "Failed"
fi
```

---

## 脚本集成示例

### Python 示例

```python
import subprocess
import json

def get_prices(coins):
    cmd = ["uv", "run", "hl", "--json", "market", "prices"] + list(coins) + ["-n", "mainnet"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        raise Exception(result.stderr)

prices = get_prices(["BTC", "ETH"])
print(f"BTC: ${prices['BTC']}")
print(f"ETH: ${prices['ETH']}")
```

### Bash 示例

```bash
#!/bin/bash

# 获取 BTC 价格并解析
btc_price=$(uv run hl --json market prices BTC -n mainnet | jq -r '.BTC')
echo "BTC Price: $btc_price"

# 获取账户余额
account_value=$(uv run hl --json account state | jq -r '.crossMarginSummary.accountValue')
echo "Account Value: $account_value"
```

### Node.js 示例

```javascript
const { execSync } = require('child_process');

function getPrices(coins) {
  const cmd = `uv run hl --json market prices ${coins.join(' ')} -n mainnet`;
  const output = execSync(cmd, { encoding: 'utf-8' });
  return JSON.parse(output);
}

const prices = getPrices(['BTC', 'ETH']);
console.log(`BTC: $${prices.BTC}`);
console.log(`ETH: $${prices.ETH}`);
```
