from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def load_vectorstore():
    """Charge l'index FAISS."""

    print("Chargement de l'index FAISS...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vectorstore


def main():
    """Teste plusieurs recherches dans la base vectorielle."""

    # Chargement de la base vectorielle
    vectorstore = load_vectorstore()

    # Questions de test
    questions = [
        "Je cherche un événement sur le cinéma à Lyon",
        "Je cherche une exposition",
        "Quels événements ont lieu à Villeurbanne ?",
        "Je cherche une activité pour les enfants",
    ]

    # Test de chaque question
    for question in questions:

        print("\n" + "=" * 80)
        print(f"Question : {question}")
        print("=" * 80)

        # Recherche des 3 chunks les plus proches
        results = vectorstore.similarity_search(
            question,
            k=3,
        )

        # Affichage des résultats
        for i, doc in enumerate(results, start=1):

            print(f"\nRésultat {i}")

            print(f"Titre : {doc.metadata['title']}")
            print(f"Ville : {doc.metadata['city']}")

            print("\nExtrait :")
            print(doc.page_content[:250])


if __name__ == "__main__":
    main()