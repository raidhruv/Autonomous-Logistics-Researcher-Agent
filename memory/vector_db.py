import hashlib
import uuid
import chromadb
from chromadb.utils import embedding_functions
from config.settings import get_settings


class VectorDB:

    def __init__(self):
        settings = get_settings()

# persistent vector database
        self.client = chromadb.PersistentClient(
            path=settings.VECTOR_DB_PATH
)

# embedding model
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
             model_name=settings.EMBEDDING_MODEL
)

# collection
        self.collection = self.client.get_or_create_collection(
            name="logistics_knowledge",
            embedding_function=self.embedding_function
)   
    
    def add_document(self, chunks: list[dict]) -> None:
        """
        Store pre-chunked documents.
        Each chunk must be a dict:
        {
            "text": "...",
            "metadata": {...}
        }
        """

        doc_id = str(uuid.uuid4())

        for i, chunk in enumerate(chunks):

            text = chunk["text"]
            metadata = chunk.get("metadata", {}).copy()

            chunk_id = f"{doc_id}_{i}"

            metadata.update({
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "chunk_index": i,
                "section": metadata.get("section") or "unknown",
                "source": metadata.get("url") or "Unknown"
            })

            existing = self.collection.get(ids=[chunk_id])

            if existing["ids"]:
                continue

            self.collection.add(
                ids=[chunk_id],
                documents=[text],
                metadatas=[metadata]
            )

    
    def search(self, query, n_results=5):

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        documents = []

        docs = results.get("documents")
        metas = results.get("metadatas")
        scores = results.get("distances")

        if not docs or not metas:
            return []

        docs = docs[0]
        metas = metas[0]
        scores = scores[0] if scores else [None] * len(docs)

        for text, meta, score in zip(docs, metas, scores):
            documents.append({
                "text": text,
                "metadata": meta,
                "score": score
            })

        return documents        