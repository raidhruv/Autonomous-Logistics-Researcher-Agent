import hashlib
from memory.vector_db import VectorDB
import uuid


class KnowledgeStore:

    def __init__(self):

        self.vector_db = VectorDB()

        # chunk settings
        self.chunk_size = 500
        self.chunk_overlap = 100


    def _generate_doc_id(self, text: str):

        return hashlib.md5(text.encode()).hexdigest()


    def _chunk_text(self, text: str):

        chunks = []

        start = 0
        length = len(text)

        while start < length:

            end = start + self.chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            start += self.chunk_size - self.chunk_overlap

        return chunks

    def store_document(self, text: str, title: str, source: str):

        chunks = self._chunk_text(text)

        doc_id = str(uuid.uuid4())

        for idx, chunk in enumerate(chunks):

            chunk_id = f"{doc_id}_{idx}"

            metadata = {
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "source": source,
                "title": title,
                "section": "unknown",  # placeholder for future section extraction
                "chunk_index": idx
            }

            self.vector_db.add_document(
                text=chunk,
                metadata=metadata
            )

    
            