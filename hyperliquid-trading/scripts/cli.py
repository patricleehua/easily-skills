"""Hyperliquid CLI - Command line interface for Hyperliquid trading."""

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.tree import Tree

from .config import load_config, setup_config_interactive
from .hyperliquid_client import HyperliquidClient

console = Console()


def get_timezone_str() -> str:
    """Get current timezone offset string."""
    offset = datetime.now().astimezone().utcoffset()
    if offset:
        hours = int(offset.total_seconds() / 3600)
        return f"UTC{hours:+d}"
    return "UTC"


def format_timestamp(ts_ms: int) -> str:
    """Format millisecond timestamp to local time."""
    dt = datetime.fromtimestamp(ts_ms / 1000)
    return dt.strftime("%Y-%m-%d %H:%M")


def setup_logging(log_level: str = "INFO"):
    """Setup logging with rich handler."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


def get_client(env_file: Optional[str] = None, require_auth: bool = True) -> HyperliquidClient:
    """Get configured client.

    Args:
        env_file: Path to .env file
        require_auth: If True, requires secret_key for trading operations
    """
    config = load_config(env_file)
    errors = config.validate(require_auth=require_auth)
    if errors:
        console.print("[red]Configuration errors:[/red]")
        for error in errors:
            console.print(f"  - {error}")
        console.print("\n[yellow]Run 'hl init' to set up configuration.[/yellow]")
        sys.exit(1)
    return HyperliquidClient(config)


def get_info_client(network: str = "testnet") -> HyperliquidClient:
    """Get read-only client for market data queries."""
    from scripts.config import HyperliquidConfig
    config = HyperliquidConfig(network=network)
    return HyperliquidClient(config)


@click.group()
@click.option("--env-file", "-e", help="Path to .env file")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--json", "output_json", "-j", is_flag=True, help="Output raw JSON")
@click.pass_context
def cli(ctx: click.Context, env_file: Optional[str], verbose: bool, output_json: bool):
    """Hyperliquid CLI - Trade crypto with ease."""
    ctx.ensure_object(dict)
    ctx.obj["env_file"] = env_file
    ctx.obj["output_json"] = output_json

    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(log_level)


def output_result(ctx: click.Context, data: any, table_func=None, **kwargs):
    """Output result as JSON or formatted table.

    Args:
        ctx: Click context
        data: Data to output (will be JSON serialized if --json)
        table_func: Optional function to render table (called if not --json)
        **kwargs: Arguments passed to table_func
    """
    if ctx.obj.get("output_json"):
        console.print_json(json.dumps(data, default=str))
    elif table_func:
        table_func(**kwargs)
    else:
        console.print(data)


@cli.command()
def init():
    """Initialize configuration interactively."""
    setup_config_interactive()


# ==================== Market Data Commands ====================

@cli.group()
def market():
    """Market data commands."""
    pass


@market.command(name="prices")
@click.argument("coins", nargs=-1, required=False)
@click.option("--network", "-n", default="testnet", help="Network (mainnet/testnet)")
@click.pass_context
def market_prices(ctx, coins: tuple, network: str):
    """Get market prices. Optional COINS to filter (space-separated)."""
    client = get_info_client(network)
    try:
        prices = client.get_all_mids()

        if ctx.obj.get("output_json"):
            if coins:
                coins = [c.upper() for c in coins]
                prices = {c: prices.get(c) for c in coins}
            output_result(ctx, prices)
            return

        if coins:
            coins = [c.upper() for c in coins]
            table = Table(title="Market Prices")
            table.add_column("Asset", style="cyan")
            table.add_column("Price", justify="right", style="green")
            for c in coins:
                if c in prices:
                    table.add_row(c, f"${float(prices[c]):,.2f}")
                else:
                    table.add_row(c, "[red]Not found[/red]")
            console.print(table)
            return

        table = Table(title="Market Prices")
        table.add_column("Asset", style="cyan")
        table.add_column("Price", justify="right", style="green")

        for c, price in sorted(prices.items()):
            table.add_row(c, f"${float(price):,.2f}")

        console.print(table)
    finally:
        client.close()


@market.command(name="book")
@click.argument("coin")
@click.option("--depth", "-d", default=10, help="Number of levels to show")
@click.option("--network", "-n", default="testnet", help="Network (mainnet/testnet)")
@click.pass_context
def market_book(ctx, coin: str, depth: int, network: str):
    """Get order book for a coin."""
    client = get_info_client(network)
    try:
        book = client.get_l2_book(coin.upper())

        if ctx.obj.get("output_json"):
            output_result(ctx, book)
            return

        table = Table(title=f"Order Book - {coin.upper()}")
        table.add_column("Bid Price", justify="right", style="green")
        table.add_column("Bid Size", justify="right")
        table.add_column("Ask Price", justify="right", style="red")
        table.add_column("Ask Size", justify="right")

        bids = book.get("levels", [[]])[0][:depth]
        asks = book.get("levels", [[], []])[1][:depth]

        for i in range(max(len(bids), len(asks))):
            bid_px = bids[i]["px"] if i < len(bids) else ""
            bid_sz = bids[i]["sz"] if i < len(bids) else ""
            ask_px = asks[i]["px"] if i < len(asks) else ""
            ask_sz = asks[i]["sz"] if i < len(asks) else ""
            table.add_row(bid_px, bid_sz, ask_px, ask_sz)

        console.print(table)
    finally:
        client.close()


@market.command(name="context")
@click.argument("coins", nargs=-1, required=False)
@click.option("--network", "-n", default="testnet", help="Network (mainnet/testnet)")
@click.pass_context
def market_context(ctx, coins: tuple, network: str):
    """Get asset contexts (trading parameters). Optional COINS to filter (space-separated)."""
    client = get_info_client(network)
    try:
        contexts = client.get_asset_contexts()
        universe = contexts.get("universe", [])

        if ctx.obj.get("output_json"):
            if coins:
                coins = [c.upper() for c in coins]
                universe = [a for a in universe if a.get("name") in coins]
            output_result(ctx, {"universe": universe})
            return

        if coins:
            coins = [c.upper() for c in coins]
            table = Table(title="Asset Contexts")
            table.add_column("Coin", style="cyan")
            table.add_column("Max Leverage")
            table.add_column("Size Decimals")
            for c in coins:
                asset = next((a for a in universe if a.get("name") == c), None)
                if asset:
                    table.add_row(
                        c,
                        str(asset.get("maxLeverage", "N/A")),
                        str(asset.get("szDecimals", "N/A")),
                    )
                else:
                    table.add_row(c, "[red]Not found[/red]", "")
            console.print(table)
            return

        table = Table(title="Asset Contexts")
        table.add_column("Coin", style="cyan")
        table.add_column("Max Leverage")
        table.add_column("Size Decimals")

        for asset in universe:
            table.add_row(
                asset.get("name", "N/A"),
                str(asset.get("maxLeverage", "N/A")),
                str(asset.get("szDecimals", "N/A")),
            )

        console.print(table)
    finally:
        client.close()


@market.command(name="candles")
@click.argument("coin")
@click.option("--interval", "-i", default="1h", help="Candle interval (1m, 5m, 15m, 1h, 4h, 1d, 1w, 1M, 3M, 6M)")
@click.option("--hours", "-H", default=None, type=int, help="Hours of history")
@click.option("--days", "-d", default=None, type=int, help="Days of history (alternative to -H)")
@click.option("--network", "-n", default="testnet", help="Network (mainnet/testnet)")
@click.option("--limit", "-l", default=50, help="Max number of candles to show")
@click.pass_context
def market_candles(ctx, coin: str, interval: str, hours: Optional[int], days: Optional[int], network: str, limit: int):
    """Get candle/OHLCV data for a coin.

    Native intervals: 1m, 5m, 15m, 1h, 4h, 1d
    Aggregated intervals (via 1d): 1w (week), 1M (month), 3M (quarter), 6M (half-year)

    Examples:
        uv run hl market candles BTC -i 1h -H 24
        uv run hl market candles ETH -i 1d -d 30 -n mainnet
        uv run hl market candles BTC -i 1w -d 365 -n mainnet
        uv run hl market candles BTC -i 1M -d 365 -n mainnet
        uv run hl market candles BTC -i 3M -d 365 -n mainnet
    """
    import time
    from datetime import datetime

    # Aggregated intervals need 1d data
    aggregated_intervals = {"1w": 7, "1M": 30, "3M": 90, "6M": 180}
    is_aggregated = interval in aggregated_intervals
    api_interval = "1d" if is_aggregated else interval

    # Calculate hours from --days or --hours (default 24h)
    if days is not None:
        total_hours = days * 24
    elif hours is not None:
        total_hours = hours
    else:
        total_hours = 24

    client = get_info_client(network)
    try:
        end_time = int(time.time() * 1000)
        start_time = end_time - (total_hours * 60 * 60 * 1000)

        candles = client.get_candle_snapshot(
            coin=coin.upper(),
            interval=api_interval,
            start_time=start_time,
            end_time=end_time,
        )

        if not candles:
            if ctx.obj.get("output_json"):
                output_result(ctx, {"coin": coin.upper(), "candles": []})
            else:
                console.print(f"[yellow]No candle data found for {coin.upper()}[/yellow]")
            return

        # Aggregate candles if needed
        if is_aggregated:
            candles = _aggregate_candles(candles, aggregated_intervals[interval])

        if ctx.obj.get("output_json"):
            output_result(ctx, {"coin": coin.upper(), "interval": interval, "candles": candles[-limit:]})
            return

        tz = get_timezone_str()
        table = Table(title=f"{coin.upper()} Candles ({interval}) [{tz}]")
        table.add_column("Time", style="cyan")
        table.add_column("Open", justify="right", style="green")
        table.add_column("High", justify="right", style="green")
        table.add_column("Low", justify="right", style="red")
        table.add_column("Close", justify="right", style="yellow")
        table.add_column("Volume", justify="right")

        for candle in candles[-limit:]:
            t = format_timestamp(candle.get("t", 0))
            o = float(candle.get("o", 0))
            h = float(candle.get("h", 0))
            l = float(candle.get("l", 0))
            c = float(candle.get("c", 0))
            v = float(candle.get("v", 0))

            # Color close based on direction
            close_str = f"${c:,.2f}" if c >= o else f"[red]${c:,.2f}[/red]"

            table.add_row(
                t,
                f"${o:,.2f}",
                f"${h:,.2f}",
                f"${l:,.2f}",
                close_str,
                f"{v:,.2f}",
            )

        console.print(table)
    finally:
        client.close()


def _aggregate_candles(candles: list[dict], days_per_candle: int) -> list[dict]:
    """Aggregate daily candles into larger periods."""
    if not candles:
        return []

    aggregated = []
    for i in range(0, len(candles), days_per_candle):
        chunk = candles[i:i + days_per_candle]
        if not chunk:
            continue

        agg = {
            "t": chunk[0]["t"],  # First candle's time
            "o": chunk[0]["o"],  # First candle's open
            "h": max(float(c["h"]) for c in chunk),  # Highest high
            "l": min(float(c["l"]) for c in chunk),  # Lowest low
            "c": chunk[-1]["c"],  # Last candle's close
            "v": sum(float(c["v"]) for c in chunk),  # Sum of volumes
        }
        aggregated.append(agg)

    return aggregated


@market.command(name="funding")
@click.argument("coin")
@click.option("--network", "-n", default="testnet", help="Network (mainnet/testnet)")
@click.option("--limit", "-l", default=10, help="Number of records to show")
@click.pass_context
def market_funding(ctx, coin: str, network: str, limit: int):
    """Get recent funding rate for a coin."""
    client = get_info_client(network)
    try:
        funding = client.get_recent_funding(coin.upper())

        if ctx.obj.get("output_json"):
            output_result(ctx, {"coin": coin.upper(), "funding": funding[:limit]})
            return

        table = Table(title=f"{coin.upper()} Funding History [{get_timezone_str()}]")
        table.add_column("Time", style="cyan")
        table.add_column("Funding Rate", justify="right")
        table.add_column("Premium", justify="right")

        for record in funding[:limit]:
            ts = format_timestamp(record["time"])
            rate = float(record["fundingRate"]) * 100
            premium = float(record["premium"]) * 100
            rate_str = f"{rate:+.4f}%"
            premium_str = f"{premium:+.4f}%"
            table.add_row(ts, rate_str, premium_str)

        console.print(table)
    finally:
        client.close()


# ==================== Account Commands ====================

@cli.group()
def account():
    """Account information commands."""
    pass


@account.command(name="state")
@click.option("--address", "-a", help="Address to query (defaults to configured)")
@click.pass_context
def account_state(ctx, address: Optional[str]):
    """Get account state (balance, positions)."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        state = client.get_user_state(address)

        if ctx.obj.get("output_json"):
            output_result(ctx, state)
            return

        # Display account summary
        tree = Tree(f"[bold cyan]Account: {state.get('address', 'N/A')[:20]}...[/bold cyan]")

        # Cross margin summary
        cross = state.get("crossMarginSummary", {})
        tree.add(f"[bold]Account Value:[/bold] ${float(cross.get('accountValue', 0)):,.2f}")
        tree.add(f"[bold]Total Margin Used:[/bold] ${float(cross.get('totalMarginUsed', 0)):,.2f}")
        tree.add(f"[bold]Withdrawable:[/bold] ${float(cross.get('withdrawable', 0)):,.2f}")

        # Positions
        positions = state.get("assetPositions", [])
        if positions:
            pos_tree = tree.add("[bold]Positions:[/bold]")
            for pos in positions:
                p = pos.get("position", {})
                coin = p.get("coin", "N/A")
                szi = float(p.get("szi", 0))
                if szi == 0:
                    continue
                entry_px = float(p.get("entryPx", 0))
                lev = p.get("leverage", {})
                lev_type = lev.get("type", "cross")
                lev_val = lev.get("value", "N/A")
                lev_str = f"{lev_val}x {lev_type}"
                pos_tree.add(
                    f"{coin}: {szi:+.4f} @ ${entry_px:,.2f} "
                    f"({lev_str}) (PNL: ${float(p.get('unrealizedPnl', 0)):,.2f})"
                )

        console.print(tree)
    finally:
        client.close()


