
from storage import load_metadata, save_metadata, load_market_data, save_market_data, get_latest_date
import numpy as np
import pandas as pd
import requests
import yfinance as yf
import datetime
import concurrent.futures

# Yahoo Finance can be flaky with 401 errors.
def fetch_info_with_retry(ticker, retries=2):
    try:
        t = yf.Ticker(ticker)
        # Accessing info can trigger the 401 if not lucky
        info = t.info
        if info:
            return info
    except Exception:
        pass
    return {}

def get_sp500_tickers():
    """Retrives S&P 500 tickers, names, and sectors from Wikipedia."""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Using lxml parser if possible to avoid dependencies issues
        tables = pd.read_html(response.text)
        df = tables[0]
        
        # Initial cleanup
        df['Symbol'] = df['Symbol'].str.replace('.', '-', regex=False)
        
        # Return relevant columns
        return df[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']]
    except Exception as e:
        print(f"Error fetching S&P 500 tickers: {e}")
        return pd.DataFrame()

def fetch_single_metadata(row, force_refresh):
    """Helper to fetch metadata for a single row."""
    ticker = row['Symbol']
    summary = row.get('Business Summary', '')
    tags = row.get('Smart Tags', '')
    industry = row.get('GICS Industry', '')
    
    needs_update = force_refresh or pd.isna(summary) or summary == "" or pd.isna(industry) or industry == ""
    
    if needs_update:
        info = fetch_info_with_retry(ticker)
        if info:
            summary = info.get('longBusinessSummary', summary)
            industry = info.get('industry', industry)
    
    # Automatic Tagging Removed - Themes are now strictly user-input
    return {
        'Symbol': ticker,
        'Security': row['Security'],
        'GICS Sector': row['GICS Sector'],
        'GICS Industry': industry,
        'GICS Sub-Industry': row['GICS Sub-Industry'],
        'Business Summary': summary,
        'Smart Tags': tags,
        'LastUpdated': datetime.datetime.now()
    }

def update_metadata(force_refresh=False):
    """
    Updates metadata for S&P 500 tickers.
    """
    print("Updating metadata...")
    current_df = load_metadata()
    wiki_df = get_sp500_tickers()
    
    if wiki_df.empty:
        print("Failed to fetch S&P 500 list.")
        return current_df
        
    if not current_df.empty:
        existing_cols = [c for c in ['Symbol', 'Business Summary', 'Smart Tags', 'GICS Industry', 'LastUpdated'] if c in current_df.columns]
        merged = pd.merge(wiki_df, current_df[existing_cols], on='Symbol', how='left')
    else:
        merged = wiki_df.copy()
        merged['Business Summary'] = ""
        merged['Smart Tags'] = ""
        merged['GICS Industry'] = ""
        merged['LastUpdated'] = pd.NaT

    rows_to_process = [row.to_dict() for _, row in merged.iterrows()]
    
    print(f"Checking metadata for {len(rows_to_process)} tickers...")
    updated_rows = []
    
    # Reduced threads to avoid Yahoo rate limits
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_single_metadata, r, force_refresh) for r in rows_to_process]
        for future in concurrent.futures.as_completed(futures):
            updated_rows.append(future.result())
        
    new_metadata_df = pd.DataFrame(updated_rows)
    save_metadata(new_metadata_df)
    return new_metadata_df

