# streamforge

A tiny, pure‑Python, in‑memory Kafka‑like streaming library used for unit‑testing
data‑ingestion pipelines.

## Features

* Automatic creation of a topic `ts_ingest`.
* Producer / Consumer with at‑least‑once delivery semantics.
* Simple back‑pressure handling – the producer blocks when the internal queue
  exceeds a configurable limit (default 1 000 messages).

The implementation uses only the Python standard library and is deliberately
minimal; it is **not** a production‑ready Kafka client.

## Running the tests
