import os
from collections import Counter

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load all words
with open(os.path.join(DATA_PATH, "words.txt"), "r") as f:
    all_words = [w.strip().upper() for w in f if len(w.strip()) == 5]

# Letter frequency
letter_counts = Counter("".join(all_words))
max_letter_freq = max(letter_counts.values())
letter_weights = {c: 1 - (f / max_letter_freq) for c, f in letter_counts.items()}

# Positional frequency
position_counters = [Counter() for _ in range(5)]
for word in all_words:
    for i, c in enumerate(word):
        position_counters[i][c] += 1
max_pos_freq = [max(p.values()) for p in position_counters]
position_weights = [
    {c: 1 - (count / max_pos_freq[i]) for c, count in pos.items()}
    for i, pos in enumerate(position_counters)
]
def compute_lfs(word: str) -> float:
    raw = sum(letter_weights.get(c, 0.5) for c in word.upper()) / 5
    # Custom remapping:
    if raw <= 0.4:
        return round(raw * (0.5 / 0.4), 3)  # Map 0–0.4 to 0–0.5
    else:
        return round(0.5 + ((raw - 0.4) * (0.5 / 0.4)), 3)  # Map 0.4–0.8 to 0.5–1.0

def compute_plfs(word: str) -> float:
    return round(sum(position_weights[i].get(c, 0.5) for i, c in enumerate(word.upper())) / 5, 3)

def compute_rlp(word: str) -> float:
    return 1.0 if len(set(word.upper())) < 5 else 0.0
