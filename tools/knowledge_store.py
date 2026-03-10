import hashlib
from memory.vector_db import VectorDB


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

        if not text or len(text.strip()) == 0:
            return

        chunks = self._chunk_text(text)

        for chunk in chunks:

            doc_id = self._generate_doc_id(chunk)

            metadata = {
                "title": title,
                "source": source
            }

            self.vector_db.add_document(
                doc_id=doc_id,
                text=chunk,
                metadata=metadata
            )