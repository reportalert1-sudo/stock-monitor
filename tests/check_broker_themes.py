
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.data import get_monitor_data
import pandas as pd

df = get_monitor_data(force_refresh_metadata=False)

new_themes = ["Social Media", "Travel & Leisure", "Robotics", "Blockchain"]
print(f"Checking for stocks in new themes: {new_themes}")

for theme in new_themes:
    # Filter stocks containing the theme
    matches = df[df['Themes'].str.contains(theme, na=False)]
    print(f"\n--- {theme} ({len(matches)}) ---")
    if not matches.empty:
        print(matches[['Ticker', 'Name']].head(10))
    else:
        print("No matches found.")

# Specific check for expected candidates
candidates = ["META", "ABNB", "BKNG", "CCL", "RCL", "DE", "CAT", "PYPL", "COIN"] 
print(f"\n--- Specific Candidates ---")
print(df[df['Ticker'].isin(candidates)][['Ticker', 'Themes']])
