import os

import requests
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

API_KEY = os.getenv("OPENAGENDA_API_KEY")

if not API_KEY:
    raise ValueError(
        "La variable OPENAGENDA_API_KEY est absente du fichier .env"
    )

# Ville recherchée
SEARCH = "Lyon"

# URL de l'API OpenAgenda
URL = "https://api.openagenda.com/v2/agendas"

# En-têtes HTTP
headers = {
    "key": API_KEY
}

# Paramètres de recherche
params = {
    "search": SEARCH,
    "official": 1,
    "size": 10,
    "includeFields": ["uid", "title", "slug"],
}

try:
    response = requests.get(
        URL,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    print(f"\nNombre d'agendas trouvés : {data['total']}\n")

    for agenda in data["agendas"]:
        print("-" * 50)
        print(f"Titre : {agenda['title']}")
        print(f"UID   : {agenda['uid']}")
        print(f"Slug  : {agenda['slug']}")

except requests.exceptions.HTTPError as e:
    print(f"Erreur HTTP : {e}")
    print(response.text)

except Exception as e:
    print(f"Erreur : {e}")