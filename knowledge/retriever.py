from embeddings.bge_embedder import BgeEmbedder
from vector_db.chroma_store import ChromaStore

class KnowledgeRetriever:

    def __init__(self):
        self.embedder = BgeEmbedder()
        self.store = ChromaStore("knowledge_base")
    
    def rerank(self, query, docs):
        return docs

    def retrieve(self, query):

        query_embedding = self.embedder.embed(query, is_query=True)

        results = self.store.search(query_embedding)

        if not results:
            return []
        
        results = sorted(results, key=lambda x: x[1])

        HARD_CUTOFF = 0.35
        TOP_K = 3

        filtered = [
            (doc, dist) for doc, dist in results
            if dist <= HARD_CUTOFF
        ]

        if not filtered:
            return []
        
        docs = [doc for doc, _ in filtered[:TOP_K]]

        unique_docs = list(dict.fromkeys(docs))

        return self.rerank(query, unique_docs)