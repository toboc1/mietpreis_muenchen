"""
Flask-Backend, das eines von mehreren trinierten Mietpreis-Modellen lädt 
und über ein Web-Formular Vorhersagen liefert.
"""

import base64
import io
import sys
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from model_config import MODEL_REGISTRY # noqa: E402

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
DATA_PATH = Path(__file__).resolve().parent.parent/ "data" / "processed" / "munich_rentals.csv"
DEFAULT_MODEL_KEY = next(iter(MODEL_REGISTRY))

app = Flask(__name__)

_models = {}


def get_model(model_key):
    if model_key not in _models:
        model_path = MODEL_DIR / f"{model_key}.pkl"
        _models[model_key] = joblib.load(model_path)
    return _models[model_key]

def build_chart(model, model_label, living_space, no_rooms, year_constructed, condition, user_prediction):
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
    ax.set_title(f"Wie {model_label} die Miete vorhersagt")
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
    selected_model = request.form.get("model_key", DEFAULT_MODEL_KEY)
    selected_model_label = MODEL_REGISTRY.get(selected_model, {}).get("label", selected_model)

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

            model = get_model(selected_model)
            prediction = round(float(model.predict(input_df)[0]), 2)
            chart = build_chart(model, selected_model_label, living_space, no_rooms, year_constructed, condition, prediction)
        except FileNotFoundError:
            error = "Es wurde noch kein Modell trainiert. Führe zuerst src/train_model.py aus."
        except Exception as exc:  # bewusst breit für ein kleines Portfolio-Projekt
            error = f"Da ist etwas schiefgelaufen: {exc}"

    model_options = [
        {"key": key,
         "label": config["label"]} for key, config in MODEL_REGISTRY.items()
    ]

    return render_template(
        "index.html", 
        prediction=prediction, 
        error=error, 
        chart=chart,
        model_options=model_options,
        selected_model=selected_model,
        selected_model_label=selected_model_label,
        )


if __name__ == "__main__":
    app.run(debug=True)
