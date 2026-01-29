
import yfinance as yf

ticker = "PFE"
t = yf.Ticker(ticker)
print(f"--- {ticker} ---")
summary = t.info.get('longBusinessSummary')
print(f"Summary length: {len(summary) if summary else 0}")
print(summary[:100] if summary else "None")
