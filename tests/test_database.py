import tempfile
import unittest
from datetime import date
from pathlib import Path

from src.database import PriceDatabase


class PriceDatabaseTests(unittest.TestCase):
    def test_upsert_updates_existing_ticker_date(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "history.sqlite"
            row = ("IVV", "2026-10-21", 10.0, 12.0, 9.0, 11.0, 11.0, 100)

            with PriceDatabase(str(database_path)) as database:
                database.upsert_prices([row])
                database.upsert_prices([(*row[:5], 12.0, 12.0, 200)])

                latest_date = database.latest_date("IVV")
                stored_row = database.connection.execute(
                    """
                    SELECT ticker, price_date, close, volume
                    FROM daily_prices
                    """
                ).fetchone()

            self.assertEqual(latest_date, date(2026, 10, 21))
            self.assertEqual(stored_row, ("IVV", "2026-10-21", 12.0, 200))

    def test_latest_date_is_none_for_unknown_ticker(self):
        with tempfile.TemporaryDirectory() as directory:
            with PriceDatabase(str(Path(directory) / "history.sqlite")) as database:
                self.assertIsNone(database.latest_date("UNKNOWN"))


if __name__ == "__main__":
    unittest.main()
