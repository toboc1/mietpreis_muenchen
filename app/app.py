"""
Kleines Flask-Backend, das das trainierte Mietpreis-Modell (Random Forest Regressor)lädt und über
ein Web-Formular Vorhersagen liefert.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "model.pkl"

app = Flask(__name__)

_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            living_space = float(request.form["living_space"])
            no_rooms = float(request.form["no_rooms"])
            year_constructed = float(request.form["year_constructed"])
            condition = request.form["condition"]

            input_df = pd.DataFrame([{
                "livingSpace": living_space,
                "noRooms": no_rooms,
                "yearConstructed": year_constructed,
                "condition": condition,
            }])

            model = get_model()
            prediction = round(float(model.predict(input_df)[0]), 2)
        except FileNotFoundError:
            error = "Es wurde noch kein Modell trainiert. Führe zuerst src/train_model.py aus."
        except Exception as exc:  # bewusst breit für ein kleines Portfolio-Projekt
            error = f"Da ist etwas schiefgelaufen: {exc}"

    return render_template("index.html", prediction=prediction, error=error)


if __name__ == "__main__":
    app.run(debug=True)
