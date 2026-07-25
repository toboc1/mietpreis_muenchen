"""
Traininert alle in mdoel_config.MODEL_REGISTRY definierten Modelle auf den
bereinigten Daten und speichert jedes einzeln unter model/<key>.pkl.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from model_config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, MODEL_REGISTRY, TARGET

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "munich_rentals.csv"
MODEL_DIR = Path(__file__).resolve().parent.parent / "model"


def build_preprocessor() -> ColumnTransformer:
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    return ColumnTransformer(transformers=[
        ("num", numeric_transformer, NUMERIC_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES),
    ])

def build_pipeline(regressor) -> Pipeline:
    return Pipeline(steps=[
    (   "preprocessor", build_preprocessor()),
        ("regressor", regressor),
])



def main():
    print(f"Lade Trainingsdaten aus {DATA_PATH} ...")
    df = pd.read_csv(DATA_PATH)

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    for key, config in MODEL_REGISTRY.items():
        print(f"\nTrainiere Modell: {config['label']} ...")
        pipeline = build_pipeline(config["regressor"]())
        pipeline.fit(X_train, y_train)

        preds = pipeline.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        print(f"MAE:  {mae:.2f} EUR")
        print(f"R^2:  {r2:.3f}")

        model_path = MODEL_DIR / f"{key}.pkl"
        joblib.dump(pipeline, model_path)
        print(f"Modell gespeichert: {model_path}")


if __name__ == "__main__":
    main()
