import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from knowledge.retriever import KnowledgeRetriever

retriever = KnowledgeRetriever()

queries = [
    "What is Python?",
    "Explain machine learning",
    "What is Rust?",
]

for q in queries:
    print(f"\nQuery: {q}")
    docs = retriever.retrieve(q)
    print(docs)