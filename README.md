#  Puls Events RAG

Puls Events RAG est un système de génération augmentée par récupération (RAG) permettant d'interroger en langage naturel les événements culturels de la Métropole de Lyon.

Le projet a été réalisé dans le cadre de la formation **AI Engineer - OpenClassrooms**. Il combine LangChain, FAISS, Hugging Face, Sentence Transformers, Mistral AI et FastAPI afin de rechercher les événements les plus pertinents dans une base vectorielle puis de générer une réponse en langage naturel à partir des informations récupérées.

---

#  Objectifs du projet

L'objectif est de concevoir un système RAG complet capable de :

- charger et préparer des données d'événements culturels ;
- transformer les événements en embeddings ;
- construire une base vectorielle avec FAISS ;
- effectuer une recherche sémantique ;
- transmettre les documents pertinents à un modèle de langage ;
- générer des réponses en langage naturel ;
- limiter les hallucinations en imposant au modèle de répondre uniquement à partir du contexte récupéré ;
- exposer le système via une API REST FastAPI ;
- fournir une documentation interactive avec Swagger ;
- automatiser les tests avec Pytest et GitHub Actions ;
- conteneuriser l'application avec Docker ;
- évaluer la qualité du RAG avec DeepEval.

---

#  Architecture du projet

Le projet est organisé en plusieurs parties ayant chacune une responsabilité précise.

Le dossier `data/` contient les données sources des événements culturels.

Le fichier `src/vectorstore.py` est chargé de préparer les données, de générer les embeddings avec Sentence Transformers et de construire la base vectorielle FAISS.

Le dossier `vectorstore/` contient l'index FAISS généré à partir des données.

Le fichier `src/rag.py` contient la logique principale du système RAG. Il charge la base vectorielle, crée le retriever LangChain, récupère les documents pertinents, construit le contexte et transmet ce contexte ainsi que la question au modèle Mistral.

Le dossier `api/` contient l'API FastAPI. `app.py` expose les endpoints permettant d'interroger le système et `schemas.py` définit les modèles de données utilisés par l'API.

Le fichier `main.py` permet également d'utiliser le RAG directement depuis le terminal.

Le dossier `tests/` contient les tests automatisés du projet.

Le dossier `evaluation/` contient le système d'évaluation DeepEval ainsi que le jeu de test annoté utilisé pour mesurer la qualité du RAG.

Le fichier `Dockerfile` permet de construire une image contenant l'application et ses dépendances.

---

#  Fonctionnement du RAG

Lorsqu'un utilisateur pose une question, le système commence par rechercher dans la base FAISS les documents sémantiquement les plus proches de la question.

Les embeddings utilisés pour cette recherche sont générés avec le modèle :

`sentence-transformers/all-MiniLM-L6-v2`

Le retriever LangChain récupère les documents les plus pertinents. Dans l'implémentation actuelle, cinq documents sont récupérés.

Ces documents sont ensuite transformés en contexte textuel.

La question et le contexte sont transmis à un prompt LangChain qui contient des instructions précises pour le modèle.

Le modèle Mistral génère ensuite la réponse finale.

Le prompt impose notamment que la réponse soit basée uniquement sur les informations présentes dans le contexte et interdit au modèle d'inventer des informations.

Si aucun document pertinent n'est trouvé, le système retourne :

`Je n'ai trouvé aucun événement correspondant à votre demande dans la base de données.`

La base vectorielle et la chaîne RAG sont chargées une seule fois puis conservées en mémoire afin d'éviter de refaire inutilement leur initialisation à chaque requête.

---

#  Choix technologiques

## LangChain

LangChain est utilisé pour orchestrer les différentes étapes du RAG.

Il permet de relier le retriever FAISS, le formatage des documents, le prompt et le modèle Mistral dans une chaîne cohérente.

L'utilisation de LangChain permet également de conserver une séparation claire entre la récupération des documents et leur génération par le LLM.

## FAISS

FAISS est utilisé comme base vectorielle.

Les événements sont convertis en embeddings puis stockés dans un index permettant de retrouver rapidement les documents les plus proches d'une question.

FAISS a été retenu pour sa simplicité, ses performances et son intégration avec LangChain.

## Hugging Face et Sentence Transformers

Sentence Transformers est utilisé pour transformer les textes des événements en vecteurs.

Le modèle `all-MiniLM-L6-v2` fournit une solution légère adaptée à un projet local et permet d'effectuer une recherche sémantique sans appeler une API externe pour chaque embedding.

