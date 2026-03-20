# Example Workflows

## 1. Portfolio Overview

User:
How is my Hyperliquid portfolio?

Suggested flow:
1. run `hl account state`
2. run `hl account orders`
3. summarize:
   - total equity
   - available balance if shown
   - open positions with unrealized PnL
   - open orders

## 2. Buy Using USD Amount

User:
Buy $100 of BTC on Hyperliquid.

Suggested flow:
1. run `hl -j calc size BTC 100 -n mainnet`
2. read `calculated_size`, `notional_value`, `current_price`, `meets_minimum`
3. run `hl market prices BTC -n mainnet`
4. run `hl account state`
5. summarize:
   - current price
   - calculated size
   - estimated notional
   - any relevant warnings
6. ask for confirmation
7. after confirmation, run:
   ```bash
   hl trade buy BTC <SIZE> -y
   ```

8. report result

## 3. Close Position

User:
Close my ETH position.

Suggested flow:

1. run `hl account state`
2. identify ETH position direction and size
3. explain what close action will do
4. ask for confirmation
5. execute close:

   ```bash
   hl trade close ETH
   ```
6. report result

## 4. Set Leverage Then Trade

User:
Set BTC to 5x and buy $50.

Suggested flow:

1. run `hl market context BTC`
2. run `hl -j calc size BTC 50 --leverage 5 -n mainnet`
3. summarize leverage and calculated size
4. ask for confirmation for the leverage change and trade
5. after confirmation:

   ```bash
   hl leverage set BTC 5
   hl trade buy BTC <SIZE> -y
   ```
6. report both results clearly

## 5. Market Order Failure Fallback

User:
Buy SOL now.

Suggested flow:

1. gather price/account context
2. confirm action
3. attempt requested order
4. if execution fails and liquidity/slippage appears to be the issue:

   * explain failure
   * inspect order book:

     ```bash
     hl market book SOL -d 5
     ```
   * propose a limit order near the ask with a clear warning
   * require confirmation before placing the replacement order

Do not automatically place the fallback order.

## 6. Withdrawal

User:
Withdraw 100 USDC to this address: 0x...

Suggested flow:

1. restate amount and destination
2. verify the user clearly intends withdrawal, not internal transfer
3. ask for explicit confirmation
4. after confirmation:

   ```bash
   hl transfer withdraw <ADDRESS> <AMOUNT> --token USDC -y
   ```
5. report result