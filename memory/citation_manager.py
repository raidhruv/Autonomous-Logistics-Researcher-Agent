class CitationManager:

    def __init__(self):
        pass


    def attach_citations(self, documents):

        formatted_docs = []

        for doc in documents:

            if isinstance(doc, dict):

                text = doc.get("text", "")
                metadata = doc.get("metadata", {})

                source = metadata.get("source", "Unknown source")
                title = metadata.get("title", "Unknown title")

                citation = f"\n\n[Source: {title} | {source}]"

                formatted_docs.append(text + citation)

            else:

                formatted_docs.append(str(doc))

        return formatted_docs