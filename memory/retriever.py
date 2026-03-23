from memory.vector_db import VectorDB
from langchain_groq import ChatGroq
from config.settings import get_settings
from sentence_transformers import CrossEncoder
from memory.citation_manager import CitationManager
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

        # Strong cross-encoder for reranking
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    # QUERY EXPANSION
    def expand_query(self, query: str):
        prompt = f"""
Generate 4 diverse semantic search queries for the topic below.

Focus on:
- different angles
- different terminology
- deeper subtopics

Topic: {query}

Return each query on a new line.
"""

        response = self.llm.invoke(prompt)

        queries = [
            q.strip()
            for q in response.content.split("\n")
            if q.strip()
        ]

        # Always include original query
        return [query] + queries


    def limit_per_source(self, documents, max_per_source=2):
        source_counts = {}
        filtered = []

        for doc in documents:
            url = doc.get("metadata", {}).get("url", "unknown")

            count = source_counts.get(url, 0)
            if count >= max_per_source:
                continue

            source_counts[url] = count + 1
            filtered.append(doc)

        return filtered

    def rerank(self, query, documents, top_k=5):
        if not documents:
            return []

        pairs = [(query, doc["text"]) for doc in documents]
        scores = self.reranker.predict(pairs)

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, _ in ranked[:top_k]]


    def retrieve(self, query: str, k: int = 5):
        queries = self.expand_query(query)

        all_docs = []

        
        for q in queries:
            results = self.vector_db.search(q, n_results=10)

            if not results:
                continue

            all_docs.extend(results)

        if not all_docs:
            logger.warning(f"No documents found for query: {query}")
            return []

        
        filtered_docs = self.limit_per_source(all_docs, max_per_source=2)

       
        reranked_docs = self.rerank(query, filtered_docs, top_k=k)

        logger.info(
            f"Retriever: {len(reranked_docs)} results selected "
            f"from {len(all_docs)} candidates for query: {query}"
        )

        return reranked_docs

    
    def build_context(self, documents):
        context_blocks = []

        for i, doc in enumerate(documents, start=1):
            text = doc.get("text", "")
            url = doc.get("metadata", {}).get("url", "unknown")

            block = f"[{i}] {text}\n(Source: {url})"
            context_blocks.append(block)

        return "\n\n".join(context_blocks)