import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

DOCS_DIR = Path("data/docs")
STORE_DIR = Path("vector_store")


def load_docs():
    docs = []
    for p in DOCS_DIR.glob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".txt"}:
            docs.append((p.name, p.read_text(encoding="utf-8")))
    return docs


def chunk_text(text, chunk_size=180, overlap=40):
    words = text.split()
    i = 0
    while i < len(words):
        yield " ".join(words[i:i + chunk_size])
        i += max(1, chunk_size - overlap)


def main():
    docs = load_docs()
    if not docs:
        raise ValueError("No documents found in data/docs")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts, meta = [], []
    for fname, content in docs:
        for chunk in chunk_text(content):
            texts.append(chunk)
            meta.append({"source": fname, "text": chunk})

    embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    STORE_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(STORE_DIR / "index.faiss"))

    with open(STORE_DIR / "meta.pkl", "wb") as f:
        pickle.dump(meta, f)

    print(f"✅ Ingested {len(docs)} docs, created {len(texts)} chunks")


if __name__ == "__main__":
    main()
