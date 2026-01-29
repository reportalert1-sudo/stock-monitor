
import pandas as pd
df = pd.read_parquet('data/metadata.parquet')
print(f"Total Tickers: {len(df)}")
print(f"Blank Industry: {df['GICS Industry'].eq('').sum()}")
print(f"Blank Summary: {df['Business Summary'].eq('').sum()}")
print("\nFirst 10 rows:")
print(df[['Symbol', 'GICS Sector', 'GICS Industry', 'GICS Sub-Industry']].head(10))
