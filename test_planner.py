from agents.query_planner import QueryPlanner

planner = QueryPlanner()

queries = planner.generate_queries("What is customs duty")

print("\nGenerated Queries:\n")

for q in queries:
    print("-", q)