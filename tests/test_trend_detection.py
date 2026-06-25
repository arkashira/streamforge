import pytest
from src.trend_detection import TrendDetector, Trend, TrendType

def test_detect_trends():
    series = [1, 2, 3, 4, 5]
    detector = TrendDetector(series)
    trends = detector.detect_trends()
    assert len(trends) == 4
    for trend in trends:
        assert trend.confidence == 0.95

def test_detect_trends_drift():
    series = [1, 2, 1, 2, 1]
    detector = TrendDetector(series)
    trends = detector.detect_trends()
    assert len(trends) == 4
    for trend in trends:
        if trend.type == TrendType.DRIFT:
            assert trend.type == TrendType.DRIFT

def test_detect_trends_spike():
    series = [1, 2, 3, 2, 1]
    detector = TrendDetector(series)
    trends = detector.detect_trends()
    assert len(trends) == 4
    for trend in trends:
        if trend.type == TrendType.SPIKE:
            assert trend.type == TrendType.SPIKE

def test_detect_trends_seasonality():
    series = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    detector = TrendDetector(series)
    trends = detector.detect_trends()
    assert len(trends) == 8
    for trend in trends:
        if trend.type == TrendType.SEASONALITY:
            assert trend.type == TrendType.SEASONALITY
