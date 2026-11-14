"""Thin ccxt wrapper. Dry-run by default: orders are logged, never sent."""
from __future__ import annotations

import logging
from typing import Any

import ccxt
import pandas as pd

from quant.config import Settings, settings

log = logging.getLogger(__name__)


class ExchangeClient:
    def __init__(self, cfg: Settings = settings):
        self.cfg = cfg
        params: dict[str, Any] = {"enableRateLimit": True}
        if cfg.api_key and cfg.api_secret:
            params.update(apiKey=cfg.api_key, secret=cfg.api_secret)
        self.ex = getattr(ccxt, cfg.exchange_id)(params)

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1d", limit: int = 720) -> pd.DataFrame:
        """Public market data. No API keys needed."""
        raw = self.ex.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(raw, columns=["ts", "open", "high", "low", "close", "volume"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        return df.set_index("ts")

    def market_order(self, symbol: str, side: str, amount: float) -> dict[str, Any]:
        """Place a market order ('buy' or 'sell'). Only logs while dry_run is True."""
        if self.cfg.dry_run:
            log.info("[DRY RUN] %s %s %s", side, amount, symbol)
            return {"dry_run": True, "symbol": symbol, "side": side, "amount": amount}
        order = self.ex.create_order(symbol, "market", side, amount)
        log.info("Order placed: %s", order.get("id"))
        return order
