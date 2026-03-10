from crewai import Agent
from tools.search_tool import SearchTool
from tools.web_scraper import WebScraper
from tools.knowledge_store import KnowledgeStore

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

    def research(self, topic: str):

        print(f"Researching topic: {topic}")

        search_results = self.search_tool.search(topic)

        if not isinstance(search_results, list):
            print("Search not available")
            return

        for i, result in enumerate(search_results):

            url = result.get("url")

            if not url:
                continue

            page = self.scraper.scrape(url)

            if page and len(page["text"]) > 300:

               text = page["text"]
               title = page["title"]

               self.knowledge_store.store_document(
                    text=text,
                    title=title,
                    source=url
)

            print(f"Stored research document from {url}")