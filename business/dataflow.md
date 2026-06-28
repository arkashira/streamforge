```markdown
# Dataflow Architecture for Streamforge

## External Data Sources
- IoT Devices
- APIs (REST, WebSocket)
- Databases (SQL, NoSQL)
- CSV/Excel files
- Streaming data sources (Kafka, MQTT)

## Ingestion Layer
- **Components:**
  - Data Ingestion API
  - Message Queue (e.g., RabbitMQ, Kafka)
  - Data Validation Service
  - Data Enrichment Service
- **Auth Boundaries:**
  - API Gateway with OAuth 2.0 for secure access to ingestion endpoints

## Processing/Transform Layer
- **Components:**
  - Stream Processing Engine (e.g., Apache Flink, Spark Streaming)
  - Batch Processing Engine (e.g., Apache Spark)
  - Data Transformation Functions (e.g., aggregation, filtering)
  - Anomaly Detection Module
- **Auth Boundaries:**
  - Role-based access control for processing jobs and transformations

## Storage Tier
- **Components:**
  - Time-Series Database (e.g., InfluxDB, TimescaleDB)
  - Object Storage (e.g., AWS S3, Google Cloud Storage)
  - Data Warehouse (e.g., Snowflake, BigQuery)
- **Auth Boundaries:**
  - Encrypted storage with IAM roles for access control

## Query/Serving Layer
- **Components:**
  - Query API (GraphQL/REST)
  - Data Aggregation Service
  - Visualization Service (e.g., Grafana, custom dashboards)
- **Auth Boundaries:**
  - API Gateway with JWT for secure query access

## Egress to User
- **Components:**
  - User Interface (Web App, Mobile App)
  - Notification Service (e.g., email, SMS alerts)
  - Data Export Functionality (CSV, JSON)
- **Auth Boundaries:**
  - User authentication via OAuth 2.0 and session management

```

```
ASCII Block Diagram:

+---------------------+
|  External Data      |
|     Sources         |
|  (IoT, APIs, etc.)  |
+----------+----------+
           |
           v
+---------------------+
|   Ingestion Layer    |
|   (API, MQ, etc.)    |
+----------+----------+
           |
           v
+---------------------+
| Processing/Transform |
|        Layer         |
|  (Stream & Batch)    |
+----------+----------+
           |
           v
+---------------------+
|     Storage Tier     |
| (Time-Series DB, etc.)|
+----------+----------+
           |
           v
+---------------------+
|  Query/Serving Layer |
|   (API, Visualization)|
+----------+----------+
           |
           v
+---------------------+
|    Egress to User    |
| (Web/Mobile App, etc.)|
+---------------------+
```