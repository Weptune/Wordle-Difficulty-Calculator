import os
import joblib

def load_wsa_model(path=None):
    if path is None:
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, "wsa_regressor.pkl")
    
    model = joblib.load(path)
    return model
