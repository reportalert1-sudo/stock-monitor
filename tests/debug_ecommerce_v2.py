
import pandas as pd
import re

df = pd.read_parquet('data/metadata.parquet')
keywords = ["e-commerce", "online retail", "digital marketplace", "internet shopping"]

for t in ['TPR', 'LULU', 'AMZN', 'EBAY']:
    row = df[df['Symbol'] == t]
    if not row.empty:
        summary = row.iloc[0]['Business Summary'].lower()
        print(f"\n--- {t} ({row.iloc[0]['GICS Sub-Industry']}) ---")
        for kw in keywords:
            if kw in summary:
                # Find context
                idx = summary.find(kw)
                ctx = summary[max(0, idx-40):min(len(summary), idx+40)]
                print(f"MATCH: '{kw}' | Context: ...{ctx}...")
