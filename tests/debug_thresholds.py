
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.classifier import get_classifier
import pandas as pd
from sentence_transformers import util

clf = get_classifier()

def debug_stock(ticker, summary):
    print(f"\n--- Debugging {ticker} ---")
    text_embedding = clf.model.encode(summary, convert_to_tensor=True)
    cosine_scores = util.cos_sim(text_embedding, clf.theme_embeddings)[0]
    
    scores = []
    for i, score in enumerate(cosine_scores):
        scores.append({'Theme': clf.theme_names[i], 'Score': float(score)})
    
    scores_df = pd.DataFrame(scores).sort_values(by='Score', ascending=False)
    print(scores_df.head(10))

# Mock summaries or real ones
wfc_summary = "Wells Fargo & Company, a diversified financial services company, provides banking, investment, mortgage, and consumer and commercial finance products and services in the United States and internationally."
wdc_summary = "Western Digital Corporation develops, manufactures, and sells data storage devices and solutions."

debug_stock("WFC", wfc_summary)
debug_stock("WDC", wdc_summary)
