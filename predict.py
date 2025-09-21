import pandas as pd
import joblib
import os

# -------------------------
# 1. Load trained model
# -------------------------
MODEL_PATH = os.path.join("model", "equipment_model.pkl")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Trained model not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
print("Model loaded successfully!")

# -------------------------
# 2. Load new equipment data
# -------------------------
NEW_DATA_PATH = os.path.join("data", "new_equipment_data.csv")
if not os.path.exists(NEW_DATA_PATH):
    raise FileNotFoundError(f"New data CSV not found at {NEW_DATA_PATH}")

new_data = pd.read_csv(NEW_DATA_PATH)
print("New data loaded successfully!")
print(new_data.head())

# -------------------------
# 3. Select features for prediction
# -------------------------
FEATURES = ["Age", "Maintenance_Cost", "Downtime", "Maintenance_Frequency", "Failure_Event_Count"]

# Ensure all required columns exist
missing_cols = [col for col in FEATURES if col not in new_data.columns]
if missing_cols:
    raise KeyError(f"The following required columns are missing in the new data: {missing_cols}")

X_new = new_data[FEATURES]

# -------------------------
# 4. Predict using trained model
# -------------------------
predictions = model.predict(X_new)
new_data["Predicted_Maintenance_Class"] = predictions

# -------------------------
# 5. Save predictions
# -------------------------
OUTPUT_PATH = os.path.join("data", "predictions.csv")
new_data.to_csv(OUTPUT_PATH, index=False)
print(f"Predictions saved successfully at {OUTPUT_PATH}")
