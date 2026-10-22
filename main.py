import os
import sys
from datetime import timedelta

from src.database import PriceDatabase
from src.market_data import MarketData

def get_input(name):
    return os.environ.get(f"INPUT_{name.upper()}")


def main():
    # 1. Recuperar configuraciones desde variables de entorno (INPUTS)
    tickers_input = get_input("tickers") or "IVV,VGT,SCHD,VHT,ITA,VFH,BTC-USD,ETH-USD"
    enable_readme = (get_input("enable_readme") or "true").lower() == "true"
    enable_telegram = (get_input("enable_telegram") or "false").lower() == "true"
    enable_email = (get_input("enable_email") or "false").lower() == "true"
    workspace = os.environ.get("GITHUB_WORKSPACE", os.path.dirname(os.path.abspath(__file__)))
    database_path = get_input("database_path") or "data/prices.sqlite"
    if not os.path.isabs(database_path):
        database_path = os.path.join(workspace, database_path)

    print(f"--- Financial Tracker & Agent Configuration ---")
    print(f"Tickers to track: {tickers_input}")
    print(f"SQLite database: {database_path}")
    print(f"Update README: {enable_readme}")
    print(f"Telegram Alerts: {enable_telegram}")
    print(f"Email Alerts: {enable_email}")
    print(f"------------------------------------------------")

    tickers_list = [ticker.strip() for ticker in tickers_input.split(",") if ticker.strip()]

    try:
        if not tickers_list:
            raise ValueError("At least one ticker must be configured")

        market_data = MarketData(tickers_list)
        with PriceDatabase(database_path) as database:
            failed_tickers = []
            for ticker in tickers_list:
                try:
                    latest_date = database.latest_date(ticker)
                    start_date = latest_date - timedelta(days=7) if latest_date else None
                    rows = market_data.fetch_history(ticker, start_date)
                    if rows:
                        database.upsert_prices(rows)
                        print(f"Stored {len(rows)} daily records for {ticker}")
                    else:
                        print(f"No market data returned for {ticker}")
                        failed_tickers.append(ticker)
                except Exception as error:
                    print(f"Error fetching or storing {ticker}: {error}")
                    failed_tickers.append(ticker)

            if failed_tickers:
                raise RuntimeError(
                    "Failed to update market history for: "
                    + ", ".join(failed_tickers)
                )

        if enable_readme:
            print("Processing README update...")

        if enable_telegram:
            print("Sending Telegram alerts...")

        if enable_email:
            print("Sending Email reports...")

    except Exception as error:
        print(f"Error during execution: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
