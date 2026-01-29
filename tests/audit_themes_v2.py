
import pandas as pd
df = pd.read_parquet('data/metadata.parquet')

def check_stock(ticker):
    row = df[df['Symbol'] == ticker]
    if not row.empty:
        print(f"{ticker} ({row.iloc[0]['GICS Sub-Industry']}): {row.iloc[0]['Smart Tags']}")
    else:
        print(f"{ticker}: NOT FOUND")

print("--- E-COMMERCE CHECK ---")
for t in ['AMZN', 'EBAY', 'TPR', 'LULU', 'ETSY']:
    check_stock(t)

print("\n--- BIG TECH / CORE THEMES ---")
for t in ['NVDA', 'MSFT', 'META', 'TSLA', 'NFLX', 'GOOGL', 'GOOG', 'AVGO', 'MU']:
    check_stock(t)

print("\n--- THEME COUNTS ---")
all_tags = []
for tags in df['Smart Tags'].dropna():
    all_tags.extend(tags.split(', '))
counts = pd.Series(all_tags).value_counts()
print(counts)
