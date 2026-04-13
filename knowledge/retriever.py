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

        best_dist = results[0][1]
        
        MARGIN = 0.15
        HARD_CUTOFF = 0.35

        filtered = [
            doc for doc, dist in results
            if dist <= best_dist + MARGIN and dist < HARD_CUTOFF
        ]
        
        unique_docs = list(dict.fromkeys(filtered))
        docs = unique_docs[:3]

        return self.rerank(query, docs)