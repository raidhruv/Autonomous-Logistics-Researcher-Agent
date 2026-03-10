from agents.researcher import ResearchAgent
from agents.analyst import AnalystAgent


def main():

    query = input("Enter research query: ")

    print("Collecting research data...")

    # Step 1: collect research material
    researcher = ResearchAgent()
    researcher.research(query)

    print("Analyzing documents...")

    # Step 2: analyze stored knowledge
    analyst = AnalystAgent()
    result = analyst.analyze(query)

    print("\n=== Analysis ===\n")
    print(result)


if __name__ == "__main__":
    main()