# Planner / Controller

from app.agents.metrics_agent import MetricsAgent
from app.agents.logs_agent import LogsAgent
from app.agents.k8s_agent import K8sAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.fix_agent import FixAgent

class Orchestrator:
    def __init__(self, settings):
        self.metrics = MetricsAgent(settings)
        self.logs = LogsAgent(settings)
        self.k8s = K8sAgent(settings)
        self.reasoning = ReasoningAgent(settings)
        self.fix = FixAgent()

    def run(self, service, namespace, symptom):
        metrics = self.metrics.collect(service, namespace)
        logs = self.logs.collect(service, namespace)
        k8s = self.k8s.collect(service, namespace)

        analysis = self.reasoning.analyze(symptom, metrics, logs, k8s)
        fixes = self.fix.propose(analysis)

        print("ANALYSIS:", analysis)
        print("FIXES:", fixes)