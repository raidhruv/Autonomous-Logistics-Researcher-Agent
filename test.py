from tools.knowledge_extractor import KnowledgeExtractor

sample = {
    "url": "example.com",
    "title": "Customs Duty",
    "text": """ Customs duties are taxes imposed on imported goods by governments. 
    They are designed to regulate trade, protect domestic industries, 
    and generate revenue. Duties can be calculated as a percentage of 
    the product value (ad valorem) or as a fixed amount per unit. 
    Subscribe to our newsletter for more updates."""
}

extractor = KnowledgeExtractor()

doc = extractor.extract(sample)

print("Extracted document:")
print(doc)