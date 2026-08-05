from pathlib import Path

import pandas as pd
from langchain_core.documents import Document


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

        document = Document(
            page_content=page_content.strip(),
            metadata=metadata,
        )

        documents.append(document)

    return documents


def main():

    df = load_dataframe()

    documents = build_documents(df)

    print(f"{len(documents)} documents créés.\n")

    print("Premier document :\n")
    print(documents[0]) 


if __name__ == "__main__":
    main()