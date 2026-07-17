"""
Lädt die rohen ImmoScout24-Mietdaten, filtert auf München und bereinigt sie
für das Modelltraining.

Vorher: Datensatz von Kaggle herunterladen und als
data/raw/immo_data.csv ablegen.
https://www.kaggle.com/datasets/corrieaar/apartment-rental-offers-in-germany
"""

import pandas as pd
from pathlib import Path

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "immo_data.csv"
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "munich_rentals.csv"

# Spalten, die wir für das Modell brauchen. Je nach Kaggle-Version können
# Spaltennamen leicht abweichen -- ggf. anpassen, nachdem du dir die Rohdaten
# einmal mit df.columns angeschaut hast.
FEATURE_COLUMNS = [
    "regio1",        # Bundesland
    "regio2",        # Stadt/Landkreis
    "livingSpace",   # Wohnfläche in qm
    "noRooms",       # Zimmeranzahl
    "yearConstructed",
    "condition",     # Zustand der Wohnung
    "totalRent",      # Zielgröße: Gesamtmiete
]


def load_and_filter_munich(raw_path: Path = RAW_PATH) -> pd.DataFrame:
    print(f"Lade Rohdaten aus {raw_path} ...")
    df = pd.read_csv(raw_path, low_memory=False)

    # Auf München filtern (regio2 enthält den Stadt-/Landkreisnamen)
    df_muc = df[df["regio2"].str.contains("München", case=False, na=False)].copy()
    print(f"München-Datensätze: {len(df_muc)} von {len(df)} gesamt")

    return df_muc


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df[[c for c in FEATURE_COLUMNS if c in df.columns]].copy()

    # Zeilen ohne Zielgröße oder wichtige Features raus
    df = df.dropna(subset=["totalRent", "livingSpace", "noRooms"])

    # Offensichtliche Ausreißer/Fehleinträge raus
    df = df[(df["totalRent"] > 100) & (df["totalRent"] < 10000)]
    df = df[(df["livingSpace"] > 10) & (df["livingSpace"] < 500)]

    print(f"Nach Bereinigung: {len(df)} Zeilen, {df.shape[1]} Spalten")
    return df


def main():
    df = load_and_filter_munich()
    df_clean = clean(df)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(OUT_PATH, index=False)
    print(f"Gespeichert: {OUT_PATH}")


if __name__ == "__main__":
    main()
