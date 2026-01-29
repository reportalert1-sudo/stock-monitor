
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data import get_sp500_tickers
df = get_sp500_tickers()
print(f"PFE in list: {'PFE' in df['Symbol'].values}")
