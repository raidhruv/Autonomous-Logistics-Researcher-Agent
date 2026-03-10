from agents.query_planner import QueryPlanner
from agents.researcher import ResearchAgent
from agents.analyst import AnalystAgent
from agents.writer import WriterAgent


class Orchestrator:

    def __init__(self):

        self.planner = QueryPlanner()
        self.researcher = ResearchAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()

    def run(self, user_query: str):

        print("\n[Orchestrator] Planning research...\n")

        research_queries = self.planner.generate_queries(user_query)

        print("Generated Queries:")
        for q in research_queries:
            print("-", q)

        print("\n[Orchestrator] Collecting research...\n")

        for query in research_queries:
            self.researcher.research(query)

        print("\n[Orchestrator] Analyzing knowledge...\n")

        analysis = self.analyst.analyze(user_query)

        print("\n[Orchestrator] Generating report...\n")

        report = self.writer.write_report(analysis)

        return report