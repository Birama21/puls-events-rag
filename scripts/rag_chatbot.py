from src.rag import ask


def main():
    """Lance le chatbot RAG en mode interactif."""

    print("\n====================================")
    print(" Chatbot RAG - Métropole de Lyon")
    print(" Tape 'quit' pour quitter.")
    print("====================================")

    while True:

        # Saisie de la question
        question = input("\nVotre question : ")

        # Quitter le programme
        if question.lower() in ["quit", "exit", "q"]:
            print("\nAu revoir !")
            break

        # Génération de la réponse
        answer = ask(question)

        print("\nRéponse :\n")
        print(answer)


if __name__ == "__main__":
    main()