def update_market_data(tickers):
    """
    Updates market data (Price, Volume, Turnover).
    """
    print("Updating market data...")
    existing_data = load_market_data()
    
    if not existing_data.empty:
        last_date = pd.to_datetime(existing_data['Date'].max()).date()
        start_date = last_date + datetime.timedelta(days=1)
    else:
        start_date = datetime.date.today() - datetime.timedelta(days=180)
        
    if start_date > datetime.date.today():
        print("Market data is up to date.")
        return existing_data

    print(f"Fetching data from {start_date}...")
    fetch_start = start_date
    if not existing_data.empty:
        fetch_start = start_date - datetime.timedelta(days=7)
    
    try:
        new_data = yf.download(tickers, start=fetch_start, group_by='ticker', auto_adjust=True, threads=True)
    except Exception as e:
        print(f"Error downloading market data: {e}")
        return existing_data
        
    if new_data.empty:
        return existing_data
        
    final_dfs = []
    for ticker in tickers:
        try:
            if ticker not in new_data.columns.levels[0]: continue
            df = new_data[ticker].copy().reset_index()
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            df['Turnover'] = df['Close'] * df['Volume']
            df['Ticker'] = ticker
            final_dfs.append(df[['Date', 'Ticker', 'Close', 'Volume', 'Turnover']])
        except: continue
            
    if not final_dfs: return existing_data
        
    new_df = pd.concat(final_dfs)
    combined = pd.concat([existing_data, new_df]).drop_duplicates(subset=['Date', 'Ticker'], keep='last')
    combined = combined.sort_values(by=['Ticker', 'Date'])
    save_market_data(combined)
    return combined

def get_monitor_data(force_refresh_metadata=False):
    """Main entry point."""
    metadata = update_metadata(force_refresh=force_refresh_metadata)
    tickers = metadata['Symbol'].tolist()
    market_data = update_market_data(tickers)
    
    if market_data.empty: return pd.DataFrame()
    
    print("Calculating metrics...")
    today = datetime.date.today()
    start_of_year = datetime.date(today.year, 1, 1)
    
    results = []
    for ticker, group in market_data.groupby('Ticker'):
        try:
            group = group.sort_values('Date')
            last_20 = group.tail(20)
            avg_turnover = last_20['Turnover'].mean() if len(last_20) >= 20 else 0
            
            group_ytd = group[group['Date'] >= start_of_year]
            ytd_perf = ((group_ytd.iloc[-1]['Close'] - group_ytd.iloc[0]['Close']) / group_ytd.iloc[0]['Close'] * 100) if not group_ytd.empty else None
            
            perf_5d = 0.0
            if len(group) >= 6:
                perf_5d = ((group.iloc[-1]['Close'] - group.iloc[-6]['Close']) / group.iloc[-6]['Close'] * 100)
            
            meta_row = metadata[metadata['Symbol'] == ticker].iloc[0]
            
            results.append({
                "Ticker": ticker,
                "Name": meta_row['Security'],
                "Themes": meta_row['Smart Tags'],
                "GICS Sector": meta_row['GICS Sector'],
                "GICS Industry": meta_row.get('GICS Industry', ''),
                "GICS Sub-Industry": meta_row['GICS Sub-Industry'],
                "Current Price": group.iloc[-1]['Close'],
                "Avg Daily Turnover (20d)": avg_turnover,
                "Latest Turnover": group.iloc[-1]['Turnover'],
                "Turnover Ratio": (group.iloc[-1]['Turnover'] / avg_turnover) if avg_turnover > 0 else 0,
                "YTD Performance (%)": ytd_perf,
                "5-Day Performance (%)": perf_5d
            })
        except: continue
            
    df_res = pd.DataFrame(results)
    if df_res.empty: return df_res
    
    # Calculate Ranks (1 is best)
    df_res['Rank YTD%'] = df_res['YTD Performance (%)'].rank(ascending=False, method='min')
    df_res['Rank 5D%'] = df_res['5-Day Performance (%)'].rank(ascending=False, method='min')
    df_res['Rank Turnover Ratio'] = df_res['Turnover Ratio'].rank(ascending=False, method='min')
    df_res['Rank 20d Vol'] = df_res['Avg Daily Turnover (20d)'].rank(ascending=False, method='min')
    
    # Overall Rank - Average of 4 individual ranks
    df_res['Overall Score'] = (df_res['Rank YTD%'] + df_res['Rank 5D%'] + 
                               df_res['Rank Turnover Ratio'] + df_res['Rank 20d Vol']) / 4
    df_res['Overall Rank'] = df_res['Overall Score'].rank(ascending=True, method='min')
    
    # Clean up intermediate score
    df_res = df_res.drop(columns=['Overall Score'])
    
    return df_res

if __name__ == "__main__":
    get_monitor_data()
