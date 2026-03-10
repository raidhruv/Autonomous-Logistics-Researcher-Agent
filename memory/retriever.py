from memory.vector_db import VectorDB
from langchain_groq import ChatGroq
from config.settings import get_settings
from sentence_transformers import CrossEncoder


class Retriever:

    def __init__(self):
        self.settings = get_settings()
        self.vector_db = VectorDB()

        self.llm = ChatGroq(
            model=self.settings.MODEL_NAME,
            temperature=0,
            groq_api_key=self.settings.GROQ_API_KEY
        )

        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def expand_query(self, query: str):

        prompt = f"""
Generate 4 alternative search queries for the following topic.

Topic: {query}

Return each query on a new line.
"""
        response = self.llm.invoke(prompt)
        queries = [q.strip() 
                   for q in response.content.split("\n") 
                   if q.strip()]
        return [query] + queries

    def rerank(self, query, documents, top_k=5):
        pairs = [(query, doc) for doc in documents]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, score in ranked[:top_k]]    

    def retrieve(self, query: str, k: int = 3):
        queries = self.expand_query(query)
        all_docs = []

        for q in queries:
            results = self.vector_db.search(q, n_results=k)
            docs = results[0] if results else []
            all_docs.extend(docs)

        unique_docs = list(dict.fromkeys(all_docs))
        reranked_docs = self.rerank(query, unique_docs, top_k=k)
        return reranked_docs

    def build_context(self, documents):

        return "\n\n".join(documents)