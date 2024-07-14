import numpy as np
from typing import Dict, List

class AnomalyDetector:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def detect_anomalies(self, history: Dict[str, List[float]], new_metrics: Dict[str, float], environment: str) -> Dict[str, bool]:
        anomalies = {}
        for key, value in new_metrics.items():
            history_key = f"{environment}_{key}"
            if history_key in history and len(history[history_key]) > 0:
                mean = np.mean(history[history_key])
                std = np.std(history[history_key])
                z_score = (value - mean) / std if std > 0 else 0
                anomalies[key] = abs(z_score) > self.threshold
            else:
                anomalies[key] = False
        return anomalies
