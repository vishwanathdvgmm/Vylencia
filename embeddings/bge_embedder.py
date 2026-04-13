from sentence_transformers import SentenceTransformer

class BgeEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")

    def embed(self, text, is_query=False):
        if isinstance(text, str):
            if is_query:
                text = f"query: {text}"
            return self.model.encode(
                text, 
                normalize_embeddings=True
            ).tolist()
        
        elif isinstance(text, list):
            if is_query:
                text = [f"query: {t}" for t in text]
            return self.model.encode(
                text, 
                normalize_embeddings=True
            ).tolist()
        
        else:
            raise ValueError("Input must be a string or list of strings.")