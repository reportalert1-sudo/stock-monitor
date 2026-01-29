
import pandas as pd
import os

metadata_path = 'data/metadata.parquet'
if os.path.exists(metadata_path):
    df = pd.read_parquet(metadata_path)
    
    # Check Memory
    mem = df[df['Smart Tags'].str.contains('Memory', na=False)]
    print(f"Total Memory stocks: {len(mem)}")
    print(f"Memory Tickers: {list(mem.Symbol)}")
    
    # Check Apple
    aapl = df[df['Symbol'] == 'AAPL']
    if not aapl.empty:
        print(f"AAPL Tags: {aapl.iloc[0]['Smart Tags']}")
    
    # Check for broad themes removal
    all_tags = set()
    for t in df['Smart Tags']:
        if t:
            all_tags.update(t.split(', '))
    
    unsuitable = {"Industrial", "Consumer Brands"}
    found_unsuitable = unsuitable.intersection(all_tags)
    print(f"Unsuitable themes found: {found_unsuitable}")
else:
    print("Metadata not found.")
