import os
import sys
import yfinance as yf
import pandas as pd

def get_input(name):
    return os.environ.get(f"INPUT_{name.upper()}")

def main():
    # 1. Recuperar configuraciones desde variables de entorno (INPUTS)
    tickers_input = get_input("tickers") or "IVV,VGT,SCHD,VHT,ITA,VFH,BTC-USD,ETH-USD"
    enable_readme = get_input("enable_readme") == "true"
    enable_telegram = get_input("enable_telegram") == "true"
    enable_email = get_input("enable_email") == "true"

    print(f"--- Financial Tracker & Agent Configuration ---")
    print(f"Tickers to track: {tickers_input}")
    print(f"Update README: {enable_readme}")
    print(f"Telegram Alerts: {enable_telegram}")
    print(f"Email Alerts: {enable_email}")
    print(f"------------------------------------------------")

    tickers_list = [t.strip() for t in tickers_input.split(",")]

    # 2. Lógica de recolección de datos (Placeholder inicial)
    try:
        print(f"Fetching data for: {tickers_list}")
        # Aquí vendrá la lógica con yfinance
        # data = yf.download(tickers_list, period="1d")
        
        # 3. Lógica de módulos (Placeholder)
        if enable_readme:
            print("Processing README update...")
        
        if enable_telegram:
            print("Sending Telegram alerts...")

        if enable_email:
            print("Sending Email reports...")

    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
