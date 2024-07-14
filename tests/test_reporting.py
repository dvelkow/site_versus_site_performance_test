import pytest
from unittest.mock import patch, mock_open
from src.reporting import ReportGenerator, Visualizer

@pytest.fixture
def sample_metrics_history():
    return {
        "production_page_load_time": [2.0, 2.1, 2.2, 2.0, 2.1],
        "production_time_to_first_byte": [0.5, 0.4, 0.6, 0.5, 0.5],
        "staging_page_load_time": [2.2, 2.3, 2.1, 2.4, 2.2]
    }

@pytest.fixture
def sample_analysis_results():
    return {
        "production": {
            "anomalies": {
                "page_load_time": False,
                "time_to_first_byte": False
            },
            "trends": {
                "page_load_time": (0.02, "degrading"),
                "time_to_first_byte": (0.01, "degrading")
            }
        },
        "staging": {
            "anomalies": {
                "page_load_time": False
            },
            "trends": {
                "page_load_time": (0.03, "degrading")
            }
        }
    }

def test_report_generator_initialization():
    generator = ReportGenerator()
    assert isinstance(generator.visualizer, Visualizer)

@patch('src.reporting.report_generator.open', new_callable=mock_open)
@patch('src.reporting.visualizer.plt')
def test_generate_report(mock_plt, mock_file, sample_metrics_history, sample_analysis_results):
    generator = ReportGenerator()
    output_file = generator.generate_report(sample_metrics_history, sample_analysis_results)
    
    assert output_file == 'performance_report.html'
    mock_file.assert_called_once_with('performance_report.html', 'w')
    mock_file().write.assert_called()
    
    # Check if the plot was created for each metric
    assert mock_plt.figure.call_count == 3
    assert mock_plt.savefig.call_count == 3

@patch('src.reporting.visualizer.plt')
def test_visualizer_plot_metric_trend(mock_plt):
    visualizer = Visualizer()
    metric_values = [1.0, 1.1, 1.2, 1.1, 1.3]
    visualizer.plot_metric_trend(metric_values, "Test Metric", "test_output.png")
    
    mock_plt.figure.assert_called_once()
    mock_plt.plot.assert_called_once_with(metric_values)
    mock_plt.title.assert_called_once_with("Test Metric Over Time")
    mock_plt.ylabel.assert_called_once_with("Test Metric")
    mock_plt.xlabel.assert_called_once_with("Test Run")
    mock_plt.savefig.assert_called_once_with("test_output.png")
    mock_plt.close.assert_called_once()