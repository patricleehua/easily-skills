# Commands

Use these command patterns when operating the `hl` CLI.

> **Note**: If installed via `pip install -e .` or `uv pip install -e .`, commands can be run directly as `hl <command>`. If running from source without installation, prefix with `uv run` (e.g., `uv run hl market prices BTC`).

---

## Global Options

```bash
hl -e /path/to/.env <command>      # Specify env file
hl -v <command>                    # Verbose logging
hl --json <command>                # Output raw JSON
hl -j <command>                    # Output raw JSON (shorthand)
hl --lang zh-CN <command>          # Set output language (en/zh-CN)
hl -l zh-CN <command>              # Set language (shorthand)
hl <command> -y                    # Skip confirmation
```

Use `-j` when structured parsing is helpful.
Use `-e` when the user is working with multiple accounts or environments.

---

## Initialization

```bash
hl init                            # Interactive configuration setup
hl version                         # Show CLI version
```

---

## Calculator (`calc`)

When the user provides a USD amount instead of a base-asset quantity, always use this command first.

```bash
hl calc size <COIN> <USD_AMOUNT>              # $20 = ? BTC
hl calc size <COIN> <USD_AMOUNT> -l <N>       # With leverage
hl calc size <COIN> <USD_AMOUNT> -n mainnet   # Specify network
```

JSON output:

```bash
hl -j calc size <COIN> <USD_AMOUNT> [-l <N>] [-n mainnet]
```

Read at least these fields from the output:

* `calculated_size`
* `meets_minimum`
* `notional_value`
* `current_price`
* `max_leverage`

---

## Market Data (`market`)

### Prices

```bash
hl market prices                     # All coins
hl market prices BTC ETH -n mainnet  # Specific coins
```

### Order Book

```bash
hl market book <COIN> -d <N>         # N = depth
hl market book BTC -d 5 -n mainnet
```

### Market Context (Asset Parameters)

Use this when you need contract metadata such as max leverage or minimum trading constraints.

```bash
hl market context                    # All assets
hl market context BTC ETH            # Specific assets
```

### Funding Rates

```bash
hl market funding <COIN> -l <N>
hl market funding ETH -n mainnet -l 5
```

### Candles (OHLCV)

Native intervals: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
Aggregated intervals: `1w`, `1M`, `3M`, `6M`

```bash
hl market candles <COIN> -i <INTERVAL> -H <HOURS>
hl market candles BTC -i 1h -H 24 -n mainnet
hl market candles ETH -i 1d -d 30 -n mainnet
hl market candles BTC -i 1w -d 365 -n mainnet
```

---

## Account (`account`)

### Account State (Balance & Positions)

```bash
hl account state
hl account state -a <ADDRESS>        # Query specific address
```

### Open Orders

```bash
hl account orders
hl account orders -a <ADDRESS>
```

### Recent Fills

```bash
hl account fills -l 20
hl account fills -a <ADDRESS> -l 20
```

### Funding Fee History

```bash
hl account funding -l 20
hl account funding -a <ADDRESS> -l 20
```

### Staking Rewards History

```bash
hl account rewards
hl account rewards -a <ADDRESS>
```

---

## Staking (`staking`)

### Validators List

```bash
hl staking validators -l 30
hl staking validators --sort stake      # Sort by stake (default)
hl staking validators --sort commission # Sort by commission
hl staking validators --sort name       # Sort by name
```

### Staking Summary

```bash
hl staking summary
hl staking summary -a <ADDRESS>
```

### Staking Delegations

```bash
hl staking delegations
hl staking delegations -a <ADDRESS>
```

### Staking Rewards

```bash
hl staking rewards -l 20
hl staking rewards -a <ADDRESS> -l 20
```

### Staking History

```bash
hl staking history -l 20
hl staking history -a <ADDRESS> -l 20
```

### Delegate HYPE

```bash
hl staking delegate <VALIDATOR_ADDRESS> <AMOUNT> -y
```

### Undelegate HYPE

```bash
hl staking undelegate <VALIDATOR_ADDRESS> <AMOUNT> -y
```

---

## Trading (`trade`)

### Market Buy

```bash
hl trade buy <COIN> <SIZE> -y
hl trade buy BTC 0.01 -y
```

### Limit Buy

```bash
hl trade buy <COIN> <SIZE> -p <PRICE>
hl trade buy BTC 0.01 -p 65000
```

### Market Sell

```bash
hl trade sell <COIN> <SIZE> -y
hl trade sell ETH 0.05 -y
```

### Limit Sell

```bash
hl trade sell <COIN> <SIZE> -p <PRICE>
hl trade sell ETH 0.05 -p 3000
```

### Close Position

```bash
hl trade close <COIN>
hl trade close BTC -y
```

### Cancel Order

```bash
hl trade cancel <COIN> <ORDER_ID>
hl trade cancel BTC 123456 -y
```

### Cancel All Orders

```bash
hl trade cancel-all -y                # All coins
hl trade cancel-all -c <COIN> -y      # Specific coin
```

### Modify Order

```bash
hl trade modify <COIN> <ORDER_ID> <NEW_SIZE> <NEW_PRICE>
hl trade modify BTC 123456 0.02 64000 -y
```

---

## Leverage (`leverage`)

### Set Leverage

```bash
hl leverage set <COIN> <VALUE>              # Isolated margin
hl leverage set <COIN> <VALUE> --cross      # Cross margin
hl leverage set BTC 10 --cross -y
```

### Update Isolated Margin

```bash
hl leverage margin <COIN> <AMOUNT>
hl leverage margin BTC 100 -y    # Add $100 margin
hl leverage margin BTC -50 -y    # Remove $50 margin
```

---

## Transfer (`transfer`)

### Internal Transfer

```bash
hl transfer send <ADDRESS> <AMOUNT> --token <TOKEN>
hl transfer send 0x... 100 --token USDC -y
```

### Cross-Chain Withdrawal

```bash
hl transfer withdraw <ADDRESS> <AMOUNT> --token <TOKEN>
hl transfer withdraw 0x... 100 --token USDC -y
```

---

## Common Workflows

### New Trade Flow

```bash
# 1. Check current price
hl market prices BTC -n mainnet

# 2. Calculate position size from USD
hl calc size BTC 100 -l 5 -n mainnet

# 3. Set leverage
hl leverage set BTC 5 --cross -y

# 4. Place order
hl trade buy BTC 0.001 -y

# 5. Verify position
hl account state
```

### Position Management Flow

```bash
# 1. Check positions
hl account state

# 2. Check open orders
hl account orders

# 3. Modify or cancel orders
hl trade modify BTC 123456 0.002 64000 -y
hl trade cancel BTC 123456 -y
hl trade cancel-all -c BTC -y

# 4. Close position
hl trade close BTC -y
```

### Multi-Account Usage

```bash
# Use different env files for different accounts
hl -e .env.test account state      # Testnet account
hl -e .env.prod account state      # Mainnet account
hl -e .env.wallet1 trade buy BTC 0.01 -y
```