## Mistral AI

Mistral AI est utilisé comme modèle de génération.

Le modèle reçoit la question ainsi que le contexte récupéré par le retriever et produit la réponse finale.

L'utilisation de Mistral permet de conserver une architecture simple tout en bénéficiant d'un modèle de langage adapté à la génération de réponses en français.

## FastAPI

FastAPI permet d'exposer le système RAG sous forme d'API REST.

Swagger est automatiquement disponible afin de tester les endpoints et de documenter l'API.

## Docker

Docker permet de reproduire l'environnement d'exécution du projet et de faciliter son déploiement.

## uv

`uv` est utilisé pour gérer l'environnement Python et les dépendances du projet.

---

#  Structure du projet

    puls-events-rag/
    ├── api/
    │   ├── app.py
    │   └── schemas.py
    ├── src/
    │   ├── rag.py
    │   └── vectorstore.py
    ├── evaluation/
    │   ├── evaluate_deepeval.py
    │   └── test_dataset.json
    ├── tests/
    ├── data/
    ├── vectorstore/
    ├── Dockerfile
    ├── pyproject.toml
    ├── README.md
    └── main.py

---

#  Installation

Le projet nécessite Python 3.10 ou une version supérieure ainsi que `uv`.

Installer les dépendances avec :

    uv sync

Créer ensuite un fichier `.env` à la racine du projet :

    MISTRAL_API_KEY=votre_cle_api

La clé API Mistral est nécessaire pour utiliser le modèle de génération.

---

#  Construction de la base vectorielle

La base vectorielle est construite à partir des données présentes dans le projet.

Exécuter :

    uv run python src/vectorstore.py

Cette étape génère l'index FAISS dans le dossier `vectorstore/`.

La base vectorielle doit être disponible avant de lancer le RAG.

---

#  Utilisation du RAG

Pour lancer l'application en mode console :

    uv run python main.py

Quelques exemples de questions :

    Je cherche une exposition à Lyon.

    Je cherche une activité pour les enfants.

    Quels événements sont prévus à Villeurbanne ?

    Y a-t-il un événement sur le cinéma ?

    Je cherche une visite historique à Oullins.

---

#  API FastAPI

Pour lancer l'API :

    uv run uvicorn api.app:app --reload

La documentation interactive Swagger est ensuite disponible à :

    http://localhost:8000/docs

L'API permet à une application cliente d'envoyer une question au système RAG et de récupérer la réponse générée.

---

#  Docker

Construire l'image Docker :

    docker build -t puls-events-rag .

Le `.` indique que le contexte de construction correspond au dossier courant du projet.

L'option `-t` permet de donner un nom à l'image Docker.

Lancer ensuite le conteneur :

    docker run -p 8000:8000 puls-events-rag

L'API est alors accessible via :

    http://localhost:8000/docs

Après une modification du code, l'image peut être reconstruite avec :

    docker build --no-cache -t puls-events-rag .

Le `--no-cache` force Docker à reconstruire les différentes étapes sans utiliser le cache précédent.

---

#  Tests

Les tests classiques sont réalisés avec Pytest.

Pour lancer l'ensemble des tests :

    uv run python -m pytest

Pour obtenir la couverture :

    uv run python -m pytest --cov=src --cov=api --cov-report=term-missing

Le projet atteint environ **97 % de couverture de code**.

Les tests permettent notamment de vérifier le comportement des différents composants de l'application et d'éviter les régressions.

---

#  Intégration continue

GitHub Actions est utilisé pour automatiser la validation du projet.

Le workflow CI permet notamment d'exécuter automatiquement les tests et de vérifier la couverture de code lors des modifications du dépôt.

Cette automatisation permet de détecter rapidement une régression après une modification du projet.

---

#  Évaluation du système RAG avec DeepEval

En complément des tests unitaires et d'intégration, une évaluation spécifique du système RAG a été mise en place avec DeepEval.

L'objectif de cette évaluation est différent des tests classiques.

Les tests Pytest vérifient principalement que le logiciel fonctionne correctement.

DeepEval permet de mesurer la qualité des réponses produites par le système RAG.

L'évaluation porte sur l'ensemble de la chaîne : question utilisateur, récupération des documents, génération de la réponse et qualité du résultat final.

---

#  Jeu de test annoté

Un jeu de test composé de **15 questions** a été créé pour évaluer le système.

Les questions couvrent différents types de recherches :

