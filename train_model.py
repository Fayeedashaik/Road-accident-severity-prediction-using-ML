# ============================================================
#   Road Accident Severity Prediction — Model Training Script
# ============================================================

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, classification_report,
                             confusion_matrix)

# ── 1. Load Dataset ──────────────────────────────────────────
print("=" * 60)
print("  ROAD ACCIDENT SEVERITY PREDICTION — MODEL TRAINING")
print("=" * 60)

df = pd.read_csv("dataset/accident_data.csv")
print(f"\n[INFO] Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ── 2. Handle Missing Values ─────────────────────────────────
print("\n[STEP 1] Handling missing values...")
for col in df.select_dtypes(include="object").columns:
    df[col].fillna(df[col].mode()[0], inplace=True)
df["Driver_Age"].fillna(df["Driver_Age"].median(), inplace=True)
print(f"         Missing values remaining: {df.isnull().sum().sum()}")

# ── 3. Encode Categorical Variables ──────────────────────────
print("\n[STEP 2] Encoding categorical variables...")
label_encoders = {}
cat_cols = ["Weather_Conditions", "Road_Type", "Light_Conditions", "Time_of_Day", "Accident_Severity"]
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"         {col}: {list(le.classes_)}")

# ── 4. Feature / Target Split ─────────────────────────────────
print("\n[STEP 3] Splitting features and target...")
FEATURES = ["Weather_Conditions", "Road_Type", "Speed_Limit",
            "Light_Conditions", "Time_of_Day", "Number_of_Vehicles", "Driver_Age"]
TARGET = "Accident_Severity"

X = df[FEATURES]
y = df[TARGET]
print(f"         Features: {FEATURES}")
print(f"         Target classes: {list(label_encoders[TARGET].classes_)}")

# ── 5. Train/Test Split ───────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n[STEP 4] Train/Test split (80/20):")
print(f"         Training samples : {X_train.shape[0]}")
print(f"         Testing samples  : {X_test.shape[0]}")

# ── 6. Train Random Forest ────────────────────────────────────
print("\n[STEP 5] Training Random Forest Classifier...")
print("         (n_estimators=200, max_depth=15, random_state=42)")
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("         ✅ Model trained successfully!")

# ── 7. Evaluate ───────────────────────────────────────────────
print("\n[STEP 6] Model Evaluation on Test Set")
print("-" * 50)
y_pred = model.predict(X_test)

acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, average="weighted")
rec  = recall_score(y_test, y_pred, average="weighted")
f1   = f1_score(y_test, y_pred, average="weighted")

print(f"  Accuracy  : {acc  * 100:.2f}%")
print(f"  Precision : {prec * 100:.2f}%")
print(f"  Recall    : {rec  * 100:.2f}%")
print(f"  F1 Score  : {f1   * 100:.2f}%")
print("-" * 50)
print("\nClassification Report:")
target_names = label_encoders[TARGET].classes_
print(classification_report(y_test, y_pred, target_names=target_names))

# ── 8. Feature Importance ─────────────────────────────────────
print("\n[STEP 7] Feature Importance Ranking:")
importances = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)
for feat, imp in importances.items():
    bar = "█" * int(imp * 50)
    print(f"  {feat:<25} {bar} {imp:.4f}")

# ── 9. Save Model & Encoders ─────────────────────────────────
os.makedirs("model", exist_ok=True)
joblib.dump(model,          "model/accident_model.pkl")
joblib.dump(label_encoders, "model/label_encoders.pkl")
joblib.dump(FEATURES,       "model/feature_names.pkl")

print("\n[STEP 8] Model saved:")
print("         ✅ model/accident_model.pkl")
print("         ✅ model/label_encoders.pkl")
print("         ✅ model/feature_names.pkl")
print("\n" + "=" * 60)
print("  Training complete! Run 'streamlit run app.py' to launch.")
print("=" * 60)
