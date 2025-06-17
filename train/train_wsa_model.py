import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')

# Load training data
df = pd.read_csv(os.path.join(DATA_PATH, "wsa_training_data.csv"))

# Extract target and invert it so that higher = harder
y_raw = df["MatchReduction"]
y_inverted = y_raw.max() - y_raw

# Drop columns safely
drop_cols = ["Word", "MatchReduction"]
if "OS" in df.columns:
    drop_cols.append("OS")
X = df.drop(columns=drop_cols)

# Save training features list (optional: can be used during inference)
features_csv = os.path.join(MODEL_PATH, "wsa_features.csv")
pd.DataFrame(X.columns).to_csv(features_csv, index=False, header=False)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_inverted, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate performance
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"✅ Model trained. Test MSE: {mse:.4f}")

# Save model
joblib.dump(model, os.path.join(MODEL_PATH, "wsa_regressor.pkl"))
print("✅ Model saved.")

# Save normalization range for inference
predicted_wsa = model.predict(X)
wsa_min = predicted_wsa.min()
wsa_max = predicted_wsa.max()
with open(os.path.join(MODEL_PATH, "wsa_range.txt"), "w") as f:
    f.write(f"{wsa_min},{wsa_max}")
print(f"✅ Saved WSA range: ({wsa_min:.3f}, {wsa_max:.3f})")
