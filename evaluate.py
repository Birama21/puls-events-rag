from src.rag import ask


def main():
    """Évalue le chatbot sur plusieurs questions."""

    questions = [
        "Je cherche une exposition",
        "Je cherche un événement sur le cinéma",
        "Je cherche une activité pour les enfants",
        "Quels événements ont lieu à Villeurbanne ?",
        "Qui est Napoléon ?",
    ] 

    for i, question in enumerate(questions, start=1):

        print("=" * 80)
        print(f"Test {i}")
        print(f"Question : {question}")
        print("=" * 80)

        answer = ask(question)

        print("\nRéponse :\n")
        print(answer)
        print()


if __name__ == "__main__":
    main()