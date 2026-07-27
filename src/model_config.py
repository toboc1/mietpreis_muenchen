"""
Zentrale Registry aller  Modelle, die trainiert und in der Web-App zur Auswahl angeboten werden.
Ein neues Modell hinzufügen = ein neuer Eintrag hier,
train_model.py und app.py müssen dafür nicht angepasst werden.
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge

NUMERIC_FEATURES = ["livingSpace", "noRooms", "yearConstructed"]
CATEGORICAL_FEATURES = ["condition", "district"]
TARGET = "totalRent"

MODEL_REGISTRY = {
    "random_forest" : {
        "label": "Random Forest",
        "regressor": lambda: RandomForestRegressor(n_estimators=200, random_state=42),
    },
    "ridge": {
        "label": "Ridge Regression",
        "regressor": lambda: Ridge(alpha=1.0, random_state=42),
    },
}