from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Question envoyée par l'utilisateur."""

    question: str


class AnswerResponse(BaseModel):
    """Réponse retournée par le chatbot."""

    answer: str