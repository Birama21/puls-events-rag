"""
Tests de la base vectorielle FAISS.
"""

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def load_vectorstore():
    """Charge la base vectorielle FAISS."""

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    )

    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vectorstore


def test_vectorstore_exists():
    """Vérifie que le dossier vectorstore existe."""

    assert Path("vectorstore").exists()


def test_vectorstore_loads():
    """Vérifie que la base vectorielle se charge correctement."""

    vectorstore = load_vectorstore()

    assert vectorstore is not None


def test_similarity_search():
    """Vérifie qu'une recherche retourne des résultats."""

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search(
        "Je cherche une exposition",
        k=3,
    )

    assert len(results) == 3

    for document in results:

        assert document.page_content != ""