from crewai import Agent
from tools.search_tool import SearchTool
from tools.web_scraper import WebScraper
from tools.knowledge_store import KnowledgeStore
from urllib.parse import urlparse

class ResearchAgent:

    def __init__(self):

        self.search_tool = SearchTool()
        self.scraper = WebScraper()
        self.knowledge_store = KnowledgeStore()

        self.agent = Agent(
            role="Logistics Research Specialist",
            goal="Find reliable information about logistics technology and supply chain innovation",
            backstory=(
                "You are an expert logistics researcher specialized in autonomous logistics systems, "
                "supply chain optimization, and transportation technology."
            ),
            verbose=True
        )

        def filter_unique_domains(self, urls):

            seen_domains = set()
            filtered_urls = []

            for url in urls:

                domain = urlparse(url).netloc

                if domain not in seen_domains:
                   filtered_urls.append(url)
                   seen_domains.add(domain)

            return filtered_urls

    def research(self, query):

        print(f"[Researcher] Searching: {query}")
        urls = self.search_tool.search(query)
        urls = self.filter_unique_domains(urls)
        for url in urls:

            try:

                page = self.scraper.scrape(url)

                if not page:
                     continue

                text = page["text"]
                title = page["title"]

                self.knowledge_store.store_document(
                    text=text,
                    title=title,
                    source=url
                )

            except Exception as e:

               print(f"[Researcher] Failed scraping {url}: {e}")