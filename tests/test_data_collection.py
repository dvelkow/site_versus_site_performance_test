import pytest
from unittest.mock import patch, MagicMock
from src.data_collection import MetricCollector

@pytest.fixture
def mock_webdriver():
    with patch('src.data_collection.metric_collector.webdriver.Chrome') as mock:
        yield mock

def test_metric_collector_initialization(mock_webdriver):
    collector = MetricCollector()
    assert collector.driver == mock_webdriver.return_value

@patch('src.data_collection.metric_collector.WebDriverWait')
def test_collect_metrics(mock_wait, mock_webdriver):
    mock_driver = MagicMock()
    mock_webdriver.return_value = mock_driver
    
    # Mock the JavaScript execution results
    mock_driver.execute_script.side_effect = [
        1000,  # navigationStart
        3000,  # loadEventEnd
        1500,  # responseStart
        800    # first contentful paint
    ]
    
    collector = MetricCollector()
    metrics = collector.collect_metrics("https://example.com")
    
    assert metrics['page_load_time'] == 2.0  # (3000 - 1000) / 1000
    assert metrics['time_to_first_byte'] == 0.5  # (1500 - 1000) / 1000
    assert metrics['first_contentful_paint'] == 0.8  # 800 / 1000
    
    mock_driver.get.assert_called_once_with("https://example.com")

def test_metric_collector_close(mock_webdriver):
    collector = MetricCollector()
    collector.close()
    mock_webdriver.return_value.quit.assert_called_once()