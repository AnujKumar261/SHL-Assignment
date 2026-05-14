import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

with open(
    "data/shl_catalog.json",
    "r",
    encoding="utf-8"
) as f:
    catalog = json.load(f)

texts = []

for item in catalog:

    text = f"""
    {item['name']}
    {item['description']}
    {item['test_type']}
    """

    texts.append(text)

embeddings = model.encode(texts)

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(
    np.array(embeddings).astype(
        "float32"
    )
)

faiss.write_index(
    index,
    "data/faiss.index"
)

np.save(
    "data/embeddings.npy",
    embeddings
)

print("Embeddings created successfully.")