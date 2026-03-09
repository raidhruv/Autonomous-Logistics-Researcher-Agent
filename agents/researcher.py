from crewai import Agent
from tools.search_tool import SearchTool
from tools.web_scraper import WebScraper
from memory.vector_db import VectorDB


class ResearchAgent:

    def __init__(self):

        self.search_tool = SearchTool()
        self.scraper = WebScraper()
        self.memory = VectorDB()

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

            content = self.scraper.scrape(url)

            if content:

                doc_id = f"research_{i}"

                self.memory.add_document(doc_id, content)

                print(f"Stored research document {doc_id}")