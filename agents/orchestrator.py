from multiprocessing import context
from memory.retriever import Retriever
from agents.query_planner import QueryPlanner
from agents.researcher import ResearchAgent
from agents.analyst import AnalystAgent
from agents.writer import WriterAgent
from evaluation.evaluator import Evaluator
from utils.logger import logger


class Orchestrator:

    def __init__(self):

        self.planner = QueryPlanner()
        self.researcher = ResearchAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()
        self.evaluator = Evaluator()
        self.retriever = Retriever()
        self.max_research_rounds = 3
        
    def run(self, user_query):
        print("\n[Orchestrator] Starting research process...\n")

        # Generate search queries
        queries = self.planner.generate_queries(user_query)

        # Run research (populate vector DB)
        for q in queries:
            self.researcher.research(q)

        print("\n[Orchestrator] Retrieving relevant documents...\n")

        # Retrieve
        documents = self.retriever.retrieve(user_query)

        if not documents:
            return "No relevant information found."

        print("\n[Orchestrator] Generating report...\n")

        # Build context
        context = self.retriever.build_context(documents)

        # Write report
        report = self.writer.write_report(user_query, context)
        # Build citations
        citations = []

        for i, chunk in enumerate(documents):
            if isinstance(chunk, dict):
                text = chunk.get("text", "")
                source = chunk.get("source", "Unknown")
            else:
                text = str(chunk)
                source = "Unknown"

            citations.append({
                "id": i + 1,
                "text": text,
                "source": source
            })

        # Evaluate
        evaluation = self.evaluator.evaluate(
            query=user_query,
            retrieved_chunks=documents,
            report=report,
            citations=citations
        )

        print("\n[Evaluator] Evaluation Results:")
        print(evaluation)

        
        return {
            "report": report,
            "evaluation": evaluation,
            "citations": citations
        }