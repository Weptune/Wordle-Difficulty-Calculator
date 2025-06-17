import os
import sys
import pandas as pd

# Allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from features.letter_features import compute_lfs, compute_plfs, compute_rlp
from features.bigram_features import compute_hlt
from features.shape_features import compute_shape_features
from features.obscurity_score import compute_os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load dictionary and starter words
with open(os.path.join(DATA_PATH, 'words.txt'), 'r') as f:
    all_words = [w.strip().upper() for w in f if len(w.strip()) == 5]

starter_words = ["STARE", "CRANE", "SLATE", "AUDIO", "RAISE", "TRACE", "ARISE", "CARTE", "SALET", "REACT", "POINT", "BLUSH", "NYMPH", "DOING", "FIGHT"]

# ✅ Load precomputed WSA values
true_wsa_df = pd.read_csv(os.path.join(DATA_PATH, "true_wsa_scores.csv"))
true_wsa_lookup = {
    row["Word"].upper(): row["WSA"]
    for _, row in true_wsa_df.iterrows()
}

def calculate_difficulty(word: str) -> dict:
    word = word.upper()

    # Core features
    lfs = compute_lfs(word)
    plfs = compute_plfs(word)
    rlp = compute_rlp(word)
    hlt = compute_hlt(word)
    os_score = compute_os(word)

    # Lookup WSA
    wsa_normalized = round(true_wsa_lookup.get(word, 0.5), 3)  # fallback to 0.5 if missing

    # Final ODS score
    ods = round(
        0.25 * lfs +
        0.15 * plfs +
        0.15 * rlp +
        0.15 * hlt +
        0.15 * wsa_normalized +
        0.15 * os_score,
        3
    )

    expected_guesses = round(2.5 + ods * 3.5, 3)

    return {
        "Word": word,
        "LFS": round(lfs, 3),
        "PLFS": round(plfs, 3),
        "RLP": round(rlp, 3),
        "HLT": round(hlt, 3),
        "WSA": wsa_normalized,
        "OS": round(os_score, 3),
        "ODS": ods,
        "ExpectedGuesses": expected_guesses
    }
