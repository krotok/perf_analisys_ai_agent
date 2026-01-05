# Kubernetes API

class K8sAgent:
    def __init__(self, settings):
        pass

    def collect(self, service, namespace):
        return {"restarts": 3, "hpa": False}