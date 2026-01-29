
import pandas as pd
import requests

def get_sp500_tickers():
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        tables = pd.read_html(response.text)
        df = tables[0]
        
        # Initial cleanup
        df['Symbol'] = df['Symbol'].str.replace('.', '-', regex=False)
        
        return df[['Symbol', 'Security']]
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

df = get_sp500_tickers()
print(f"Total tickers: {len(df)}")
pfe = df[df['Symbol'] == 'PFE']
print(f"PFE Found: {not pfe.empty}")
if not pfe.empty:
    print(pfe)
