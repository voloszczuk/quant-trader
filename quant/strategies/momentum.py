"""Time-series momentum with a trend filter."""
from __future__ import annotations

import pandas as pd

from quant.strategies.base import Strategy


class MomentumStrategy(Strategy):
    """Long when recent returns are positive AND price is above its moving average."""

    name = "momentum"

    def __init__(self, lookback: int = 48, trend_window: int = 200):
        self.lookback = lookback
        self.trend_window = trend_window

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        close = df["close"]
        rising = close.pct_change(self.lookback) > 0
        uptrend = close > close.rolling(self.trend_window).mean()
        return (rising & uptrend).astype(int)
