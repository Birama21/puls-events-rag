"""
Tests de la logique métier du système RAG.
"""

from src.rag import ask


def test_ask_returns_string():
    """Vérifie que ask() retourne une chaîne de caractères."""

    response = ask("Je cherche une exposition")

    assert isinstance(response, str)

    assert len(response) > 0


def test_unknown_question():
    """Vérifie qu'une question hors domaine renvoie une réponse."""

    response = ask("Qui est Napoléon ?")

    assert isinstance(response, str)

    assert len(response) > 0


def test_children_activity():
    """Vérifie que le RAG répond à une recherche d'activité pour les enfants."""

    response = ask("Je cherche une activité pour les enfants")

    assert isinstance(response, str)

    assert len(response) > 0