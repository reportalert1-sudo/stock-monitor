"""
Automated Daily Stock Monitor Scheduler

This script runs the stock monitor scan and saves a daily snapshot.
Designed to be run via Windows Task Scheduler at a specific time each day.
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data import get_monitor_data
from storage import save_daily_snapshot, load_metadata, save_metadata

def run_daily_snapshot():
    """Execute daily scan and save snapshot."""
    print(f"[{datetime.now()}] Starting automated daily snapshot...")
    
    try:
        # Fetch fresh data (no force refresh to use cached metadata)
        print("Fetching market data...")
        df = get_monitor_data(force_refresh_metadata=False)
        
        if df.empty:
            print("ERROR: No data retrieved. Aborting snapshot.")
            return False
        
        # Save snapshot with today's date
        today = datetime.now().date()
        save_daily_snapshot(df, scan_date=today)
        
        print(f"✅ SUCCESS: Snapshot saved for {today} ({len(df)} stocks)")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to create snapshot: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_daily_snapshot()
    sys.exit(0 if success else 1)
