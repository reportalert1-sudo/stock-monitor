
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classifier import get_classifier
from sentence_transformers import util
import pandas as pd

clf = get_classifier()

pfe_summary = "Pfizer Inc. discovers, develops, manufactures, and markets biopharmaceutical products worldwide."

# Manual score check
embedding = clf.model.encode(pfe_summary, convert_to_tensor=True)
scores = util.cos_sim(embedding, clf.theme_embeddings)[0]

print("\nScores for Pfizer:")
for name, score in zip(clf.theme_names, scores):
    print(f"{name}: {score:.4f}")
