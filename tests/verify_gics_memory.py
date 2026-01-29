
import pandas as pd
import os

metadata_path = 'data/metadata.parquet'
if os.path.exists(metadata_path):
    df = pd.read_parquet(metadata_path)
    
    # Check Columns
    target_cols = ['GICS Sector', 'GICS Industry', 'GICS Sub-Industry']
    found_cols = [c for c in target_cols if c in df.columns]
    print(f"GICS Columns found: {found_cols}")
    
    # Check Industry Sample
    print("\nIndustry Samples (first 5):")
    print(df[['Symbol', 'GICS Industry']].head())
    
    # Check Memory
    mem = df[df['Smart Tags'].str.contains('Memory', na=False)]
    print(f"\nTotal Memory stocks: {len(mem)}")
    print(f"Memory Tickers: {list(mem.Symbol)}")
    
    # Check Specific Disputed Tickers
    disputed = ['AVGO', 'DELL', 'SMCI', 'AAPL']
    print("\nVerification for Disputed Tickers:")
    for t in disputed:
        row = df[df['Symbol'] == t]
        if not row.empty:
            print(f"{t} Tags: {row.iloc[0]['Smart Tags']}")
        else:
            print(f"{t} not found in metadata.")
else:
    print("Metadata not found.")
