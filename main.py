from agents.orchestrator import Orchestrator


def main():

    query = input("Enter research query: ")

    orchestrator = Orchestrator()

    result = orchestrator.run(query)

    print("\n===== FINAL REPORT =====\n")
    print(result)


if __name__ == "__main__":
    main()