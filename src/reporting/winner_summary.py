import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List

def generate_winner_summary(metrics_history: Dict[str, List[float]], output_file: str = 'comparison.png'):
    # Calculate averages
    averages = {}
    for key, values in metrics_history.items():
        site, metric = key.split('_', 1)
        if metric not in averages:
            averages[metric] = {}
        averages[metric][site] = sum(values) / len(values)

    # Determine winners
    winners = {}
    for metric, site_averages in averages.items():
        winner = min(site_averages, key=site_averages.get)
        winners[metric] = {
            "winner": winner,
            "average": site_averages[winner]
        }

    # Prepare data for plotting
    metrics = list(winners.keys())
    sites = list(set(site for metric in averages for site in averages[metric]))
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i, site in enumerate(sites):
        site_averages = [averages[metric][site] if site in averages[metric] else 0 for metric in metrics]
        rects = ax.bar(x + i*width, site_averages, width, label=site.capitalize())
        ax.bar_label(rects, fmt='%.2f')

    ax.set_ylabel('Average Time (seconds)')
    ax.set_title('Performance Comparison by Metric')
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels([metric.replace('_', ' ').title() for metric in metrics])
    ax.legend()

    fig.tight_layout()

    # Save the plot
    plt.savefig(output_file)
    plt.close()

    return output_file