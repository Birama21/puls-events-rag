import json
from pathlib import Path

# Chargement du fichier JSON
json_path = Path("data/raw/events.json")

with open(json_path, "r", encoding="utf-8") as file:
    events = json.load(file)

print(f"Nombre d'événements : {len(events)}\n")

# Premier événement
event = events[0]

print("Colonnes disponibles :\n")

for key in sorted(event.keys()):
    value = event[key]
    print(f"- {key:<25} {type(value).__name__}")

print("\n==============================")
print("Structure des champs complexes")
print("==============================\n")

complex_fields = [
    "location",
    "originAgenda",
    "firstTiming",
]

for field in complex_fields:
    print(f"\n{field}")
    print("-" * len(field))

    value = event.get(field)

    if isinstance(value, dict):
        for key, val in value.items():
            print(f"{key:<20} {type(val).__name__}")

    else:
        print(value)

print("\n==============================")
print("Valeurs manquantes")
print("==============================\n")

fields = [
    "title",
    "description",
    "longDescription",
    "location",
    "firstTiming",
]

for field in fields:
    missing = sum(
        1 for event in events
        if event.get(field) is None or event.get(field) == ""
    )

    print(f"{field:<20} {missing} valeurs manquantes")