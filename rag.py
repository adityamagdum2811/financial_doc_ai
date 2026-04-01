import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder
from app.config import settings

client = chromadb.PersistentClient(path=settings.chroma_path)
collection = client.get_or_create_collection(name="financial_documents")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def index_document(document_id: int, text: str):
    chunks = chunk_text(text)
    embeddings = embedding_model.encode(chunks).tolist()

    ids = [f"{document_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"document_id": str(document_id), "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )

    return len(chunks)


def remove_document(document_id: int):
    existing = collection.get()
    ids_to_delete = []

    for i, meta in enumerate(existing.get("metadatas", [])):
        if meta.get("document_id") == str(document_id):
            ids_to_delete.append(existing["ids"][i])

    if ids_to_delete:
        collection.delete(ids=ids_to_delete)

    return ids_to_delete


def semantic_search(query: str, top_k: int = 20, rerank_top_k: int = 5):
    query_embedding = embedding_model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    if not docs:
        return []

    pairs = [[query, doc] for doc in docs]
    scores = reranker.predict(pairs)

    combined = []
    for doc, meta, score in zip(docs, metas, scores):
        combined.append({
            "document_id": meta["document_id"],
            "chunk_text": doc,
            "score": float(score)
        })

    combined.sort(key=lambda x: x["score"], reverse=True)
    return combined[:rerank_top_k]


def get_document_context(document_id: int):
    existing = collection.get()
    contexts = []

    for i, meta in enumerate(existing.get("metadatas", [])):
        if meta.get("document_id") == str(document_id):
            contexts.append(existing["documents"][i])

    return contexts