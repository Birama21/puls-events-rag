from pathlib import Path

import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_dataframe():
    """Charge le fichier CSV des événements."""

    input_file = Path("data/processed/events.csv")
    return pd.read_csv(input_file)


def build_documents(df):
    """Transforme chaque ligne du DataFrame en Document LangChain."""

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

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def main():

    df = load_dataframe()

    documents = build_documents(df)

    chunks = split_documents(documents)

    print(f"Documents : {len(documents)}")
    print(f"Chunks    : {len(chunks)}\n")

    print("Premier chunk :\n")
    print(chunks[0])


if __name__ == "__main__":
    main()