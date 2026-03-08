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

    def add_document(self, doc_id: str, text: str):

        self.collection.add(
            ids=[doc_id],
            documents=[text]
        )

    def search(self, query: str, n_results: int = 3):

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        return results["documents"]