from fastapi import FastAPI, HTTPException

from api.schemas import AnswerResponse, QuestionRequest
from src.rag import ask
from src.vectorstore import main as rebuild_vectorstore

# Création de l'application FastAPI
app = FastAPI(
    title="Puls Events RAG API",
    description="API REST pour interroger le chatbot RAG des événements culturels.",
    version="1.0.0",
)


@app.get("/")
def home():
    """Route d'accueil."""

    return {
        "message": "Bienvenue sur l'API Puls Events RAG !"
    }


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    """
    Interroge le chatbot RAG.

    Entrée :
        - question

    Sortie :
        - réponse générée par le chatbot
    """

    # Vérifie que la question n'est pas vide
    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="La question ne peut pas être vide.",
        )

    # Génération de la réponse
    answer = ask(request.question)

    return AnswerResponse(
        answer=answer,
    )

@app.post("/rebuild")
def rebuild():
    """
    Reconstruit la base vectorielle FAISS.
    """

    rebuild_vectorstore()

    return {
        "message": "Base vectorielle reconstruite avec succès."
    }