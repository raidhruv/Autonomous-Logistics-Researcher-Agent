from typing import Dict
import re


class KnowledgeExtractor:

    def __init__(self):
        pass

    def _normalize_whitespace(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _remove_boilerplate(self, text: str) -> str:

        boilerplate_patterns = [
            "subscribe",
            "sign up",
            "newsletter",
            "all rights reserved",
            "cookie policy",
            "privacy policy"
        ]

        lines = text.split(".")

        cleaned_lines = []

        for line in lines:
            if not any(bp in line.lower() for bp in boilerplate_patterns):
                cleaned_lines.append(line)

        return ".".join(cleaned_lines)

    def extract(self, scraped_doc: Dict) -> Dict | None:
        print("Extractor received:", scraped_doc)
        if not scraped_doc:
            return None

        text = scraped_doc["text"]

        text = self._normalize_whitespace(text)

        text = self._remove_boilerplate(text)

        if len(text) < 300:
            return None

        return {
            "title": scraped_doc["title"],
            "url": scraped_doc["url"],
            "text": text
        }