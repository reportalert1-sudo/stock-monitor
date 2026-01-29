
import pandas as pd
import os

metadata_path = 'data/metadata.parquet'
if os.path.exists(metadata_path):
    df = pd.read_parquet(metadata_path)
    tickers = ['AVGO', 'DELL', 'SMCI']
    
    for t in tickers:
        row = df[df['Symbol'] == t]
        if not row.empty:
            print(f"\n--- {t} ---")
            print(f"Sector: {row.iloc[0]['GICS Sector']}")
            print(f"Sub-Industry: {row.iloc[0]['GICS Sub-Industry']}")
            print(f"Tags: {row.iloc[0]['Smart Tags']}")
            print(f"Summary Snippet: {row.iloc[0]['Business Summary'][:500]}...")
else:
    print("Metadata not found.")
