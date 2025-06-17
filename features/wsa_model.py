import os
import joblib
import numpy as np
from features.shape_features import compute_shape_features
from features.letter_features import compute_lfs, compute_plfs, compute_rlp
from features.bigram_features import compute_hlt

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'wsa_regressor.pkl')

# Load dictionary and starter words
with open(os.path.join(DATA_PATH, "words.txt"), "r") as f:
    all_words = [w.strip().upper() for w in f if len(w.strip()) == 5]

starter_words = ["STARE", "CRANE", "SLATE", "AUDIO", "RAISE", "TRACE", "ARISE", "CARTE", "SALET", "REACT"]

# Load trained model
def load_wsa_model():
    return joblib.load(MODEL_PATH)

def predict_wsa_score(word: str, model=None) -> float:
    if model is None:
        model = load_wsa_model()

    shape_feats = compute_shape_features(word, all_words, starter_words)

    features = {
        "LFS": compute_lfs(word),
        "PLFS": compute_plfs(word),
        "RLP": compute_rlp(word),
        "HLT": compute_hlt(word),
        **shape_feats
    }

    X = np.array([[features[f] for f in model.feature_names_in_]])
    return float(model.predict(X)[0])
