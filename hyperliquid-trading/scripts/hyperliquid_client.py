"""Hyperliquid SDK client wrapper."""

import logging
from typing import Any, Optional

from hyperliquid.api import API
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils.types import Cloid

from scripts.config import HyperliquidConfig

logger = logging.getLogger(__name__)


class HyperliquidClient:
    """Client for Hyperliquid API operations."""

    def __init__(self, config: HyperliquidConfig):
        """Initialize client with configuration.

        Args:
            config: Hyperliquid configuration
        """
        self.config = config
        self._api: Optional[API] = None
        self._info: Optional[Info] = None
        self._exchange: Optional[Exchange] = None

    @property
    def api(self) -> API:
        """Get or create API instance for direct API calls."""
        if self._api is None:
            self._api = API(self.config.api_url)
            logger.debug(f"API client initialized: {self.config.api_url}")
        return self._api

    @property
    def info(self) -> Info:
        """Get or create Info instance."""
        if self._info is None:
            base_url = self.config.api_url
            self._info = Info(base_url, skip_ws=True)
            logger.debug(f"Info client initialized: {base_url}")
        return self._info

    @property
    def exchange(self) -> Exchange:
        """Get or create Exchange instance."""
        if self._exchange is None:
            base_url = self.config.api_url
            # Use API secret key if available, otherwise use main secret key
            secret_key = self.config.api_secret_key or self.config.secret_key
            if not secret_key:
                raise ValueError("Secret key required for trading operations")
            from eth_account import Account
            wallet = Account.from_key(secret_key)

            # Fetch and filter spot_meta to fix testnet API bug
            # (some token indices may be out of range)
            spot_meta = self._get_filtered_spot_meta()

            self._exchange = Exchange(
                wallet,
                base_url=base_url,
                account_address=self.config.account_address,
                spot_meta=spot_meta,
            )
            logger.debug(f"Exchange client initialized: {base_url}")
        return self._exchange

    def _get_filtered_spot_meta(self) -> dict:
        """Fetch spot_meta and filter out invalid entries."""
        resp = self.api.post("/info", {"type": "spotMeta"})
        spot_meta = resp

        # Filter out universe items with out-of-range token indices
        tokens_count = len(spot_meta.get("tokens", []))
        valid_universe = [
            item for item in spot_meta.get("universe", [])
            if all(idx < tokens_count for idx in item.get("tokens", []))
        ]
        spot_meta["universe"] = valid_universe
        return spot_meta

    def close(self):
        """Close all connections."""
        if self._info:
            self._info.disconnect_websocket()
            self._info = None
        self._exchange = None
        self._api = None

    # ==================== Info Methods (using direct API for stability) ====================

    def get_all_mids(self) -> dict[str, str]:
        """Get all market mid prices.

        Returns:
            Dictionary mapping coin to mid price
        """
        return self.api.post("/info", {"type": "allMids"})

    def get_user_state(self, address: Optional[str] = None) -> dict:
        """Get user state including balances and positions.

        Args:
            address: User address (defaults to configured address)

        Returns:
            User state data
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "clearinghouseState", "user": addr})

    def get_user_fills(self, address: Optional[str] = None) -> list[dict]:
        """Get user's fill history.

        Args:
            address: User address (defaults to configured address)

        Returns:
            List of fill records
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "userFills", "user": addr})

    def get_open_orders(self, address: Optional[str] = None) -> list[dict]:
        """Get user's open orders.

        Args:
            address: User address (defaults to configured address)

        Returns:
            List of open orders
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "openOrders", "user": addr})

    def get_order_status(self, address: str, oid: int) -> dict:
        """Get status of a specific order.

        Args:
            address: User address
            oid: Order ID

        Returns:
            Order status data
        """
        return self.api.post("/info", {"type": "orderStatus", "user": address, "oid": oid})

    def get_asset_contexts(self) -> dict:
        """Get asset contexts (trading parameters).

        Returns:
            Asset context data with universe and tokens
        """
        return self.api.post("/info", {"type": "meta"})

    def get_spot_meta(self) -> dict:
        """Get spot market metadata.

        Returns:
            Spot metadata with tokens and universe
        """
        return self.api.post("/info", {"type": "spotMeta"})

    def get_candle_snapshot(
        self, coin: str, interval: str, start_time: int, end_time: int
    ) -> list[dict]:
        """Get candle/OHLCV data.

        Args:
            coin: Asset symbol (e.g., "BTC")
            interval: Time interval (e.g., "1h", "1d")
            start_time: Start timestamp (ms)
            end_time: End timestamp (ms)

        Returns:
            List of candle data
        """
        return self.api.post("/info", {
            "type": "candleSnapshot",
            "req": {
                "coin": coin,
                "interval": interval,
                "startTime": start_time,
                "endTime": end_time,
            }
        })

    def get_l2_book(self, coin: str) -> dict:
        """Get L2 order book.

        Args:
            coin: Asset symbol

        Returns:
            Order book data with levels [[bids], [asks]]
        """
        return self.api.post("/info", {"type": "l2Book", "coin": coin})

    def get_funding_history(
        self, coin: str, start_time: int, end_time: Optional[int] = None
    ) -> list[dict]:
        """Get funding rate history.

        Args:
            coin: Asset symbol
            start_time: Start timestamp (ms)
            end_time: End timestamp (ms), defaults to now

        Returns:
            List of funding rate records
        """
        req = {"type": "fundingHistory", "coin": coin, "startTime": start_time}
        if end_time:
            req["endTime"] = end_time
        return self.api.post("/info", req)

    def get_recent_funding(self, coin: str, hours: int = 24) -> list[dict]:
        """Get recent funding rate history.

        Args:
            coin: Asset symbol
            hours: Number of hours of history (default 24)

        Returns:
            Recent funding rate data
        """
        import time
        start_time = int(time.time() * 1000) - (hours * 60 * 60 * 1000)
        return self.api.post("/info", {"type": "fundingHistory", "coin": coin, "startTime": start_time})

    def get_account_funding_history(
        self, address: Optional[str] = None
    ) -> list[dict]:
        """Get account funding payment history.

        Args:
            address: User address (defaults to configured address)

        Returns:
            List of funding payments
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "userFunding", "user": addr})

    def get_deposits(self, address: Optional[str] = None) -> list[dict]:
        """Get deposit history.

        Args:
            address: User address (defaults to configured address)

        Returns:
            List of deposit records
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "userDeposits", "user": addr})

    def get_withdrawals(self, address: Optional[str] = None) -> list[dict]:
        """Get withdrawal history.

        Args:
            address: User address (defaults to configured address)

        Returns:
            List of withdrawal records
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "userWithdrawals", "user": addr})

    # ==================== Trading Methods ====================

    def place_order(
        self,
        coin: str,
        is_buy: bool,
        sz: float,
        limit_px: float,
        order_type: dict = None,
        reduce_only: bool = False,
        cloid: Optional[str] = None,
    ) -> dict:
        """Place a new order.

        Args:
            coin: Asset symbol (e.g., "BTC")
            is_buy: True for buy, False for sell
            sz: Order size (in coins)
            limit_px: Limit price
            order_type: SDK format, e.g. {"limit": {"tif": "Gtc"}}
            reduce_only: Whether order is reduce-only
            cloid: Optional client order ID

        Returns:
            Order result
        """
        if order_type is None:
            order_type = {"limit": {"tif": "Gtc"}}
        cloid_obj = Cloid.from_str(cloid) if cloid else None

        order_result = self.exchange.order(
            name=coin,
            is_buy=is_buy,
            sz=sz,
            limit_px=limit_px,
            order_type=order_type,
            reduce_only=reduce_only,
            cloid=cloid_obj,
        )
        logger.info(f"Order placed: {order_result}")
        return order_result

    def place_market_order(
        self,
        coin: str,
        is_buy: bool,
        sz: float,
        reduce_only: bool = False,
        cloid: Optional[str] = None,
    ) -> dict:
        """Place a market order using IOC with order book pricing.

        Uses order book best bid/ask for more accurate pricing.

        Args:
            coin: Asset symbol
            is_buy: True for buy, False for sell
            sz: Order size
            reduce_only: Whether order is reduce-only
            cloid: Optional client order ID

        Returns:
            Order result
        """
        # Get order book for best bid/ask prices
        book = self.get_l2_book(coin)
        levels = book.get("levels", [[], []])
        bids = levels[0] if len(levels) > 0 else []
        asks = levels[1] if len(levels) > 1 else []

        if is_buy:
            # For buy, use best ask price + small buffer
            if not asks:
                raise ValueError(f"No asks available for {coin}")
            best_ask = float(asks[0]["px"])
            limit_px = int(best_ask) + 1  # Just 1 tick above ask
            ref_price = best_ask
        else:
            # For sell, use best bid price - small buffer
            if not bids:
                raise ValueError(f"No bids available for {coin}")
            best_bid = float(bids[0]["px"])
            limit_px = int(best_bid) - 1  # Just 1 tick below bid
            if limit_px <= 0:
                limit_px = 1  # Safety floor
            ref_price = best_bid

        logger.info(f"Market order: {coin} {'BUY' if is_buy else 'SELL'} {sz} @ ~${ref_price:.2f} (limit: {limit_px})")

        return self.place_order(
            coin=coin,
            is_buy=is_buy,
            sz=sz,
            limit_px=limit_px,
            order_type={"limit": {"tif": "Ioc"}},
            reduce_only=reduce_only,
            cloid=cloid,
        )

    def cancel_order(self, coin: str, oid: int) -> dict:
        """Cancel an order by ID.

        Args:
            coin: Asset symbol
            oid: Order ID

        Returns:
            Cancel result
        """
        result = self.exchange.cancel(coin, oid)
        logger.info(f"Order cancelled: {result}")
        return result

    def cancel_all_orders(self, coin: Optional[str] = None) -> dict:
        """Cancel all open orders.

        Args:
            coin: Optional coin to filter by

        Returns:
            Cancel result
        """
        # Get open orders first
        open_orders = self.get_open_orders()

        if coin:
            open_orders = [o for o in open_orders if o.get("coin") == coin]

        results = []
        for order in open_orders:
            coin_symbol = order.get("coin")
            oid = order.get("oid")
            if coin_symbol and oid:
                result = self.cancel_order(coin_symbol, oid)
                results.append(result)

        return {"cancelled": len(results), "results": results}

    def modify_order(
        self,
        coin: str,
        oid: int,
        new_sz: float,
        new_limit_px: float,
    ) -> dict:
        """Modify an existing order.

        Args:
            coin: Asset symbol
            oid: Order ID to modify
            new_sz: New size
            new_limit_px: New limit price

        Returns:
            Modify result
        """
        # 查询订单信息获取 is_buy
        open_orders = self.get_open_orders()
        target_order = None
        for order in open_orders:
            if order.get("oid") == oid:
                target_order = order
                break

        if not target_order:
            raise ValueError(f"Order {oid} not found in open orders")

        # side: "B" = Buy, "A" = Ask/Sell
        is_buy = target_order.get("side") == "B"

        # 使用默认的限价单类型
        order_type = {"limit": {"tif": "Gtc"}}

        result = self.exchange.modify_order(
            oid=oid,
            name=coin,
            is_buy=is_buy,
            sz=new_sz,
            limit_px=new_limit_px,
            order_type=order_type,
        )
        logger.info(f"Order modified: {result}")
        return result

    # ==================== Spot Trading ====================

    def place_spot_order(
        self,
        coin: str,
        is_buy: bool,
        sz: float,
        limit_px: float,
        order_type: str = "Limit",
    ) -> dict:
        """Place a spot order.

        Args:
            coin: Spot asset symbol
            is_buy: True for buy, False for sell
            sz: Order size
            limit_px: Limit price
            order_type: Order type

        Returns:
            Order result
        """
        order_result = self.exchange.spot_order(
            coin=coin,
            is_buy=is_buy,
            sz=sz,
            limit_px=limit_px,
            order_type=order_type,
        )
        logger.info(f"Spot order placed: {order_result}")
        return order_result

    def get_spot_balances(self, address: Optional[str] = None) -> list[dict]:
        """Get spot token balances.

        Args:
            address: User address (defaults to configured address)

        Returns:
            List of spot balances
        """
        addr = address or self.config.account_address
        user_state = self.get_user_state(addr)
        return user_state.get("balances", [])

    # ==================== Transfer/Withdraw ====================

    def transfer(self, destination: str, amount: float, token: str = "USDC") -> dict:
        """Transfer tokens to another address.

        Args:
            destination: Destination address
            amount: Amount to transfer
            token: Token symbol

        Returns:
            Transfer result
        """
        result = self.exchange.transfer(destination, amount, token)
        logger.info(f"Transfer executed: {result}")
        return result

    def withdraw(self, destination: str, amount: float, token: str = "USDC") -> dict:
        """Withdraw tokens to another chain.

        Args:
            destination: Destination address
            amount: Amount to withdraw
            token: Token symbol

        Returns:
            Withdrawal result
        """
        result = self.exchange.withdraw(destination, amount, token)
        logger.info(f"Withdrawal executed: {result}")
        return result

    # ==================== Leverage/Position ====================

    def update_leverage(self, coin: str, leverage: int, is_cross: bool = False) -> dict:
        """Update leverage for a coin.

        Args:
            coin: Asset symbol
            leverage: Leverage value (1-50)
            is_cross: True for cross margin, False for isolated

        Returns:
            Update result
        """
        result = self.exchange.update_leverage(leverage, coin, is_cross)
        logger.info(f"Leverage updated: {result}")
        return result

    def update_isolated_margin(self, coin: str, amount: float) -> dict:
        """Update isolated margin for a position.

        Args:
            coin: Asset symbol
            amount: Amount to add/remove

        Returns:
            Update result
        """
        result = self.exchange.update_isolated_margin(amount, coin)
        logger.info(f"Isolated margin updated: {result}")
        return result

    def close_position(self, coin: str) -> dict:
        """Close a position for a coin using IOC market order.

        Args:
            coin: Asset symbol

        Returns:
            Close result
        """
        # Get current position to determine size and direction
        user_state = self.get_user_state()

        # Handle both dict and list responses
        if isinstance(user_state, list):
            positions = user_state
        elif isinstance(user_state, dict):
            # Check for nested structure
            asset_positions = user_state.get("assetPositions")
            if isinstance(asset_positions, dict):
                positions = asset_positions.get("values", [])
            elif isinstance(asset_positions, list):
                positions = asset_positions
            else:
                positions = []
        else:
            positions = []

        position = None
        for pos in positions:
            pos_data = pos.get("position", pos)
            if pos_data.get("coin") == coin:
                position = pos_data
                break

        if not position:
            return {"status": "error", "message": f"No position found for {coin}"}

        szi = float(position.get("szi", 0))
        if szi == 0:
            return {"status": "error", "message": f"Position for {coin} is already closed"}

        # Close position: sell if long, buy if short (reduce-only)
        result = self.place_market_order(
            coin=coin,
            is_buy=(szi < 0),  # Buy to close short, sell to close long
            sz=abs(szi),
            reduce_only=True,
        )
        logger.info(f"Position closed: {result}")
        return result

    # ==================== Staking Methods ====================

    def get_validators(self) -> list[dict]:
        """Get list of all validators.

        Returns:
            List of validators with name, address, commission, stake info
        """
        return self.api.post("/info", {"type": "validatorSummaries"})

    def get_staking_summary(self, address: Optional[str] = None) -> dict:
        """Get staking summary for an address.

        Args:
            address: User address (defaults to configured address)

        Returns:
            Staking summary with delegated, undelegated amounts
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "delegatorSummary", "user": addr})

    def get_staking_delegations(self, address: Optional[str] = None) -> list[dict]:
        """Get staking delegations for an address.

        Args:
            address: User address (defaults to configured address)

        Returns:
            List of delegations with validator, amount, locked_until_timestamp
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "delegations", "user": addr})

    def get_staking_rewards(self, address: Optional[str] = None) -> list[dict]:
        """Get staking rewards history for an address.

        Args:
            address: User address (defaults to configured address)

        Returns:
            List of rewards with time, source, total_amount
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "delegatorRewards", "user": addr})

    def get_staking_history(self, address: Optional[str] = None) -> list[dict]:
        """Get comprehensive staking history for an address.

        Args:
            address: User address (defaults to configured address)

        Returns:
            List of staking history events
        """
        addr = address or self.config.account_address
        return self.api.post("/info", {"type": "delegatorHistory", "user": addr})

    def delegate(self, validator: str, amount: float) -> dict:
        """Delegate tokens to a validator.

        Args:
            validator: Validator address
            amount: Amount to delegate (in HYPE)

        Returns:
            Delegation result
        """
        # Convert amount to wei (HYPE has 18 decimals)
        wei = int(amount * 10**18)
        result = self.exchange.token_delegate(validator, wei, is_undelegate=False)
        logger.info(f"Delegated {amount} HYPE to {validator}: {result}")
        return result

    def undelegate(self, validator: str, amount: float) -> dict:
        """Undelegate tokens from a validator.

        Args:
            validator: Validator address
            amount: Amount to undelegate (in HYPE)

        Returns:
            Undelegation result
        """
        # Convert amount to wei (HYPE has 18 decimals)
        wei = int(amount * 10**18)
        result = self.exchange.token_delegate(validator, wei, is_undelegate=True)
        logger.info(f"Undelegated {amount} HYPE from {validator}: {result}")
        return result
