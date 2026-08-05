# Puls-Events RAG

## Description

Ce projet est un Proof of Concept (POC) d'un système Retrieval-Augmented Generation (RAG)
permettant de répondre à des questions sur des événements culturels issus de l'API OpenAgenda.

Le système s'appuie sur :

- LangChain
- FAISS
- Mistral
- FastAPI

---

## Structure

```
api/
data/
docs/
scripts/
tests/
vectorstore/
```

---

## Installation

Créer l'environnement :

```bash
uv sync
```

---

## Lancer un script

```bash
uv run scripts/test_imports.py
```

---

## Technologies

- Python 3.10
- LangChain
- FAISS
- HuggingFace Embeddings
- Mistral AI
- FastAPI