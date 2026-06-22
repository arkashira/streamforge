import json
from dataclasses import dataclass
from typing import List

@dataclass
class Anomaly:
    timestamp: str
    score: float

class IsolationForest:
    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination

    def fit(self, data: List[float]):
        # Simplified Isolation Forest implementation for demonstration purposes
        self.data = data

    def predict(self, data: List[float]) -> List[float]:
        # Simplified anomaly scoring for demonstration purposes
        scores = []
        for x in data:
            score = 1 - (x / max(self.data))
            scores.append(score)
        return scores

class AnomalyDetector:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self.isolation_forest = IsolationForest()

    def detect_anomalies(self, data: List[float]) -> List[Anomaly]:
        self.isolation_forest.fit(data)
        scores = self.isolation_forest.predict(data)
        anomalies = []
        for i, score in enumerate(scores):
            if score > self.threshold:
                anomalies.append(Anomaly(timestamp=f"2022-01-01 {i:02d}:00:00", score=score))
        return anomalies

    def persist_anomalies(self, anomalies: List[Anomaly]):
        # In-memory persistence for demonstration purposes
        self.anomalies = anomalies

    def get_anomalies(self) -> List[Anomaly]:
        return self.anomalies

def get_anomaly_scores(data: List[float]) -> List[Anomaly]:
    detector = AnomalyDetector()
    anomalies = detector.detect_anomalies(data)
    detector.persist_anomalies(anomalies)
    return detector.get_anomalies()
