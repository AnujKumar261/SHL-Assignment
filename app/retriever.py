import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


# -----------------------------
# Load Embedding Model
# -----------------------------
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -----------------------------
# Load FAISS Index
# -----------------------------
index = faiss.read_index(
    "data/faiss.index"
)


# -----------------------------
# Load Catalog
# -----------------------------
with open(
    "data/shl_catalog.json",
    "r",
    encoding="utf-8"
) as f:
    catalog = json.load(f)


# -----------------------------
# Retrieval Function
# -----------------------------
def retrieve_assessments(
    query,
    top_k=5
):

    # Convert query to embedding
    query_embedding = model.encode([query])

    # Search FAISS index
    distances, indices = index.search(
        np.array(query_embedding).astype(
            "float32"
        ),
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(catalog):

            item = catalog[idx]

            results.append({
                "name": item.get(
                    "name",
                    "Unknown"
                ),
                "url": item.get(
                    "url",
                    ""
                ),
                "description": item.get(
                    "description",
                    ""
                ),
                "test_type": item.get(
                    "test_type",
                    "Unknown"
                )
            })

    return results