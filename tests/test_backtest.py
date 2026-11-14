import numpy as np
import pandas as pd

from quant.backtesting.engine import run_backtest
from quant.strategies.base import Strategy


class AlwaysLong(Strategy):
    def generate_signals(self, df):
        return pd.Series(1, index=df.index)


def _prices(n=300):
    rng = np.random.default_rng(1)
    return pd.DataFrame({"close": 100 * np.cumprod(1 + rng.normal(0.0005, 0.01, n))})


def test_first_bar_is_never_traded():
    result = run_backtest(_prices(), AlwaysLong())
    assert result.returns.iloc[0] == 0  # signals are shifted one bar


def test_always_long_zero_fee_matches_buy_and_hold():
    df = _prices()
    result = run_backtest(df, AlwaysLong(), fee=0.0)
    assert abs(result.stats["total_return"] - result.stats["buy_hold_return"]) < 1e-9


def test_fees_reduce_returns():
    df = _prices()
    free = run_backtest(df, AlwaysLong(), fee=0.0).stats["total_return"]
    paid = run_backtest(df, AlwaysLong(), fee=0.01).stats["total_return"]
    assert paid < free
