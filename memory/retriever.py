from typer import prompt
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
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        print("Reranker initialized:", hasattr(self, "reranker"))

    def deduplicate_docs(self, documents):
        seen = set()
        unique = []

        for doc in documents:
            text = doc.get("text", "").strip()
            if not text:
                continue

            if text in seen:
                continue

            seen.add(text)
            unique.append(doc)

        return unique

        # cross-encoder for reranking
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    def clean_text(self, text):
        if not text:
            return ""

        blacklist = [
            "ignore previous instructions",
            "system:",
            "assistant:",
            "user:"
        ]

        text_lower = text.lower()
        for b in blacklist:
            if b in text_lower:
                text = text.replace(b, "")

        return text.strip()[:800]
    
        # query expansion       
    def expand_query(self, query: str):
            prompt = f"""
        Generate 3 short semantic search queries for retrieval.

        Rules:
        - Each query must be under 10 words
        - No questions
        - No explanations
        - No punctuation like '?'
        - Focus on keywords and phrases


        Topic: {query}

        Return each query on a new line. No numbering, no explanation.
        """

            response = self.llm.invoke(prompt)

            raw_queries = response.content.split("\n")

            # Step 1: clean + normalize
            queries = [
                q.strip().lower()
                for q in raw_queries
                if q.strip()
                and len(q.split()) <= 10
                and "?" not in q
            ]

            # Step 2: deduplicate
            queries = list(set(queries))

            # Step 3: enforce strict limit
            queries = queries[:3]

            # Step 4: always include original query FIRST
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

        # SCORE FILTER
        threshold = 0.8

        filtered = [
            doc for doc, score in ranked
            if score is not None and score > threshold
        ]

        # fallback
        if not filtered:
            filtered = [doc for doc, _ in ranked[:top_k]]

        return filtered[:top_k]
        print(f"[DEBUG] Rerank scores: {[round(s,2) for s in scores]}")

    def retrieve(self, query: str, k: int = 5):
        queries = self.expand_query(query)


        all_docs = []
  
        for q in queries:
            results = self.vector_db.search(q, n_results=10)

            if not results:
                continue

            all_docs.extend(results)

        all_docs = self.deduplicate_docs(all_docs)

        if not all_docs:
            logger.warning(f"No documents found for query: {query}")
            return []

        filtered_docs = self.limit_per_source(all_docs, max_per_source=2)

        # HARD CAP BEFORE RERANK
        filtered_docs = filtered_docs[:15]

        reranked_docs = self.rerank(query, filtered_docs, top_k=k)

        logger.info(
            f"Retriever: {len(reranked_docs)} results selected "
            f"from {len(all_docs)} candidates for query: {query}"
        )

        return reranked_docs

    
    def build_context(self, documents):
        context_blocks = []

        for i, doc in enumerate(documents, start=1):
            text = self.clean_text(doc.get("text", ""))
            url = doc.get("metadata", {}).get("url", "unknown")

            block = f"[{i}] {text}\n(Source: {url})"
            context_blocks.append(block)

        return "\n\n".join(context_blocks)