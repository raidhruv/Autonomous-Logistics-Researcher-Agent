from memory.vector_db import VectorDB

db = VectorDB()

db.add_document(
    "doc1",
    "Autonomous trucks are transforming logistics supply chains."
)

results = db.search("future logistics automation")

print(results)