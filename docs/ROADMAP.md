# Roadmap – streamforge

> **Author**: Senior Product & Engineering Lead  
> **Version**: 1.0.0  
> **Last Updated**: 2026‑06‑21  

---

## Table of Contents

1. [Vision & Goals](#vision--goals)
2. [MVP Milestone](#mvp-milestone)
3. [Phase 1 – v1.0](#phase‑1---v10)
4. [Phase 2 – v2.0](#phase‑2---v20)
5. [Themes & Feature Sets](#themes--feature-sets)
6. [Timeline & Cadence](#timeline--cadence)
7. [Success Metrics](#success-metrics)
8. [Risks & Mitigations](#risks--mitigations)
9. [Dependencies & Integrations](#dependencies--integrations)
10. [Governance & Release Process](#governance--release-process)
11. [Contribution & Documentation](#contribution--documentation)
12. [License & Community](#license--community)
13. [Next Steps](#next-steps)

---

## Vision & Goals

- **Deliver a production‑ready time‑series platform** that lets data scientists and developers ingest, process, and visualize data at scale.
- **Leverage Axentx’s autonomous AI‑workforce** to continuously improve ingestion pipelines, data quality, and analytics.
- **Avoid duplication** of existing Axentx portfolio (e.g., iceoryx2) while extending the product family with unique value‑add.
- **Open‑source first**: core platform under MIT, with commercial extensions for enterprise customers.

---

## MVP Milestone

| # | Feature | Description | MVP‑Critical? | Acceptance Criteria |
|---|---------|-------------|---------------|---------------------|
| 1 | **Core Ingestion Engine** | Pull data from Kafka, MQTT, HTTP, and local files into a time‑series store. | ✅ | • 99.9 % success rate on 1 M events/day<br>• Latency < 200 ms (real‑time) |
| 2 | **Time‑Series Store** | Underlying storage (TimescaleDB
