"""Strategy interface."""
from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class Strategy(ABC):
    """Maps an OHLCV DataFrame to a position Series: 1 = long, 0 = flat."""

    name: str = "base"

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """Return one signal per row of `df`, using only data up to that row."""
