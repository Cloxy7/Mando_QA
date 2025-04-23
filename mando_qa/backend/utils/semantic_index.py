# utils/semantic_index.py

import faiss
import numpy as np

class SemanticSearchIndex:
    def __init__(self, embedding_dim=384):  # all-MiniLM-L6-v2 gives 384-dim vectors
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.chunks = []

    def add(self, embeddings, texts):
        self.index.add(np.array(embeddings).astype('float32'))
        self.chunks.extend(texts)

    def search(self, query_embedding, top_k=5):
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        return [self.chunks[i] for i in I[0]]
