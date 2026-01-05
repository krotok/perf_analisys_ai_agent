# Latency AI Agent for Kubernetes

## Overview

**Latency AI Agent** is a production-oriented skeleton for an autonomous Performance Engineering agent designed to analyze **p95 latency degradations** in 
Kubernetes-based services.

The agent correlates **metrics, logs, Kubernetes state, and recent code changes**, reasons about potential bottlenecks, and proposes **actionable fixes**.

This project is intentionally designed as a **hybrid system**:
- deterministic, rule-based logic for critical decisions
- LLM-based reasoning for hypothesis generation and recommendations

The goal is **explainability, safety, and production readiness**, not blind automation.

---

## Key Capabilities

- Detect and analyze p95 latency degradation
- Collect and correlate:
  - Prometheus metrics
  - Loki / ELK logs
  - Kubernetes runtime state
  - Recent code changes
- Identify probable bottlenecks with confidence scores
- Generate concrete fix recommendations
- Deliver results to engineers and stakeholders

---

## Non-Goals

This project **does NOT**:
- Automatically deploy fixes to production
- Replace human SRE judgment
- Allow LLMs to decide pass/fail or SLO compliance

All critical decisions remain **deterministic and auditable**.

---

## High-Level Architecture



## Run:
kubectl apply -f deployment.yaml or python -m app.main or Alertmanager → Webhook → Agent