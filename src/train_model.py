"""
Trainiert ein Regressionsmodell zur Mietpreisvorhersage auf den bereinigten
München-Daten und speichert es als model/model.pkl.
"""

import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "munich_rentals.csv"
MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "model.pkl"

NUMERIC_FEATURES = ["livingSpace", "noRooms", "yearConstructed"]
CATEGORICAL_FEATURES = ["condition"]
TARGET = "totalRent"


def build_pipeline() -> Pipeline:
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, NUMERIC_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES),
    ])

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=200, random_state=42)),
    ])
    return model


def main():
    print(f"Lade Trainingsdaten aus {DATA_PATH} ...")
    df = pd.read_csv(DATA_PATH)

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"MAE:  {mae:.2f} EUR")
    print(f"R^2:  {r2:.3f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Modell gespeichert: {MODEL_PATH}")


if __name__ == "__main__":
    main()
