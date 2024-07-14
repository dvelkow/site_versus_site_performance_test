import pytest
from src.analyzer import PerformanceAnalyzer, AnomalyDetector, TrendAnalyzer

@pytest.fixture
def sample_config():
    return {
        "window_size": 5,
        "threshold": 2.0,
        "metrics": ["page_load_time", "time_to_first_byte", "first_contentful_paint"],
        "environments": ["production", "staging"]
    }

@pytest.fixture
def sample_metrics():
    return {
        "page_load_time": 2.5,
        "time_to_first_byte": 0.5,
        "first_contentful_paint": 1.2
    }

def test_performance_analyzer_initialization(sample_config):
    analyzer = PerformanceAnalyzer(sample_config)
    assert analyzer.config == sample_config
    assert isinstance(analyzer.anomaly_detector, AnomalyDetector)
    assert isinstance(analyzer.trend_analyzer, TrendAnalyzer)

def test_performance_analyzer_add_test_result(sample_config, sample_metrics):
    analyzer = PerformanceAnalyzer(sample_config)
    analyzer.add_test_result(sample_metrics, "production")
    
    for metric in sample_config['metrics']:
        assert len(analyzer.metrics_history[f"production_{metric}"]) == 1
        assert analyzer.metrics_history[f"production_{metric}"][0] == sample_metrics[metric]

def test_performance_analyzer_analyze_performance(sample_config, sample_metrics):
    analyzer = PerformanceAnalyzer(sample_config)
    
    # Add some historical data
    for _ in range(5):
        analyzer.add_test_result(sample_metrics, "production")
    
    # Analyze with a new set of metrics
    new_metrics = {key: value * 1.5 for key, value in sample_metrics.items()}
    results = analyzer.analyze_performance(new_metrics, "production")
    
    assert "anomalies" in results
    assert "trends" in results
    assert all(metric in results["anomalies"] for metric in sample_config['metrics'])
    assert all(metric in results["trends"] for metric in sample_config['metrics'])

def test_anomaly_detector(sample_config):
    detector = AnomalyDetector(sample_config['threshold'])
    history = {
        "production_page_load_time": [2.0, 2.1, 2.2, 2.0, 2.1]
    }
    new_metrics = {"page_load_time": 5.0}
    
    anomalies = detector.detect_anomalies(history, new_metrics, "production")
    assert anomalies["page_load_time"] == True

def test_trend_analyzer():
    analyzer = TrendAnalyzer()
    history = {
        "production_page_load_time": [2.0, 2.1, 2.2, 2.3, 2.4]
    }
    
    trends = analyzer.analyze_trends(history, "production")
    assert "page_load_time" in trends
    assert trends["page_load_time"][1] == "degrading"