from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)
DOCUMENTS = []

def embed_documents(summary):
    text = str(summary)
    embedding = model.encode([text]).astype("float32")

    index.add(embedding)
    DOCUMENTS.append(text)
