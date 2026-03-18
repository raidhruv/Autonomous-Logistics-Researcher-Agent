from agents.researcher import ResearchAgent


def main():
    print("=== Autonomous Logistics Research Agent ===")

    agent = ResearchAgent()

    while True:
        query = input("\nEnter research query (or 'exit'): ")

        if query.lower() == "exit":
            break

        try:
            agent.research(query)
            print("\n[✔] Research completed.\n")

        except Exception as e:
            print(f"\n[✖] Error: {e}\n")


if __name__ == "__main__":
    main()