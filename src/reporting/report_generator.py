from typing import Dict, List
from .visualizer import Visualizer

class ReportGenerator:
    def __init__(self):
        self.visualizer = Visualizer()

    def determine_winner(self, metrics_history: Dict[str, List[float]]) -> Dict[str, Dict[str, str]]:
        averages = {}
        for key, values in metrics_history.items():
            site, metric = key.split('_', 1)
            if site not in averages:
                averages[site] = {}
            averages[site][metric] = sum(values) / len(values)

        winners = {}
        for metric in averages[list(averages.keys())[0]].keys():
            best_site = min(averages.keys(), key=lambda site: averages[site][metric])
            winners[metric] = {
                "winner": best_site,
                "average": averages[best_site][metric]
            }

        return winners

    def generate_report(self, metrics_history: Dict[str, List[float]], analysis_results: Dict[str, Dict], output_file: str = 'performance_report.html'):
        report = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px; }
                h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
                h2 { color: #34495e; margin-top: 30px; }
                h3 { color: #16a085; }
                .metric { background-color: #f2f2f2; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
                .anomaly { color: #c0392b; font-weight: bold; }
                .trend { color: #2980b9; }
                .winner { color: #27ae60; font-weight: bold; }
                img { max-width: 100%; height: auto; margin-top: 10px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
        <h1>Web Performance Analysis Report: Site Comparison</h1>
        """

        # Determine winners
        winners = self.determine_winner(metrics_history)

        # Add winner summary
        report += "<h2>Performance Winners</h2>"
        report += "<table>"
        report += "<tr><th>Metric</th><th>Winner</th><th>Average Time</th></tr>"
        for metric, result in winners.items():
            report += f"<tr><td>{metric.replace('_', ' ').title()}</td><td class='winner'>{result['winner'].capitalize()}</td><td>{result['average']:.2f} seconds</td></tr>"
        report += "</table>"

        # Organize metrics by metric name
        metric_data = {}
        sites = set()
        for key, values in metrics_history.items():
            site, metric = key.split('_', 1)
            sites.add(site)
            if metric not in metric_data:
                metric_data[metric] = {}
            metric_data[metric][site] = values

        # Generate comparison plots and analysis for each metric
        for metric, site_data in metric_data.items():
            report += f"<h2>{metric.replace('_', ' ').title()} Comparison</h2>"
            
            # Generate and add comparison plot
            plot_filename = f"{metric}_comparison.png"
            self.visualizer.plot_metric_comparison(site_data, metric, plot_filename)
            report += f"<img src='{plot_filename}' alt='{metric} comparison across sites'>"
            
            # Add analysis table
            report += "<table>"
            report += "<tr><th>Site</th><th>Latest Value</th><th>Average Value</th><th>Anomaly</th><th>Trend</th></tr>"
            for site in sites:
                report += "<tr>"
                report += f"<td>{site.capitalize()}</td>"
                if site in site_data:
                    avg_value = sum(site_data[site]) / len(site_data[site])
                    report += f"<td>{site_data[site][-1]:.2f}</td>"
                    report += f"<td>{avg_value:.2f}</td>"
                    if site in analysis_results and 'anomalies' in analysis_results[site] and metric in analysis_results[site]['anomalies']:
                        is_anomaly = analysis_results[site]['anomalies'][metric]
                        report += f"<td class='anomaly'>{'Yes' if is_anomaly else 'No'}</td>"
                    else:
                        report += "<td>N/A</td>"
                    if site in analysis_results and 'trends' in analysis_results[site] and metric in analysis_results[site]['trends']:
                        slope, trend = analysis_results[site]['trends'][metric]
                        report += f"<td class='trend'>{trend.capitalize()} (slope: {slope:.4f})</td>"
                    else:
                        report += "<td>N/A</td>"
                else:
                    report += "<td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td>"
                report += "</tr>"
            report += "</table>"

        report += "</body></html>"

        with open(output_file, 'w') as f:
            f.write(report)

        return output_file