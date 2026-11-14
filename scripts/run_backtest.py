"""Usage: python -m scripts.run_backtest [--strategy momentum] [--plot]"""
from __future__ import annotations

import argparse
from pathlib import Path

from quant.backtesting.engine import run_backtest
from quant.execution.exchange import ExchangeClient
from quant.strategies.mean_reversion import MeanReversionStrategy
from quant.strategies.momentum import MomentumStrategy

PERIODS = {"1h": 24 * 365, "1d": 365}
PARAMS = {
    "1h": {"momentum": dict(lookback=48, trend_window=200), "mean_reversion": dict(window=48)},
    "1d": {"momentum": dict(lookback=20, trend_window=100), "mean_reversion": dict(window=20)},
}
STRATEGIES = {"momentum": MomentumStrategy, "mean_reversion": MeanReversionStrategy}
PCT_KEYS = {"total_return", "buy_hold_return", "max_drawdown", "time_in_market"}


def save_plot(result, df, path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    buy_hold = df["close"] / df["close"].iloc[0]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(result.equity.index, result.equity.values, label="Strategy", linewidth=1.8)
    ax.plot(buy_hold.index, buy_hold.values, label="Buy & hold", alpha=0.7)
    ax.set_title("Equity curve (growth of 1.0)")
    ax.grid(alpha=0.3)
    ax.legend()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=130)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="BTC/USD")
    parser.add_argument("--timeframe", default="1d", choices=list(PERIODS))
    parser.add_argument("--strategy", default="momentum", choices=list(STRATEGIES))
    parser.add_argument("--plot", action="store_true", help="save docs/equity_curve.png")
    args = parser.parse_args()

    df = ExchangeClient().fetch_ohlcv(args.symbol, args.timeframe, limit=720)
    strategy = STRATEGIES[args.strategy](**PARAMS[args.timeframe][args.strategy])
    result = run_backtest(df, strategy, periods_per_year=PERIODS[args.timeframe])

    print(f"{args.strategy} on {args.symbol} {args.timeframe} ({len(df)} bars)")
    for key, value in result.stats.items():
        text = f"{value:.2%}" if key in PCT_KEYS else f"{value:.2f}"
        print(f"{key:>18}: {text}")
    if args.plot:
        save_plot(result, df, "docs/equity_curve.png")
        print("saved docs/equity_curve.png")


if __name__ == "__main__":
    main()
