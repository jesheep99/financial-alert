import os
import sqlite3
from datetime import date
from typing import Iterable, Optional, Tuple


PriceRow = Tuple[
    str,
    str,
    Optional[float],
    Optional[float],
    Optional[float],
    float,
    Optional[float],
    Optional[int],
]


class PriceDatabase:
    def __init__(self, path: str):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_prices (
                ticker TEXT NOT NULL,
                price_date TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL NOT NULL,
                adj_close REAL,
                volume INTEGER,
                PRIMARY KEY (ticker, price_date)
            )
            """
        )
        self.connection.commit()

    def latest_date(self, ticker: str) -> Optional[date]:
        row = self.connection.execute(
            "SELECT MAX(price_date) FROM daily_prices WHERE ticker = ?",
            (ticker,),
        ).fetchone()
        return date.fromisoformat(row[0]) if row and row[0] else None

    def upsert_prices(self, rows: Iterable[PriceRow]):
        with self.connection:
            self.connection.executemany(
                """
                INSERT INTO daily_prices (
                    ticker, price_date, open, high, low, close, adj_close, volume
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ticker, price_date) DO UPDATE SET
                    open = excluded.open,
                    high = excluded.high,
                    low = excluded.low,
                    close = excluded.close,
                    adj_close = excluded.adj_close,
                    volume = excluded.volume
                """,
                rows,
            )

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "PriceDatabase":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
