import asyncio
import argparse
import logging
from src.analyzer.performance_analyzer import PerformanceAnalyzer
from src.data_collection.metric_collector import MetricCollector
from src.reporting.report_generator import ReportGenerator
from src.reporting.winner_summary import generate_winner_summary
from src.utils.config_loader import load_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main(config_path: str, verbose: bool):
    config = load_config(config_path)
    analyzer = PerformanceAnalyzer(config)
    collector = MetricCollector(timeout=config.get('timeout', 30))
    report_generator = ReportGenerator()

    all_analysis_results = {}

    try:
        for _ in range(config.get('num_runs', 5)):
            for env, url in config['urls'].items():
                logger.info(f"Analyzing {env} environment: {url}")
                metrics = await collector.collect_metrics(url)
                logger.info(f"Metrics collected for {env}: {metrics}")
                
                valid_metrics = {k: v for k, v in metrics.items() if v is not None}
                analyzer.add_test_result(valid_metrics, env)
                analysis_results = analyzer.analyze_performance(valid_metrics, env)
                all_analysis_results[env] = analysis_results
                
                logger.info(f"Analysis results for {env}:")
                logger.info(f"Anomalies: {analysis_results['anomalies']}")
                logger.info(f"Trends: {analysis_results['trends']}")
                logger.info("---")
            
            await asyncio.sleep(config.get('delay_between_runs', 5))

        report_file = report_generator.generate_report(analyzer.metrics_history, all_analysis_results)
        logger.info(f"Report generated: {report_file}")

        # Generate winner summary
        winner_plot, winner_text = generate_winner_summary(analyzer.metrics_history)
        logger.info(f"Winner summary plot generated: {winner_plot}")
        logger.info(f"Winner summary text generated: {winner_text}")

    finally:
        await collector.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SiteVersus Performance Test")
    parser.add_argument("-c", "--config", default="config/config.json", help="Path to configuration file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    args = parser.parse_args()

    asyncio.run(main(args.config, args.verbose))