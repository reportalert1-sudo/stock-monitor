
import pandas as pd
import re

df = pd.read_parquet('data/metadata.parquet')
avgo = df[df['Symbol'] == 'AVGO'].iloc[0]
summary = avgo['Business Summary'].lower()

keywords = ["nand", "dram", "ssd", "hard disk", "hdd", "flash memory", "non-volatile memory", "memory chip", "solid state drive"]
print(f"AVGO Summary head: {summary[:500]}...")

for kw in keywords:
    if kw in summary:
        print(f"MATCH FOUND: '{kw}'")
        # Print context
        idx = summary.find(kw)
        context = summary[max(0, idx-50):min(len(summary), idx+50)]
        print(f"Context: ...{context}...")
