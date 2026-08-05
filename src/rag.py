import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from mistralai.client import Mistral


# Variables globales pour éviter de recharger FAISS et Mistral
vectorstore = None
client = None


def load_vectorstore():
    """Charge la base vectorielle FAISS une seule fois."""

    global vectorstore

    if vectorstore is None:

        print("Chargement de la base vectorielle...")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.load_local(
            "vectorstore",
            embeddings,
            allow_dangerous_deserialization=True,
        )

    return vectorstore


def load_mistral():
    """Charge le client Mistral une seule fois."""

    global client

    if client is None:

        print("Connexion à Mistral...")

        load_dotenv()

        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            raise ValueError(
                "MISTRAL_API_KEY introuvable dans le fichier .env"
            )

        client = Mistral(api_key=api_key)

    return client


def retrieve_context(question):
    """Recherche les événements les plus pertinents."""

    vectorstore = load_vectorstore()

    docs = vectorstore.similarity_search(
        question,
        k=5,
    )

    context = ""

    for i, doc in enumerate(docs, start=1):

        context += f"\n===== ÉVÉNEMENT {i} =====\n"
        context += doc.page_content
        context += "\n"

    return context


def generate_answer(question, context):
    """Génère une réponse avec Mistral."""

    client = load_mistral()

    prompt = f"""
Tu es un assistant spécialisé dans les événements culturels de la Métropole de Lyon.

Tu dois répondre uniquement à partir du contexte fourni.

Consignes :

- Réponds uniquement à partir du contexte fourni.
- Si plusieurs événements correspondent à la demande, présente-les du plus pertinent au moins pertinent.
- Pour chaque événement, indique :
  - son nom ;
  - une courte description ;
  - le lieu si disponible ;
  - la date si disponible.
- Ne crée jamais d'informations qui ne figurent pas dans le contexte.
- Si aucune information pertinente n'est trouvée, réponds :
  "Je n'ai trouvé aucun événement correspondant à votre demande dans la base de données."

Contexte :

{context}

Question :

{question}
"""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content


def ask(question):
    """
    Fonction principale du RAG.

    Entrée :
        question (str)

    Sortie :
        réponse (str)
    """

    context = retrieve_context(question)

    answer = generate_answer(
        question,
        context,
    )

    return answer