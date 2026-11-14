"""Central settings loader. Everything comes from environment variables / .env."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    exchange_id: str = "kraken"
    api_key: str = ""
    api_secret: str = ""
    dry_run: bool = True  # safe default: orders are logged, never sent
    risk_per_trade: float = 0.01
    max_position_pct: float = 0.25
    stop_loss_pct: float = 0.03

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            exchange_id=os.getenv("EXCHANGE_ID", "kraken"),
            api_key=os.getenv("API_KEY", ""),
            api_secret=os.getenv("API_SECRET", ""),
            dry_run=_bool("DRY_RUN", True),
            risk_per_trade=float(os.getenv("RISK_PER_TRADE", 0.01)),
            max_position_pct=float(os.getenv("MAX_POSITION_PCT", 0.25)),
            stop_loss_pct=float(os.getenv("STOP_LOSS_PCT", 0.03)),
        )


settings = Settings.from_env()
