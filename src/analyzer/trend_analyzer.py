import numpy as np
from typing import Dict, List, Tuple

class TrendAnalyzer:
    def analyze_trends(self, history: Dict[str, List[float]], environment: str) -> Dict[str, Tuple[float, str]]:
        trends = {}
        for key, values in history.items():
            if key.startswith(f"{environment}_") and len(values) >= 2:
                slope, _ = np.polyfit(range(len(values)), values, 1)
                trend_description = "improving" if slope < 0 else "degrading"
                trends[key.split('_', 1)[1]] = (slope, trend_description)
        return trends
