
import pandas as pd
import re

df = pd.read_parquet('data/metadata.parquet')
avgo = df[df['Symbol'] == 'AVGO'].iloc[0]
summary = avgo['Business Summary'].lower()

rules = [r"\bnand\b", r"\bdram\b", r"dynamic random access memory", r"solid-state drive", r"hard disk drive", r"\bhdd\b", r"flash memory chip"]

for pattern in rules:
    if re.search(pattern, summary):
        print(f"MATCH: {pattern}")
        # Find match
        m = re.search(pattern, summary)
        print(f"Match found: {m.group(0)}")
        print(f"Context: ...{summary[max(0, m.start()-50):min(len(summary), m.end()+50)]}...")
