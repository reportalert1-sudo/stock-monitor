
import pandas as pd
import os

df = pd.read_parquet('data/metadata.parquet')
for t in ['MU', 'WDC', 'STX']:
    row = df[df['Symbol'] == t]
    print(f"\n--- {t} ---")
    print(row.iloc[0]['Business Summary'])
