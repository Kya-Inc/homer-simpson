import streamlit as st # yes I'm lazy and doing this for the global secrets
import pandas as pd
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

data: DataFrame = pd.read_csv("simpsons_script_lines.csv")
df = pd.DataFrame(data)

# filter out non-speaking lines
lines: DataFrame = df[df["speaking_line"].isin(["True", "true", True])]
# filter out non-homer lines
homer_df: DataFrame = lines[lines["raw_character_text"] == "Homer Simpson"]

print(homer_df)

qdrant = QdrantClient(url=st.secrets.qdrant_url, api_key=st.secrets.qdrant_api_key)

semantic_model = SentenceTransformer("thenlper/gte-large")

# qdrant.recreate_collection(
#     collection_name="prompts",
#     vectors_config=models.VectorParams(
#         size=semantic_model.get_sentence_embedding_dimension(),  # Vector size is defined by used model
#         distance=models.Distance.COSINE,
#     ),
# )

# qdrant.recreate_collection(
#     collection_name="responses",
#     vectors_config=models.VectorParams(
#         size=semantic_model.get_sentence_embedding_dimension(),
#         distance=models.Distance.COSINE,
#     ),
# )


documents: list = []

for i, row in homer_df.iterrows():
    response: str = row["spoken_words"]

    prev_row = df.loc[i - 1]
    prev_char: str = prev_row["raw_character_text"]
    prompt: str = prev_row["spoken_words"]

    if prev_row["speaking_line"] is True:
        context: DataFrame = df.loc[max(0, i - 2) : i + 2][
            ["raw_character_text", "spoken_words"]
        ]

        clean: DataFrame = context.dropna()
        chunk: list = clean.values.tolist()

        metadata = {
            "precontext": clean[0:2].to_json(orient="records"),
            "prompting_character": prev_char,
            "prompt": prompt,
            "response": response,
            "postcontext": clean[2:].to_json(orient="records"),
            "persona_id": "6513a240c54d7ab4cc90e370"
        }

        documents.append(metadata)



prompt_records = []
response_records = []

for idx, doc in enumerate(documents):
    response_encoding = doc["response"]
    if isinstance(response_encoding, float):
        print("problem document: ", doc)

    if isinstance(response_encoding, str):
        prompt_record = models.Record(
            id=idx, vector=semantic_model.encode(doc["prompt"]).tolist(), payload=doc
        )

        response_record = models.Record(
            id=idx, vector=semantic_model.encode(doc["response"]).tolist(), payload=doc
        )

    prompt_records.append(prompt_record)
    response_records.append(response_record)


qdrant.upload_records(collection_name="prompts", records=prompt_records)
qdrant.upload_records(collection_name="responses", records=response_records)