
import pandas as pd

df = pd.read_parquet("data/metadata.parquet")
target_tickers = ["WDC", "STX", "mu", "PFE", "HD", "LMT", "NVDA"]

# Set option to display full text
pd.set_option('display.max_colwidth', None)

print(df[df['Symbol'].isin(target_tickers)][['Symbol', 'Smart Tags']])
