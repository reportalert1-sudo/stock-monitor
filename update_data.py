"""
Simplified Daily Market Data Update Script

This script only updates the market data (no snapshot saving).
Snapshots are calculated on-demand when viewing historical data.

Schedule this to run daily (e.g., after market close at 5 PM EST).
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data import update_metadata, update_market_data
from datetime import datetime

def main():
    print(f"=== Market Data Update - {datetime.now()} ===")
    
    try:
        # Update S&P 500 list (in case of changes)
        print("Updating S&P 500 metadata...")
        metadata = update_metadata(force_refresh=False)
        tickers = metadata['Symbol'].tolist()
        print(f"Found {len(tickers)} tickers")
        
        # Update market data (only fetches new data since last update)
        print("Updating market data...")
        market_data = update_market_data(tickers)
        
        if not market_data.empty:
            latest_date = market_data['Date'].max()
            print(f"✅ Market data updated successfully!")
            print(f"   Latest date: {latest_date}")
            print(f"   Total records: {len(market_data)}")
        else:
            print("⚠️ No market data available")
            
    except Exception as e:
        print(f"❌ Error updating market data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
