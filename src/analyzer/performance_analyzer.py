from typing import Dict, List
from collections import defaultdict
from .anomaly_detector import AnomalyDetector
from .trend_analyzer import TrendAnalyzer

class PerformanceAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        self.metrics_history: Dict[str, List[float]] = defaultdict(list)
        self.anomaly_detector = AnomalyDetector(config['threshold'])
        self.trend_analyzer = TrendAnalyzer()

    def add_test_result(self, metrics: Dict[str, float], environment: str):
        for key, value in metrics.items():
            if key in self.config['metrics']:
                self.metrics_history[f"{environment}_{key}"].append(value)
                if len(self.metrics_history[f"{environment}_{key}"]) > self.config['window_size']:
                    self.metrics_history[f"{environment}_{key}"].pop(0)

    def analyze_performance(self, new_metrics: Dict[str, float], environment: str) -> Dict[str, Dict]:
        anomalies = self.anomaly_detector.detect_anomalies(self.metrics_history, new_metrics, environment)
        trends = self.trend_analyzer.analyze_trends(self.metrics_history, environment)
        return {
            "anomalies": anomalies,
            "trends": trends
        }
