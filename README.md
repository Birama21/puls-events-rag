# 🎭 Puls Events RAG

Système de génération augmentée par récupération (RAG) permettant d'interroger les événements culturels de la Métropole de Lyon grâce à l'intelligence artificielle.

Le projet utilise **LangChain**, **FAISS**, **Hugging Face**, **Mistral AI** et **FastAPI** afin de proposer un assistant capable de répondre à des questions en langage naturel sur les événements présents dans une base de données.

---

# Objectifs du projet 

Ce projet a été réalisé dans le cadre de la formation **AI Engineer - OpenClassrooms**.

L'objectif est de développer un système RAG complet permettant de :

- prétraiter des données d'événements culturels ;
- construire une base vectorielle FAISS ;
- rechercher les événements les plus pertinents grâce aux embeddings ;
- générer une réponse en langage naturel avec Mistral AI ;
- exposer le système via une API FastAPI ;
- automatiser les tests avec GitHub Actions ;
- conteneuriser l'application avec Docker.

---

# Fonctionnalités

- Prétraitement des données
- Construction d'un index vectoriel FAISS
- Recherche sémantique avec LangChain
- Génération de réponses avec Mistral AI
- API REST FastAPI
- Documentation interactive Swagger
- Tests unitaires et d'intégration
- Couverture de code
- Intégration continue avec GitHub Actions
- Conteneurisation avec Docker

---

# Architecture du projet

```text
puls-events-rag/
│
├── api/
│   ├── app.py
│   └── schemas.py
│
├── src/
│   ├── rag.py
│   └── vectorstore.py
│
├── scripts/
│
├── tests/
│
├── data/
│
├── vectorstore/
│
├── Dockerfile
├── pyproject.toml
├── README.md
└── main.py
```

---

# Technologies utilisées

- Python 3.10
- FastAPI
- LangChain
- FAISS
- Hugging Face Embeddings
- Sentence Transformers
- Mistral AI
- Pandas
- Pytest
- GitHub Actions
- Docker
- uv

---

# Installation

## Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>

cd puls-events-rag
```

## Installer les dépendances

```bash
uv sync
```

---

# Variables d'environnement

Créer un fichier `.env` à la racine du projet :

```text
MISTRAL_API_KEY=votre_cle_api
```

---

# Construire la base vectorielle

Le fichier CSV est transformé en documents LangChain puis indexé dans FAISS.

```bash
uv run python src/vectorstore.py
```

L'index est enregistré dans le dossier :

```text
vectorstore/
```

---

# Lancer le chatbot

Une interface console est disponible.

```bash
uv run python main.py
```

---

# Lancer l'API

```bash
uv run uvicorn api.app:app --reload
```

Documentation interactive :

```
http://localhost:8000/docs
```

---

# Docker

Construire l'image :

```bash
docker build -t puls-events-rag .
```

Lancer le conteneur :

```bash
docker run -p 8000:8000 puls-events-rag
```

Accéder à Swagger :

```
http://localhost:8000/docs
```

---

# Tests

Lancer tous les tests :

```bash
uv run python -m pytest
```

Lancer les tests avec la couverture :

```bash
uv run python -m pytest --cov=src --cov=api --cov-report=term-missing
```

---

# Intégration continue

Le projet utilise **GitHub Actions** afin d'exécuter automatiquement :

- les tests unitaires ;
- les tests d'intégration ;
- la couverture de code.

Chaque push déclenche automatiquement le workflow CI.

---

# Exemple de requêtes

```text
Je cherche une exposition
```

```text
Je cherche une activité pour les enfants
```

```text
Je cherche un événement sur le cinéma
```

```text
Quels événements ont lieu à Villeurbanne ?
```

```text
Je cherche une visite guidée dans un musée
```

---

# Résultats

Le système est capable de :

- retrouver les événements les plus pertinents ;
- générer une réponse structurée ;
- éviter les hallucinations en répondant uniquement à partir des documents récupérés.

Le projet comprend :

- API FastAPI
- Swagger UI
- Tests unitaires
- Tests d'intégration
- GitHub Actions
- Couverture de code d'environ **97 %**
- Conteneurisation Docker

---

# Perspectives d'amélioration

- Déploiement cloud (Azure, AWS ou GCP)
- Interface utilisateur Streamlit ou React
- Filtrage des résultats par score de similarité
- Évaluation automatique avec Ragas lorsque les dépendances seront compatibles
- Mise en cache des réponses fréquentes

---

# Auteur

Projet réalisé dans le cadre de la formation **AI Engineer - OpenClassrooms**.