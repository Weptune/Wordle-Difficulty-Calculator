import os
import pandas as pd
from tqdm import tqdm

from features.shape_features import compute_shape_features
from features.letter_features import compute_lfs, compute_plfs, compute_rlp
from features.bigram_features import compute_hlt

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

with open(os.path.join(DATA_PATH, "words.txt")) as f:
    all_words = [w.strip().upper() for w in f if len(w.strip()) == 5]

starter_words = ["STARE", "CRANE", "SLATE", "AUDIO", "RAISE", "TRACE", "ARISE", "CARTE", "SALET", "REACT", "POINT", "BLUSH", "NYMPH", "DOING", "FIGHT"]

rows = []

for word in tqdm(all_words, desc="Generating training data"):
    shape_feats = compute_shape_features(word, all_words, starter_words)

    row = {
        "Word": word,
        "LFS": compute_lfs(word),
        "PLFS": compute_plfs(word),
        "RLP": compute_rlp(word),
        "HLT": compute_hlt(word),
        **shape_feats
    }

    rows.append(row)

df = pd.DataFrame(rows)

# ✅ Drop OS only (optional: keep it for full-feature ODS)
if "OS" in df.columns:
    df = df.drop(columns=["OS"])

df.to_csv(os.path.join(DATA_PATH, "wsa_training_data.csv"), index=False)
print("✅ Saved clean wsa_training_data.csv")
