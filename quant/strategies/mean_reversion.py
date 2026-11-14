"""Z-score mean reversion (long-only)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from quant.strategies.base import Strategy


class MeanReversionStrategy(Strategy):
    """Buy when price is `entry_z` std-devs below its rolling mean; exit near the mean."""

    name = "mean_reversion"

    def __init__(self, window: int = 48, entry_z: float = 2.0, exit_z: float = 0.5):
        self.window = window
        self.entry_z = entry_z
        self.exit_z = exit_z

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        close = df["close"]
        z = (close - close.rolling(self.window).mean()) / close.rolling(self.window).std()
        state, states = 0, []
        for value in z:
            if np.isnan(value):
                state = 0
            elif state == 0 and value < -self.entry_z:
                state = 1
            elif state == 1 and value > -self.exit_z:
                state = 0
            states.append(state)
        return pd.Series(states, index=df.index, dtype=int)
