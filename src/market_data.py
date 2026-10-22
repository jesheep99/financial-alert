import yfinance as yf
import pandas as pd


class MarketData:
    def __init__(self, tickers):
        self.tickers = tickers

    def fetch_history(self, ticker, start_date=None):
        ticker_data = yf.Ticker(ticker)
        if start_date is None:
            history = ticker_data.history(period="max", auto_adjust=False)
        else:
            history = ticker_data.history(
                start=start_date.isoformat(),
                auto_adjust=False,
            )

        rows = []
        for session_date, values in history.iterrows():
            close = values.get("Close")
            if pd.isna(close):
                continue

            adj_close = values.get("Adj Close")
            volume = values.get("Volume")
            rows.append(
                (
                    ticker,
                    session_date.strftime("%Y-%m-%d"),
                    self._number(values.get("Open")),
                    self._number(values.get("High")),
                    self._number(values.get("Low")),
                    float(close),
                    self._number(adj_close),
                    int(volume) if pd.notna(volume) else None,
                )
            )
        return rows

    @staticmethod
    def _number(value):
        return float(value) if pd.notna(value) else None

    def fetch_data(self):
        print(f"Fetching market data for: {self.tickers}")
        data_list = []
        for ticker in self.tickers:
            try:
                t = yf.Ticker(ticker)
                # Obtenemos el historial para el último cierre y el actual
                hist = t.history(period="2d")
                if len(hist) >= 1:
                    price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else price
                    change = ((price - prev_price) / prev_price) * 100
                    
                    data_list.append({
                        "ticker": ticker,
                        "price": round(price, 2),
                        "change": round(change, 2)
                    })
            except Exception as e:
                print(f"Error fetching {ticker}: {e}")
        return pd.DataFrame(data_list)
