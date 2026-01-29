
import pandas as pd
df = pd.read_parquet('data/metadata.parquet')
for t in ['MU', 'WDC', 'STX', 'AVGO']:
    row = df[df['Symbol'] == t]
    print(f"{t}: {row.iloc[0]['Smart Tags']}")
