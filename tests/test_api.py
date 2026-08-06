"""
Tests fonctionnels de l'API REST.
"""

from fastapi.testclient import TestClient

from api.app import app

# Création d'un client de test FastAPI
client = TestClient(app)


def test_home():
    """Vérifie que la route d'accueil répond correctement."""

    response = client.get("/")

    assert response.status_code == 200

    assert "message" in response.json()


def test_ask():
    """Vérifie que le chatbot répond à une question."""

    response = client.post(
        "/ask",
        json={
            "question": "Je cherche une activité pour les enfants",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "answer" in body

    assert isinstance(body["answer"], str)

    assert len(body["answer"]) > 0


def test_rebuild():
    """Vérifie que la reconstruction de la base vectorielle fonctionne."""

    response = client.post("/rebuild")

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Base vectorielle reconstruite avec succès."