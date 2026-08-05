import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

API_KEY = os.getenv("OPENAGENDA_API_KEY")

if not API_KEY:
    raise ValueError("OPENAGENDA_API_KEY est introuvable dans le fichier .env")

# UID de l'agenda sélectionné
AGENDA_UID = "87532799"

BASE_URL = f"https://api.openagenda.com/v2/agendas/{AGENDA_UID}/events"

HEADERS = {
    "key": API_KEY
}


def fetch_all_events():
    """Télécharge tous les événements de l'agenda."""

    all_events = []
    after = None

    while True:

        params = {
            "detailed": 1,
            "monolingual": "fr",
            "size": 100,
        }

        if after is not None:
            params["after"] = after

        response = requests.get(
            BASE_URL,
            headers=HEADERS,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        events = data.get("events", [])

        # S'il n'y a plus d'événements, on arrête la boucle
        if not events:
            break

        all_events.extend(events)

        print(f"→ {len(all_events)} événements récupérés")

        after = data.get("after")

        # Plus de page suivante
        if after is None:
            break

    return all_events


def save_events(events):
    """Sauvegarde les événements au format JSON."""

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "events.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(events, file, ensure_ascii=False, indent=4)

    print(f"\n{len(events)} événements sauvegardés.")
    print(f"Fichier : {output_file}")


def main():
    """Point d'entrée du script."""

    events = fetch_all_events()
    save_events(events)


if __name__ == "__main__":
    main()