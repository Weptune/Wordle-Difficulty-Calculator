import os
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')
FREQ_FILE = os.path.join(DATA_PATH, 'word_frequencies.csv')

# Load frequency data
freq_df = pd.read_csv(FREQ_FILE)
freq_df = freq_df[freq_df['word'].apply(lambda x: isinstance(x, str) and len(x) == 5)]
freq_df['word'] = freq_df['word'].str.upper()

# Build frequency dictionary
freq_map = dict(zip(freq_df['word'], freq_df['frequency']))

def remap_frequency(freq: float) -> float:
    """
    Remap frequency to OS using updated tier cutoffs:
    - ≥ 2,000,000     → OS 0.0–0.5
    - 100k–2,000,000  → OS 0.5–0.7
    - 50k–100k        → OS 0.7–0.9
    - < 50k           → OS 0.9–1.0
    """
    if freq >= 2_000_000:
        return round(0.0 + (2_000_000 / freq) * 0.5, 3)
    elif 100_000 <= freq < 2_000_000:
        norm = (2_000_000 - freq) / (2_000_000 - 100_000)
        return round(0.5 + norm * 0.2, 3)
    elif 50_000 <= freq < 100_000:
        norm = (100_000 - freq) / (100_000 - 50_000)
        return round(0.7 + norm * 0.2, 3)
    else:
        return 1.0

def compute_os(word: str) -> float:
    word = word.upper()
    freq = freq_map.get(word, 0)
    if freq == 0:
        return 1.0
    return remap_frequency(freq)
