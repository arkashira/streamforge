import threading
import time
import pytest
from streamforge import (
    InMemoryKafka,
    Message,
    TopicNotFoundError,
)


def test_topic_auto_creation():
    broker = InMemoryKafka()
    # No topics initially.
    assert broker.list_topics() == []
    # Producing to a new topic auto‑creates it.
    broker.produce("ts_ingest", key=1, value="first")
    assert "ts_ingest" in broker.list_topics()


def test_produce_consume_at_least_once():
    broker = InMemoryKafka()
    broker.create_topic("ts_ingest")
    # Produce two messages.
    m1 = broker.produce("ts_ingest", key="a", value=10)
    m2 = broker.produce("ts_ingest", key="b", value=20)
    assert m1.offset == 0
    assert m2.offset == 1

    # Consume one message.
    batch = broker.consume("ts_ingest", batch_size=1)
    assert len(batch) == 1
    assert batch[0].key == "a"
    assert batch[0].value == 10

    # Simulate processing failure by re‑inserting the message.
    # (In real Kafka this would be handled by not committing offsets.)
    broker._ensure_topic("ts_ingest").appendleft(batch[0])
    broker._total_messages += 1

    # Consume again, should get the same message first (at‑least‑once).
    batch2 = broker.consume("ts_ingest", batch_size=2)
    keys = [msg.key for msg in batch2]
    assert keys == ["a", "b"]  # 'a' appears again before 'b'


def test_consume_from_missing_topic_raises():
    broker = InMemoryKafka()
    with pytest.raises(TopicNotFoundError):
        broker.consume("nonexistent")


def test_back_pressure_blocks_producer():
    # Small queue to trigger back‑pressure quickly.
    broker = InMemoryKafka(max_queue_size=5)

    # Fill the queue to the limit.
    for i in range(5):
        broker.produce("ts_ingest", key=i, value=str(i))

    # In another thread, attempt to produce one more message; it should block
    # until a consumer removes an item.
    produced = {}

    def producer():
        produced["msg"] = broker.produce("ts_ingest", key=99, value="blocked")

    t = threading.Thread(target=producer)
    t.start()
    # Give the thread a moment to attempt production and block.
    time.sleep(0.1)
    assert not produced  # still blocked

    # Consume a single message, freeing space.
    broker.consume("ts_ingest", batch_size=1)

    # Now the producer should finish.
    t.join(timeout=1.0)
    assert "msg" in produced
    assert produced["msg"].key == 99
    assert produced["msg"].value == "blocked"
