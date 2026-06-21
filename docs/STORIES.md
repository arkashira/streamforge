# STORIES.md
**Project:** `streamforge` – Time‑Series Data Management & Analysis Platform  
**Owner:** Axentx Product Team  
**Target Release:** MVP (v0.1) → Full Feature Set (v1.0)  

---  

## Table of Contents
1. [Epics Overview](#epics-overview)  
2. [User Story Backlog](#user-story-backlog)  
   - [Epic 1 – Data Ingestion](#epic-1-data-ingestion)  
   - [Epic 2 – Stream Processing](#epic-2-stream-processing)  
   - [Epic 3 – Storage & Retrieval](#epic-3-storage--retrieval)  
   - [Epic 4 – Visualization & Exploration](#epic-4-visualization--exploration)  
   - [Epic 5 – Operations & Security](#epic-5-operations--security)  

---  

## Epics Overview
| Epic | Goal (MVP) | Primary Users | Rough Priority |
|------|------------|---------------|----------------|
| **1 – Data Ingestion** | Accept high‑throughput time‑series streams from multiple sources (HTTP, gRPC, Kafka) and persist them reliably. | Data Engineers, DevOps | ★★★★★ |
| **2 – Stream Processing** | Provide low‑latency transformation (filter, aggregate, enrich) using a declarative pipeline DSL. | Data Scientists, Backend Engineers | ★★★★☆ |
| **3 – Storage & Retrieval** | Store ingested data in a columnar, time‑partitioned store; expose fast point‑lookup & range queries. | Analysts, Application Developers | ★★★★☆ |
| **4 – Visualization & Exploration** | Offer an interactive web UI + API for charting, dashboards, and ad‑hoc queries. | Data Scientists, Business Users | ★★★☆☆ |
| **5 – Operations & Security** | Enable multi‑tenant isolation, RBAC, audit logging, and observability (metrics, tracing). | Platform Ops, Security Teams | ★★★☆☆ |

---  

## User Story Backlog  

### Epic 1 – Data Ingestion
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **1.1** | **As a Data Engineer, I want to push time‑series points over HTTP POST, so that I can quickly prototype ingestion without extra infrastructure.** | • Endpoint `POST /ingest` accepts JSON lines `{timestamp, metric, value, tags}`.<br>• Returns `202 Accepted` with ingestion ID.<br>• Handles ≥ 10 k req/s with < 100 ms latency (load‑tested). |
| **1.2** | **As a Data Engineer, I want a gRPC ingestion service, so that high‑performance clients can stream data efficiently.** | • Service `IngestStream` defined in `proto/ingest.proto`.<br>• Supports bidirectional streaming, back‑pressure handling.<br>• Guarantees at‑least‑once delivery with client‑acknowledged offsets. |
| **1.3** | **As a DevOps Engineer, I want a Kafka connector, so that existing event pipelines can feed StreamForge directly.** | • Connector `streamforge-kafka-sink` reads from configurable topics.<br>• Auto‑creates topic partitions based on metric cardinality.<br>• Emits metrics `ingest.kafka.success`, `ingest.kafka.error`. |
| **1.4** | **As a Data Engineer, I want schema validation and automatic type coercion, so that bad data does not corrupt the store.** | • Validation rules defined in a YAML schema file.<br>• Invalid records are routed to a dead‑letter queue with error details.<br>• Success rate ≥ 99.9 % on valid payloads. |

### Epic 2 – Stream Processing
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **2.1** | **As a Data Scientist, I want to define a processing pipeline using a simple DSL, so that I can filter, aggregate, and enrich streams without writing code.** | • DSL file (`pipeline.sf`) supports `filter`, `window`, `aggregate`, `map`.<br>• Pipeline can be hot‑reloaded without downtime.<br>• Unit‑test harness validates DSL syntax. |
| **2.2** | **As a Backend Engineer, I want built‑in windowed aggregations (e.g., tumbling, sliding), so that I can compute real‑time metrics.** | • Supports time‑based windows down to 1 s.<br>• Guarantees deterministic results under out‑of‑order data (watermark handling). |
| **2.3** | **As a Data Scientist, I want to enrich events with external reference data (e.g., device metadata), so that downstream analysis has context.** | • Enrichment step can query a key‑value store via async API.<br>• Latency impact ≤ 5 ms per record. |
| **2.4** | **As a Platform Engineer, I want pipeline health metrics (throughput, latency, error rate), so that I can monitor and autoscale.** | • Exposes Prometheus metrics `pipeline.processed_total`, `pipeline.latency_seconds`, `pipeline.errors_total`. |
| **2.5** | **As a Data Scientist, I want to preview pipeline output on a sample dataset, so that I can iterate quickly.** | • CLI command `sf preview --pipeline my.sf --sample 10k` prints first 100 transformed rows.<br>• No side‑effects on production data. |

### Epic 3 – Storage & Retrieval
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **3.1** | **As an Analyst, I want to query a metric by time range via REST, so that I can retrieve data for ad‑hoc analysis.** | • Endpoint `GET /query?metric=cpu&start=…&end=…` returns JSON array sorted by timestamp.<br>• Supports pagination (`limit`, `offset`). |
| **3.2** | **As an Application Developer, I want a high‑performance columnar store (e.g., Parquet on object storage) with time‑partitioning, so that queries are fast and cost‑effective.** | • Data written in Parquet files partitioned by `year/month/day/hour`.<br>• Query latency for 1 M points ≤ 200 ms. |
| **3.3** | **As a Data Engineer, I want to down‑sample older data automatically, so that storage cost grows sub‑linearly.** | • Retention policy: raw → 1‑hour resolution for 30 d, then 1‑day resolution for 1 y.<br>• Down‑sampling runs as a nightly job with < 5 % of daily ingest load. |
| **3.4** | **As a Data Scientist, I need a bulk export (CSV/Parquet) of a query result, so that I can feed external ML pipelines.** | • `GET /export?format=parquet&metric=…` streams file directly from storage.<br>• Export completes within 2× the query latency. |

### Epic 4 – Visualization & Exploration
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **4.1** | **As a Business User, I want a web dashboard to plot time‑series with zoom/pan, so that I can spot trends.** | • UI built with React + Plotly.<br>• Supports line, area, and heat‑map charts.<br>• Interaction latency ≤ 300 ms for 10 k points. |
| **4.2** | **As a Data Scientist, I want to save and share query‑based dashboards, so that collaborators can view the same visualizations.** | • Dashboard objects stored with UUID, owner, and ACL.<br>• Share link respects RBAC (read‑only). |
| **4.3** | **As an Analyst, I want to apply ad‑hoc filters (tags, value ranges) on the UI, so that I can drill‑down without writing code.** | • UI filter panel updates chart in < 500 ms.<br>• Filters are reflected in the underlying API query parameters. |
| **4.4** | **As a Platform Engineer, I want the UI to use the same authentication token as the API, so that SSO works across the stack.** | • UI obtains JWT via OAuth2 Authorization Code flow.<br>• Token refresh handled transparently. |

### Epic 5 – Operations & Security
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **5.1** | **As a Security Engineer, I want multi‑tenant isolation at the data layer, so that one tenant cannot read another’s metrics.** | • Tenant ID is a mandatory field on every ingest request.<br>• Queries automatically filter by tenant context derived from JWT. |
| **5.2** | **As a Platform Ops Engineer, I want role‑based access control (RBAC) for API endpoints, so that permissions are fine‑grained.** | • Roles: `viewer`, `ingestor`, `pipeline_editor`, `admin`.<br>• Enforced via middleware; unauthorized calls return `403`. |
| **5.3** | **As a DevOps Engineer, I want full audit logging of ingest, query, and pipeline changes, so that we can investigate incidents.** | • Logs written to centralized Loki/ELK with fields: `user`, `action`, `resource`, `timestamp`, `status`. |
| **5.4** | **As a Site Reliability Engineer, I want health‑check endpoints and graceful shutdown, so that the service can be orchestrated by Kubernetes.** | • `/healthz` returns `200` only when ingestion, storage, and pipeline workers are ready.<br>• SIGTERM triggers drain of in‑flight ingest batches before exit. |
| **5.5** | **As a Platform Engineer, I want observability dashboards (Prometheus + Grafana) pre‑bundled, so that we can monitor system health from day 0.** | • Exported metrics cover ingestion rate, storage latency, pipeline backlog, UI error rate.<br>• Sample Grafana dashboard JSON included in repo. |

---  

## Prioritisation for MVP (v0.1)

| Priority | Stories (by ID) |
|----------|-----------------|
| **Critical** | 1.1, 1.2, 3.1, 3.2, 5.1, 5.2, 5.4 |
| **High** | 2.1, 2.2, 4.1, 4.4 |
| **Medium** | 1.3, 1.4, 2.3, 2.4, 3.3, 4.2, 5.3 |
| **Low** | 2.5, 3.4, 4.3, 5.5 |

The MVP will deliver a **complete ingestion‑query‑visualize loop** with security and basic ops support. Subsequent sprints will expand processing DSL, down‑sampling, export, and richer UI features.  

---  

*Prepared by the StreamForge Product Team – Axentx*
