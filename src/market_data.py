import yfinance as yf
import pandas as pd

class MarketData:
    def __init__(self, tickers):
        self.tickers = tickers

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
