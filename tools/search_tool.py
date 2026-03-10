from tavily import TavilyClient
from config.settings import get_settings


class SearchTool:

    def __init__(self):

        settings = get_settings()

        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)


    def search(self, query: str, max_results: int = 5):

        try:

            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced"
            )

            urls = [r["url"] for r in response["results"]]

            return urls

        except Exception as e:

            print(f"[SearchTool] Error: {e}")
            return []