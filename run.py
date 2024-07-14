import asyncio
import argparse
import sys
import os
import time

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.analyzer.performance_analyzer import PerformanceAnalyzer
from src.data_collection.metric_collector import MetricCollector
from src.reporting.report_generator import ReportGenerator
from src.utils.config_loader import load_config

async def main(config_path, verbose=False):
    config = load_config(config_path)
    analyzer = PerformanceAnalyzer(config)
    collector = MetricCollector()
    report_generator = ReportGenerator()

    all_analysis_results = {}

    try:
        for _ in range(5):  # Collect 5 data points for each environment
            for env, url in config['urls'].items():
                if verbose:
                    print(f"Analyzing {env} environment: {url}")
                metrics = collector.collect_metrics(url)
                if verbose:
                    print(f"Metrics collected: {metrics}")
                
                # Only analyze metrics that were successfully collected
                valid_metrics = {k: v for k, v in metrics.items() if v is not None}
                analyzer.add_test_result(valid_metrics, env)
                analysis_results = analyzer.analyze_performance(valid_metrics, env)
                all_analysis_results[env] = analysis_results
                
                if verbose:
                    print(f"Anomalies detected: {analysis_results['anomalies']}")
                    print(f"Trends identified: {analysis_results['trends']}")
                    print("---")
            
            time.sleep(5)  # Wait 5 seconds between data collections

        report_file = report_generator.generate_report(analyzer.metrics_history, all_analysis_results)
        print(f"Report generated: {report_file}")

    finally:
        collector.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run WebPerformanceGuardian")
    parser.add_argument("-c", "--config", default="config/config.json", help="Path to configuration file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    args = parser.parse_args()

    asyncio.run(main(args.config, args.verbose))
    
    