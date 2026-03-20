# Environment and Configuration

## Required Environment Variables

### Read-only Operations

```bash
HL_ACCOUNT_ADDRESS=0x...        # Wallet address (required for all operations)
```

### State-changing Operations

```bash
HL_SECRET_KEY=0x...             # Private key (required for trading/transfer/staking)
```

## Optional Variables

```bash
HL_NETWORK=testnet              # Network: mainnet or testnet (default: testnet)
HL_API_SECRET_KEY=...           # API wallet key (alternative to HL_SECRET_KEY)
HL_LOG_LEVEL=INFO               # Log level: DEBUG, INFO, WARNING, ERROR
HL_LANGUAGE=en                  # Output language: en or zh-CN
```

## API Wallet

`HL_API_SECRET_KEY` is an optional alternative to `HL_SECRET_KEY`. API wallets can be created at https://app.hyperliquid.xyz/API and provide scoped permissions for safer trading operations.

## Network

If the user does not specify otherwise, follow the environment in use. Be careful not to assume mainnet when the active setup may be testnet.

When the user explicitly wants mainnet or testnet, pass:

```bash
-n mainnet
```

or

```bash
-n testnet
```

## Env Files

Use an env file when the user has multiple accounts or wants a specific setup:

```bash
hl -e .env.prod account state
hl -e .env.prod trade buy BTC 0.01 -y
hl -e .env.test account state
```

## Multi-Account Handling

When the user clearly refers to different environments or accounts, prefer explicit `-e` usage so the target account is unambiguous.

## Missing Credentials

If a required variable is missing:

* stop
* explain which variable is needed
* explain whether the request is read-only or state-changing
