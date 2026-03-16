from agents.orchestrator import Orchestrator
from utils.logger import logger


def main():

    query = input("Enter research query: ")

    logger.info(f"User query received: {query}")

    orchestrator = Orchestrator()

    report = orchestrator.run(query)

    print("\n===== FINAL REPORT =====\n")
    print(report)


if __name__ == "__main__":
    main()