from urllib import response
from annotated_types import doc
from langchain_groq import ChatGroq
from pydantic_settings import sources
from config.settings import get_settings
from utils.logger import logger


class WriterAgent:

    def __init__(self):

        self.settings = get_settings()

        self.llm = ChatGroq(
            model=self.settings.MODEL_NAME,
            temperature=0.3,
            groq_api_key=self.settings.GROQ_API_KEY
        )

    def write_report(self, analysis: str, documents: list):
        
        sources = []

        for i, doc in enumerate(documents, 1):
            meta = doc.get("metadata", {})
            source = meta.get("source", "unknown")
            sources.append(f"[{i}] {source}")

        sources_text = "\n".join(sources)

        prompt = f"""
        You are a professional research report writer.

        Convert the following analysis into a clear structured report.

        Use the provided sources to support claims and reference them using
        [1], [2], etc.

        Structure the report with these sections:

        1. Executive Summary
        2. Key Insights
        3. Detailed Explanation
        4. Conclusion

        Sources:
        {sources_text}

        Analysis:
        {analysis}
    """
        
        response = self.llm.invoke(prompt)
        report = response.content
        logger.info("Research report generated")
        return report
