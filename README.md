# web_app_anomaly_detection
This project is a Python-based tool designed to compare the performance of two competitor websites and to clearly show which one runs more smoothly. It provides detailed metrics and analysis to help devs and site owners understand and improve their web performance.

## Features

- Comparative analysis of multiple websites
- Measurement of key performance metrics:
  - Page Load Time
  - Time to First Byte
  - First Contentful Paint
- Anomaly detection to identify unexpected performance changes
- Trend analysis to track performance over time
- Visual representation of results through graphs and charts
- Comprehensive HTML report generation
- Clear winner summary based on average performance

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/site_versus_site_performance_test.git
   cd site_versus_site_performance_test
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Configuration

Edit the `config/config.json` file to specify URLs of the websites to compare, you can also:
- change performance metrics to measure
- alter the threshold for anomaly detection

Example configuration:

```json
{
    "urls": {
        "github": "https://www.github.com",
        "hubgit": "https://www.hubgit.com"
    },
    "metrics": [
        "page_load_time",
        "time_to_first_byte",
        "first_contentful_paint"
    ],
    "threshold": 2.0,
    "window_size": 20
}
```

### Usage

Run the tool using:

```
python3 run.py

```

## Output

SiteVersus generates:

1. An HTML report with detailed performance comparisons
2. A "Winner Summary" plot visualizing the overall performance
3. A text file summarizing the results