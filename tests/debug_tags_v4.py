
import pandas as pd
import re
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))
from classifier import get_classifier

df = pd.read_parquet('data/metadata.parquet')

def debug_theme(ticker, theme):
    row = df[df['Symbol'] == ticker]
    if row.empty:
        print(f"{ticker} not found")
        return
    summary = row.iloc[0]['Business Summary'].lower()
    clf = get_classifier()
    rule = clf.rules[theme]
    
    print(f"\n--- DEBUGGING {ticker} FOR {theme} ---")
    sector = row.iloc[0]['GICS Sector']
    sub = row.iloc[0]['GICS Sub-Industry']
    sector_match = (sector in rule["sectors"]) or (sub in rule["sectors"])
    print(f"Sector: {sector} | Sub: {sub} | Sector Match: {sector_match}")
    print(f"Summary Start: {summary[:200]}...")
    
    for pattern in rule["keywords"]:
        if re.search(pattern, summary):
            print(f"MATCH FOUND: {pattern}")

debug_theme('META', 'Social Media')
debug_theme('MSFT', 'AI')
debug_theme('META', 'AI')
debug_theme('ADBE', 'AI')
