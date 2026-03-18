from memory.vector_db import VectorDB
from langchain_groq import ChatGroq
from config.settings import get_settings
from sentence_transformers import CrossEncoder
from memory.citation_manager import CitationManager
from rank_bm25 import BM25Okapi
from utils.logger import logger


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

    # -----------------------------
    # Query Expansion
    # -----------------------------
    def expand_query(self, query: str):
        prompt = f"""
Generate 4 alternative search queries for the following topic.

Topic: {query}

Return each query on a new line.
"""

        response = self.llm.invoke(prompt)

        queries = [
            q.strip()
            for q in response.content.split("\n")
            if q.strip()
        ]

        return [query] + queries

    # -----------------------------
    # Keyword Search (BM25)
    # -----------------------------
    def keyword_search(self, query, documents, top_k=5):
        if not documents:
            return []

        def get_text(doc):
            return doc["text"] if isinstance(doc, dict) else doc

        tokenized_docs = [get_text(doc).split() for doc in documents]
        bm25 = BM25Okapi(tokenized_docs)

        tokenized_query = query.split()
        scores = bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, score in ranked[:top_k]]

    # -----------------------------
    # Reranking (FIXED)
    # -----------------------------
    def rerank(self, query, documents, top_k=5):
        if not documents:
            return []

        pairs = [(query, doc["text"]) for doc in documents]
        scores = self.reranker.predict(pairs)

        weighted = []
        split_index = len(documents) // 2  # semantic first, keyword later

        for i, (doc, score) in enumerate(zip(documents, scores)):
            if i < split_index:
                score *= 1.3  # semantic boost
            weighted.append((doc, score))

        ranked = sorted(weighted, key=lambda x: x[1], reverse=True)

        # deduplicate AFTER ranking
        seen = set()
        final = []

        for doc, score in ranked:
            if doc["text"] not in seen:
                seen.add(doc["text"])
                final.append(doc)

            if len(final) >= top_k:
                break

        return final

    # -----------------------------
    # MAIN RETRIEVE
    # -----------------------------
    def retrieve(self, query: str, k: int = 3):
        queries = self.expand_query(query)

        all_docs = []

        for q in queries:
            results = self.vector_db.search(q, n_results=k)
            if results:
                all_docs.extend(results)

        # deduplicate early
        unique_docs = all_docs

        # hybrid retrieval
        keyword_docs = self.keyword_search(query, unique_docs, top_k=k)

        # combine (NO duplication hack)
        combined_docs = unique_docs + keyword_docs

        # rerank with weighting
        reranked_docs = self.rerank(query, combined_docs, top_k=k)

        logger.info(f"Retriever returned {len(reranked_docs)} chunks for query: {query}")

        return reranked_docs

    # -----------------------------
    # CONTEXT BUILDER
    # -----------------------------
    def build_context(self, documents):
        texts = []

        for doc in documents:
            if isinstance(doc, dict):
                texts.append(doc.get("text", ""))
            else:
                texts.append(str(doc))

        return "\n\n".join(texts)