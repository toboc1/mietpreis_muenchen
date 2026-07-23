# Mietpreisvorhersage München 🏠

Ein Machine-Learning-Projekt (auf Basis des Rent Prediction Projekts aus der Vorlesung "Hands-on-Machine-Learning"), das Mietpreise für Wohnungen in München auf Basis
realer Immobiliendaten mit dem Random Forest Regressor vorhersagt – inklusive einer kleinen Web-App, in der man
Wohnungseckdaten eingeben und eine Vorhersage zurück bekommen kann.

## Warum dieses Projekt?

Ich wollte mein bestehendes Python/Data-Science Wissen mit ersten
Full-Stack-Skills verbinden: Daten aufbereiten und ein Modell trainieren
(Data Science) und das Modell dann über ein Backend + einfaches Frontend
nutzbar machen (Full Stack).
Im Rahmen der Hands-on-Machine-Learning Vorlesung durfte ich bereits mit streamlit eine Web-App erstellen,
welche über Ridge Regression oder den Decision Tree Regressor eine Miet-Preis Schätzung berechnet.


## Datengrundlage

[Apartment rental offers in Germany](https://www.kaggle.com/datasets/corrieaar/apartment-rental-offers-in-germany)
(Kaggle) – reale Mietangebote von ImmoScout24, gefiltert auf München.

## Projektstruktur

```
mietpreis-muenchen/
├── data/
│   ├── raw/            # Rohdaten (CSV von Kaggle, nicht im Repo enthalten)
│   └── processed/       # Bereinigte/gefilterte Daten
├── src/
│   ├── data_prep.py     # Laden, Filtern (München), Bereinigen der Daten
│   └── train_model.py   # Training & Speichern des Modells
├── model/
│   └── model.pkl         # Trainiertes Modell (nicht im Repo, wird von train_model.py lokal erzeugt)
├── app/
│   ├── app.py            # Flask-Backend mit Vorhersage-API
│   ├── templates/
│   │   └── index.html    # Formular + Ergebnisanzeige
│   └── static/
│       └── style.css
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 1. Daten vorbereiten

1. Datensatz von Kaggle herunterladen (`immo_data.csv`)
2. Datei nach `data/raw/immo_data.csv` legen
3. Ausführen:

```bash
python src/data_prep.py
```

Das erzeugt `data/processed/munich_rentals.csv`.

## 2. Modell trainieren

```bash
python src/train_model.py
```

Das erzeugt `model/model.pkl` und gibt die Modellgüte (R², MAE) in der
Konsole aus.

## Modell-Performance
- MAE: 353€
- R²: 0.742

## 3. Web-App starten

```bash
python app/app.py
```

Dann im Browser öffnen: http://127.0.0.1:5000

## Was ich dabei gelernt habe

*(Zwar ist Streamlit für Daten -und KI-Anwendungen intuitiver und es erfordert weniger Code,
aber Flask ermöglicht mir das Front-End der Web-App zu gestallten ohne das komisch in den Python Code einzubetten)*

## Nächste Schritte / Ideen

- Deployment (z. B. Render.com oder Fly.io), damit es einen Live-Link gibt
- Karte mit Stadtteil-Auswahl statt Freitextfeld
- Modellvergleich (Lineare Regression vs. Random Forest)
- Front-End visuell Anspruchsvoller gestalten