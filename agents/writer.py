from langchain_groq import ChatGroq
from config.settings import get_settings


class WriterAgent:

    def __init__(self):

        self.settings = get_settings()

        self.llm = ChatGroq(
            model=self.settings.MODEL_NAME,
            temperature=0.3,
            groq_api_key=self.settings.GROQ_API_KEY
        )

    def write_report(self, analysis: str):

        prompt = f"""
You are a professional research report writer.

Convert the following analysis into a clear structured report.

Structure the report with these sections:

1. Executive Summary
2. Key Insights
3. Detailed Explanation
4. Conclusion

Analysis:
{analysis}
"""

        response = self.llm.invoke(prompt)

        return response.content