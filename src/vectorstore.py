from pathlib import Path

import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def load_dataframe():
    """Charge le fichier CSV contenant les événements."""

    print("Chargement du fichier CSV...")

    input_file = Path("data/processed/events.csv")

    return pd.read_csv(input_file)


def build_documents(df):
    """Transforme chaque ligne du DataFrame en Document LangChain."""

    print("Création des documents LangChain...")

    documents = []

    for _, row in df.iterrows():

        page_content = f"""
Titre : {row['title']}

Description :
{row['description']}

Description détaillée :
{row['long_description']}

Lieu : {row['location_name']}
Ville : {row['location_city']}
Adresse : {row['location_address']}

Début : {row['begin']}
Fin : {row['end']}
"""

        metadata = {
            "uid": row["uid"],
            "title": row["title"],
            "city": row["location_city"],
            "begin": row["begin"],
            "end": row["end"],
            "origin_agenda": row["origin_agenda"],
        }

        documents.append(
            Document(
                page_content=page_content.strip(),
                metadata=metadata,
            )
        )

    return documents


def split_documents(documents):
    """Découpe les documents en chunks."""

    print("Découpage des documents en chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    return splitter.split_documents(documents)


def build_vectorstore(chunks):
    """Crée la base vectorielle FAISS."""

    print("Chargement du modèle d'embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Création de l'index FAISS...")

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    return vectorstore


def save_vectorstore(vectorstore):
    """Sauvegarde la base vectorielle sur le disque."""

    output_dir = "vectorstore"

    print("Sauvegarde de l'index...")

    vectorstore.save_local(output_dir)

    print(f"Index sauvegardé dans : {output_dir}")


def main():

    df = load_dataframe()

    documents = build_documents(df)

    chunks = split_documents(documents)

    print(f"{len(documents)} documents")
    print(f"{len(chunks)} chunks\n")

    vectorstore = build_vectorstore(chunks)

    save_vectorstore(vectorstore)

    print("\nÉtape 3 terminée avec succès !")


if __name__ == "__main__":
    main()