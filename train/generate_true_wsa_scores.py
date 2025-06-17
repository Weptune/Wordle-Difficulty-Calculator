import os
import pandas as pd
from tqdm import tqdm
from features.true_wsa import compute_true_wsa

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load full word list
with open(os.path.join(DATA_PATH, 'words.txt'), 'r') as f:
    words = [w.strip().upper() for w in f if len(w.strip()) == 5]

# Step 1: Compute raw WSA values
wsa_raw = []
for word in tqdm(words, desc="Computing true WSA"):
    avg_remaining = compute_true_wsa(word)
    wsa_raw.append((word, avg_remaining))

# Step 2: Normalize WSA to [0, 1]
df = pd.DataFrame(wsa_raw, columns=["Word", "RawWSA"])
min_val = df["RawWSA"].min()
max_val = df["RawWSA"].max()
df["WSA"] = df["RawWSA"].apply(lambda x: round((x - min_val) / (max_val - min_val), 3))

# Step 3: Save
output_path = os.path.join(DATA_PATH, "true_wsa_scores.csv")
df.to_csv(output_path, index=False)
print(f"✅ Saved normalized WSA scores to {output_path}")
print(f"⚙️ WSA min: {min_val}, max: {max_val}")
