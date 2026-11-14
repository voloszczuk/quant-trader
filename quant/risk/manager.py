"""Risk management: position sizing, stop-losses and a daily loss limit."""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import date
from typing import Literal

import pandas as pd

log = logging.getLogger(__name__)
Side = Literal["long", "short"]


def position_size(
    equity: float,
    entry: float,
    stop: float,
    risk_per_trade: float = 0.01,
    max_position_pct: float = 0.25,
    step: float = 0.0,
) -> float:
    """Fixed-fractional sizing.

    Risk `risk_per_trade` of equity between entry and stop, then cap the
    notional at `max_position_pct` of equity. `step` rounds down to lot size.
    """
    risk_per_unit = abs(entry - stop)
    if equity <= 0 or entry <= 0 or risk_per_unit == 0:
        return 0.0
    qty = (equity * risk_per_trade) / risk_per_unit
    qty = min(qty, (equity * max_position_pct) / entry)
    if step > 0:
        qty = math.floor(qty / step) * step
    return max(qty, 0.0)


def fixed_stop(entry: float, side: Side, pct: float) -> float:
    """Percentage stop-loss price."""
    return entry * (1 - pct) if side == "long" else entry * (1 + pct)


def atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    """Average True Range from high/low/close columns."""
    prev_close = df["close"].shift(1)
    true_range = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return true_range.rolling(window).mean()


def atr_stop(entry: float, atr_value: float, side: Side, mult: float = 2.0) -> float:
    """Volatility-adjusted stop: `mult` ATRs away from entry."""
    return entry - mult * atr_value if side == "long" else entry + mult * atr_value


def trailing_stop(current_stop: float, price: float, side: Side, pct: float) -> float:
    """Ratchet a stop in the profitable direction only. It never loosens."""
    candidate = fixed_stop(price, side, pct)
    return max(current_stop, candidate) if side == "long" else min(current_stop, candidate)


@dataclass
class RiskManager:
    """Tracks daily PnL and blocks new trades once the loss limit is hit."""

    max_daily_loss_pct: float = 0.05
    _day: date = field(default_factory=date.today)
    _start_equity: float | None = None

    def can_trade(self, equity: float) -> bool:
        today = date.today()
        if self._start_equity is None or today != self._day:
            self._day, self._start_equity = today, equity
        drawdown = (self._start_equity - equity) / self._start_equity
        if drawdown >= self.max_daily_loss_pct:
            log.warning("Daily loss limit hit (%.2f%%). Trading halted.", drawdown * 100)
            return False
        return True
