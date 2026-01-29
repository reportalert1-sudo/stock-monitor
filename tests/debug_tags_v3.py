
import pandas as pd
import re

df = pd.read_parquet('data/metadata.parquet')

def debug_theme(ticker, theme):
    row = df[df['Symbol'] == ticker]
    summary = row.iloc[0]['Business Summary'].lower()
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from classifier import get_classifier
    clf = get_classifier()
    rule = clf.rules[theme]
    
    print(f"\n--- DEBUGGING {ticker} FOR {theme} ---")
    sector = row.iloc[0]['GICS Sector']
    sub = row.iloc[0]['GICS Sub-Industry']
    sector_match = (sector in rule["sectors"]) or (sub in rule["sectors"])
    print(f"Sector: {sector} | Sub: {sub} | Sector Match: {sector_match}")
    
    for pattern in rule["keywords"]:
        if re.search(pattern, summary):
            print(f"MATCH FOUND: {pattern}")
        else:
            # print(f"NO MATCH: {pattern}")
            pass

debug_theme('META', 'Social Media')
debug_theme('MSFT', 'AI')
debug_theme('META', 'AI')
