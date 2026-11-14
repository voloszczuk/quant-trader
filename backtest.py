"""Downloads real prices and tests the strategy on past data."""
import ccxt
import pandas as pd
from config import EXCHANGE_ID
from strategy import momentum_signals

exchange = getattr(ccxt, EXCHANGE_ID)()
raw = exchange.fetch_ohlcv("BTC/USD", "1h", limit=700)
df = pd.DataFrame(raw, columns=["ts", "open", "high", "low", "close", "volume"])

# Shift by 1 so we trade on the NEXT bar (avoids cheating with future info)
position = momentum_signals(df, lookback=48, trend_window=200).shift(1).fillna(0)
returns = df["close"].pct_change().fillna(0)
fees = position.diff().abs().fillna(0) * 0.001
strategy_returns = position * returns - fees
equity = (1 + strategy_returns).cumprod()

print(f"Strategy return:  {equity.iloc[-1] - 1:.2%}")
print(f"Buy & hold:       {df['close'].iloc[-1] / df['close'].iloc[0] - 1:.2%}")
print(f"Max drawdown:     {(equity / equity.cummax() - 1).min():.2%}")
