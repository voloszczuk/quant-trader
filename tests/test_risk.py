from quant.risk.manager import RiskManager, fixed_stop, position_size, trailing_stop


def test_position_size_capped_by_max_position():
    # 1% of 10k = $100 risk over $2 -> 50 units, but cap is 25% of 10k / $100 = 25
    assert position_size(10_000, entry=100, stop=98) == 25


def test_position_size_uses_risk_budget_when_under_cap():
    # $100 risk over $10 stop distance -> 10 units
    assert position_size(10_000, entry=100, stop=90) == 10


def test_position_size_zero_when_no_stop_distance():
    assert position_size(10_000, entry=100, stop=100) == 0.0


def test_fixed_stop():
    assert fixed_stop(100, "long", 0.03) == 97
    assert fixed_stop(100, "short", 0.03) == 103


def test_trailing_stop_never_loosens():
    assert trailing_stop(97, price=90, side="long", pct=0.03) == 97
    assert trailing_stop(97, price=110, side="long", pct=0.03) > 97


def test_daily_loss_limit_halts_trading():
    rm = RiskManager(max_daily_loss_pct=0.05)
    assert rm.can_trade(10_000)
    assert not rm.can_trade(9_000)
