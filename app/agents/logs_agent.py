# Loki / Elastic

class LogsAgent:
    def __init__(self, settings):
        pass

    def collect(self, service, namespace):
        return {"errors": 120, "patterns": ["timeout", "db pool exhausted"]}