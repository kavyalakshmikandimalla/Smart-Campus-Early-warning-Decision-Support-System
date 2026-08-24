import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


# =====================================================
# 1. LOAD DATASET
# =====================================================

DATASET_FILE = "smart_campus(1).csv"

df = pd.read_csv(DATASET_FILE)

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# =====================================================
# 2. FEATURES
# =====================================================

features = [
    "Attendance",
    "Current_GPA",
    "Previous_GPA",
    "Assignment_Rate",
    "Backlogs",
    "Occupancy_Rate",
    "Electricity_Usage",
    "Internet_Usage",
    "Maintenance_Complaints",
    "Temperature",
    "Humidity",
    "Rainfall",
    "Water_Level",
    "Air_Quality_Index"
]


# =====================================================
# 3. TARGET
# =====================================================

target = "Risk_Level"


# =====================================================
# 4. CHECK COLUMNS
# =====================================================

missing_columns = []

for column in features + [target]:

    if column not in df.columns:
        missing_columns.append(column)


if missing_columns:

    print("ERROR!")
    print("Missing columns:", missing_columns)
    exit()


# =====================================================
# 5. PREPARE DATA
# =====================================================

X = df[features].copy()
y = df[target].astype(str)


# =====================================================
# 6. HANDLE MISSING VALUES
# =====================================================

X = X.fillna(X.median(numeric_only=True))

X = X.fillna(0)


# =====================================================
# 7. ENCODE RISK LEVEL
# =====================================================

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)


print("\nRisk Classes:")
print(list(encoder.classes_))


# =====================================================
# 8. TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# =====================================================
# 9. CREATE MODEL
# =====================================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=10,
    min_samples_split=2
)


# =====================================================
# 10. TRAIN MODEL
# =====================================================

print("\nTraining ML model...")

model.fit(
    X_train,
    y_train
)


# =====================================================
# 11. TEST MODEL
# =====================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nModel Training Completed!")
print("Accuracy:", round(accuracy * 100, 2), "%")


# =====================================================
# 12. SAVE MODEL
# =====================================================

with open("risk_model.pkl", "wb") as file:

    pickle.dump(
        model,
        file
    )


# =====================================================
# 13. SAVE MODEL COLUMNS
# =====================================================

with open("model_columns.pkl", "wb") as file:

    pickle.dump(
        features,
        file
    )


# =====================================================
# 14. SAVE LABEL ENCODER
# =====================================================

with open("risk_label_encoder.pkl", "wb") as file:

    pickle.dump(
        encoder,
        file
    )


# =====================================================
# 15. FINAL MESSAGE
# =====================================================

print("\n===================================")
print("MODEL FILES CREATED SUCCESSFULLY!")
print("===================================")

print("\nCreated files:")

print("1. risk_model.pkl")
print("2. model_columns.pkl")
print("3. risk_label_encoder.pkl")

print("\nYou can now run the Streamlit app.")