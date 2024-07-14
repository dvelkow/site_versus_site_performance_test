import asyncio
from typing import Dict
from utils.config_loader import load_config
from analyzer.performance_analyzer import PerformanceAnalyzer
from data_collection.metric_collector import MetricCollector
from reporting.report_generator import ReportGenerator

async def run_analysis(config: Dict):
    analyzer = PerformanceAnalyzer(config)
    collector = MetricCollector()
    report_generator = ReportGenerator()

    try:
        for env, url in config['urls'].items():
            metrics = collector.collect_metrics(url)
            analyzer.add_test_result(metrics, env)
            analysis_results = analyzer.analyze_performance(metrics, env)
            
            print(f"Analysis results for {env}:")
            print(f"Metrics: {metrics}")
            print(f"Anomalies: {analysis_results['anomalies']}")
            print(f"Trends: {analysis_results['trends']}")
            print("---")

        report_file = report_generator.generate_report(analyzer.metrics_history, analysis_results)
        print(f"Report generated: {report_file}")

    finally:
        collector.close()

if __name__ == "__main__":
    config = load_config('config/config.json')
    asyncio.run(run_analysis(config))