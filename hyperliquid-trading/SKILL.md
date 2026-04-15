---
name: hyperliquid-trading
description: use when working with hyperliquid through the hl cli for market data, account state, order execution, leverage changes, transfers, withdrawals, or hype staking. triggers include checking prices, positions, orders, fills, funding, order books, candles, placing or cancelling trades, closing positions, setting leverage, or moving funds on hyperliquid. do not use for general crypto discussion, discretionary market commentary, or non-hyperliquid workflows.
---

# Hyperliquid Trading

Use this skill to operate the `hl` CLI safely and consistently for Hyperliquid.

## Permissions

Read-only requests require `HL_ACCOUNT_ADDRESS`.

State-changing requests require `HL_SECRET_KEY`, including:
- placing or cancelling orders
- closing positions
- setting leverage
- transfers or withdrawals
- staking or unstaking HYPE

If the required credential is missing, stop and explain what is needed.

## Request Classification

Classify the user request into one of these categories:

1. market data
   - price, order book, funding, candles, market context

2. account state
   - balance, equity, positions, open orders, fills, export positions

3. trade execution
   - buy, sell, close, cancel, cancel-all

4. leverage management
   - set leverage, cross/isolated changes

5. funds operations
   - transfer, withdraw

6. staking
   - delegate, undelegate HYPE

Read `references/commands.md` for exact command syntax.

## Non-Negotiable Rules

These rules are mandatory. Do not skip them.

### 1. Never estimate order size from a USD amount
If the user specifies trade size in USD terms, always calculate size with `hl calc size`.
Do not infer or approximate quantity from market price.

Required flow:
1. run `hl calc size`
2. read `calculated_size`
3. verify `meets_minimum`
4. show the calculated result to the user
5. only execute after explicit confirmation

### 2. Always gather context before any state-changing action
Before any trade, leverage change, transfer, withdrawal, or staking action, always gather the relevant context first.

At minimum:
- for trades: current market price and current account state
- for close-position requests: current position direction and size
- for leverage changes: current market context and leverage limits
- for transfers and withdrawals: destination, amount, whether the destination is clearly provided, and network/environment if relevant
- for staking: validator, amount, and action type

Do this even if the user did not explicitly ask for the extra information, because it is required for safe execution.

### 3. Never execute a state-changing action without explicit confirmation
Do not execute any state-changing action unless the user has clearly confirmed the exact action.

Before asking for confirmation, restate the exact action in plain language.

This applies to:
- buy / sell / close
- cancel / cancel-all
- leverage changes
- transfers / withdrawals
- staking / unstaking

Confirmation must restate the important parameters relevant to the action, such as:
- coin
- side
- size
- order type
- price if limit order
- leverage if relevant
- destination address for transfer/withdrawal
- validator and amount for staking

Do not use the -y parameter unless the user is very explicit that you can use it. Do not execute any irreversible or state-changing commands before the user explicitly confirms the operation.

### 4. Do not automatically retry state-changing actions
If a trade, transfer, withdrawal, leverage update, cancellation, or staking action fails:
- report the error
- explain likely causes
- suggest the next step
- do not retry automatically

### 5. Risk warnings are mandatory
Warn the user before execution when any of the following applies:
- trade notional appears large relative to account equity
- leverage is high
- limit price is far from current market price
- implied slippage is unusually high
- withdrawal or transfer destination should be double-checked

Do not skip warnings just because the operation is simple to execute.

## Mandatory Risk Thresholds

Use these thresholds as mandatory warning rules.

### Trade size warning
Warn if requested trade notional appears to be greater than 20% of account equity.

### Leverage warning
Warn clearly when:
- leverage >= 10x: high risk
- leverage >= 20x: very high risk and requires especially explicit confirmation
- leverage >= 40x: extreme risk and requires especially explicit confirmation

For leverage >= 20x, do not execute on the same turn as the initial request unless the user explicitly confirms after the warning.
For leverage >= 40x, require an especially explicit confirmation after clearly restating the leverage, coin, and risk.

These warnings are mandatory even if the user directly requested the leverage value.

Never infer that a leverage increase is safe to execute without confirmation just because it may reduce margin requirements or appear operationally simple.

### Limit price deviation
Warn if the limit price differs from the current market price by more than 5%.

### Market-order failure fallback
If a market order fails and liquidity or volatility may be the cause:
- explain the likely reason
- inspect the order book if needed
- suggest a limit order if appropriate
- do not place the fallback order automatically without confirmation

## Standard Workflow

### Market data requests
Execute the requested read-only command directly and summarize the result clearly.

### Account state requests
Execute the requested read-only command directly and summarize:
- equity / available balance when relevant
- positions and unrealized PnL when relevant
- open orders or fills when relevant

### Trade execution requests
Follow this exact sequence:

1. identify side, coin, size basis, order type, and any conditions
2. if size is given in USD, run `hl calc size`
3. fetch current market price
4. fetch relevant account state
5. apply risk checks
6. present a concise execution summary including:
   - coin
   - side
   - calculated size or requested size
   - current price
   - estimated notional
   - any warnings
7. ask for explicit confirmation
8. only after confirmation, execute the requested command
9. report the result clearly

Do not skip steps 2 through 7.
Do not execute the trade on the initial request unless the user has explicitly confirmed after seeing the summary and warnings.

### Close-position requests
1. inspect current position
2. determine the correct closing side and size
3. summarize the close action in plain language
4. ask for explicit confirmation
5. only after confirmation, execute the close action
6. report the result

### Leverage requests
Treat every leverage change as a state-changing action that requires explicit confirmation before execution.

Follow this exact sequence:
1. identify the coin and requested leverage
2. check current market context and leverage limits
3. apply leverage risk warnings
4. restate the exact leverage change in plain language
5. ask for explicit confirmation
6. only after confirmation, execute the leverage command
7. report the result

For leverage >= 20x, the warning and confirmation step is mandatory and cannot be skipped.
Do not execute leverage changes immediately, even if the change appears operationally simple or reduces margin requirements.

### Funds and staking requests
Treat these as high-risk state-changing actions.

Always restate:
- destination or validator
- amount
- network/environment when relevant

For transfers and withdrawals, if the destination is missing or ambiguous, stop and ask the user to provide or confirm it clearly.

Then ask for explicit confirmation before execution.

Do not execute transfers, withdrawals, staking, or unstaking immediately.

## Reference Guide

Use these files only when needed:

- `references/commands.md`
  - exact CLI commands and common syntax patterns

- `references/examples.md`
  - example workflows for common user requests

- `references/env.md`
  - environment variables, networks, env files, and multi-account usage

## Response Style

For read-only responses:
- be concise
- summarize the key numbers first
- include relevant supporting details

For state-changing responses before execution:
- summarize the intended action in one compact block
- include the parameters that matter
- include any warnings
- ask for explicit confirmation

For execution results:
- say whether it succeeded
- report the key returned fields
- mention anything the user should verify next