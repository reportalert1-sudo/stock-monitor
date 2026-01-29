
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.data import get_monitor_data

# mimic logic in app.py
def calculate_theme_performance(df):
    theme_rows = []
    for _, row in df.iterrows():
        if pd.notna(row['Themes']) and row['Themes']:
            themes = row['Themes'].split(', ')
            for theme in themes:
                theme_rows.append({
                    'Theme': theme,
                    'YTD Performance (%)': row['YTD Performance (%)'],
                    '5-Day Performance (%)': row.get('5-Day Performance (%)', 0.0),
                    'Turnover Ratio': row.get('Turnover Ratio', 0.0)
                })
    
    theme_df = pd.DataFrame(theme_rows)
    if theme_df.empty:
        return pd.DataFrame()
        
    leaderboard = theme_df.groupby('Theme').agg({
        'YTD Performance (%)': 'mean',
        '5-Day Performance (%)': 'mean',
        'Turnover Ratio': 'mean',
        'Theme': 'count'
    }).rename(columns={'Theme': 'Count'})
    
    return leaderboard.sort_values(by='5-Day Performance (%)', ascending=False)

print("Fetching data...")
# Force refresh to ensure new 5-day column is there if not cached
# Note: get_monitor_data(force=False) reads from parquet. If parquet was written by OLD data.py, it won't have 5-Day.
# We might need to run update to populate it first.
df = get_monitor_data() 

if '5-Day Performance (%)' not in df.columns:
    print("5-Day Performance column MISSING from dataframe. Triggering update...")
    from src.data import update_market_data, update_metadata
    # This rebuilds the parquet with new logic
    df = get_monitor_data(force_refresh_metadata=False)

print("Columns:", df.columns)
print("Leaderboard:")
leaderboard = calculate_theme_performance(df)
print(leaderboard.head(10))
