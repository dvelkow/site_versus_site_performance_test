from typing import Dict, List
from .visualizer import Visualizer
import matplotlib.pyplot as plt

class ReportGenerator:
    def __init__(self):
        self.visualizer = Visualizer()

    def generate_report(self, metrics_history: Dict[str, List[float]], analysis_results: Dict[str, Dict], output_file: str = 'performance_report.html'):
        report = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
                h2 { color: #34495e; margin-top: 30px; }
                h3 { color: #16a085; }
                .metric { background-color: #f2f2f2; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
                .anomaly { color: #c0392b; font-weight: bold; }
                .trend { color: #2980b9; }
                img { max-width: 100%; height: auto; margin-top: 10px; }
            </style>
        </head>
        <body>
        <h1>Web Performance Analysis Report</h1>
        """

        for env, env_results in analysis_results.items():
            report += f"<h2>Environment: {env}</h2>"
            
            for metric in metrics_history.keys():
                if metric.startswith(f"{env}_"):
                    metric_name = metric.split('_', 1)[1]
                    report += f"<div class='metric'>"
                    report += f"<h3>{metric_name.replace('_', ' ').title()}</h3>"
                    
                    # Add anomaly information
                    if 'anomalies' in env_results and metric_name in env_results['anomalies']:
                        is_anomaly = env_results['anomalies'][metric_name]
                        report += f"<p class='anomaly'>Anomaly detected: {'Yes' if is_anomaly else 'No'}</p>"
                    
                    # Add trend information
                    if 'trends' in env_results and metric_name in env_results['trends']:
                        slope, trend = env_results['trends'][metric_name]
                        report += f"<p class='trend'>Trend: {trend.capitalize()} (slope: {slope:.4f})</p>"
                    
                    # Generate and add plot
                    plot_filename = f"{env}_{metric_name}_trend.png"
                    self.visualizer.plot_metric_trend(metrics_history[metric], metric_name, env, plot_filename)
                    report += f"<img src='{plot_filename}' alt='{metric_name} trend for {env}'>"
                    
                    report += "</div>"

        report += "</body></html>"

        with open(output_file, 'w') as f:
            f.write(report)

        return output_file