import os

from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


# Base vectorielle chargée une seule fois
vectorstore = None

# Chaîne RAG chargée une seule fois
rag_chain = None


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


def get_retriever():
    """Retourne le retriever FAISS utilisé par le RAG."""

    vectorstore = load_vectorstore()

    return vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )


def retrieve_context(question):
    """
    Récupère les vrais documents utilisés par le retriever.

    Cette fonction est utilisée par DeepEval pour évaluer
    la pertinence du contexte récupéré.
    """

    retriever = get_retriever()

    docs = retriever.invoke(question)

    return [doc.page_content for doc in docs]


def format_docs(docs):
    """Transforme les documents récupérés en contexte texte."""

    context = ""

    for i, doc in enumerate(docs, start=1):
        context += f"\n===== ÉVÉNEMENT {i} =====\n"
        context += doc.page_content
        context += "\n"

    return context


def create_rag_chain():
    """Construit la chaîne RAG orchestrée par LangChain."""

    global rag_chain

    if rag_chain is None:

        retriever = get_retriever()

        # Prompt utilisé par le modèle
        prompt = ChatPromptTemplate.from_template(
            """
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
        )

        # Client Mistral géré par LangChain
        load_dotenv()

        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            raise ValueError(
                "MISTRAL_API_KEY introuvable dans les variables d'environnement."
            )

        llm = ChatMistralAI(
            model="mistral-small-latest",
            api_key=api_key,
        )

        # Orchestration complète du RAG par LangChain
        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
        )

    return rag_chain


def ask(question):
    """
    Fonction principale du RAG.

    Entrée :
        question (str)

    Sortie :
        réponse (str)
    """

    chain = create_rag_chain()

    response = chain.invoke(question)

    return response.content