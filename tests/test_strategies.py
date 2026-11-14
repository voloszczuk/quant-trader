import numpy as np
import pandas as pd

from quant.strategies.mean_reversion import MeanReversionStrategy
from quant.strategies.momentum import MomentumStrategy


def test_momentum_long_in_steady_uptrend():
    df = pd.DataFrame({"close": np.linspace(100, 200, 400)})
    sig = MomentumStrategy(lookback=20, trend_window=100).generate_signals(df)
    assert (sig.iloc[:90] == 0).all()  # warm-up: no signal yet
    assert sig.iloc[-1] == 1


def test_mean_reversion_buys_a_sharp_drop():
    rng = np.random.default_rng(0)
    close = np.append(100 + rng.normal(0, 0.1, 60), 90.0)
    sig = MeanReversionStrategy(window=20, entry_z=2.0).generate_signals(pd.DataFrame({"close": close}))
    assert sig.iloc[-1] == 1
    assert set(sig.unique()) <= {0, 1}
