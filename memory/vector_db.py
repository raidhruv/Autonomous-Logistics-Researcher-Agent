import hashlib
import uuid
import chromadb
from chromadb.utils import embedding_functions
from config.settings import get_settings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorDB:

    def __init__(self):
        settings = get_settings()

# text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " "
            ]
        )


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
    def add_document(self, text: str, metadata: dict | None = None) -> None:

        chunks = self.text_splitter.split_text(text)

        doc_id = str(uuid.uuid4())

        for i, chunk in enumerate(chunks):

            chunk_id = f"{doc_id}_{i}"

            chunk_metadata = metadata.copy() if metadata else {}

            chunk_metadata.update({
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "chunk_index": i,
                "section": chunk_metadata.get("section", "unknown")
            })

            existing = self.collection.get(ids=[chunk_id])

            if existing["ids"]:
                continue

            self.collection.add(
                ids=[chunk_id],
                documents=[chunk],
                metadatas=[chunk_metadata]
            )
    
    def search(self, query, n_results=5):

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        documents = []
    
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        for text, meta in zip(docs, metas):
            documents.append({
                "text": text,
                "metadata": meta
            })

        return documents