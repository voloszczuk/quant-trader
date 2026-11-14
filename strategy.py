"""Momentum: be long when price is rising AND above its long-term average."""
import pandas as pd


def momentum_signals(df, lookback=48, trend_window=200):
    close = df["close"]
    rising = close.pct_change(lookback) > 0
    uptrend = close > close.rolling(trend_window).mean()
    return (rising & uptrend).astype(int)  # 1 = long, 0 = stay out
