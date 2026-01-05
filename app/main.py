# Entry point

from app.orchestrator import Orchestrator
from app.config import Settings

def main():
    settings = Settings()
    orchestrator = Orchestrator(settings)
    orchestrator.run(
        service="payments-api",
        namespace="prod",
        symptom="p95 latency degradation"
    )

if __name__ == "__main__":
    main()