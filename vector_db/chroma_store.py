import chromadb
import uuid
import hashlib
from utils.logger import log

class ChromaStore:

    def __init__(self, collection_name="knowledge_base"):
        self.client = chromadb.PersistentClient(path="data/vector_db")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, text, embedding):

        if not text or not isinstance(text, str):
            return
        
        if not embedding or not isinstance(embedding, list):
            return

        doc_id = hashlib.md5(text.encode("utf-8")).hexdigest()

        try:
            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                ids=[doc_id]
            )
        except Exception as e:
            log(f"ChromaStore add skipped (likely duplicate): {e}")

    def search(self, embedding, k=3):

        if not embedding:
            return []
        
        try:
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=k
            )
        except Exception as e:
            log(f"Chroma search error: {e}")
            return []

        if not results or not results.get("documents"):
            return []
        
        docs = results["documents"][0] or []
        distances = results.get("distances")

        # fallback if distances missing
        if not distances or not distances[0]:
            paired = [(doc, 1.0) for doc in docs]
        else:
            distances = distances[0]
            paired = list(zip(docs, distances))

        # ✅ DEDUP LOGIC (ADD THIS PART)
        seen = set()
        unique = []

        for doc, dist in paired:
            if doc not in seen:
                seen.add(doc)
                unique.append((doc, dist))

        return unique
