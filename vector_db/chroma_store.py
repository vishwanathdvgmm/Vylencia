import chromadb
import uuid
import hashlib

class ChromaStore:

    def __init__(self, collection_name="knowledge_base"):
        self.client = chromadb.PersistentClient(path="data/vector_db")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, text, embedding):

        doc_id = hashlib.md5(text.encode("utf-8")).hexdigest()

        try:
            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                ids=[doc_id]
            )
        except Exception:
            pass

    def search(self, embedding, k=3):

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k
        )

        if not results or not results.get("documents"):
            return []
        
        docs = results["documents"][0]
        distances = results.get("distances", [[]])[0]

        if not distances:
            return [(doc, 1.0) for doc in docs]

        return list(zip(docs, distances))
