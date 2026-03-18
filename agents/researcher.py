from crewai import Agent
from sqlalchemy import text
from sympy import content
from tools.search_tool import SearchTool
from tools.web_scraper import WebScraper
from tools.knowledge_store import KnowledgeStore
from urllib.parse import urlparse
from memory.chunker import SemanticChunker

class ResearchAgent:

    def __init__(self):

        self.search_tool = SearchTool()
        self.scraper = WebScraper()
        self.knowledge_store = KnowledgeStore()
        self.chunker = SemanticChunker()
        self.scraped_domains = set()
    
    def clean_text(self, text: str) -> str:
        lines = text.split("\n")

        cleaned = []
        for line in lines:
            line = line.strip()

            # remove junk patterns
            if not line:
                continue
            if line.lower().startswith("image"):
                continue
            if line.lower().startswith("figure"):
                continue
            if line.endswith("?"):  # remove Q/A prompts
                continue
            if len(line) < 30:  # too short = noise
                continue

            cleaned.append(line)

        return " ".join(cleaned)

        self.agent = Agent(
            role="Logistics Research Specialist",
            goal="Find reliable information about logistics technology and supply chain innovation",
            backstory=(
                "You are an expert logistics researcher specialized in autonomous logistics systems, "
                "supply chain optimization, and transportation technology."
            ),
            verbose=True
        )

    def filter_unique_domains(self, results):
        filtered_results = []

        for item in results:
            url = item["url"]
            domain = urlparse(url).netloc

            if domain not in self.scraped_domains:
                filtered_results.append(item)
                self.scraped_domains.add(domain)

        return filtered_results

    def research(self, query):

        print(f"[Researcher] Searching: {query}")
        results = self.search_tool.search(query)
        results = self.filter_unique_domains(results)

        for item in results:
            url = item["url"]
            content = item.get("content")
            
            try:
                # KEY LOGIC
                if content and len(content.strip()) > 100:
                    page = {
                        "text": content,
                    "title": item.get("title", ""),
                    }
                else:
                    page = self.scraper.scrape(url)

                if not page:
                    continue

                document = {
                    "text": page["text"],
                    "title": page["title"],
                    "url": url
                }
                document["text"] = self.clean_text(document["text"])

                print("\n=== DOCUMENT SAMPLE ===")
                print(document["text"][:300])

                chunks = self.chunker.chunk(document)
                self.knowledge_store.store_document(chunks)

            except Exception as e:
                print(f"[Researcher] Failed processing {url}: {e}")