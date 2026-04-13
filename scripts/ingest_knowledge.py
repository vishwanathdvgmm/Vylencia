import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from embeddings.bge_embedder import BgeEmbedder
from vector_db.chroma_store import ChromaStore

embedder = BgeEmbedder()
emotional_store = ChromaStore("emotional_memory")
knowledge_store = ChromaStore("knowledge_base")

jsonl_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "vylencia_language.jsonl"
)

entries = []
with open(jsonl_path, "r", encoding="utf-8") as f:
    content = f.read()

current = ""
depth = 0

for line in content.splitlines():
    if not line.strip():
        continue

    for ch in line.strip():
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1

    current += line + "\n"

    if depth == 0 and current.strip():
        try:
            entries.append(json.loads(current.strip()))
        except Exception as e:
            print(f"Skipping invalid entry: {e}")
        current = ""

print(f"Found {len(entries)} entries to ingest...")

count = 0

for entry in entries:
    
    text = f"{entry['context'].strip()} {entry['response'].strip()}"

    embedding = embedder.embed(text, is_query=False)
    emotional_store.add(text, embedding)

    count += 1

    if count % 10 == 0:
        print(f"  Ingested {count}/{len(entries)}")

# -------------------------------
# KNOWLEDGE INGESTION
# -------------------------------
kb_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "knowledge_base.jsonl"
)

if os.path.exists(kb_path):

    print("Ingesting knowledge base...")

    with open(kb_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                item = json.loads(line.strip())
                text = item.get("text", "").strip()
                if not text:
                    continue
            except Exception as e:
                print(f"Skipping KB entry: {e}")
                continue

            embedding = embedder.embed(text, is_query=False)
            knowledge_store.add(text, embedding)

            if (i + 1) % 5 == 0:
                print(f"  Knowledge entries: {i+1}")

print(f"Knowledge ingested successfully! Total: {count} entries.")