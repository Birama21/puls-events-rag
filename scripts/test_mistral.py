import os

from dotenv import load_dotenv
from mistralai.client import Mistral


def main():
    """Teste la connexion à l'API Mistral."""

    # Chargement des variables d'environnement
    load_dotenv()

    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise ValueError("La variable MISTRAL_API_KEY est introuvable dans le fichier .env")

    print("Connexion à Mistral...")

    # Création du client Mistral
    client = Mistral(api_key=api_key)

    # Envoi d'une question très simple
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": "Dis simplement : Bonjour, le test fonctionne !"
            }
        ],
    )

    print("\nRéponse de Mistral :\n")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()