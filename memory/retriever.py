from memory.vector_db import VectorDB

class Retriever:

    def __init__(self):
        self.vector_db = VectorDB()
        
    def retrieve(self, query: str, k: int = 5):

        results = self.vector_db.search(query, n_results=k)

        documents = results[0] if results else []

        return documents
    
    def build_context(self, documents):

        context = "\n\n".join(documents)

        return context
    