"""
Kleines Flask-Backend, das das trainierte Mietpreis-Modell (Random Forest Regressor)lädt und über
ein Web-Formular Vorhersagen liefert.
"""

import base64
import io
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "model.pkl"
DATA_PATH = Path(__file__).resolve().parent.parent/ "data" / "processed" / "munich_rentals.csv"

app = Flask(__name__)

_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def build_chart(model, living_space, no_rooms, year_constructed, condition, user_prediction):
    """
    Zeigt an, wie die Miete laut dem Model mit der Wohnfläche steigt (roter Faden),
    zusammen mit den echten Angeboten aus dem Trainingsset (graue Punkte)."""
    df = pd.read_csv(DATA_PATH)

    space_range = np.linspace(df["livingSpace"].min(), df["livingSpace"].max(), 50)
    curve_input = pd.DataFrame({
        "livingSpace": space_range,
        "noRooms": no_rooms,
        "yearConstructed": year_constructed,
        "condition": condition,
    })
    curve_pred = model.predict(curve_input)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(df["livingSpace"], df["totalRent"], alpha=0.3, s=15,
               color="gray", label="Echte Angebote (München)")
    ax.plot(space_range, curve_pred, color="#e63946", linewidth=2,
            label="Modellvorhersage bei deinen Eingaben")
    ax.scatter([living_space], [user_prediction], color="#e63946", s=80,
               zorder=5, edgecolor="black", label="Deine Eigabe")
    ax.set_xlabel("Wohnfläche (qm)")
    ax.set_ylabel("Miete (€)")
    ax.set_title("Wie RandomForest die Miete vorhersagt")
    ax.legend()
    fig.tight_layout

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    chart = None

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
            chart = build_chart(model, living_space, no_rooms, year_constructed, condition, prediction)
        except FileNotFoundError:
            error = "Es wurde noch kein Modell trainiert. Führe zuerst src/train_model.py aus."
        except Exception as exc:  # bewusst breit für ein kleines Portfolio-Projekt
            error = f"Da ist etwas schiefgelaufen: {exc}"

    return render_template("index.html", prediction=prediction, error=error, chart=chart)


if __name__ == "__main__":
    app.run(debug=True)
