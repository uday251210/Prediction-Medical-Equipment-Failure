# ======================================================
# Medical Equipment Failure Prediction - Training Script
# ======================================================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# -------------------------
# 1. Load dataset
# -------------------------
DATA_PATH = os.path.join("data", "Medical_Device_Failure_dataset.csv")
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

data = pd.read_csv(DATA_PATH)
print("Dataset loaded successfully!")
print("Columns:", data.columns.tolist())
print(data.head())

# -------------------------
# 1a. Create binary target column
# -------------------------
if 'Failure_Event_Count' in data.columns:
    data['Failure_Event'] = data['Failure_Event_Count'].apply(lambda x: 1 if x > 0 else 0)
else:
    raise KeyError("Column 'Failure_Event_Count' not found in dataset.")

# -------------------------
# 2. Define features and target
# -------------------------
FEATURES = [
    "Age",
    "Maintenance_Cost",
    "Downtime",
    "Maintenance_Frequency",
    "Device_Type",
    "Manufacturer",
    "Country"
]

TARGET = "Failure_Event"

X = data[FEATURES]
y = data[TARGET]

# -------------------------
# 3. Preprocessing
# -------------------------
numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# -------------------------
# 4. Create full pipeline with model
# -------------------------
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# -------------------------
# 5. Train-test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------
# 6. Train the model
# -------------------------
model.fit(X_train, y_train)
print("Model trained successfully!")

# -------------------------
# 7. Evaluate the model
# -------------------------
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# -------------------------
# 8. Save the model
# -------------------------
MODEL_PATH = os.path.join("model", "equipment_model.pkl")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH, protocol=4)  # Python 3.7 compatible
print(f"Model saved successfully at {MODEL_PATH}")