@account.command(name="orders")
@click.option("--address", "-a", help="Address to query")
@click.pass_context
def account_orders(ctx, address: Optional[str]):
    """Get open orders."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        orders = client.get_open_orders(address)

        if ctx.obj.get("output_json"):
            output_result(ctx, {"orders": orders})
            return

        if not orders:
            console.print("[yellow]No open orders[/yellow]")
            return

        table = Table(title="Open Orders")
        table.add_column("Coin", style="cyan")
        table.add_column("Side", style="green")
        table.add_column("Size", justify="right")
        table.add_column("Price", justify="right")
        table.add_column("Order ID")

        for order in orders:
            side = "[green]Buy[/green]" if order.get("side") == "B" else "[red]Sell[/red]"
            table.add_row(
                order.get("coin", "N/A"),
                side,
                str(order.get("sz", "N/A")),
                f"${order.get('limitPx', 'N/A')}",
                str(order.get("oid", "N/A")),
            )

        console.print(table)
    finally:
        client.close()


@account.command(name="fills")
@click.option("--address", "-a", help="Address to query")
@click.option("--limit", "-l", default=20, help="Number of fills to show")
@click.pass_context
def account_fills(ctx, address: Optional[str], limit: int):
    """Get recent fills."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        fills = client.get_user_fills(address)[:limit]

        if ctx.obj.get("output_json"):
            output_result(ctx, {"fills": fills})
            return

        if not fills:
            console.print("[yellow]No fills found[/yellow]")
            return

        table = Table(title=f"Recent Fills [{get_timezone_str()}]")
        table.add_column("Time")
        table.add_column("Coin", style="cyan")
        table.add_column("Side", style="green")
        table.add_column("Size", justify="right")
        table.add_column("Price", justify="right")
        table.add_column("PNL", justify="right")

        for fill in fills:
            side = "[green]Buy[/green]" if fill.get("side") == "B" else "[red]Sell[/red]"
            table.add_row(
                format_timestamp(fill.get("time", 0)),
                fill.get("coin", "N/A"),
                side,
                str(fill.get("sz", "N/A")),
                f"${fill.get('px', 'N/A')}",
                f"${float(fill.get('closedPnl', 0)):,.2f}",
            )

        console.print(table)
    finally:
        client.close()


