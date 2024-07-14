import pytest
from src.utils import load_config

@pytest.fixture(scope="session")
def global_config():
    """
    A session-scoped fixture that loads the configuration once for all tests.
    """
    return load_config('config/config.json')

@pytest.fixture(scope="session")
def sample_metrics():
    """
    A session-scoped fixture that provides a sample set of metrics for testing.
    """
    return {
        "page_load_time": 2.5,
        "time_to_first_byte": 0.5,
        "first_contentful_paint": 1.2
    }