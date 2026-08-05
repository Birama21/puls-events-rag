import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


def load_events():
    """Charge les événements depuis le fichier JSON."""

    input_file = Path("data/raw/events.json")

    with open(input_file, "r", encoding="utf-8") as file:
        return json.load(file)


def preprocess_events(events):
    """Nettoie et structure les événements."""

    rows = []

    for event in events:

        row = {
            "uid": event["uid"],
            "title": event["title"],
            "description": event["description"],
            "long_description": event["longDescription"],
            "begin": event["firstTiming"]["begin"],
            "end": event["firstTiming"]["end"],
            "location_name": event["location"]["name"],
            "location_city": event["location"]["city"],
            "location_address": event["location"]["address"],
            "origin_agenda": event["originAgenda"]["title"],
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    # Conversion des dates
    df["begin"] = pd.to_datetime(df["begin"])
    df["end"] = pd.to_datetime(df["end"])

    # Historique d'un an
    one_year_ago = pd.Timestamp.now(tz="Europe/Paris") - timedelta(days=365)

    # Conserver :
    # - les événements de l'année écoulée
    # - les événements futurs
    df = df[df["end"] >= one_year_ago]

    return df


def save_dataframe(df):
    """Sauvegarde le DataFrame au format CSV."""

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "events.csv"

    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"{len(df)} événements sauvegardés.")
    print(f"Fichier : {output_file}")


def main():

    events = load_events()

    df = preprocess_events(events)

    save_dataframe(df)


if __name__ == "__main__":
    main()