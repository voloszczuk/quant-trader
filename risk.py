"""Risk tools: how much to buy, and where to put the stop-loss."""
from config import RISK_PER_TRADE, MAX_POSITION_PCT


def position_size(equity, entry, stop):
    """Risk only a small % of your account per trade."""
    risk_per_unit = abs(entry - stop)
    if risk_per_unit == 0:
        return 0.0
    qty = (equity * RISK_PER_TRADE) / risk_per_unit
    max_qty = (equity * MAX_POSITION_PCT) / entry  # never go all-in
    return min(qty, max_qty)


def stop_loss(entry, pct=0.03, side="long"):
    """Stop price pct away from entry (3% default)."""
    return entry * (1 - pct) if side == "long" else entry * (1 + pct)
