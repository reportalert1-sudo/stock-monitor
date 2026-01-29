
import yfinance as yf

tickers = ["WDC", "STX", "MU"]

print("Fetching summaries...")
for ticker in tickers:
    try:
        t = yf.Ticker(ticker)
        summary = t.info.get('longBusinessSummary', 'No summary found')
        print(f"\n--- {ticker} ---")
        print(summary)
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
