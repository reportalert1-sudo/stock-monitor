
import yfinance as yf
import pandas as pd

def get_tickers():
    # Placeholder: getting a small list of tech stocks to test
    return ["AAPL", "NVDA", "MSFT", "TSLA", "GOOG", "AMD", "INTC", "AMZN", "META", "NFLX"]

def test_fetch_and_calc():
    tickers = get_tickers()
    print(f"Fetching data for {len(tickers)} tickers...")
    
    # Fetch 1 month of data to ensure we have 20 days
    data = yf.download(tickers, period="1mo", group_by='ticker', auto_adjust=True)
    
    results = []
    
    for ticker in tickers:
        try:
            df = data[ticker]
            # Calculate daily turnover
            df['Turnover'] = df['Close'] * df['Volume']
            
            # Get last 20 days
            last_20 = df.tail(20)
            avg_turnover = last_20['Turnover'].mean()
            
            # Get YTD (approximate using 1 month data for now, or fetch YTD separately)
            # For this test, we just check if we can calculate turnover
            
            print(f"{ticker}: Avg Turnover 20d = ${avg_turnover:,.2f}")
            results.append({
                "Ticker": ticker, 
                "AvgTurnover": avg_turnover
            })
        except Exception as e:
            print(f"Error for {ticker}: {e}")
            
    return pd.DataFrame(results)

if __name__ == "__main__":
    df = test_fetch_and_calc()
    print("\nResults:")
    print(df)
