
import pandas as pd
import os

df = pd.read_parquet('data/metadata.parquet')
for t in ['TPR', 'LULU', 'AMZN', 'EBAY']:
    row = df[df['Symbol'] == t]
    if not row.empty:
        print(f"\n--- {t} ---")
        print(f"Sector: {row.iloc[0]['GICS Sector']}")
        print(f"Sub-Industry: {row.iloc[0]['GICS Sub-Industry']}")
        print(f"Tags: {row.iloc[0]['Smart Tags']}")
        print(row.iloc[0]['Business Summary'][:500] + "...")
