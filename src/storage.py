
import pandas as pd
import os
from datetime import datetime

DATA_DIR = "data"
METADATA_FILE = os.path.join(DATA_DIR, "metadata.parquet")
MARKET_DATA_FILE = os.path.join(DATA_DIR, "market_data.parquet")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# --- Metadata Storage ---

def load_metadata():
    """Loads metadata from parquet file."""
    if os.path.exists(METADATA_FILE):
        try:
            return pd.read_parquet(METADATA_FILE)
        except Exception as e:
            print(f"Error loading metadata: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

def save_metadata(df):
    """Saves metadata to parquet file."""
    ensure_data_dir()
    # Ensure LastUpdated is datetime
    if 'LastUpdated' not in df.columns:
        df['LastUpdated'] = datetime.now()
    
    # Store 'Themes' as string to avoid parquet issues with lists if any
    # (Though pyarrow handles lists, strings are safer for simple reading)
    # Checks if 'Themes' needs conversion? 
    # Our data.py puts a string "Theme1, Theme2". Correct.
    
    try:
        df.to_parquet(METADATA_FILE, index=False)
        print(f"Metadata saved to {METADATA_FILE}")
    except Exception as e:
        print(f"Error saving metadata: {e}")

# --- Market Data Storage ---

def load_market_data():
    """Loads market data from parquet file."""
    if os.path.exists(MARKET_DATA_FILE):
        try:
            return pd.read_parquet(MARKET_DATA_FILE)
        except Exception as e:
            print(f"Error loading market data: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

def save_market_data(df):
    """Saves market data to parquet file."""
    ensure_data_dir()
    try:
        df.to_parquet(MARKET_DATA_FILE, index=False)
        print(f"Market data saved to {MARKET_DATA_FILE}")
    except Exception as e:
        print(f"Error saving market data: {e}")

import json

SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

def load_settings():
    """Loads UI settings from json file."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            return {}
    return {}

def save_settings(settings):
    """Saves UI settings to json file."""
    ensure_data_dir()
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        print(f"Settings saved to {SETTINGS_FILE}")
    except Exception as e:
        print(f"Error saving settings: {e}")


def get_latest_date(df):
    """Returns the latest date in the dataframe or None."""
    if df.empty or 'Date' not in df.columns:
        return None
    return df['Date'].max()

# --- Historical Snapshot Storage ---

import sqlite3

SNAPSHOT_DB = os.path.join(DATA_DIR, "snapshots.db")

def init_snapshot_db():
    """Initialize the snapshot database with schema."""
    ensure_data_dir()
    conn = sqlite3.connect(SNAPSHOT_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_date DATE NOT NULL,
            ticker TEXT NOT NULL,
            name TEXT,
            themes TEXT,
            overall_rank INTEGER,
            rank_ytd INTEGER,
            rank_5d INTEGER,
            rank_turnover_ratio INTEGER,
            rank_20d_vol INTEGER,
            gics_sector TEXT,
            gics_industry TEXT,
            gics_sub_industry TEXT,
            current_price REAL,
            latest_turnover REAL,
            avg_daily_turnover_20d REAL,
            turnover_ratio REAL,
            ytd_performance REAL,
            five_day_performance REAL,
            UNIQUE(scan_date, ticker)
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_scan_date ON daily_snapshots(scan_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ticker ON daily_snapshots(ticker)")
    
    conn.commit()
    conn.close()

def save_daily_snapshot(df, scan_date=None):
    """Save a complete scan result with timestamp."""
    if df.empty:
        return
    
    if scan_date is None:
        scan_date = datetime.now().date()
    
    init_snapshot_db()
    conn = sqlite3.connect(SNAPSHOT_DB)
    
    # Prepare data for insertion
    records = []
    for _, row in df.iterrows():
        records.append((
            str(scan_date),
            row.get('Ticker', ''),
            row.get('Name', ''),
            row.get('Themes', ''),
            int(row.get('Overall Rank', 0)) if pd.notna(row.get('Overall Rank')) else None,
            int(row.get('Rank YTD%', 0)) if pd.notna(row.get('Rank YTD%')) else None,
            int(row.get('Rank 5D%', 0)) if pd.notna(row.get('Rank 5D%')) else None,
            int(row.get('Rank Turnover Ratio', 0)) if pd.notna(row.get('Rank Turnover Ratio')) else None,
            int(row.get('Rank 20d Vol', 0)) if pd.notna(row.get('Rank 20d Vol')) else None,
            row.get('GICS Sector', ''),
            row.get('GICS Industry', ''),
            row.get('GICS Sub-Industry', ''),
            float(row.get('Current Price', 0)) if pd.notna(row.get('Current Price')) else None,
            float(row.get('Latest Turnover', 0)) if pd.notna(row.get('Latest Turnover')) else None,
            float(row.get('Avg Daily Turnover (20d)', 0)) if pd.notna(row.get('Avg Daily Turnover (20d)')) else None,
            float(row.get('Turnover Ratio', 0)) if pd.notna(row.get('Turnover Ratio')) else None,
            float(row.get('YTD Performance (%)', 0)) if pd.notna(row.get('YTD Performance (%)')) else None,
            float(row.get('5-Day Performance (%)', 0)) if pd.notna(row.get('5-Day Performance (%)')) else None,
        ))
    
    # Use INSERT OR REPLACE to handle duplicates
    conn.executemany("""
        INSERT OR REPLACE INTO daily_snapshots (
            scan_date, ticker, name, themes, overall_rank, rank_ytd, rank_5d,
            rank_turnover_ratio, rank_20d_vol, gics_sector, gics_industry,
            gics_sub_industry, current_price, latest_turnover, avg_daily_turnover_20d,
            turnover_ratio, ytd_performance, five_day_performance
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    
    conn.commit()
    conn.close()
    print(f"Snapshot saved for {scan_date} ({len(records)} stocks)")

def get_available_dates():
    """Return list of all dates with saved snapshots."""
    if not os.path.exists(SNAPSHOT_DB):
        return []
    
    conn = sqlite3.connect(SNAPSHOT_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT scan_date FROM daily_snapshots ORDER BY scan_date DESC")
    dates = [row[0] for row in cursor.fetchall()]
    conn.close()
    return dates

def load_snapshot_by_date(scan_date):
    """Retrieve full dataset for a specific date."""
    if not os.path.exists(SNAPSHOT_DB):
        return pd.DataFrame()
    
    conn = sqlite3.connect(SNAPSHOT_DB)
    query = """
        SELECT 
            ticker as 'Ticker',
            name as 'Name',
            themes as 'Themes',
            overall_rank as 'Overall Rank',
            rank_ytd as 'Rank YTD%',
            rank_5d as 'Rank 5D%',
            rank_turnover_ratio as 'Rank Turnover Ratio',
            rank_20d_vol as 'Rank 20d Vol',
            gics_sector as 'GICS Sector',
            gics_industry as 'GICS Industry',
            gics_sub_industry as 'GICS Sub-Industry',
            current_price as 'Current Price',
            latest_turnover as 'Latest Turnover',
            avg_daily_turnover_20d as 'Avg Daily Turnover (20d)',
            turnover_ratio as 'Turnover Ratio',
            ytd_performance as 'YTD Performance (%)',
            five_day_performance as '5-Day Performance (%)'
        FROM daily_snapshots
        WHERE scan_date = ?
        ORDER BY overall_rank
    """
    df = pd.read_sql_query(query, conn, params=(str(scan_date),))
    conn.close()
    return df

def get_latest_snapshot_date():
    """Get the most recent snapshot date."""
    dates = get_available_dates()
    return dates[0] if dates else None