@account.command(name="funding")
@click.option("--address", "-a", help="Address to query")
@click.option("--limit", "-l", default=20, help="Number of records to show")
@click.pass_context
def account_funding(ctx, address: Optional[str], limit: int):
    """Get funding payment history."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        funding = client.get_account_funding_history(address)[:limit]

        if ctx.obj.get("output_json"):
            output_result(ctx, {"funding": funding})
            return

        if not funding:
            console.print("[yellow]No funding history found[/yellow]")
            return

        table = Table(title=f"Funding History [{get_timezone_str()}]")
        table.add_column("Time")
        table.add_column("Coin", style="cyan")
        table.add_column("Payment", justify="right")

        for f in funding:
            payment = float(f.get("fundingPayment", 0))
            color = "green" if payment >= 0 else "red"
            table.add_row(
                format_timestamp(f.get("time", 0)),
                f.get("coin", "N/A"),
                f"[{color}]${payment:,.4f}[/{color}]",
            )

        console.print(table)
    finally:
        client.close()


@account.command(name="rewards")
@click.option("--address", "-a", help="Address to query")
@click.pass_context
def account_rewards(ctx, address: Optional[str]):
    """Get staking rewards history."""
    client = get_client(ctx.obj.get("env_file"), require_auth=False)
    try:
        rewards = client.get_staking_rewards(address)

        if ctx.obj.get("output_json"):
            output_result(ctx, {"rewards": rewards})
            return

        if not rewards:
            console.print("[yellow]No staking rewards found[/yellow]")
            return

        table = Table(title=f"Staking Rewards [{get_timezone_str()}]")
        table.add_column("Time")
        table.add_column("Source", style="cyan")
        table.add_column("Amount", justify="right", style="green")

        for reward in rewards:
            amount = float(reward.get("totalAmount", 0))
            table.add_row(
                format_timestamp(reward.get("time", 0)),
                reward.get("source", "N/A"),
                f"{amount:,.4f} HYPE",
            )

        console.print(table)
    finally:
        client.close()


# ==================== Staking Commands ====================

@cli.group()
def staking():
    """Staking commands for HYPE delegation."""
    pass


@staking.command(name="summary")
@click.option("--address", "-a", help="Address to query")
@click.pass_context
def staking_summary(ctx, address: Optional[str]):
    """Get staking summary."""
    client = get_client(ctx.obj.get("env_file"), require_auth=False)
    try:
        summary = client.get_staking_summary(address)

        if ctx.obj.get("output_json"):
            output_result(ctx, summary)
            return

        delegated = float(summary.get("delegated", 0))
        undelegated = float(summary.get("undelegated", 0))
        total_pending = float(summary.get("totalPendingWithdrawal", 0))
        n_pending = summary.get("nPendingWithdrawals", 0)

        table = Table(title="Staking Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="green")
        table.add_row("Delegated", f"{delegated:,.4f} HYPE")
        table.add_row("Undelegated (Pending)", f"{undelegated:,.4f} HYPE")
        table.add_row("Total Pending Withdrawal", f"{total_pending:,.4f} HYPE")
        table.add_row("Pending Withdrawals Count", str(n_pending))

        console.print(table)
    finally:
        client.close()


@staking.command(name="validators")
@click.option("--limit", "-l", default=30, help="Number of validators to show")
@click.option("--sort", "sort_by", type=click.Choice(["stake", "commission", "name"]), default="stake", help="Sort by field")
@click.pass_context
def staking_validators(ctx, limit: int, sort_by: str):
    """Get list of all validators."""
    client = get_client(ctx.obj.get("env_file"), require_auth=False)
    try:
        validators = client.get_validators()

        if ctx.obj.get("output_json"):
            output_result(ctx, {"validators": validators[:limit]})
            return

        if not validators:
            console.print("[yellow]No validators found[/yellow]")
            return

        # Sort validators
        if sort_by == "stake":
            validators = sorted(validators, key=lambda x: float(x.get("stake", 0)), reverse=True)
        elif sort_by == "commission":
            validators = sorted(validators, key=lambda x: float(x.get("commission", 0)))
        else:  # name
            validators = sorted(validators, key=lambda x: x.get("name", "").lower())

        table = Table(title=f"Validators (Top {min(limit, len(validators))})")
        table.add_column("#", justify="right", style="dim")
        table.add_column("Name", style="cyan")
        table.add_column("Address", style="dim")
        table.add_column("Stake", justify="right", style="green")
        table.add_column("Commission", justify="right")
        table.add_column("Delegations", justify="right")

        for i, v in enumerate(validators[:limit]):
            stake = float(v.get("stake", 0))
            commission = float(v.get("commission", 0)) * 100
            n_delegations = v.get("nDelegations", 0)
            address = v.get("validator", "N/A")
            address_short = address[:10] + "..." if len(address) > 10 else address

            table.add_row(
                str(i + 1),
                v.get("name", "Unknown"),
                address_short,
                f"{stake:,.2f} HYPE",
                f"{commission:.1f}%",
                str(n_delegations),
            )

        console.print(table)
        console.print(f"\n[dim]Total validators: {len(validators)}[/dim]")
        console.print(f"[dim]Use --sort name|stake|commission to change sort order[/dim]")
    finally:
        client.close()


@staking.command(name="delegations")
@click.option("--address", "-a", help="Address to query")
@click.pass_context
def staking_delegations(ctx, address: Optional[str]):
    """Get staking delegations."""
    client = get_client(ctx.obj.get("env_file"), require_auth=False)
    try:
        delegations = client.get_staking_delegations(address)

        if ctx.obj.get("output_json"):
            output_result(ctx, {"delegations": delegations})
            return

        if not delegations:
            console.print("[yellow]No staking delegations found[/yellow]")
            return

        table = Table(title="Staking Delegations")
        table.add_column("Validator", style="cyan")
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Locked Until")

        for delegation in delegations:
            amount = float(delegation.get("amount", 0))
            locked_until = delegation.get("lockedUntilTimestamp", 0)
            locked_str = format_timestamp(locked_until) if locked_until else "Unlocked"
            table.add_row(
                delegation.get("validator", "N/A")[:20] + "...",
                f"{amount:,.4f} HYPE",
                locked_str,
            )

        console.print(table)
    finally:
        client.close()


@staking.command(name="rewards")
@click.option("--address", "-a", help="Address to query")
@click.option("--limit", "-l", default=20, help="Number of records to show")
@click.pass_context
def staking_rewards(ctx, address: Optional[str], limit: int):
    """Get staking rewards history."""
    client = get_client(ctx.obj.get("env_file"), require_auth=False)
    try:
        rewards = client.get_staking_rewards(address)[:limit]

        if ctx.obj.get("output_json"):
            output_result(ctx, {"rewards": rewards})
            return

        if not rewards:
            console.print("[yellow]No staking rewards found[/yellow]")
            return

        table = Table(title=f"Staking Rewards [{get_timezone_str()}]")
        table.add_column("Time")
        table.add_column("Source", style="cyan")
        table.add_column("Amount", justify="right", style="green")

        for reward in rewards:
            amount = float(reward.get("totalAmount", 0))
            table.add_row(
                format_timestamp(reward.get("time", 0)),
                reward.get("source", "N/A"),
                f"{amount:,.6f} HYPE",
            )

        console.print(table)
    finally:
        client.close()


@staking.command(name="history")
@click.option("--address", "-a", help="Address to query")
@click.option("--limit", "-l", default=20, help="Number of records to show")
@click.pass_context
def staking_history(ctx, address: Optional[str], limit: int):
    """Get staking history (delegations/undelegations)."""
    client = get_client(ctx.obj.get("env_file"), require_auth=False)
    try:
        history = client.get_staking_history(address)[:limit]

        if ctx.obj.get("output_json"):
            output_result(ctx, {"history": history})
            return

        if not history:
            console.print("[yellow]No staking history found[/yellow]")
            return

        table = Table(title=f"Staking History [{get_timezone_str()}]")
        table.add_column("Time")
        table.add_column("Type", style="cyan")
        table.add_column("Validator")
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Hash", style="dim")

        for event in history:
            event_type = event.get("type", "N/A")
            is_delegate = "delegate" in event_type.lower() and "undelegate" not in event_type.lower()
            type_str = "[green]Delegate[/green]" if is_delegate else "[red]Undelegate[/red]"

            amount = float(event.get("amount", 0))
            hash_val = event.get("hash", "N/A")
            hash_str = hash_val[:16] + "..." if hash_val and len(hash_val) > 16 else hash_val

            table.add_row(
                format_timestamp(event.get("time", 0)),
                type_str,
                event.get("validator", "N/A")[:16] + "...",
                f"{amount:,.4f} HYPE",
                hash_str,
            )

        console.print(table)
    finally:
        client.close()


@staking.command(name="delegate")
@click.argument("validator")
@click.argument("amount", type=float)
@click.confirmation_option("-y", "--yes", prompt="Confirm delegation?")
@click.pass_context
def staking_delegate(ctx, validator: str, amount: float):
    """Delegate HYPE tokens to a validator.

    VALIDATOR: Validator address (0x...)
    AMOUNT: Amount of HYPE to delegate
    """
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.delegate(validator, amount)
        console.print(f"[green]Successfully delegated {amount} HYPE to {validator[:16]}...[/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


@staking.command(name="undelegate")
@click.argument("validator")
@click.argument("amount", type=float)
@click.confirmation_option("-y", "--yes", prompt="Confirm undelegation?")
@click.pass_context
def staking_undelegate(ctx, validator: str, amount: float):
    """Undelegate HYPE tokens from a validator.

    VALIDATOR: Validator address (0x...)
    AMOUNT: Amount of HYPE to undelegate
    """
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.undelegate(validator, amount)
        console.print(f"[green]Successfully undelegated {amount} HYPE from {validator[:16]}...[/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


# ==================== Trading Commands ====================

@cli.group()
def trade():
    """Trading commands."""
    pass


@trade.command(name="buy")
@click.argument("coin")
@click.argument("size", type=float)
@click.option("--price", "-p", type=float, help="Limit price (omit for market order)")
@click.option("--cloid", help="Client order ID")
@click.confirmation_option("-y", "--yes", prompt="Confirm buy order?")
@click.pass_context
def trade_buy(ctx, coin: str, size: float, price: Optional[float], cloid: Optional[str]):
    """Place a buy order."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        if price:
            result = client.place_order(
                coin=coin.upper(),
                is_buy=True,
                sz=size,
                limit_px=price,
                order_type={"limit": {"tif": "Gtc"}},
                cloid=cloid,
            )
        else:
            result = client.place_market_order(
                coin=coin.upper(),
                is_buy=True,
                sz=size,
                cloid=cloid,
            )
        console.print("[green]Order placed successfully![/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


@trade.command(name="sell")
@click.argument("coin")
@click.argument("size", type=float)
@click.option("--price", "-p", type=float, help="Limit price (omit for market order)")
@click.option("--reduce-only", is_flag=True, help="Reduce-only order")
@click.option("--cloid", help="Client order ID")
@click.confirmation_option("-y", "--yes", prompt="Confirm sell order?")
@click.pass_context
def trade_sell(ctx, coin: str, size: float, price: Optional[float], reduce_only: bool, cloid: Optional[str]):
    """Place a sell order."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        if price:
            result = client.place_order(
                coin=coin.upper(),
                is_buy=False,
                sz=size,
                limit_px=price,
                order_type={"limit": {"tif": "Gtc"}},
                reduce_only=reduce_only,
                cloid=cloid,
            )
        else:
            result = client.place_market_order(
                coin=coin.upper(),
                is_buy=False,
                sz=size,
                reduce_only=reduce_only,
                cloid=cloid,
            )
        console.print("[green]Order placed successfully![/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


@trade.command(name="cancel")
@click.argument("coin")
@click.argument("order_id", type=int)
@click.confirmation_option("-y", "--yes", prompt="Confirm cancellation?")
@click.pass_context
def trade_cancel(ctx, coin: str, order_id: int):
    """Cancel an order by ID."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.cancel_order(coin.upper(), order_id)
        console.print("[green]Order cancelled![/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


@trade.command(name="cancel-all")
@click.option("--coin", "-c", help="Filter by coin")
@click.confirmation_option("-y", "--yes", prompt="Cancel all open orders?")
@click.pass_context
def trade_cancel_all(ctx, coin: Optional[str]):
    """Cancel all open orders."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.cancel_all_orders(coin.upper() if coin else None)
        console.print(f"[green]Cancelled {result['cancelled']} orders[/green]")
    finally:
        client.close()


@trade.command(name="modify")
@click.argument("coin")
@click.argument("order_id", type=int)
@click.argument("new_size", type=float)
@click.argument("new_price", type=float)
@click.confirmation_option("-y", "--yes", prompt="Confirm order modification?")
@click.pass_context
def trade_modify(ctx, coin: str, order_id: int, new_size: float, new_price: float):
    """Modify an existing order."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.modify_order(coin.upper(), order_id, new_size, new_price)
        console.print("[green]Order modified![/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


@trade.command(name="close")
@click.argument("coin")
@click.confirmation_option("-y", "--yes", prompt="Close position?")
@click.pass_context
def trade_close(ctx, coin: str):
    """Close position for a coin."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.close_position(coin.upper())
        console.print("[green]Position closed![/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


# ==================== Leverage Commands ====================

@cli.group()
def leverage():
    """Leverage and margin commands."""
    pass


@leverage.command(name="set")
@click.argument("coin")
@click.argument("value", type=int)
@click.option("--cross", is_flag=True, help="Use cross margin")
@click.confirmation_option("-y", "--yes", prompt="Update leverage?")
@click.pass_context
def leverage_set(ctx, coin: str, value: int, cross: bool):
    """Set leverage for a coin."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.update_leverage(coin.upper(), value, is_cross=cross)
        margin_type = "cross" if cross else "isolated"
        console.print(f"[green]Leverage updated to {value}x {margin_type}![/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


@leverage.command(name="margin")
@click.argument("coin")
@click.argument("amount", type=float)
@click.confirmation_option("-y", "--yes", prompt="Update margin?")
@click.pass_context
def leverage_margin(ctx, coin: str, amount: float):
    """Update isolated margin for a position."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.update_isolated_margin(coin.upper(), amount)
        action = "Added" if amount > 0 else "Removed"
        console.print(f"[green]{action} ${abs(amount)} margin![/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


# ==================== Transfer Commands ====================

@cli.group()
def transfer():
    """Transfer and withdrawal commands."""
    pass


@transfer.command(name="send")
@click.argument("destination")
@click.argument("amount", type=float)
@click.option("--token", default="USDC", help="Token to transfer")
@click.confirmation_option("-y", "--yes", prompt="Confirm transfer?")
@click.pass_context
def transfer_send(ctx, destination: str, amount: float, token: str):
    """Transfer tokens to another address."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.transfer(destination, amount, token)
        console.print(f"[green]Transferred {amount} {token}![/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


@transfer.command(name="withdraw")
@click.argument("destination")
@click.argument("amount", type=float)
@click.option("--token", default="USDC", help="Token to withdraw")
@click.confirmation_option("-y", "--yes", prompt="Confirm withdrawal?")
@click.pass_context
def transfer_withdraw(ctx, destination: str, amount: float, token: str):
    """Withdraw tokens to another chain."""
    client = get_client(ctx.obj.get("env_file"))
    try:
        result = client.withdraw(destination, amount, token)
        console.print(f"[green]Withdrew {amount} {token}![/green]")
        console.print_json(json.dumps(result))
    finally:
        client.close()


# ==================== Utility Commands ====================

@cli.command()
def version():
    """Show CLI version."""
    console.print("[bold cyan]Hyperliquid CLI[/bold cyan] v0.1.0")


def main():
    """Entry point."""
    cli()


if __name__ == "__main__":
    main()
