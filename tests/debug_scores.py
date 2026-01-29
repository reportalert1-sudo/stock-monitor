
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classifier import get_classifier
from sentence_transformers import util
import pandas as pd
import yfinance as yf

clf = get_classifier()

tickers = ["LMT", "WDC", "PFE"]
summaries = {}

# Fetch fresh summaries (or hardcode representative ones if we trusted cache, 
# but let's see what the classifier sees)
# Actually, let's load from cache to be sure we test exactly what triggered the tag
df = pd.read_parquet("data/metadata.parquet")

for t in tickers:
    row = df[df['Symbol'] == t]
    if not row.empty:
        summaries[t] = row.iloc[0]['Business Summary']

print(f"\nAnalyzing Scores (Threshold=0.20 resulted in noise)...")

for ticker, summary in summaries.items():
    if not summary:
        print(f"No summary for {ticker}")
        continue
        
    print(f"\n--- {ticker} ---")
    embedding = clf.model.encode(summary, convert_to_tensor=True)
    scores = util.cos_sim(embedding, clf.theme_embeddings)[0]
    
    # Print all scores > 0.15 to see the distribution
    score_pairs = []
    for name, score in zip(clf.theme_names, scores):
        score_pairs.append((name, score.item()))
    
    # Sort by score descending
    score_pairs.sort(key=lambda x: x[1], reverse=True)
    
    for name, score in score_pairs:
        if score > 0.15:
            print(f"{name}: {score:.4f}")
