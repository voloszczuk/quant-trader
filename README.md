# quant-trader

Modular Python framework for researching and backtesting systematic crypto trading strategies.

> **Status:** research and paper trading only. No live capital.

## Features

- Vectorized backtester with transaction costs and next-bar execution (no look-ahead bias)
- Time-series momentum strategy with a trend filter
- Risk module: fixed-fractional position sizing and percentage stop-losses
- Market data via [ccxt](https://github.com/ccxt/ccxt)
- Secrets and settings loaded from environment variables

## Quickstart

```bash
pip install -r requirements.txt
python backtest.py
```

## Methodology

- Signals are shifted one bar, so trades execute on the following bar
- A 0.1% fee is charged on every position change
- Results are compared against a buy-and-hold benchmark
- Not yet modeled: slippage, funding rates, partial fills

## Roadmap

- [ ] Multi-year backtests with out-of-sample validation
- [ ] Mean-reversion strategy
- [ ] Paper-trading execution loop

## Disclaimer

Educational project. Not financial advice. Backtest results do not predict future performance.
