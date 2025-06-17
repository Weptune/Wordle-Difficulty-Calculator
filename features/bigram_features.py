import os
import pandas as pd
from collections import Counter
from scipy.stats import rankdata

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load dictionary
with open(os.path.join(DATA_PATH, "words.txt"), "r") as f:
    all_words = [w.strip().upper() for w in f if len(w.strip()) == 5]

# Load bigram rarity data
bigram_df = pd.read_csv(os.path.join(DATA_PATH, "bigram_log_rarity_scores.csv"))
bigram_scores = {
    row["bigram"].upper(): float(row["log_rarity_score"])
    for _, row in bigram_df.iterrows()
    if isinstance(row["bigram"], str) and isinstance(row["log_rarity_score"], (int, float))
}

def original_hlt(word: str) -> float:
    """Compute raw average bigram rarity score for a word (before normalization)."""
    word = word.upper()
    bigrams = [word[i:i+2] for i in range(4)]
    return sum(bigram_scores.get(bg, 0.5) for bg in bigrams) / 4

# Compute raw HLT for all words
raw_hlt_values = [original_hlt(w) for w in all_words]

# Convert to percentile ranks
ranks = rankdata(raw_hlt_values, method='average')
normalized_hlt_map = {
    word: round((rank - 1) / (len(all_words) - 1), 3)
    for word, rank in zip(all_words, ranks)
}

def compute_hlt(word: str) -> float:
    return normalized_hlt_map.get(word.upper(), 0.5)  # default to 0.5 if word not found
