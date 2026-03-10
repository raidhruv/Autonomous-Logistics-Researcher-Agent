from langchain_groq import ChatGroq
from config.settings import get_settings


class QueryPlanner:

    def __init__(self):

        self.settings = get_settings()

        self.llm = ChatGroq(
            model=self.settings.MODEL_NAME,
            temperature=0,
            groq_api_key=self.settings.GROQ_API_KEY
        )

    def generate_queries(self, user_query: str):

        prompt = f"""
You are a research planner.

Break the following topic into 4 concise search queries that would help gather comprehensive information.

Topic:
{user_query}

Return each query on a new line.
"""

        response = self.llm.invoke(prompt)

        queries = [
            q.strip("- ").strip()
            for q in response.content.split("\n")
            if q.strip()
        ]

        return queries