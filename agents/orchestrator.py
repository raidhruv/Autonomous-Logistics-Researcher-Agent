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

        self.max_research_rounds = 3

    def run(self, user_query):

        print("\n[Orchestrator] Starting research process...\n")

        research_round = 0

        while research_round < self.max_research_rounds:

            print(f"\n[Orchestrator] Research Round {research_round + 1}")

            documents = self.analyst.retriever.retrieve(user_query)

            # Knowledge coverage check
            if len(documents) >= 3:

               print("[Orchestrator] Knowledge coverage sufficient.")
               break

            print("[Orchestrator] Knowledge insufficient. Generating research queries.")

            queries = self.planner.generate_queries(user_query)

            for q in queries:
                self.researcher.research(q)

            research_round += 1


        print("\n[Orchestrator] Running final analysis...\n")

        analysis = self.analyst.analyze(user_query)

        print("\n[Orchestrator] Generating report...\n")

        report = self.writer.write_report(analysis)

        return report