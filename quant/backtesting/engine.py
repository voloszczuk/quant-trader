"""Minimal vectorized backtester. Built for research, not fill-level simulation."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from quant.strategies.base import Strategy


@dataclass
class BacktestResult:
    equity: pd.Series
    returns: pd.Series
    stats: dict[str, float]


def run_backtest(
    df: pd.DataFrame,
    strategy: Strategy,
    fee: float = 0.001,
    periods_per_year: int = 365,
) -> BacktestResult:
    """Run `strategy` over `df`.

    Signals are shifted one bar so a signal computed on bar t is traded on
    bar t+1 (no look-ahead). `fee` is charged on every position change.
    """
    position = strategy.generate_signals(df).shift(1).fillna(0)
    bar_returns = df["close"].pct_change().fillna(0.0)
    changes = position.diff().abs().fillna(0.0)
    strat_returns = position * bar_returns - changes * fee
    equity = (1 + strat_returns).cumprod()

    drawdown = equity / equity.cummax() - 1
    std = strat_returns.std()
    stats = {
        "total_return": float(equity.iloc[-1] - 1),
        "buy_hold_return": float(df["close"].iloc[-1] / df["close"].iloc[0] - 1),
        "ann_sharpe": float(strat_returns.mean() / std * np.sqrt(periods_per_year)) if std > 0 else 0.0,
        "max_drawdown": float(drawdown.min()),
        "time_in_market": float((position != 0).mean()),
        "position_changes": float((changes > 0).sum()),
    }
    return BacktestResult(equity=equity, returns=strat_returns, stats=stats)
