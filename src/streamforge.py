import threading
import collections
from dataclasses import dataclass
from typing import Any, Dict, List, Callable, Optional


class TopicNotFoundError(RuntimeError):
    """Raised when an operation references a non‑existent topic."""


@dataclass
class Message:
    """A simple message container."""
    key: Any
    value: Any
    offset: int = -1  # set by the broker when stored


class InMemoryKafka:
    """
    Very small in‑memory broker that mimics a subset of Kafka behaviour.

    * Topics are created on first use (auto‑create).
    * Each topic stores messages in a FIFO deque.
    * A configurable `max_queue_size` triggers back‑pressure: producers block
      when the total number of stored messages exceeds the limit.
    """

    def __init__(self, max_queue_size: int = 1_000):
        self._topics: Dict[str, collections.deque[Message]] = {}
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._max_queue_size = max_queue_size
        self._total_messages = 0

    # --------------------------------------------------------------------- #
    # Topic management
    # --------------------------------------------------------------------- #
    def _ensure_topic(self, name: str) -> collections.deque[Message]:
        """Create the topic if it does not exist and return its deque."""
        if name not in self._topics:
            self._topics[name] = collections.deque()
        return self._topics[name]

    def create_topic(self, name: str) -> None:
        """Public API to explicitly create a topic."""
        with self._lock:
            self._ensure_topic(name)

    def list_topics(self) -> List[str]:
        with self._lock:
            return list(self._topics.keys())

    # --------------------------------------------------------------------- #
    # Producer API
    # --------------------------------------------------------------------- #
    def produce(self, topic: str, key: Any, value: Any) -> Message:
        """
        Append a message to the topic, blocking if back‑pressure limit is hit.
        Returns the stored Message (with offset assigned).
        """
        with self._not_full:
            while self._total_messages >= self._max_queue_size:
                self._not_full.wait()
            q = self._ensure_topic(topic)
            offset = len(q)
            msg = Message(key=key, value=value, offset=offset)
            q.append(msg)
            self._total_messages += 1
            # Notify potential consumers that a new message is available.
            self._not_full.notify_all()
            return msg

    # --------------------------------------------------------------------- #
    # Consumer API
    # --------------------------------------------------------------------- #
    def consume(
        self,
        topic: str,
        batch_size: int = 1,
        timeout: Optional[float] = None,
        on_message: Optional[Callable[[Message], None]] = None,
    ) -> List[Message]:
        """
        Retrieve up to `batch_size` messages from `topic`. If no messages are
        available, block up to `timeout` seconds. Returns the list of messages.
        The caller is responsible for processing each message; if processing
        fails, the same message will be delivered again on the next call
        (at‑least‑once semantics).
        """
        with self._not_full:
            q = self._topics.get(topic)
            if q is None:
                raise TopicNotFoundError(f"Topic '{topic}' does not exist")
            if not q:
                # Wait for a message or timeout.
                waited = self._not_full.wait(timeout=timeout)
                if not waited:
                    return []
                # Re‑check after waking.
                if not q:
                    return []
            msgs = []
            for _ in range(min(batch_size, len(q))):
                msgs.append(q.popleft())
                self._total_messages -= 1
            # Notify producers that space may be available.
            self._not_full.notify_all()
        if on_message:
            for m in msgs:
                on_message(m)
        return msgs