- art ;
- expositions ;
- événements à Villeurbanne ;
- activités pour enfants ;
- cinéma ;
- recherche par date ;
- patrimoine ;
- astronomie ;
- musique ;
- histoire ;
- médecine ;
- soierie lyonnaise ;
- questions hors domaine.

Le fichier utilisé pour cette évaluation se trouve dans :

    evaluation/test_dataset.json

Chaque cas de test contient notamment une question, une réponse attendue et un contexte attendu.

`expected_answer` correspond à la réponse de référence attendue pour la question.

`expected_context` correspond aux informations ou documents de référence qui doivent permettre de répondre correctement à la question.

Ces éléments permettent à DeepEval de comparer les résultats produits par le RAG avec des références définies à l'avance.

---

#  Métriques utilisées

Trois métriques DeepEval ont été utilisées.

## Answer Relevancy

Cette métrique mesure si la réponse générée est pertinente par rapport à la question de l'utilisateur.

Elle permet notamment de détecter une réponse qui ne répond pas réellement à la demande.

## Faithfulness

Cette métrique mesure si la réponse générée est fidèle au contexte fourni au modèle.

Elle est particulièrement importante pour un système RAG car l'objectif est d'éviter que le modèle ajoute des informations qui ne sont pas présentes dans les documents récupérés.

## Contextual Relevancy

Cette métrique évalue la pertinence du contexte récupéré par rapport à la question.

Elle permet donc d'observer la qualité de la partie retrieval du RAG et de vérifier si les documents sélectionnés sont réellement utiles pour répondre à la question.

---

#  Résultats de l'évaluation

L'évaluation des 15 questions a donné les scores moyens suivants :

    Answer Relevancy      : 0.762
    Faithfulness          : 0.577
    Contextual Relevancy  : 0.551

Ces résultats montrent une pertinence globale correcte des réponses.

La fidélité au contexte et la pertinence des documents récupérés restent cependant des axes d'amélioration.

L'évaluation a également rencontré ponctuellement des erreurs HTTP 429 provenant de l'API Mistral lorsque plusieurs appels au modèle étaient effectués rapidement.

Ces limitations de rate limit peuvent influencer certaines exécutions de l'évaluation et constituent une limite de l'environnement de test.

---

#  Pourquoi DeepEval plutôt que Ragas ?

Ragas avait initialement été envisagé pour l'évaluation du RAG.

Cependant, sa mise en place dans l'environnement du projet a posé plusieurs problèmes de compatibilité et d'exécution liés aux versions des différentes dépendances.

L'objectif étant d'obtenir une évaluation fonctionnelle sans modifier l'architecture du RAG, DeepEval a finalement été retenu.

DeepEval permettait de mettre en place directement les métriques nécessaires : Answer Relevancy, Faithfulness et Contextual Relevancy.

Le choix de DeepEval est donc un choix pragmatique : il permet d'évaluer le système RAG de manière reproductible tout en restant compatible avec l'environnement utilisé pour le projet.

Le RAG lui-même n'a pas été modifié pour intégrer l'évaluation. DeepEval intervient comme une couche d'évaluation externe qui exécute les questions du jeu de test, récupère les réponses du RAG et calcule ensuite les métriques.

---

#  Résultats du projet

Le projet fournit actuellement :

- un système RAG fonctionnel ;
- une recherche sémantique avec FAISS ;
- des embeddings Sentence Transformers ;
- une génération avec Mistral AI ;
- une orchestration avec LangChain ;
- une API REST FastAPI ;
- une documentation Swagger ;
- des tests Pytest ;
- environ 97 % de couverture de code ;
- une intégration continue avec GitHub Actions ;
- une conteneurisation Docker ;
- un jeu de test annoté ;
- une évaluation automatique avec DeepEval.

---

#  Perspectives d'amélioration

Plusieurs améliorations pourraient être apportées au système :

- améliorer la qualité des embeddings ;
- optimiser le nombre de documents récupérés ;
- ajouter un mécanisme de reranking ;
- améliorer le prompt ;
- améliorer le traitement des requêtes ;
- mettre en place une gestion plus robuste des rate limits Mistral ;
- enrichir le jeu de test ;
- améliorer les performances du retrieval ;
- ajouter une interface utilisateur avec Streamlit ou React ;
- déployer l'application dans le cloud ;
- mettre en place un suivi régulier des métriques d'évaluation.

---

#  Auteur

Projet réalisé dans le cadre de la formation **AI Engineer - OpenClassrooms**.

**Puls Events RAG — Système RAG pour l'exploration des événements culturels de la Métropole de Lyon.**