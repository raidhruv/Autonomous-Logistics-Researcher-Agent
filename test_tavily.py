from config.settings import get_settings
from tavily import TavilyClient

def test_tavily():
    settings = get_settings()

    print("KEY:", settings.TAVILY_API_KEY)

    client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    response = client.search(
        query="global trade market trends 2025",
        search_depth="advanced",
        max_results=5
    )

    print("\nRAW RESPONSE:\n", response)


if __name__ == "__main__":
    test_tavily()