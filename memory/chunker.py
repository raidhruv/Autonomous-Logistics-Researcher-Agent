import tiktoken
import re

class SemanticChunker:

    def __init__(self, max_tokens=400, overlap=80):
        self.max_tokens = max_tokens
        self.overlap = overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def _token_count(self, text):
        return len(self.encoding.encode(text))

    def chunk(self, document):

        paragraphs = re.split(r'(?<=[.!?]) +', document["text"])

        chunks = []
        current_chunk = []
        current_tokens = 0

        for p in paragraphs:

            tokens = self._token_count(p)

            if current_tokens + tokens > self.max_tokens or len(current_chunk) >= 5:

                chunk_text = " ".join(current_chunk)

                chunks.append({
                    "text": chunk_text,
                    "source": document.get("url", "Unknown"),
                    "title": document.get("title", "")
                })

                # overlap
                current_chunk = current_chunk[-2:]
                current_tokens = self._token_count(" ".join(current_chunk))

            current_chunk.append(p)
            current_tokens += tokens

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        results = []

        print("\n=== CHUNK DEBUG ===")
        print(f"Input length: {len(document['text'])}")
        print(f"Chunks created: {len(chunks)}")
        for i, chunk in enumerate(chunks):

            results.append({
                "text": chunk if isinstance(chunk, str) else chunk.get("text", ""),
                "source": document.get("url", "Unknown"),
                "title": document.get("title", ""),
                "chunk_id": i
            })
            print("\n=== FINAL CHUNK DEBUG ===")
            print(results[0])

        return results