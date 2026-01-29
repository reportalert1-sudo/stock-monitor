
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pandas as pd
from src.data import get_monitor_data

df = get_monitor_data(force_refresh_metadata=False)
memory_stocks = df[df['Themes'].str.contains('Memory & Storage', na=False)]

print(f"Total Memory & Storage stocks: {len(memory_stocks)}")
print("\nTicker - Name - Summary Snippet")
for _, row in memory_stocks.iterrows():
    # Fetch summary from cache if possible, but for now just print names
    # We need to load full metadata to see summary
    print(f"{row['Ticker']} - {row['Name']}")

# Also debugging semantic scores for a known false positive if we can guess one
# likely candidates: Public Storage (PSA), Iron Mountain (IRM) - REITs
