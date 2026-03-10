class CitationManager:

    def __init__(self):
        pass


    def attach_citations(self, documents):

        formatted_docs = []

        for doc in documents:

            text = doc.get("text", "")
            metadata = doc.get("metadata", {})

            citation = (
                f"\n\n[Citation | "
                f"DocID: {metadata.get('doc_id')} | "
                f"Chunk: {metadata.get('chunk_index')} | "
                f"Source: {metadata.get('source')} | "
                f"Section: {metadata.get('section')}]"
            )

            formatted_docs.append(text + citation)

        return formatted_docs