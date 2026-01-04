from sentence_transformers import SentenceTransformer
import numpy as np
from rag.embed import index, DOCUMENTS

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(query, k=1):
    if index.ntotal == 0:
        return "No indexed report context available."

    query_emb = model.encode([query]).astype("float32")
    _, idx = index.search(query_emb, k)

    return DOCUMENTS[idx[0][0]]
