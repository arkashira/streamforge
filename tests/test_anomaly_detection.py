import pytest
from anomaly_detection import get_anomaly_scores, Anomaly

def test_get_anomaly_scores():
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 10.0]
    anomalies = get_anomaly_scores(data)
    assert len(anomalies) == 1
    assert anomalies[0].score > 0.8

def test_get_anomaly_scores_no_anomalies():
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    anomalies = get_anomaly_scores(data)
    assert len(anomalies) == 0

def test_get_anomaly_scores_empty_data():
    data = []
    anomalies = get_anomaly_scores(data)
    assert len(anomalies) == 0

def test_get_anomaly_scores_invalid_data():
    data = ["a", "b", "c"]
    with pytest.raises(TypeError):
        get_anomaly_scores(data)
