
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.data import get_monitor_data
import pandas as pd

df = get_monitor_data(force_refresh_metadata=False)
print("Columns:", df.columns)
print("\nSample Data:")
print(df[['Ticker', 'Latest Turnover', 'Avg Daily Turnover (20d)', 'Turnover Ratio']].head())

# Check ratio logic
row = df.iloc[0]
calc_ratio = row['Latest Turnover'] / row['Avg Daily Turnover (20d)']
print(f"\nVerification for {row['Ticker']}:")
print(f"Latest: {row['Latest Turnover']}")
print(f"Avg: {row['Avg Daily Turnover (20d)']}")
print(f"Ratio (Data): {row['Turnover Ratio']}")
print(f"Ratio (Calc): {calc_ratio}")
print(f"Match: {abs(row['Turnover Ratio'] - calc_ratio) < 0.0001}")
