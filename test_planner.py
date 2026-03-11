from memory.vector_db import VectorDB
from memory.retriever import Retriever

# initialize
vector_db = VectorDB()
retriever = Retriever()

# add one document with metadata
vector_db.add_document(
    text="""
Customs duties are taxes imposed on imported goods.
Ad valorem duty is calculated as a percentage of product value.
""",
    metadata={
        "source": "test_source",
        "title": "Customs Duty Guide",
        "section": "Duty Calculation"
    }
)

# query
query = "percentage customs duty calculation"

docs = retriever.retrieve(query, k=2)

print("\nRetrieved Documents With Citations:\n")

for d in docs:
    print(d)
    print("\n--------------------\n")