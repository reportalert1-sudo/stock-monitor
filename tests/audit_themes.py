
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.data import get_monitor_data
import pandas as pd

df = get_monitor_data(force_refresh_metadata=False)

themes_to_audit = ["Consumer Brands", "Industrial"]
print(f"Auditing themes: {themes_to_audit}")

for theme in themes_to_audit:
    matches = df[df['Themes'].str.contains(theme, na=False)]
    print(f"\n--- {theme} ({len(matches)}) ---")
    print(matches[['Ticker', 'Name']].head(15))
    
    # Check overlap with new themes
    if theme == "Consumer Brands":
        overlap = matches[matches['Themes'].str.contains('E-commerce|Travel|Social|Gaming', regex=True)]
        print(f"Overlap with sharp themes: {len(overlap)} / {len(matches)}")
    if theme == "Industrial":
        overlap = matches[matches['Themes'].str.contains('Robotics|Defense|EV', regex=True)]
        print(f"Overlap with sharp themes: {len(overlap)} / {len(matches)}")
