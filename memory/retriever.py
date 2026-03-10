from memory.vector_db import VectorDB
from langchain_groq import ChatGroq
from config.settings import get_settings
from sentence_transformers import CrossEncoder
from memory.citation_manager import CitationManager
from rank_bm25 import BM25Okapi


class Retriever:

    def __init__(self):
        self.settings = get_settings()
        self.vector_db = VectorDB()
        self.citation_manager = CitationManager()

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
        pairs = [(query, doc["text"]) for doc in documents]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, score in ranked[:top_k]]

    def keyword_search(self, query, documents, top_k=5):

        if not documents:
           return []

        tokenized_docs = [doc["text"].split() for doc in documents]
        bm25 = BM25Okapi(tokenized_docs)
        tokenized_query = query.split()
        scores = bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, score in ranked[:top_k]]    

    def retrieve(self, query: str, k: int = 3):

        queries = self.expand_query(query)
        all_docs = []

        for q in queries:
            results = self.vector_db.search(q, n_results=k)
            docs = results[0] if results else []
            all_docs.extend(docs)

        unique_docs = list(dict.fromkeys(all_docs))

        # Hybrid Retrieval
        keyword_docs = self.keyword_search(query, unique_docs, top_k=k)

        # slight weighting toward semantic search
        semantic_weighted = unique_docs * 2

        combined_docs = list(dict.fromkeys(unique_docs + keyword_docs))
        # Hybrid End
        reranked_docs = self.rerank(query, combined_docs, top_k=k)

        docs_with_citations = self.citation_manager.attach_citations(reranked_docs)

        return docs_with_citations

    def build_context(self, documents):

        return "\n\n".join(documents)