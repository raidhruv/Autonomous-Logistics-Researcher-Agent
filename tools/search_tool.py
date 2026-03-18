from tavily import TavilyClient
from config.settings import get_settings
from utils.logger import logger

class SearchTool:

    def __init__(self):
        settings = get_settings()
        if not settings.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is missing — check .env loading")
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY) 

    def search(self, query: str, max_results: int = 5):

        try:

            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced"
            )

            documents = [
                {
                    "url": r.get("url"),
                    "content": r.get("content"),
                    "title": r.get("title")
                }
                for r in response["results"]
            ]

            logger.info(f"Search returned {len(documents)} documents for query: {query}")

            return documents

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise RuntimeError(f"Tavily search failed: {e}")